# The name for the SSH key pair
variable "ssh_key_name" {
  description = "Name for the SSH key pair"
  type        = string
}

# The file path to the public key to be used
variable "ssh_public_key_path" {
  description = "File path to the public key to be used for the SSH key pair"
  type        = string
}
