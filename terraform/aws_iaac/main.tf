provider "aws" {
  access_key = var.access_key
  secret_key = var.secret_key
  region     = var.region
}

module "vpc" {
  source   = "./modules/vpc"
  vpc_cidr = var.vpc_cidr
  vpc_name = var.vpc_name
}


module "security_group" {
  depends_on          = [module.vpc]
  source              = "./modules/security-group"
  vpc_id              = module.vpc.vpc_id
  security_group_name = var.security_group_name
  ingress_rules       = var.ingress_rules
  egress_rules        = var.egress_rules
}


module "igw" {
  depends_on = [module.vpc]
  source     = "./modules/igw"
  name       = var.igw_name
  vpc_id     = module.vpc.vpc_id
}

module "rtb" {
  depends_on          = [module.vpc, module.igw]
  source              = "./modules/rtb"
  vpc_id              = module.vpc.vpc_id
  internet_gateway_id = module.igw.id
  route_table_name    = var.route_table_name
  default_route_cidr  = "0.0.0.0/0"
}

module "subnets" {
  depends_on         = [module.vpc, module.rtb]
  source             = "./modules/subnets"
  vpc_id             = module.vpc.vpc_id
  subnet_cidrs       = var.subnet_cidrs
  availability_zones = var.availability_zones
  route_table_id     = module.rtb.route_table_id

}

module "ssh_key" {
  source              = "./modules/aws_key_pair"
  ssh_key_name        = var.ssh_key_name
  ssh_public_key_path = var.ssh_public_key_path
}

module "master_instance" {
  depends_on                                   = [module.security_group, module.subnets]
  source                                       = "./modules/master_instance"
  ami_id                                       = var.ami_id
  instance_name                                = var.master_instance_name
  ssh_key_name                                 = var.ssh_key_name
  subnet_id                                    = module.subnets.public_subnet_ids[0]
  instance_type                                = var.instance_type
  master_allocation_ip                         = var.master_allocation_ip
  sleep_interval                               = var.sleep_interval
  ssh_private_key_path                         = var.ssh_private_key_path
  ansible_installation_command                 = var.ansible_installation_command
  ansible_master_destination_file_path         = var.ansible_master_destination_file_path
  ansible_master_file_path                     = var.ansible_master_file_path
  ansible_worker_starter_destination_file_path = var.ansible_worker_starter_destination_file_path
  ansible_worker_starter_file_path             = var.ansible_worker_starter_file_path
  connection_type                              = var.connection_type
  flask_file_destination_file_path             = var.flask_file_destination_file_path
  flask_file_source_file_path                  = var.flask_file_source_file_path
  update_command                               = var.update_command
  user_name                                    = var.user_name
  security_group_id                            = module.security_group.security_group_id
  availability_zones                           = var.availability_zones[0]
  access_key                                   = var.access_key
  secret_key                                   = var.secret_key
}


module "auto_scaling" {
  depends_on                                   = [module.master_instance, module.subnets, module.security_group]
  source                                       = "./modules/auto_scaling"
  ansible_master_destination_file_path         = var.ansible_master_destination_file_path
  ssh_key_name                                 = var.ssh_key_name
  ansible_worker_starter_destination_file_path = var.ansible_worker_starter_destination_file_path
  sleep_interval                               = var.sleep_interval
  user_name                                    = var.user_name
  spark_worker_launch_template                 = var.spark_worker_launch_template
  instance_type                                = var.instance_type
  worker_instance_name                         = var.worker_instance_name
  worker_min_size                              = var.worker_min_size
  worker_desired_capacity                      = var.worker_desired_capacity
  worker_max_size                              = var.worker_max_size
  master_instance_id                           = module.master_instance.ec2_instance_id
  master_instance_ip                           = module.master_instance.master_instance_ip
  connection_type                              = var.connection_type
  security_group_id                            = module.security_group.security_group_id
  ssh_private_key_path                         = var.ssh_private_key_path
  subnet_id                                    = module.subnets.public_subnet_ids
}
