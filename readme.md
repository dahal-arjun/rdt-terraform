# Terraform Configuration Documentation

## Table of Contents

1. **Introduction**
    - Purpose of the Documentation
    - Prerequisites
    - Terraform Overview

2. **Terraform Configuration**
    - `main.tf` Overview
    - Provider Configuration
    - AWS Key Pair Resource
    - AWS Security Group Resource
    - AWS EC2 Instance Resource
    - Ansible Host Resource
    

3. **Variable Definitions**
    - Input Variables
    - Output Variables

4. **Usage**
    - Initializing Terraform
    - Planning the Infrastructure
    - Applying the Configuration
    - Destroying Resources

---

## 1. Introduction

### Purpose of the Documentation

This documentation provides an overview and explanation of the `main.tf` Terraform configuration file. The configuration file defines the AWS infrastructure provisioning and management using Terraform, along with Ansible integration.

### Prerequisites

Before using this Terraform configuration, make sure you have the following prerequisites:

- [Terraform](https://www.terraform.io/downloads.html) installed.
- AWS access and secret keys with the necessary permissions.
- A valid SSH key pair for connecting to EC2 instances.
- Ansible installed (if using Ansible provisioner).

### Terraform Overview

Terraform is an infrastructure-as-code (IAC) tool that allows you to define and provision infrastructure in a declarative configuration language. It creates and manages resources such as virtual machines, networks, and storage in a consistent and predictable manner.

## 2. Terraform Configuration

### `main.tf` Overview

The `main.tf` file contains the main Terraform configuration for provisioning AWS resources and integrating Ansible for configuration management. Here's an overview of its contents:

```hcl
terraform {
  required_providers {
    ansible = {
      source  = "ansible/ansible"
      version = "~> 1.1.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  access_key = var.access_key
  secret_key = var.secret_key
  region     = var.region
}

resource "aws_key_pair" "ssh_key" {
  key_name   = var.ssh_key_name
  public_key = file(var.ssh_public_key_path)
}

resource "aws_security_group" "ec2_security_group" {
  name = var.security_group_name

  dynamic "ingress" {
    for_each = var.ingress_rules
    content {
      from_port   = ingress.value.from_port
      to_port     = ingress.value.to_port
      protocol    = ingress.value.protocol
      cidr_blocks = ingress.value.cidr_blocks
    }
  }
}

resource "aws_instance" "ec2_instance" {
  ami             = var.ami_id
  instance_type   = var.instance_type
  security_groups = [aws_security_group.ec2_security_group.name]
  key_name        = aws_key_pair.ssh_key.key_name
  tags = {
    Name = var.instance_name
  }
}

resource "ansible_host" "my_ec2" {
  name   = aws_instance.ec2_instance.public_dns
  groups = ["nginx"]
  variables = {
    ansible_user                 = "ec2-user"
    ansible_ssh_private_key_file = var.ssh_private_key_path
    ansible_python_interpreter   = "/usr/bin/python3"
  }
}
```

### Provider Configuration

The `required_providers` block specifies the required providers for this configuration, including Ansible and AWS. It also defines their versions.

### AWS Provider

The `provider "aws"` block configures the AWS provider with the access key, secret key, and AWS region obtained from input variables.

### AWS Key Pair Resource

The `resource "aws_key_pair" "ssh_key"` block creates an AWS key pair using the provided public key file.

### AWS Security Group Resource

The `resource "aws_security_group" "ec2_security_group"` block defines an AWS security group with dynamic ingress rules based on input variables.

### AWS EC2 Instance Resource

The `resource "aws_instance" "ec2_instance"` block creates an AWS EC2 instance using the specified AMI, instance type, security group, and SSH key pair.

### Ansible Host Resource

The `resource "ansible_host" "my_ec2"` block defines an Ansible host that corresponds to the AWS EC2 instance. It specifies Ansible-specific variables for configuring the remote connection.

## 3. Variable Definitions

This configuration relies on input variables to make it flexible and reusable. Below are the input variables:

- `access_key`: AWS access key.
- `secret_key`: AWS secret key.
- `region`: AWS region.
- `ssh_key_name`: Name of the SSH key pair.
- `ssh_public_key_path`: Path to the SSH public key file.
- `security_group_name`: Name of the AWS security group.
- `ingress_rules`: List of ingress rules for the security group.
- `ami_id`: ID of the AMI to use for the EC2 instance.
- `instance_type`: EC2 instance type.
- `instance_name`: Name tag for the EC2 instance.
- `ssh_private_key_path`: Path to the SSH private key file.

## 4. Usage

### Initializing Terraform

Before using this configuration, initialize Terraform in the working directory:

```bash
terraform init
```

### Planning the Infrastructure

To see what resources Terraform will create or modify, use the `terraform plan` command:

```bash
terraform plan
```

### Applying the Configuration

To create or modify AWS resources, apply the Terraform configuration:

```bash
terraform apply
```

### Destroying Resources

When you no longer need the resources created by Terraform, you can destroy them using:

```bash
terraform destroy
```

Remember that this will delete all resources created by this configuration, so use it with caution.

---

This documentation provides an overview of the Terraform configuration in `main.tf`. Ensure you have the required prerequisites and customize the input variables to match your needs before running Terraform commands.

## Variable Definitions

This Terraform configuration uses several input variables to customize and tailor the infrastructure provisioning. Below are the descriptions of these input variables:

- **`access_key`** (Required)

   - **Description:** The AWS access key is used for authenticating with the AWS console and provisioning resources. It should have the necessary permissions for the required operations.
   - **Example Value:** `"YOUR_ACCESS_KEY"`

- **`secret_key`** (Required)

   - **Description:** The AWS secret key is used in conjunction with the access key for authentication when interacting with the AWS services.
   - **Example Value:** `"YOUR_SECRET_KEY"`

- **`region`** (Required)

   - **Description:** The AWS region where the resources will be created. Different regions represent geographically distinct AWS data centers.
   - **Example Value:** `"us-east-1"`

- **`instance_name`** (Required)

   - **Description:** This variable specifies the desired name for the EC2 instance(s) that will be created.
   - **Example Value:** `"MyInstance"`

- **`instance_type`** (Required)

   - **Description:** The instance type determines the computational capacity of the EC2 instance(s) to be launched, such as CPU and memory.
   - **Example Value:** `"t2.micro"`

- **`subnet_id`** (Required)

   - **Description:** The VPC subnet ID specifies the specific Virtual Private Cloud (VPC) subnet where the EC2 instance(s) will be deployed.
   - **Example Value:** `"subnet-12345678"`

- **`ami_id`** (Required)

   - **Description:** The AMI (Amazon Machine Image) ID represents the base image used to create the EC2 instance(s). It contains the operating system and additional software.
   - **Example Value:** `"ami-0123456789abcdef0"`

- **`number_of_instances`** (Required)

   - **Description:** This variable determines the number of EC2 instances to be created within the specified subnet.
   - **Example Value:** `2`

- **`security_group_name`** (Optional)

   - **Description:** The name of the AWS security group that will be associated with the EC2 instances. If not provided, the default value is `"default-security-group"`.
   - **Example Value:** `"my-security-group"`

- **`ingress_rules`** (Optional)

   - **Description:** Ingress rules define the list of inbound traffic rules for the security group. You can specify allowed ports, protocols, and source IP ranges.
   - **Example Value:** See the example below:

     ```hcl
     ingress_rules = [
       {
         from_port   = 22
         to_port     = 22
         protocol    = "tcp"
         cidr_blocks = ["0.0.0.0/0"]
       },
       {
         from_port   = 80
         to_port     = 80
         protocol    = "tcp"
         cidr_blocks = ["0.0.0.0/0"]
       }
     ]
     ```

- **`ssh_key_name`** (Required)

   - **Description:** The name of the SSH key pair used for SSH access to the EC2 instance(s). This key pair should already exist in your AWS account.
   - **Example Value:** `"my-ssh-key"`

- **`ssh_public_key_path`** (Required)

   - **Description:** The local file path to the SSH public key used for authenticating to the EC2 instance(s). This file should exist on your local machine.
   - **Example Value:** `"~/.ssh/id_rsa.pub"`

- **`ssh_private_key_path`** (Required)

   - **Description:** The local file path to the SSH private key corresponding to the public key defined above. This key is used for SSH access to the EC2 instance(s). This file should exist on your local machine and match the public key.
   - **Example Value:** `"~/.ssh/id_rsa"`

These input variables provide flexibility and customization options for configuring your AWS infrastructure using Terraform.


It looks like you have a project structure with directories for Ansible and Terraform. Here's a brief explanation of the contents of each directory and the project structure:

```plaintext
.
├── ansible
│   └── playbook.yml
├── readme.md
└── terraform
    ├── main.tf
    ├── terraform.tfstate
    ├── terraform.tfstate.backup
    ├── terraform.tfvars
    └── variables.tf
```

- **ansible**: This directory contains Ansible-related files.

  - `playbook.yml`: This file likely contains Ansible playbook(s) that define tasks and configurations for managing servers or services.

- **terraform**: This directory contains Terraform-related files.

  - `main.tf`: This is the main Terraform configuration file you provided earlier, which defines your AWS infrastructure and integrates Ansible.

  - `terraform.tfstate` and `terraform.tfstate.backup`: These files store the state of your Terraform-managed infrastructure. They should be kept in version control, but they contain sensitive information and should be protected.

  - `terraform.tfvars`: This file can store input variable values for your Terraform configuration. It is a convenient way to separate variable values from the main configuration.

  - `variables.tf`: This file defines your Terraform input variables along with their descriptions.

- `readme.md`: This is likely your project's README file, which should contain documentation, usage instructions, and explanations of your project's structure and purpose.
