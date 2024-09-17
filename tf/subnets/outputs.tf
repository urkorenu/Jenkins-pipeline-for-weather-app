output "public_a" {
  value = aws_subnet.public_a.id
}

output "private" {
  value = aws_subnet.private.id
}

output "private_rt" {
  value = aws_route_table.private.id
}