#!/usr/bin/env bash

stack_name="$1"
template_file="$2"

aws cloudformation deploy \
  --stack-name "$stack_name" \
  --template-file "$template_file"

