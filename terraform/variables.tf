variable "region" {
  default     = "eu-west-1"
  description = "AWS region to deploy resources"
}

variable "ami_id" {
  default     = "ami-03fd334507439f4d1"
  description = "AMI ID for the EC2 instances"
}

variable "instance_type" {
  default     = "t2.micro"
  description = "Instance type for the EC2 instance"
}

variable "iilin_ssh_public_key" {
  description = "Public SSH key from i.ilin"
  default     = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIOkAhvfRyUvgsUwENIds1a/4OvuHQgLki8K1EzPltl5M i.ilin@iilin-pro14.local"
}