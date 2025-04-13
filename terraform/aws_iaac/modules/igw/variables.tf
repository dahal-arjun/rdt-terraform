# The VPC ID where the Internet Gateway will be attached
variable "vpc_id" {
  description = "The VPC ID where the Internet Gateway will be attached"
  type        = string
}

# Name tag for the Internet Gateway
variable "name" {
  description = "Name tag for the Internet Gateway"
  type        = string
}
