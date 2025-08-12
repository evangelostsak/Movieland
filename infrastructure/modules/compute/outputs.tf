output "launch_template_id" {
  description = "ID of the EC2 launch template"
  value       = aws_launch_template.app_template.id
}

output "launch_template_name" {
  description = "Name of the EC2 launch template"
  value       = aws_launch_template.app_template.name
}

output "autoscaling_group_name" {
  description = "Name of the Auto Scaling Group"
  value       = aws_autoscaling_group.app_asg.name
}

output "autoscaling_group_arn" {
  description = "ARN of the Auto Scaling Group"
  value       = aws_autoscaling_group.app_asg.arn
}