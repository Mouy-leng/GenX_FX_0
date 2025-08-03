#!/usr/bin/env python3
"""
Railway Deployment Script for GenX FX Trading System
Uses Railway API directly to deploy the application
"""

import requests
import json
import os
import subprocess
import time
from pathlib import Path

# Railway configuration
RAILWAY_TOKEN = "b82dcb0b-b5da-41ba-9541-7aac3471eb96"
RAILWAY_API_URL = "https://backboard.railway.app/graphql/v2"
PROJECT_NAME = "genx-fx-trading"

# Headers for API requests
headers = {
    "Authorization": f"Bearer {RAILWAY_TOKEN}",
    "Content-Type": "application/json"
}

def make_graphql_request(query, variables=None):
    """Make a GraphQL request to Railway API"""
    payload = {
        "query": query,
        "variables": variables or {}
    }
    
    response = requests.post(RAILWAY_API_URL, headers=headers, json=payload)
    return response.json()

def get_user_info():
    """Get current user information"""
    query = """
    query {
        me {
            id
            name
            email
        }
    }
    """
    return make_graphql_request(query)

def list_projects():
    """List all projects"""
    query = """
    query {
        projects {
            nodes {
                id
                name
                description
            }
        }
    }
    """
    return make_graphql_request(query)

def create_project(name, description=""):
    """Create a new project"""
    query = """
    mutation projectCreate($input: ProjectCreateInput!) {
        projectCreate(input: $input) {
            project {
                id
                name
                description
            }
        }
    }
    """
    variables = {
        "input": {
            "name": name,
            "description": description
        }
    }
    return make_graphql_request(query, variables)

def create_service(project_id, name, source_image=None):
    """Create a new service in a project"""
    query = """
    mutation serviceCreate($input: ServiceCreateInput!) {
        serviceCreate(input: $input) {
            service {
                id
                name
            }
        }
    }
    """
    variables = {
        "input": {
            "projectId": project_id,
            "name": name,
            "sourceImage": source_image
        }
    }
    return make_graphql_request(query, variables)

def deploy_service(service_id, variables=None):
    """Deploy a service"""
    query = """
    mutation deploymentCreate($input: DeploymentCreateInput!) {
        deploymentCreate(input: $input) {
            deployment {
                id
                status
            }
        }
    }
    """
    variables = {
        "input": {
            "serviceId": service_id,
            "variables": variables or {}
        }
    }
    return make_graphql_request(query, variables)

def main():
    print("🚀 Starting Railway deployment for GenX FX Trading System...")
    
    # Check authentication
    print("🔐 Checking authentication...")
    user_info = get_user_info()
    if "errors" in user_info:
        print(f"❌ Authentication failed: {user_info['errors']}")
        return
    
    print(f"✅ Authenticated as: {user_info['data']['me']['name']}")
    
    # List existing projects
    print("📋 Checking existing projects...")
    projects_response = list_projects()
    if "errors" in projects_response:
        print(f"❌ Failed to list projects: {projects_response['errors']}")
        return
    
    projects = projects_response.get('data', {}).get('projects', {}).get('nodes', [])
    project_id = None
    
    # Check if project already exists
    for project in projects:
        if project['name'] == PROJECT_NAME:
            project_id = project['id']
            print(f"✅ Found existing project: {PROJECT_NAME}")
            break
    
    # Create project if it doesn't exist
    if not project_id:
        print(f"📦 Creating new project: {PROJECT_NAME}")
        create_response = create_project(PROJECT_NAME, "GenX FX Trading System - AI-powered Forex trading platform")
        if "errors" in create_response:
            print(f"❌ Failed to create project: {create_response['errors']}")
            return
        
        project_id = create_response['data']['projectCreate']['project']['id']
        print(f"✅ Created project with ID: {project_id}")
    
    # Create services for the application
    print("🔧 Setting up services...")
    
    # Create API service (FastAPI backend)
    api_service_response = create_service(project_id, "api", "python:3.11")
    if "errors" in api_service_response:
        print(f"❌ Failed to create API service: {api_service_response['errors']}")
        return
    
    api_service_id = api_service_response['data']['serviceCreate']['service']['id']
    print(f"✅ Created API service with ID: {api_service_id}")
    
    # Create web service (React frontend)
    web_service_response = create_service(project_id, "web", "node:18")
    if "errors" in web_service_response:
        print(f"❌ Failed to create web service: {web_service_response['errors']}")
        return
    
    web_service_id = web_service_response['data']['serviceCreate']['service']['id']
    print(f"✅ Created web service with ID: {web_service_id}")
    
    print("🎉 Railway project setup complete!")
    print(f"📊 Project ID: {project_id}")
    print(f"🔌 API Service ID: {api_service_id}")
    print(f"🌐 Web Service ID: {web_service_id}")
    print("\nNext steps:")
    print("1. Use 'railway link' to connect your local project")
    print("2. Use 'railway up' to deploy your application")
    print("3. Set up environment variables in Railway dashboard")

if __name__ == "__main__":
    main()