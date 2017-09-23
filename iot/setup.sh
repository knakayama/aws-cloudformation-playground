#!/usr/bin/env bash

set -eux

aws_region="ap-northeast-1"
output="iot-cert.json"
private="private.pem.key"
certificate="certificate.pem.crt"

usage() {
  cat <<'EOT'
Usage: setup.sh [-r region] [-h]
  -r     AWS region
  -h     Print this help
EOT
}

while getopts ':r:h' args; do
  case "$args" in
    r)
      aws_region="$OPTARG"
      ;;
    h)
      usage
      exit 0
      ;;
    *)
      usage
      exit 1
      ;;
  esac
done

aws iot create-keys-and-certificate --set-as-active --region "$aws_region" > "$output"
cat "$output" | jq -r '.keyPair.PrivateKey' > "$private"
cat "$output" | jq -r '.certificatePem' > "$certificate"
