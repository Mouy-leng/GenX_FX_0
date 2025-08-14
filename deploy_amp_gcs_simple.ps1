# GenX FX AMP System - Simple GCS Deployment Script (PowerShell)
# This script deploys the AMP system to Google Cloud Platform

Write-Host "Starting AMP System deployment to Google Cloud..." -ForegroundColor Green

# Set project variables
$PROJECT_ID = if ($env:GCP_PROJECT_ID) { $env:GCP_PROJECT_ID } else { "genx-467217" }
$REGION = if ($env:GCP_REGION) { $env:GCP_REGION } else { "us-central1" }
$SERVICE_NAME = "genx-amp-system"

Write-Host "Configuration:" -ForegroundColor Cyan
Write-Host "   Project ID: $PROJECT_ID" -ForegroundColor White
Write-Host "   Region: $REGION" -ForegroundColor White
Write-Host "   Service Name: $SERVICE_NAME" -ForegroundColor White

# Authenticate with Google Cloud
Write-Host "Authenticating with Google Cloud..." -ForegroundColor Yellow
gcloud auth login
gcloud config set project $PROJECT_ID

# Enable required APIs
Write-Host "Enabling required Google Cloud APIs..." -ForegroundColor Yellow
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable storage.googleapis.com

# Create storage bucket for data
Write-Host "Creating storage bucket..." -ForegroundColor Yellow
$BUCKET_NAME = "$PROJECT_ID-amp-data-$(Get-Date -Format 'yyyyMMdd')"
try {
    gsutil mb -p $PROJECT_ID -c STANDARD -l $REGION "gs://$BUCKET_NAME/"
} catch {
    Write-Host "Bucket already exists or creation failed"
}

# Copy simple dockerfile
Copy-Item "Dockerfile.simple" "Dockerfile" -Force

# Build and deploy to Cloud Run
Write-Host "Building and deploying to Cloud Run..." -ForegroundColor Yellow
gcloud run deploy $SERVICE_NAME --source . --platform managed --region $REGION --allow-unauthenticated --set-env-vars "BUCKET_NAME=$BUCKET_NAME" --set-env-vars "GCP_PROJECT_ID=$PROJECT_ID" --memory 2Gi --cpu 1 --max-instances 10

# Get service URL
$SERVICE_URL = gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)"

Write-Host "Deployment completed successfully!" -ForegroundColor Green
Write-Host "Service URL: $SERVICE_URL" -ForegroundColor Cyan
Write-Host "Storage Bucket: gs://$BUCKET_NAME" -ForegroundColor Cyan

Write-Host "AMP System is now live on Google Cloud!" -ForegroundColor Green
