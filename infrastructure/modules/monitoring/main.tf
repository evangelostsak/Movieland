resource "aws_cloudwatch_metric_alarm" "high_cpu_usage" {
  alarm_name          = "asg-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80.0
  alarm_description   = "Average CPU usage of ASG instances is too high"
  actions_enabled     = true
  alarm_actions       = [aws_sns_topic.cloudwatch_alerts.arn]
  ok_actions          = [aws_sns_topic.cloudwatch_alerts.arn]

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app_asg.name
  }
}

resource "aws_cloudwatch_metric_alarm" "low_disk_space" {
  alarm_name          = "asg-low-disk-space"
  comparison_operator = "LessThanThreshold"
  evaluation_periods  = 2
  metric_name         = "disk_used_percent"
  namespace           = "CWAgent"
  period              = 300
  statistic           = "Average"
  threshold           = 80.0
  alarm_description   = "Disk usage is over 80% on ASG instances"
  actions_enabled     = true
  alarm_actions       = [aws_sns_topic.cloudwatch_alerts.arn]
  ok_actions          = [aws_sns_topic.cloudwatch_alerts.arn]

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app_asg.name
    Filesystem           = "/dev/xvda1"
    MountPath            = "/"
  }
}

resource "aws_sns_topic" "cloudwatch_alerts" {
  name = "cloudwatch-alerts"
}

resource "aws_sns_topic_subscription" "email_subscription" {
  topic_arn = aws_sns_topic.cloudwatch_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}