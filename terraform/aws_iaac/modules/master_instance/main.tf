
# ============================== Starting For Master =============================
resource "aws_instance" "ec2_master_instance" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  key_name                    = var.ssh_key_name
  vpc_security_group_ids      = [var.security_group_id]
  subnet_id                   = var.subnet_id
  associate_public_ip_address = true
  availability_zone           = var.availability_zones
  tags = {
    Name = var.instance_name
  }
  root_block_device {
    volume_type           = "gp2"
    volume_size           = 60
    delete_on_termination = true
  }

}

resource "aws_eip_association" "eip_assoc" {
  depends_on    = [aws_instance.ec2_master_instance]
  instance_id   = aws_instance.ec2_master_instance.id
  allocation_id = var.master_allocation_ip
}

resource "null_resource" "wait_for_master_instance_ready" {
  depends_on = [aws_eip_association.eip_assoc]
  provisioner "local-exec" {
    command = var.sleep_interval
  }
}

resource "null_resource" "install_ansible" {
  depends_on = [null_resource.wait_for_master_instance_ready]
  provisioner "remote-exec" {
    inline = [
      var.update_command,
      var.ansible_installation_command,
    ]
    connection {
      type        = var.connection_type
      user        = var.user_name
      private_key = file(var.ssh_private_key_path)
      host        = aws_eip_association.eip_assoc.public_ip
    }
  }
}

resource "null_resource" "upload_ansible_playbook_execute" {
  depends_on = [null_resource.install_ansible]
  provisioner "file" {
    source      = var.ansible_master_file_path
    destination = var.ansible_master_destination_file_path
    connection {
      type        = var.connection_type
      user        = var.user_name
      private_key = file(var.ssh_private_key_path)
      host        = aws_eip_association.eip_assoc.public_ip
    }
  }
  provisioner "file" {
    source      = var.ansible_worker_starter_file_path
    destination = var.ansible_worker_starter_destination_file_path
    connection {
      type        = var.connection_type
      user        = var.user_name
      private_key = file(var.ssh_private_key_path)
      host        = aws_eip_association.eip_assoc.public_ip
    }
  }

  provisioner "file" {
    source      = var.flask_file_source_file_path
    destination = var.flask_file_destination_file_path
    connection {
      type        = var.connection_type
      user        = var.user_name
      private_key = file(var.ssh_private_key_path)
      host        = aws_eip_association.eip_assoc.public_ip

    }
  }

  provisioner "remote-exec" {
    inline = [
      "ansible-playbook -e 'public_ip=${aws_instance.ec2_master_instance.public_ip}' ${var.ansible_master_destination_file_path}",
    ]
    connection {
      type        = var.connection_type
      user        = var.user_name
      private_key = file(var.ssh_private_key_path)
      host        = aws_eip_association.eip_assoc.public_ip
    }
  }
}

# ============================== Done For Master ==============================
