resource "tls_private_key" "my_key" {
  algorithm = "ED25519"
}

resource "aws_key_pair" "my_ssh_key" {
  key_name   = "my-key-pair"
  public_key = tls_private_key.my_key.public_key_openssh # Use correct attribute
}

resource "aws_instance" "server_1" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = aws_key_pair.my_ssh_key.key_name
  security_groups = [aws_security_group.server_sg.name]

  tags = {
    Name = "server-1"
  }

  user_data = <<-EOF
  #!/bin/bash
  mkdir -p /home/ubuntu/.ssh
  echo "${tls_private_key.my_key.public_key_openssh}" >> /home/ubuntu/.ssh/authorized_keys
  echo "${var.iilin_ssh_public_key}" >> /home/ubuntu/.ssh/authorized_keys
  chmod 700 /home/ubuntu/.ssh
  chmod 600 /home/ubuntu/.ssh/authorized_keys
  chown -R ubuntu:ubuntu /home/ubuntu/.ssh
  EOF
}

resource "aws_instance" "server_2" {
  ami           = var.ami_id
  instance_type = var.instance_type
  key_name      = aws_key_pair.my_ssh_key.key_name
  security_groups = [aws_security_group.server_sg.name]

  tags = {
    Name = "server-2"
  }

  user_data = <<-EOF
  #!/bin/bash
  mkdir -p /home/ubuntu/.ssh
  echo "${tls_private_key.my_key.public_key_openssh}" >> /home/ubuntu/.ssh/authorized_keys
  echo "${var.iilin_ssh_public_key}" >> /home/ubuntu/.ssh/authorized_keys
  chmod 700 /home/ubuntu/.ssh
  chmod 600 /home/ubuntu/.ssh/authorized_keys
  chown -R ubuntu:ubuntu /home/ubuntu/.ssh
  EOF
}