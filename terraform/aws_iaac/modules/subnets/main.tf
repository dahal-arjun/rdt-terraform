resource "aws_subnet" "public_subnet" {
  count      = length(var.subnet_cidrs)
  vpc_id     = var.vpc_id
  availability_zone = element(var.availability_zones, count.index)
  cidr_block = element(var.subnet_cidrs, count.index)
  tags = {
    "Name" = "Spark Subnet ${count.index + 1}",
  }
}


resource "aws_route_table_association" "public_subnet_asso" {
  count          = length(var.subnet_cidrs)
  subnet_id      = element(aws_subnet.public_subnet[*].id, count.index)
  route_table_id = var.route_table_id
}

