output "server_1_ip" {
  description = "The public IP address of server_1"
  value       = aws_instance.server_1.public_ip
}

output "server_2_ip" {
  description = "The public IP address of server_2"
  value       = aws_instance.server_2.public_ip
}

output "security_group_id" {
  description = "The Security Group ID for the servers"
  value       = aws_security_group.server_sg.id
}