resource "aws_instance" "devops_lab_terraform" {
  ami           = "ami-03fd334507439f4d1" # eu-west-1
  instance_type = "t2.micro"

  tags = {
    Name = "devops_lab_terraform_instance"
  }

}