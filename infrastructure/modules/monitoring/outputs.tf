output "sns_topic_arn" {
  description = "ARN of the SNS topic for CloudWatch alerts"
  value       = aws_sns_topic.cloudwatch_alerts.arn
}

output "high_cpu_alarm_arn" {
  description = "ARN of the high CPU CloudWatch alarm"
  value       = aws_cloudwatch_metric_alarm.high_cpu_usage.arn
}

output "low_disk_alarm_arn" {
  description = "ARN of the low disk space CloudWatch alarm"
  value       = aws_cloudwatch_metric_alarm.low_disk_space.arn
}