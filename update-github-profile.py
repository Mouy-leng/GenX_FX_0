import requests
import os

GITHUB_TOKEN = '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'
USERNAME = 'Mouy-leng'

# Update user profile
profile_data = {
    'blog': 'https://genx-fx.vercel.app',
    'company': 'GenX Trading Systems',
    'location': 'Cambodia',
    'bio': 'AI-Powered Forex Trading Platform Developer | GenX-FX Creator'
}

url = f'https://api.github.com/user'
headers = {'Authorization': f'token {GITHUB_TOKEN}'}
response = requests.patch(url, headers=headers, json=profile_data)

if response.status_code == 200:
    print("Profile updated successfully")
else:
    print(f"Error: {response.status_code}")

# Update repository settings
repo_data = {
    'homepage': 'https://genx-fx.vercel.app',
    'description': 'AI-Powered Forex Trading Platform with ML Predictions & Expert Advisors',
    'topics': ['forex', 'trading', 'ai', 'machine-learning', 'expert-advisor', 'mt4', 'mt5']
}

repo_url = f'https://api.github.com/repos/{USERNAME}/GenX_FX'
repo_response = requests.patch(repo_url, headers=headers, json=repo_data)

if repo_response.status_code == 200:
    print("Repository updated successfully")
else:
    print(f"Repository error: {repo_response.status_code}")