terraform {
    required_version = ">= 0.11"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.89"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-west-1"
}