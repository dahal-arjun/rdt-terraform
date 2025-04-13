variable "access_key" {
  type = string
  sensitive = true
  description = "Access key to AWS console"
}

variable "secret_key" {
  type = string
  sensitive = true
  description = "Secret key to AWS console"
}

variable "region" {
  type = string
  description = "Region to AWS console"
}

variable "vpc_name" {
  type = string
  description = "Name of the VPC to AWS console"
}

variable "vpc_cidr" {

  description = "Block number to AWS console"
}


variable "security_group_name" {
  description = "Name of the security group"
}

variable "ingress_rules" {
  description = "List of ingress rules for the security group"
}

variable "egress_rules" {
  description = "List of egress rules for the security group"
}

# List of private subnet CIDR blocks
variable "subnet_cidrs" {
  description = "A list of CIDR blocks for subnets"
  type        = list(string)
}

# Name tag for the Internet Gateway
variable "igw_name" {
  description = "Name tag for the Internet Gateway"
  type        = string
}

# Name tag for the route table
variable "route_table_name" {
  description = "Name tag for the route table"
  type        = string
}

# The name for the SSH key pair
variable "ssh_key_name" {
  description = "Name for the SSH key pair"
  type        = string
}

# The file path to the public key to be used
variable "ssh_public_key_path" {
  description = "File path to the public key to be used for the SSH key pair"
  type        = string
}

variable "ami_id" {
  description = "The AMI to use"
  type = string
}

variable "instance_type" {
  description = "Instance type that we will be creating"
  type = string
}

variable "master_instance_name" {
  description = "Name of the instance to be created"
  type = string
}
variable "master_allocation_ip" {
  type = string
  description = "master allocation IP to AWS console"
}

variable "availability_zones" {
  type = list(string)
  description = "Availability Zone to AWS console"
}

variable "sleep_interval" {
  type = string
  description = "sleep interval in seconds"
}

variable "update_command" {
  type = string
  description = "update command"
}

variable "ansible_installation_command" {
  type = string
  description = "installation command"
}

variable "connection_type" {
  type = string
  description = "connection type"
}

variable "user_name" {
  type = string
  description = "instance user name"
}

variable "ssh_private_key_path" {
  type = string
  description = "Path to the SSH private key file"
}


variable "ansible_master_file_path" {
  type = string
  description = "path to the master file"
}


variable "ansible_master_destination_file_path" {
  type = string
  description = "path to the ansible master destination file"
}

variable "worker_instance_name" {
  type = string
  description = "Name of the instance to be created"
}

variable "ansible_worker_file_path" {
  type = string
  description = "path to the ansible worker file"
}


variable "ansible_worker_destination_file_path" {
  type = string
  description = "path to the ansible worker destination file"
}


variable "ansible_worker_starter_file_path" {
  type = string
  description = "path to the ansible workerstarter file"
}

variable "ansible_worker_starter_destination_file_path" {
  type = string
  description = "path to the ansible workerstarter destination file"
}

variable "flask_file_source_file_path" {
  type = string
  description = "flask file source file path"
}

variable "flask_file_destination_file_path" {
  type = string
  description = "flask destination file path"
}

variable "worker_min_size" {
  description = "The minimum size for the worker auto-scaling group"
  type        = number
}

variable "worker_desired_capacity" {
  description = "The desired capacity for the worker auto-scaling group"
  type        = number
}

variable "worker_max_size" {
  description = "The maximum size for the worker auto-scaling group"
  type        = number
}

variable "spark_worker_launch_template" {
  description = "The name prefix for the worker launch template"
  type        = string
}
