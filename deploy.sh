#!/bin/bash

# Exit on error
set -e

# Configuration
DOCKER_REGISTRY=${DOCKER_REGISTRY:-"your-registry.example.com"}
PROJECT_NAME=${PROJECT_NAME:-"m87-lensing"}

# Build the Docker image
echo "Building Docker image..."
docker build -t ${DOCKER_REGISTRY}/m87-lensing-visualizer:latest .

# Push the image to registry
echo "Pushing image to registry..."
docker push ${DOCKER_REGISTRY}/m87-lensing-visualizer:latest

# Create OpenShift project if it doesn't exist
echo "Creating OpenShift project..."
oc new-project ${PROJECT_NAME} --description="M87 Gravitational Lensing Visualization" --display-name="M87 Lensing" || true

# Deploy to OpenShift
echo "Deploying to OpenShift..."
envsubst < openshift-deployment.yaml | oc apply -f -

# Wait for deployment to complete
echo "Waiting for deployment to complete..."
oc rollout status deployment/m87-lensing-visualizer

echo "Deployment complete! The visualization will run daily at midnight."
echo "You can check the results in the persistent volume claim." 