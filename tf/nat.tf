resource "aws_eip" "nat" {
  tags = {
    Name = "${local.env}"
  }
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_zone1.id

  tags = {
    Name = "${local.env}"
  }

  depends_on = [aws_internet_gateway.igw]
}

