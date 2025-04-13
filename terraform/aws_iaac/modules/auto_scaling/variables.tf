variable "worker_instance_name" {
  description = "The name tag for the EC2 worker instance"
  type        = string
}

variable "spark_worker_launch_template" {
  description = "The name prefix for the worker launch template"
  type        = string
}

variable "worker_desired_capacity" {
  description = "The desired capacity for the worker auto-scaling group"
  type        = number
}

variable "worker_max_size" {
  description = "The maximum size for the worker auto-scaling group"
  type        = number
}

variable "worker_min_size" {
  description = "The minimum size for the worker auto-scaling group"
  type        = number
}
variable "sleep_interval" {
  description = "The number of seconds to sleep"
  type        = string
}

variable "user_name" {
  description = "The username for remote execution"
  type        = string
}

variable "ansible_master_destination_file_path" {
  description = "The destination path on the EC2 instance for the Ansible playbook"
  type        = string
}
variable "instance_type" {
  description = "The instance type for the EC2 instances"
  type        = string
}
variable "ssh_key_name" {
  description = "The name of the SSH key pair"
  type        = string
}

variable "ansible_worker_starter_destination_file_path" {
  description = "The destination path on the EC2 instance for the Ansible worker starter script"
  type        = string
}

variable "master_instance_ip" {
  type = string
  description = "The IP on the master instance"
}

variable "master_instance_id" {
  type = string
  description = "master instance id on the master instance"
}

variable "connection_type" {
  type = string
  description = "connection type on the connection"
}

variable "ssh_private_key_path" {
  type = string

}

variable "security_group_id" {
  type = string
}

variable "subnet_id" {
  type = list(string)
}