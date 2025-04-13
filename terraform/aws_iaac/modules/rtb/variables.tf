# The VPC ID where the route table will be associated
variable "vpc_id" {
  description = "The VPC ID where the route table will be associated"
  type        = string
}

# The CIDR block for the default route
variable "default_route_cidr" {
  description = "The CIDR block for the default route (0.0.0.0/0)"
  type        = string
}

# The ID of the Internet Gateway
variable "internet_gateway_id" {
  description = "The ID of the Internet Gateway to be used as the default route target"
  type        = string
}

# Name tag for the route table
variable "route_table_name" {
  description = "Name tag for the route table"
  type        = string
}

