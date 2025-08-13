resource "aws_security_group" "ec2_sg" {
  name = "${var.app_name}-${var.environment_name}-instance-security-group"
  vpc_id = var.vpc_id
}

# Allow traffic from ALB to EC2 on flask port
resource "aws_security_group_rule" "allow_flask_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = var.flask_port
  to_port     = var.flask_port
  protocol    = "tcp"
  source_security_group_id = aws_security_group.alb.id  # Only allow ALB traffic
}

# Allow SSH from a specific IP
resource "aws_security_group_rule" "allow_ssh_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = var.ssh_port
  to_port     = var.ssh_port
  protocol    = "tcp"
  cidr_blocks = [var.allowed_ssh_ip]
}

# Allow all outbound from EC2 (needed for internet access rn, will be restricted later)
resource "aws_security_group_rule" "ec2_allow_all_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.ec2_sg.id
  from_port         = 0
  to_port           = 0
  protocol          = "-1"
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group" "alb" {
  name   = "${var.app_name}-${var.environment_name}-alb-security-group"
  vpc_id = var.vpc_id
}

# Allow public access to ALB on Port 80
resource "aws_security_group_rule" "allow_alb_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.alb.id
  from_port   = var.http_port
  to_port     = var.http_port
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

# Allow public access to ALB on Port 443
resource "aws_security_group_rule" "allow_alb_https_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.alb.id
  from_port   = var.https_port
  to_port     = var.https_port
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group" "rds_sg" {
  name   = "${var.app_name}-${var.environment_name}-rds-security-group"
  vpc_id = var.vpc_id
}

# Allow EC2 to access PostgreSQL on RDS
resource "aws_security_group_rule" "allow_rds_from_ec2" {
  type              = "ingress"
  security_group_id = aws_security_group.rds_sg.id

  from_port   = var.postgres_port
  to_port     = var.postgres_port
  protocol    = "tcp"
  source_security_group_id = aws_security_group.ec2_sg.id
}