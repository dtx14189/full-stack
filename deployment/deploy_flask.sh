#!/bin/bash

# Config
ACCOUNT_ID="644160558196"
REGION="us-west-1"
LOCAL_DOCKER_IMAGE="deployment-backend"
REPO_NAME="bank-backend"
DEPLOYMENT_NAME="flask-deployment"
IMAGE_TAG="latest"
ECR_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME"

echo "Building All Docker image..."
docker-compose build

# Remove stopped containers
docker container prune

# Remove dangling images
docker image prune

# Wipe old images
aws ecr list-images \
  --repository-name bank-backend \
  --region us-west-1 \
  --query 'imageIds[*]' \
  --output json > images-to-delete.json

aws ecr batch-delete-image \
  --repository-name bank-backend \
  --region us-west-1 \
  --image-ids file://images-to-delete.json

echo "Tagging image as $ECR_URI:$IMAGE_TAG"
docker tag $LOCAL_DOCKER_IMAGE $ECR_URI:$IMAGE_TAG

echo "Logging into Amazon ECR..."
aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ECR_URI

echo "Pushing image to ECR..."
docker push $ECR_URI:$IMAGE_TAG

echo "Applying backend.yaml and postgres.yaml to cluster..."
kubectl apply -f backend.yaml -f postgres.yaml

echo "Restarting Kubernetes deployment..."
kubectl rollout restart deployment $DEPLOYMENT_NAME

rm images-to-delete.json

echo "Deployment complete. Use 'kubectl get pods' to check status."

