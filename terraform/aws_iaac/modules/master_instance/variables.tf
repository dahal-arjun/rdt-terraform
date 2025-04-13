variable "ami_id" {
  description = "The AMI ID for the EC2 instance"
  type        = string
}

variable "instance_type" {
  description = "The instance type for the EC2 instance"
  type        = string
}

variable "ssh_key_name" {
  description = "The name of the SSH key pair"
  type        = string
}

variable "subnet_id" {
  description = "The ID of the subnet where the EC2 instance will be deployed"
  type        = string
}

variable "instance_name" {
  description = "The name tag for the EC2 instance"
  type        = string
}

variable "security_group_id" {
  description = "security group IDs to attach to the EC2 instance"
  type        = string
}

variable "master_allocation_ip" {
  description = "The Elastic IP allocation ID for the EC2 Master instance"
  type        = string
}

variable "update_command" {
  description = "The command to update the EC2 instance"
  type        = string
}

variable "ansible_installation_command" {
  description = "The command to install Ansible on the EC2 instance"
  type        = string
}

variable "connection_type" {
  description = "The type of connection for remote execution"
  type        = string
}

variable "user_name" {
  description = "The username for remote execution"
  type        = string
}

variable "ssh_private_key_path" {
  description = "The file path to the SSH private key"
  type        = string
}

variable "ansible_master_file_path" {
  description = "The file path to the Ansible playbook on your local machine"
  type        = string
}

variable "ansible_master_destination_file_path" {
  description = "The destination path on the EC2 instance for the Ansible playbook"
  type        = string
}

variable "ansible_worker_starter_file_path" {
  description = "The file path to the Ansible worker starter script on your local machine"
  type        = string
}

variable "ansible_worker_starter_destination_file_path" {
  description = "The destination path on the EC2 instance for the Ansible worker starter script"
  type        = string
}

variable "flask_file_source_file_path" {
  description = "The file path to the Flask application on your local machine"
  type        = string
}

variable "flask_file_destination_file_path" {
  description = "The destination path on the EC2 instance for the Flask application"
  type        = string
}

variable "sleep_interval" {
  description = "The number of seconds to sleep"
  type = string
}


variable "availability_zones" {
  description = "avaliable_zones"
}

variable "access_key" {
  description = "access key for environment setup"
}

variable "secret_key" {
  description = "sec"
}