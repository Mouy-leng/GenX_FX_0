#!/bin/bash

# GenX FX AMP System - Simple GCS Deployment Script
# This script deploys the AMP system to Google Cloud Platform

set -e

echo "🚀 Starting AMP System deployment to Google Cloud..."

# Check if gcloud CLI is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud CLI not found. Please install gcloud CLI first."
    echo "Visit: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set project variables
PROJECT_ID=${GCP_PROJECT_ID:-"genx-fx-trading"}
REGION=${GCP_REGION:-"us-central1"}
SERVICE_NAME="genx-amp-system"

echo "📋 Configuration:"
echo "   Project ID: $PROJECT_ID"
echo "   Region: $REGION"
echo "   Service Name: $SERVICE_NAME"

# Authenticate with Google Cloud
echo "🔐 Authenticating with Google Cloud..."
gcloud auth login
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com

# Create storage bucket for data
echo "💾 Creating storage bucket..."
BUCKET_NAME="${PROJECT_ID}-amp-data"
gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION gs://$BUCKET_NAME/ || echo "Bucket might already exist"

# Build and deploy to Cloud Run
echo "🏗️ Building and deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --set-env-vars "BUCKET_NAME=$BUCKET_NAME" \
    --set-env-vars "GCP_PROJECT_ID=$PROJECT_ID" \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')

echo "✅ Deployment completed successfully!"
echo "🌐 Service URL: $SERVICE_URL"
echo "📊 Storage Bucket: gs://$BUCKET_NAME"
echo ""
echo "🔗 Useful commands:"
echo "   View logs: gcloud logging read 'resource.type=cloud_run_revision AND resource.labels.service_name=$SERVICE_NAME' --limit 50"
echo "   Update service: gcloud run deploy $SERVICE_NAME --source . --region $REGION"
echo "   Delete service: gcloud run services delete $SERVICE_NAME --region $REGION"

echo "🎉 AMP System is now live on Google Cloud!"
