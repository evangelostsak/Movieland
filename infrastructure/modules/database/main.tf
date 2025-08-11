resource "aws_db_instance" "db_instance" {
  allocated_storage   = 20
  storage_type        = "standard"
  engine              = "postgres"
  engine_version      = "15.12"
  instance_class      = var.db_class
  identifier          = var.db_name
  username            = var.db_user
  password            = var.db_pass
  skip_final_snapshot = true
  backup_retention_period = 7
  monitoring_interval = 60  # Enhanced monitoring every 60s
  monitoring_role_arn = aws_iam_role.rds_monitoring.arn
  db_subnet_group_name = aws_db_subnet_group.db_subnet_group.name
  publicly_accessible  = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
}

resource "aws_db_instance" "db_read_replica" {
  identifier              = "${var.db_name}-replica"
  instance_class          = var.db_class
  engine                  = "postgres"
  replicate_source_db     = aws_db_instance.db_instance.identifier
  backup_retention_period = 7
  skip_final_snapshot     = true
  publicly_accessible     = false
  monitoring_interval     = 60
  monitoring_role_arn     = aws_iam_role.rds_monitoring.arn
  availability_zone       = var.read_replica_az

  depends_on = [aws_db_instance.db_instance]
}
resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "movieland-db-subnet-group"
  subnet_ids = [
    aws_subnet.private_a.id,
    aws_subnet.private_b.id,
    aws_subnet.private_c.id,
  ]

  tags = {
    Name = "movieland-db-subnet-group"
  }
}


# IAM Role for RDS Monitoring
resource "aws_iam_role" "rds_monitoring" {
  name = "rds-monitoring-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "monitoring.rds.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}

# Attach RDS monitoring policy to the role
resource "aws_iam_role_policy_attachment" "rds_monitoring_policy" {
  role       = aws_iam_role.rds_monitoring.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonRDSEnhancedMonitoringRole"
}