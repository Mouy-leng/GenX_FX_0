#!/usr/bin/env python3
"""
AMP CLI - Automated Model Pipeline for GenX Trading Platform
Local implementation to connect with existing AMP configuration
"""

import os
import sys
import json
import subprocess
import argparse
from pathlib import Path
from typing import Dict, List, Optional

class AMPCLI:
    def __init__(self):
        self.project_root = Path.cwd()
        self.config_file = self.project_root / "amp_config.json"
        self.plugins_dir = self.project_root / "amp-plugins"
        self.env_file = self.project_root / ".env"
        
    def load_config(self) -> Dict:
        """Load AMP configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {
            "api_provider": "gemini",
            "plugins": [],
            "services": [],
            "dependencies": [],
            "env_vars": {}
        }
    
    def save_config(self, config: Dict):
        """Save AMP configuration"""
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def update(self, **kwargs):
        """Main update command"""
        print("🚀 Starting GenX Trading Platform AMP Update...")
        
        config = self.load_config()
        
        # Update configuration based on kwargs
        for key, value in kwargs.items():
            if key == "env" and value:
                self._load_env_vars(value)
            elif key == "set" and value:
                for setting in value:
                    if "=" in setting:
                        k, v = setting.split("=", 1)
                        config[k] = v
            elif key == "add_dependency" and value:
                config.setdefault("dependencies", []).extend(value)
            elif key == "add_env" and value:
                config.setdefault("env_vars", {}).update(value)
            elif key == "description":
                config["description"] = value
        
        self.save_config(config)
        print("✅ Main AMP update complete!")
        
    def plugin_install(self, plugin_name: str, **kwargs):
        """Install AMP plugin"""
        print(f"📦 Installing AMP plugin: {plugin_name}")
        
        config = self.load_config()
        plugin_config = {
            "name": plugin_name,
            "source": kwargs.get("source", "genx-trading"),
            "enabled": True,
            "services": kwargs.get("enable_service", []),
            "description": kwargs.get("description", "")
        }
        
        config.setdefault("plugins", []).append(plugin_config)
        self.save_config(config)
        
        print(f"✅ Plugin {plugin_name} installed successfully!")
    
    def config_set(self, **kwargs):
        """Set AMP configuration"""
        print("⚙️ Configuring services...")
        
        config = self.load_config()
        
        for key, value in kwargs.items():
            if key.startswith("enable_") and value:
                config[key] = value == "true"
            elif key == "api_provider":
                config["api_provider"] = value
        
        self.save_config(config)
        print("🔧 Service configuration complete!")
    
    def service_enable(self, **kwargs):
        """Enable services"""
        config = self.load_config()
        services = kwargs.get("service", [])
        config.setdefault("enabled_services", []).extend(services)
        self.save_config(config)
    
    def verify(self, **kwargs):
        """Verify installation"""
        print("🔍 Verifying installation...")
        
        config = self.load_config()
        
        if kwargs.get("check_dependencies"):
            self._check_dependencies(config.get("dependencies", []))
        
        if kwargs.get("check_env_vars"):
            self._check_env_vars(config.get("env_vars", {}))
        
        if kwargs.get("check_services"):
            self._check_services(config.get("enabled_services", []))
        
        if kwargs.get("check_api_keys"):
            self._check_api_keys()
        
        print("✅ Installation verification complete!")
    
    def test(self, **kwargs):
        """Run tests"""
        if kwargs.get("all"):
            print("🧪 Running all tests...")
            self._run_python_tests()
            self._run_node_tests()
        else:
            print("🧪 Running specific tests...")
            self._run_python_tests()
    
    def deploy(self):
        """Deploy to production"""
        print("🚀 Deploying to production...")
        self._run_docker_deploy()
    
    def _load_env_vars(self, env_file: str):
        """Load environment variables from file"""
        if Path(env_file).exists():
            print(f"📄 Loading environment variables from {env_file}")
    
    def _check_dependencies(self, dependencies: List[str]):
        """Check if dependencies are installed"""
        print("📦 Checking dependencies...")
        for dep in dependencies:
            try:
                if ">=" in dep:
                    package = dep.split(">=")[0]
                else:
                    package = dep
                __import__(package.replace("-", "_"))
                print(f"  ✅ {package}")
            except ImportError:
                print(f"  ❌ {package} - Not installed")
    
    def _check_env_vars(self, env_vars: Dict[str, str]):
        """Check environment variables"""
        print("🔑 Checking environment variables...")
        for key, value in env_vars.items():
            if os.getenv(key):
                print(f"  ✅ {key}")
            else:
                print(f"  ❌ {key} - Not set")
    
    def _check_services(self, services: List[str]):
        """Check services"""
        print("🔧 Checking services...")
        for service in services:
            service_file = self.project_root / "api" / "services" / f"{service}.py"
            if service_file.exists():
                print(f"  ✅ {service}")
            else:
                print(f"  ❌ {service} - Service file not found")
    
    def _check_api_keys(self):
        """Check API keys"""
        print("🔑 Checking API keys...")
        required_keys = [
            "GEMINI_API_KEY",
            "BYBIT_API_KEY", 
            "BYBIT_API_SECRET"
        ]
        
        for key in required_keys:
            if os.getenv(key):
                print(f"  ✅ {key}")
            else:
                print(f"  ❌ {key} - Not set")
    
    def _run_python_tests(self):
        """Run Python tests"""
        try:
            subprocess.run([sys.executable, "run_tests.py"], check=True)
            print("✅ Python tests passed!")
        except subprocess.CalledProcessError:
            print("❌ Python tests failed!")
    
    def _run_node_tests(self):
        """Run Node.js tests"""
        try:
            subprocess.run(["npm", "test"], check=True)
            print("✅ Node.js tests passed!")
        except subprocess.CalledProcessError:
            print("❌ Node.js tests failed!")
    
    def _run_docker_deploy(self):
        """Run Docker deployment"""
        try:
            subprocess.run(["docker-compose", "-f", "docker-compose.production.yml", "up", "-d"], check=True)
            print("✅ Docker deployment successful!")
        except subprocess.CalledProcessError:
            print("❌ Docker deployment failed!")

def main():
    parser = argparse.ArgumentParser(description="AMP CLI - Automated Model Pipeline")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update AMP configuration")
    update_parser.add_argument("--env", help="Environment file")
    update_parser.add_argument("--set", nargs="+", help="Set configuration values")
    update_parser.add_argument("--add-dependency", nargs="+", help="Add dependencies")
    update_parser.add_argument("--add-env", nargs="+", help="Add environment variables")
    update_parser.add_argument("--description", help="Description")
    
    # Plugin install command
    plugin_parser = subparsers.add_parser("plugin", help="Plugin commands")
    plugin_subparsers = plugin_parser.add_subparsers(dest="plugin_command")
    install_parser = plugin_subparsers.add_parser("install", help="Install plugin")
    install_parser.add_argument("plugin_name", help="Plugin name")
    install_parser.add_argument("--source", help="Plugin source")
    install_parser.add_argument("--enable-service", nargs="+", help="Enable services")
    install_parser.add_argument("--description", help="Description")
    
    # Config command
    config_parser = subparsers.add_parser("config", help="Configuration commands")
    config_subparsers = config_parser.add_subparsers(dest="config_command")
    set_parser = config_subparsers.add_parser("set", help="Set configuration")
    set_parser.add_argument("--api-provider", help="API provider")
    set_parser.add_argument("--enable-sentiment-analysis", help="Enable sentiment analysis")
    set_parser.add_argument("--enable-social-signals", help="Enable social signals")
    set_parser.add_argument("--enable-news-feeds", help="Enable news feeds")
    set_parser.add_argument("--enable-websocket-streams", help="Enable WebSocket streams")
    
    # Service command
    service_parser = subparsers.add_parser("service", help="Service commands")
    service_subparsers = service_parser.add_subparsers(dest="service_command")
    enable_parser = service_subparsers.add_parser("enable", help="Enable services")
    enable_parser.add_argument("--service", nargs="+", help="Services to enable")
    
    # Verify command
    verify_parser = subparsers.add_parser("verify", help="Verify installation")
    verify_parser.add_argument("--check-dependencies", action="store_true", help="Check dependencies")
    verify_parser.add_argument("--check-env-vars", action="store_true", help="Check environment variables")
    verify_parser.add_argument("--check-services", action="store_true", help="Check services")
    verify_parser.add_argument("--check-api-keys", action="store_true", help="Check API keys")
    
    # Test command
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--all", action="store_true", help="Run all tests")
    
    # Deploy command
    deploy_parser = subparsers.add_parser("deploy", help="Deploy to production")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    amp = AMPCLI()
    
    if args.command == "update":
        amp.update(**vars(args))
    elif args.command == "plugin" and args.plugin_command == "install":
        # Remove plugin_name from kwargs to avoid duplicate argument
        kwargs = vars(args).copy()
        kwargs.pop('plugin_name', None)
        amp.plugin_install(args.plugin_name, **kwargs)
    elif args.command == "config" and args.config_command == "set":
        amp.config_set(**vars(args))
    elif args.command == "service" and args.service_command == "enable":
        amp.service_enable(**vars(args))
    elif args.command == "verify":
        amp.verify(**vars(args))
    elif args.command == "test":
        amp.test(**vars(args))
    elif args.command == "deploy":
        amp.deploy()

if __name__ == "__main__":
    main()