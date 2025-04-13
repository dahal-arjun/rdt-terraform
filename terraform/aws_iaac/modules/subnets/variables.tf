# List of private subnet CIDR blocks
variable "subnet_cidrs" {
  description = "A list of CIDR blocks for public subnets"
  type        = list(string)
}
variable "availability_zones" {
  description = "A list of CIDR blocks for availibility zones"
  type        = list(string)
}

# Reference to the VPC ID
variable "vpc_id" {
  description = "The VPC ID where the subnets will be created"
  type        = string
}

variable "route_table_id" {
  description = "Route table ID where the subnets will be created"
  type = string
}