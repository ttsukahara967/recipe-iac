resource "random_password" "db" {
  length  = 32
  special = false
}

# Password reaches ECS tasks via Secrets Manager (never in plain text in the task definition)
resource "aws_secretsmanager_secret" "db" {
  name = "${local.name}/db-password"
  # Delete immediately (no recovery window) so the same name can be reused right after destroy
  recovery_window_in_days = 0
}

resource "aws_secretsmanager_secret_version" "db" {
  secret_id     = aws_secretsmanager_secret.db.id
  secret_string = random_password.db.result
}

resource "aws_db_subnet_group" "main" {
  name       = local.name
  subnet_ids = aws_subnet.private[*].id
}

resource "aws_rds_cluster" "main" {
  cluster_identifier     = local.name
  engine                 = "aurora-postgresql"
  engine_mode            = "provisioned"
  engine_version         = var.db_engine_version
  database_name          = "recipes"
  master_username        = "recipe_admin"
  master_password        = random_password.db.result
  db_subnet_group_name   = aws_db_subnet_group.main.name
  vpc_security_group_ids = [aws_security_group.db.id]
  storage_encrypted      = true
  apply_immediately      = true

  # Lets `make destroy` remove everything in one go. Revisit before running real production
  skip_final_snapshot = true
  deletion_protection = false

  serverlessv2_scaling_configuration {
    min_capacity             = var.db_min_acu
    max_capacity             = var.db_max_acu
    seconds_until_auto_pause = var.db_min_acu == 0 ? var.db_auto_pause_seconds : null
  }
}

resource "aws_rds_cluster_instance" "main" {
  identifier         = "${local.name}-1"
  cluster_identifier = aws_rds_cluster.main.id
  instance_class     = "db.serverless"
  engine             = aws_rds_cluster.main.engine
  engine_version     = aws_rds_cluster.main.engine_version
  apply_immediately  = true
}
