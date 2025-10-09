resource "aws_cloudwatch_metric_alarm" "high_cpu_usage" {
  alarm_name          = "${var.app_name}-${var.environment_name}-high_cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = var.cpu_threshold
  alarm_description   = "Average CPU usage of ASG instances is too high"
  actions_enabled     = true
  alarm_actions       = [aws_sns_topic.cloudwatch_alerts.arn]
  ok_actions          = [aws_sns_topic.cloudwatch_alerts.arn]

 dimensions = {
  AutoScalingGroupName = var.asg_name
 }
}

resource "aws_cloudwatch_metric_alarm" "low_disk_space" {
  alarm_name          = "${var.app_name}-${var.environment_name}-low_disk_space"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  metric_name         = "disk_used_percent"
  namespace           = "CWAgent"
  period              = 300
  statistic           = "Average"
  threshold           = var.disk_threshold
  alarm_description   = "Disk usage is over 80% on ASG instances"
  actions_enabled     = true
  alarm_actions       = [aws_sns_topic.cloudwatch_alerts.arn]
  ok_actions          = [aws_sns_topic.cloudwatch_alerts.arn]

  dimensions = {
    AutoScalingGroupName = var.asg_name
    Filesystem           = "/dev/xvda1"
    MountPath            = "/"
  }
}

resource "aws_sns_topic" "cloudwatch_alerts" {
  name = "${var.app_name}-${var.environment_name}-cloudwatch_alerts"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.cloudwatch_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}