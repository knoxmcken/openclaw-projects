#!/bin/bash

# Script to list Google Cloud VM instances in us-central1-a
# Usage: ./list_vms.sh

ZONE="us-central1-a"

echo "Listing instances in zone: $ZONE..."
echo

gcloud compute instances list \
    --zones="$ZONE" \
    --format="table(name,status,INTERNAL_IP,EXTERNAL_IP)"
