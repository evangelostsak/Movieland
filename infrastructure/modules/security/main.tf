resource "aws_security_group" "ec2_sg" {
  name = "${var.app_name}-${var.environment_name}-instance-security-group"
  vpc_id = aws_vpc.main.id
}

# Allow traffic from ALB to EC2 on flask port
resource "aws_security_group_rule" "allow_flask_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = var.security_group_ports[4]
  to_port     = var.security_group_ports[4]
  protocol    = var.protocols[2]
  source_security_group_id = aws_security_group.alb.id  # Only allow ALB traffic
}

# Allow SSH from a specific IP
resource "aws_security_group_rule" "allow_ssh_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = var.security_group_ports[0]
  to_port     = var.security_group_ports[0]
  protocol    = var.protocols[2]
  cidr_blocks = [var.allowed_ssh_ip]
}

resource "aws_security_group" "alb" {
  name   = "${var.app_name}-${var.environment_name}-alb-security-group"
  vpc_id = aws_vpc.main.id
}

# Allow public access to ALB on Port 80
resource "aws_security_group_rule" "allow_alb_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.alb.id
  from_port   = var.security_group_ports[1]
  to_port     = var.security_group_ports[1]
  protocol    = var.protocols[0]
  cidr_blocks = ["0.0.0.0/0"]
}

# Allow public access to ALB on Port 443
resource "aws_security_group_rule" "allow_alb_https_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.alb.id
  from_port   = var.security_group_ports[2]
  to_port     = var.security_group_ports[2]
  protocol    = var.protocols[1]
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group" "rds_sg" {
  name   = "${var.app_name}-${var.environment_name}-rds-security-group"
  vpc_id = aws_vpc.main.id
}

# Allow EC2 to access PostgreSQL on RDS
resource "aws_security_group_rule" "allow_rds_from_ec2" {
  type              = "ingress"
  security_group_id = aws_security_group.rds_sg.id

  from_port   = var.security_group_ports[3]
  to_port     = var.security_group_ports[3]
  protocol    = var.protocols[2]
  source_security_group_id = aws_security_group.ec2_sg.id
}