output "db_instance_addr" {
  value = aws_db_instance.db_instance.address
}

output "db_endpoint" {
  description = "Database endpoint"
  value       = aws_db_instance.db_instance.endpoint
}

output "db_identifier" {
  description = "Database identifier"
  value       = aws_db_instance.db_instance.id
}

output "read_replica_endpoint" {
  description = "Read replica endpoint"
  value       = aws_db_instance.db_read_replica.endpoint
}