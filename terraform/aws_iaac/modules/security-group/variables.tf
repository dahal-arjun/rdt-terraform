variable "security_group_name" {
  description = "Name of the security group."
}

variable "vpc_id" {
  description = "vpc id"
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
