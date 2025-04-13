resource "aws_route_table" "route_table" {
  vpc_id = var.vpc_id

  route {
    cidr_block = var.default_route_cidr
    gateway_id = var.internet_gateway_id
  }

  tags = {
    "Name" = var.route_table_name
  }
}



