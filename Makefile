# ==============================================================================
#  recipe-iac
#    Local:     make local-up / make local-down
#    AWS:       make bootstrap                 (once per account: S3 state bucket + ECR)
#               make deploy  ENV=develop       (push image -> Terraform -> SST; builds the whole env)
#               make destroy ENV=develop       (tears down the whole env)
#               make nuke                      (deletes every env + state bucket + ECR)
# ==============================================================================

ENV        ?= develop
ENVS       := develop staging production
AWS_REGION ?= ap-northeast-1
STACK      := infra/stack
BOOTSTRAP  := infra/bootstrap
TF_VERSION ?= 1.16

export AWS_REGION

AWS_DOCKER_OPTS = -v "$(HOME)/.aws:/root/.aws" \
	-e AWS_PROFILE -e AWS_REGION -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN

# Fall back to the official docker images when terraform / aws CLI are not installed
ifeq ($(shell command -v terraform 2>/dev/null),)
TF = docker run --rm -i -v "$(CURDIR):/work" -w /work $(AWS_DOCKER_OPTS) \
	-e TF_DATA_DIR -e TF_IN_AUTOMATION hashicorp/terraform:$(TF_VERSION)
else
TF = terraform
endif

ifeq ($(shell command -v aws 2>/dev/null),)
AWS = docker run --rm -i $(AWS_DOCKER_OPTS) amazon/aws-cli
else
AWS = aws
endif

# Separate .terraform dir per env so switching backends never mixes state
TF_STACK = TF_DATA_DIR=.terraform-$(ENV) $(TF) -chdir=$(STACK)

# Image tag = hash of the backend sources, so unchanged code never triggers a redeploy
IMAGE_TAG := $(shell cat backend/Dockerfile backend/requirements.txt $$(find backend/app -name '*.py' | sort) | shasum | cut -c1-12)

# Shell snippet that reads the state bucket / ECR repo from the bootstrap outputs
GET_BOOTSTRAP = bucket=$$($(TF) -chdir=$(BOOTSTRAP) output -raw state_bucket 2>/dev/null) && \
	repo=$$($(TF) -chdir=$(BOOTSTRAP) output -raw ecr_repository_url 2>/dev/null) && \
	[ -n "$$bucket" ] && [ -n "$$repo" ] \
	|| { echo "Bootstrap not found. Run 'make bootstrap' first."; exit 1; }

.PHONY: help local-up local-down local-clean local-logs bootstrap push-image tf-init plan \
	deploy deploy-backend deploy-frontend outputs destroy destroy-frontend destroy-backend nuke check-env confirm

help:
	@grep -E '^#  |^#    ' Makefile | sed 's/^#//'

# ---------------------------------------------------------------- local (docker)
local-up:
	docker compose up --build -d
	@echo ""
	@echo "  Frontend: http://localhost:3000"
	@echo "  API:      http://localhost:8000/docs"

local-down:
	docker compose down

local-clean:
	docker compose down -v --rmi local

local-logs:
	docker compose logs -f

# ---------------------------------------------------------------- AWS
check-env:
	@case "$(ENV)" in develop|staging|production) ;; \
	  *) echo "ENV must be one of develop / staging / production (got ENV=$(ENV))"; exit 1;; esac

# Pass YES=1 to skip the confirmation prompt
confirm:
	@if [ "$(YES)" != "1" ]; then \
	  printf "⚠️  This will delete $(TARGET_DESC). Continue? [y/N] "; read ans; \
	  [ "$$ans" = "y" ] || [ "$$ans" = "Y" ] || { echo "Aborted."; exit 1; }; \
	fi

bootstrap:
	$(TF) -chdir=$(BOOTSTRAP) init -input=false
	$(TF) -chdir=$(BOOTSTRAP) apply -input=false -auto-approve

# Build the API image (arm64) and push it to ECR
push-image:
	@$(GET_BOOTSTRAP); \
	echo "==> $$repo:$(IMAGE_TAG)"; \
	$(AWS) ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $${repo%%/*} && \
	docker build --platform linux/arm64 -t $$repo:$(IMAGE_TAG) backend && \
	docker push $$repo:$(IMAGE_TAG)

tf-init: check-env
	@$(GET_BOOTSTRAP); \
	$(TF_STACK) init -input=false -reconfigure \
	  -backend-config="bucket=$$bucket" \
	  -backend-config="key=stack/$(ENV).tfstate" \
	  -backend-config="region=$(AWS_REGION)"

plan: check-env tf-init
	@$(GET_BOOTSTRAP); \
	$(TF_STACK) plan -input=false -var-file=envs/$(ENV).tfvars -var="api_image=$$repo:$(IMAGE_TAG)"

deploy: check-env deploy-backend deploy-frontend
	@echo ""
	@echo "✅ Deployed $(ENV)"

deploy-backend: check-env push-image tf-init
	@$(GET_BOOTSTRAP); \
	$(TF_STACK) apply -input=false -auto-approve -var-file=envs/$(ENV).tfvars -var="api_image=$$repo:$(IMAGE_TAG)"

deploy-frontend: check-env tf-init
	cd frontend && npm install --no-audit --no-fund
	@api_url=$$($(TF_STACK) output -raw api_url) && \
	  echo "API_URL=$$api_url" && \
	  cd frontend && API_URL=$$api_url npx sst deploy --stage $(ENV)

outputs: check-env tf-init
	$(TF_STACK) output

destroy: check-env
	@$(MAKE) --no-print-directory confirm TARGET_DESC="the $(ENV) environment"
	@$(MAKE) --no-print-directory destroy-frontend destroy-backend ENV=$(ENV)
	@echo ""
	@echo "🗑  Destroyed $(ENV)"

destroy-frontend: check-env
	cd frontend && npm install --no-audit --no-fund
	cd frontend && API_URL=removing npx sst remove --stage $(ENV)

destroy-backend: check-env tf-init
	$(TF_STACK) destroy -input=false -auto-approve -var-file=envs/$(ENV).tfvars

nuke:
	@$(MAKE) --no-print-directory confirm TARGET_DESC="ALL environments ($(ENVS)) plus the Terraform state bucket and ECR"
	@for e in $(ENVS); do \
	  $(MAKE) --no-print-directory destroy-frontend destroy-backend ENV=$$e || exit 1; \
	done
	$(TF) -chdir=$(BOOTSTRAP) destroy -input=false -auto-approve
