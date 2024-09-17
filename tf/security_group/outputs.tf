output "allow_all_id" {
  value = aws_security_group.allow_all_sg.id
}

output "prod_id" {
  value = aws_security_group.production_sg.id
}
