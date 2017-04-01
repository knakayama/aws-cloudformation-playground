S3_BUCKET = _YOUR_S3_BUCKET_
STACK_NAME = lambda-backed-custom-resource-backed-aws-transform

package:
	@[ -d .cfn ] || mkdir .cfn
	@aws s3 cp ../latest-ami.yml s3://$(S3_BUCKET)
	@aws cloudformation package \
		--template-file cfn.yml \
		--s3-bucket $(S3_BUCKET) \
		--s3-prefix cfn/$(STACK_NAME)/`date '+%Y%m%d'` \
		--output-template-file .cfn/packaged.yml

deploy:
	@if [ -f params/param.json ]; then \
		aws cloudformation deploy \
			--template-file .cfn/packaged.yml \
			--stack-name $(STACK_NAME) \
			--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
			--parameter-overrides `cat params/param.json | jq -r '.Parameters | to_entries | map("\(.key)=\(.value|tostring)") | .[]' | tr '\n' ' ' | awk '{print}'` \
			--no-execute-changeset; \
	else \
		aws cloudformation deploy \
			--template-file .cfn/packaged.yml \
			--stack-name $(STACK_NAME) \
			--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
			--no-execute-changeset; \
	fi

execute-changeset:
	@aws cloudformation execute-change-set \
		--stack-name $(STACK_NAME) \
		--change-set-name `aws cloudformation list-change-sets \
			--stack-name $(STACK_NAME) \
			--query 'reverse(sort_by(Summaries,&CreationTime))[0].ChangeSetName' \
			--output text`

all: package deploy execute-changeset

.PHONY: package deploy execute-changeset all
