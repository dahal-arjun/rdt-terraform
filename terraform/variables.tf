variable "access_key" {
  type = string
  description = "Access key to AWS console"
}

variable "secret_key" {
  type = string
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


variable "subnet_cidrs" {
 type        = list(string)
 description = "Public Subnet CIDR values"
}


variable "availability_zones" {
  type = list(string)
  description = "Availability Zone to AWS console"
}

variable "master_allocation_ip" {
  type = string
  description = "master allocation IP to AWS console"
}



variable "ssh_key_name" {
  type = string
  description = "Key for my computer to run SSH"
}

variable "ssh_public_key_path" {
  type = string
  description = "Path to the SSH public key file"
}

variable "security_group_name" {
  type = string
  description = "Name of the security group"
  default     = "default-security-group"
}

variable "ingress_rules" {
  description = "List of ingress rules for the security group."
  type        = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
}

variable "egress_rules" {
  description = "List of egress rules for the security group."
  type        = list(object({
    from_port   = number
    to_port     = number
    protocol    = string
    cidr_blocks = list(string)
  }))
}
variable "ami_id" {
  type = string
  description = "The AMI to use"
}

variable "instance_type" {
  type = string
  description = "Instance type that we will be creating"
}

variable "master_instance_name" {
  type = string
  description = "Name of the instance to be created"
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

variable "spark_worker_launch_template" {
  type = string
  description = "name of the spark worker template"
}


variable "worker_desired_capacity" {
  type = string
  description = "worker desired capacity"
}

variable "worker_max_size" {
  type = number
  description = "no of max workers to launch"
}


variable "worker_min_size" {
  type = number
  description = "no of min workers to launch"
}

variable "flask_file_source_file_path" {
  type = string
  description = "flask file source file path"
}

variable "flask_file_destination_file_path" {
  type = string
  description = "flask destination file path"
}

variable "vpc_cidr" {
  type = string
  description = "Block number to AWS console"
}


variable "igw_name" {
  description = "spark Internet Gateway name"
}

variable "route_table_name" {
  
}
