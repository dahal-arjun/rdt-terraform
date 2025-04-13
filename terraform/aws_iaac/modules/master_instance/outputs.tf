output "ec2_instance_id" {
  value = aws_instance.ec2_master_instance.id
}

output "master_instance_ip" {
  value = aws_eip_association.eip_assoc.public_ip
}