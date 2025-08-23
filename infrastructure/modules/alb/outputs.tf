output "alb_target_group_arn" {
  description = "ARN of the ALB target group"
  value       = aws_lb_target_group.instances.arn
}

output "alb_dns_name" {
  description = "DNS name of the ALB"
  value       = aws_lb.load_balancer.dns_name
}