resource "null_resource" "pre_configuration" {
  provisioner "local-exec" {
    command = <<-EOT
      ../rename.sh  ${var.secret_key} ${var.access_key} ${var.region}
    EOT
  }
}

module "aws_iaac" {
  source = "./aws_iaac"
  access_key = var.access_key
  secret_key = var.secret_key
  region = var.region
  vpc_cidr = var.vpc_cidr
  vpc_name = var.vpc_name
  security_group_name = var.security_group_name
  ingress_rules = var.ingress_rules
  egress_rules = var.egress_rules
  subnet_cidrs = var.subnet_cidrs
  igw_name = var.igw_name
  ssh_key_name = var.ssh_key_name
  ssh_public_key_path = var.ssh_public_key_path
  ami_id = var.ami_id
  route_table_name = var.route_table_name
  instance_type = var.instance_type
  master_instance_name = var.master_instance_name
  master_allocation_ip = var.master_allocation_ip
  sleep_interval = var.sleep_interval
  ansible_installation_command = var.ansible_installation_command
  ansible_master_destination_file_path = var.ansible_master_destination_file_path
  ansible_master_file_path = var.ansible_master_file_path
  ansible_worker_destination_file_path = var.ansible_worker_destination_file_path
  ansible_worker_file_path = var.ansible_worker_file_path
  ansible_worker_starter_destination_file_path = var.ansible_worker_starter_destination_file_path
  ansible_worker_starter_file_path = var.ansible_worker_starter_file_path
  availability_zones = var.availability_zones
  connection_type = var.connection_type
  flask_file_destination_file_path = var.flask_file_destination_file_path
  flask_file_source_file_path = var.flask_file_source_file_path
  ssh_private_key_path = var.ssh_private_key_path
  update_command = var.update_command
  worker_instance_name = var.worker_instance_name
  user_name = var.user_name
  spark_worker_launch_template = var.spark_worker_launch_template
  worker_desired_capacity = var.worker_desired_capacity
  worker_max_size = var.worker_max_size
  worker_min_size = var.worker_min_size
  
}
