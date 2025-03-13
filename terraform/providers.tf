terraform {
  required_version = ">= 0.11"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.89"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0.5"
    }
  }
}

provider "aws" {
  region = var.region
}