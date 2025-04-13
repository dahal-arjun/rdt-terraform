
# ============================== Start For Auto Scaling =============================
resource "aws_ami_from_instance" "worker_ami_instance" {
  name                    = var.worker_instance_name
  source_instance_id      = var.master_instance_id
  snapshot_without_reboot = false
}

resource "null_resource" "wait_for_worker_instance_ready_restart" {
  depends_on = [aws_ami_from_instance.worker_ami_instance]

  provisioner "local-exec" {
    command = var.sleep_interval
  }
}
resource "null_resource" "connect-master-to-worker" {
  depends_on = [null_resource.wait_for_worker_instance_ready_restart]
  
  provisioner "remote-exec" {
    inline = [
      "ansible-playbook -e 'public_ip=${var.master_instance_ip}' ${var.ansible_master_destination_file_path}",
    ]
    connection {
      type        = var.connection_type
      user        = var.user_name
      private_key = file(var.ssh_private_key_path)
      host        = var.master_instance_ip
    }
  }
}


resource "aws_launch_template" "worker_auto_scaling_template" {
  depends_on = [ null_resource.connect-master-to-worker ]
  name_prefix   = var.spark_worker_launch_template
  image_id      = aws_ami_from_instance.worker_ami_instance.id
  instance_type = var.instance_type
  key_name      = var.ssh_key_name

  network_interfaces {
    associate_public_ip_address = true
    security_groups = [var.security_group_id]
  }

  user_data = base64encode("#!/bin/bash\nsudo -i -u ubuntu ansible-playbook -e 'master_public_ip=${var.master_instance_ip}' ${var.ansible_worker_starter_destination_file_path}")
}




resource "aws_autoscaling_group" "worker_auto_scaling_group" {
  depends_on          = [aws_launch_template.worker_auto_scaling_template]
  desired_capacity    = var.worker_desired_capacity
  max_size            = var.worker_max_size
  min_size            = var.worker_min_size 
  vpc_zone_identifier = var.subnet_id
  
  

  launch_template {
    id      = aws_launch_template.worker_auto_scaling_template.id
    version = "$Latest"
  }
  
  tag {
    key                 = "AUTO_SCALING_GROUP"
    value               = "sparl-worker-group"
    propagate_at_launch = true
  }

}

resource "aws_autoscaling_policy" "worker_auto_scaling_policy" {
  depends_on = [ aws_autoscaling_group.worker_auto_scaling_group ]
  name                      = "step-scaling-policy"
  policy_type               = "StepScaling"
  autoscaling_group_name    = aws_autoscaling_group.worker_auto_scaling_group.name
  estimated_instance_warmup = 2
  adjustment_type           = "ChangeInCapacity"

  metric_aggregation_type = "Average"

  step_adjustment {
    metric_interval_lower_bound = 0
    metric_interval_upper_bound = 10
    scaling_adjustment = 1
  }

  step_adjustment {
    metric_interval_lower_bound = 10
    metric_interval_upper_bound = 20
    scaling_adjustment = 2
  }

  step_adjustment {
    metric_interval_lower_bound = 20
    scaling_adjustment = 3
  }
}


resource "aws_cloudwatch_metric_alarm" "ram_utilization_alarm" {
  depends_on = [ aws_autoscaling_group.worker_auto_scaling_group, aws_autoscaling_policy.worker_auto_scaling_policy ]
  alarm_name          = "ram-utilization-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "MemoryUtilization" 
  namespace           = "System/Linux"
  period              = 300
  statistic           = "Average"
  threshold           = 70 

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.worker_auto_scaling_group.name
  }

  alarm_description = "Alarm when RAM utilization exceeds 70% for 2 consecutive periods"

  alarm_actions = [
    aws_autoscaling_policy.worker_auto_scaling_policy.arn,
  ]
}


resource "aws_cloudwatch_metric_alarm" "cpu_utilization_alarm" {
  depends_on = [ aws_autoscaling_group.worker_auto_scaling_group, aws_autoscaling_policy.worker_auto_scaling_policy ]
  alarm_name          = "cpu-utilization-alarm"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.worker_auto_scaling_group.name
  }

  alarm_description = "Alarm when CPU utilization exceeds 80% for 2 consecutive periods"

  alarm_actions = [
    aws_autoscaling_policy.worker_auto_scaling_policy.arn,
  ]
}


