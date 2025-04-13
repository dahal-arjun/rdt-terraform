output "vpc_id" {
  description = "The ID of the VPC."
  value       = aws_vpc.spark_vpc.id
}