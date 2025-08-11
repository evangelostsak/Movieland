resource "aws_security_group" "ec2_sg" {
  name = "${var.app_name}-${var.environment_name}-instance-security-group"
  vpc_id = aws_vpc.main.id
}

# Allow ALB to send traffic to Flask on EC2 (Port 5000)
resource "aws_security_group_rule" "allow_flask_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = 80
  to_port     = 80
  protocol    = "http"
  source_security_group_id = aws_security_group.alb.id  # Only allow ALB traffic
}

# Allow SSH from your IP (Replace with your actual IP)
resource "aws_security_group_rule" "allow_ssh_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = 22
  to_port     = 22
  protocol    = "tcp"
  cidr_blocks = [var.allowed_ssh_ip]
}

# Allow EC2 to communicate with RDS on Port 5432
resource "aws_security_group_rule" "allow_rds_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = 5432
  to_port     = 5432
  protocol    = "tcp"
  source_security_group_id = aws_security_group.rds_sg.id
}

# Allow all outbound traffic from EC2
resource "aws_security_group_rule" "allow_ec2_all_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.ec2_sg.id

  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}

resource "aws_security_group" "alb" {
  name   = "${var.app_name}-${var.environment_name}-alb-security-group"
  vpc_id = aws_vpc.main.id
}

# Allow public access to ALB on Port 80
resource "aws_security_group_rule" "allow_alb_http_inbound" {
  type              = "ingress"
  security_group_id = aws_security_group.alb.id

  from_port   = 80
  to_port     = 80
  protocol    = "tcp"
  cidr_blocks = ["0.0.0.0/0"]
}

# Allow ALB to send traffic to EC2 on Port 5000
resource "aws_security_group_rule" "allow_alb_flask_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.alb.id

  from_port   = 80
  to_port     = 80
  protocol    = "http"
  source_security_group_id = aws_security_group.ec2_sg.id
}

resource "aws_security_group" "rds_sg" {
  name   = "${var.app_name}-${var.environment_name}-rds-security-group"
  vpc_id = aws_vpc.main.id
}

# Allow EC2 to access PostgreSQL on RDS
resource "aws_security_group_rule" "allow_rds_from_ec2" {
  type              = "ingress"
  security_group_id = aws_security_group.rds_sg.id

  from_port   = 5432
  to_port     = 5432
  protocol    = "tcp"
  source_security_group_id = aws_security_group.ec2_sg.id
}

# Allow RDS to communicate out
resource "aws_security_group_rule" "allow_rds_all_outbound" {
  type              = "egress"
  security_group_id = aws_security_group.rds_sg.id

  from_port   = 0
  to_port     = 0
  protocol    = "-1"
  cidr_blocks = ["0.0.0.0/0"]
}