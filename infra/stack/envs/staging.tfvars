# staging environment. All envs start at the minimum spec; change sizes here when needed
environment       = "staging"
vpc_cidr          = "10.20.0.0/16"
db_min_acu        = 0
db_max_acu        = 1
api_cpu           = 256
api_memory        = 512
api_desired_count = 1
