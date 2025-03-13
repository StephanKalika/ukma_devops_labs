resource "aws_security_group" "server_sg" {
  name        = "server-sg"
  description = "Allow authorized access to servers"
}

# Allow SSH (port 22) from all IPs
resource "aws_vpc_security_group_ingress_rule" "ssh_ingress" {
  security_group_id    = aws_security_group.server_sg.id
  from_port            = 22
  to_port              = 22
  ip_protocol          = "tcp"
  cidr_ipv4            = "0.0.0.0/0"
}

resource "aws_vpc_security_group_ingress_rule" "db_intraserver" {
  security_group_id    = aws_security_group.server_sg.id
  from_port            = 5432
  to_port              = 5435
  ip_protocol          = "tcp"
  referenced_security_group_id = aws_security_group.server_sg.id
}

# Allow unrestricted outbound traffic
resource "aws_vpc_security_group_egress_rule" "all_egress" {
  security_group_id    = aws_security_group.server_sg.id
  from_port            = 0
  to_port              = 0
  ip_protocol          = "-1"
  cidr_ipv4            = "0.0.0.0/0"
}