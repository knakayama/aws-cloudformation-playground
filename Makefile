SHELL = /usr/bin/env bash -xeuo pipefail

STACK_NAME =
OUTPUT = $(STACK_NAME)/output/output.json
PRIVATE_KEY = $(STACK_NAME)/output/private.key
CERTIFICATE = $(STACK_NAME)/output/cert.crt

iot-certificate:
	@aws iot create-keys-and-certificate --set-as-active > $(OUTPUT)
	@cat $(OUTPUT) | jq -r '.keyPair.PrivateKey' > $(PRIVATE_KEY)
	@cat $(OUTPUT) | jq -r '.certificatePem' > $(CERTIFICATE)

deploy:
	@aws cloudformation deploy \
		--template-file $(STACK_NAME)/template.yml \
		--stack-name $(STACK_NAME) \
		--capabilities CAPABILITY_IAM \
		--parameter-overrides IoTCertificateArn=$$(cat $(OUTPUT) | jq -r '.certificateArn')
	@$(MAKE) output

output:
	@aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[].Outputs' \
		--output table

output:
	@aws cloudformation describe-stacks \
		--stack-name $(STACK_NAME) \
		--query 'Stacks[].Outputs' \
		--output table

.PHONY: \
	iot-certificate \
	deploy \
	output
