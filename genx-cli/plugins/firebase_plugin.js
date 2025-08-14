#!/usr/bin/env node

import { spawn } from 'child_process';
import fs from 'fs';
import path from 'path';

export const firebasePlugin = {
  name: 'firebase',
  description: 'Firebase CLI integration for GenX FX Trading Platform',
  version: '1.0.0',
  
  async run(config, args = []) {
    const command = args[0] || 'help';
    
    switch (command) {
      case 'init':
        await this.initFirebase(args.slice(1));
        break;
      case 'deploy':
        await this.deployToFirebase(args.slice(1));
        break;
      case 'hosting':
        await this.manageHosting(args.slice(1));
        break;
      case 'functions':
        await this.manageFunctions(args.slice(1));
        break;
      case 'firestore':
        await this.manageFirestore(args.slice(1));
        break;
      case 'auth':
        await this.manageAuth(args.slice(1));
        break;
      case 'status':
        await this.showStatus();
        break;
      case 'login':
        await this.firebaseLogin();
        break;
      case 'logout':
        await this.firebaseLogout();
        break;
      default:
        this.showHelp();
    }
  },

  async initFirebase(args) {
    console.log('🔥 Initializing Firebase for GenX FX Trading Platform...');
    
    const features = args.length > 0 ? args : ['hosting', 'functions', 'firestore'];
    
    try {
      // Check if Firebase CLI is installed
      await this.checkFirebaseCLI();
      
      // Initialize Firebase project
      const initProcess = spawn('firebase', ['init', ...features], {
        stdio: 'inherit',
        shell: true
      });
      
      initProcess.on('close', (code) => {
        if (code === 0) {
          console.log('✅ Firebase initialization complete!');
          this.createGenXFirebaseConfig();
        } else {
          console.error('❌ Firebase initialization failed');
        }
      });
      
    } catch (error) {
      console.error('❌ Error initializing Firebase:', error.message);
    }
  },

  async deployToFirebase(args) {
    console.log('🚀 Deploying GenX FX to Firebase...');
    
    const target = args[0] || 'all';
    const deployArgs = ['deploy'];
    
    if (target !== 'all') {
      deployArgs.push('--only', target);
    }
    
    try {
      const deployProcess = spawn('firebase', deployArgs, {
        stdio: 'inherit',
        shell: true
      });
      
      deployProcess.on('close', (code) => {
        if (code === 0) {
          console.log('✅ Deployment successful!');
          this.showDeploymentInfo();
        } else {
          console.error('❌ Deployment failed');
        }
      });
      
    } catch (error) {
      console.error('❌ Error deploying to Firebase:', error.message);
    }
  },

  async manageHosting(args) {
    const action = args[0] || 'status';
    
    switch (action) {
      case 'deploy':
        await this.runFirebaseCommand(['deploy', '--only', 'hosting']);
        break;
      case 'serve':
        await this.runFirebaseCommand(['serve', '--only', 'hosting']);
        break;
      case 'channel':
        const channelName = args[1] || 'preview';
        await this.runFirebaseCommand(['hosting:channel:deploy', channelName]);
        break;
      default:
        console.log('📊 Hosting Status:');
        await this.runFirebaseCommand(['hosting:sites:list']);
    }
  },

  async manageFunctions(args) {
    const action = args[0] || 'status';
    
    switch (action) {
      case 'deploy':
        await this.runFirebaseCommand(['deploy', '--only', 'functions']);
        break;
      case 'logs':
        await this.runFirebaseCommand(['functions:log']);
        break;
      case 'shell':
        await this.runFirebaseCommand(['functions:shell']);
        break;
      default:
        console.log('⚡ Functions Status:');
        await this.runFirebaseCommand(['functions:list']);
    }
  },

  async manageFirestore(args) {
    const action = args[0] || 'status';
    
    switch (action) {
      case 'deploy':
        await this.runFirebaseCommand(['deploy', '--only', 'firestore']);
        break;
      case 'indexes':
        await this.runFirebaseCommand(['firestore:indexes']);
        break;
      case 'rules':
        await this.runFirebaseCommand(['deploy', '--only', 'firestore:rules']);
        break;
      default:
        console.log('🗄️ Firestore Status:');
        console.log('Use: genx-cli firebase firestore [deploy|indexes|rules]');
    }
  },

  async manageAuth(args) {
    const action = args[0] || 'status';
    
    switch (action) {
      case 'export':
        const exportFile = args[1] || 'auth-export.json';
        await this.runFirebaseCommand(['auth:export', exportFile]);
        break;
      case 'import':
        const importFile = args[1] || 'auth-export.json';
        await this.runFirebaseCommand(['auth:import', importFile]);
        break;
      default:
        console.log('🔐 Auth Status:');
        console.log('Use: genx-cli firebase auth [export|import] [filename]');
    }
  },

  async showStatus() {
    console.log('🔥 Firebase Status for GenX FX:');
    console.log('================================');
    
    try {
      // Check login status
      console.log('👤 Authentication:');
      await this.runFirebaseCommand(['login:list']);
      
      // Show current project
      console.log('\n📊 Current Project:');
      await this.runFirebaseCommand(['projects:list']);
      
      // Show hosting sites
      console.log('\n🌐 Hosting Sites:');
      await this.runFirebaseCommand(['hosting:sites:list']);
      
    } catch (error) {
      console.error('❌ Error getting Firebase status:', error.message);
    }
  },

  async firebaseLogin() {
    console.log('🔐 Logging into Firebase...');
    await this.runFirebaseCommand(['login']);
  },

  async firebaseLogout() {
    console.log('👋 Logging out of Firebase...');
    await this.runFirebaseCommand(['logout']);
  },

  async checkFirebaseCLI() {
    return new Promise((resolve, reject) => {
      const checkProcess = spawn('firebase', ['--version'], { shell: true });
      
      checkProcess.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error('Firebase CLI not installed. Install with: npm install -g firebase-tools'));
        }
      });
      
      checkProcess.on('error', () => {
        reject(new Error('Firebase CLI not found. Install with: npm install -g firebase-tools'));
      });
    });
  },

  async runFirebaseCommand(args) {
    return new Promise((resolve, reject) => {
      const firebaseProcess = spawn('firebase', args, {
        stdio: 'inherit',
        shell: true
      });
      
      firebaseProcess.on('close', (code) => {
        if (code === 0) {
          resolve();
        } else {
          reject(new Error(`Firebase command failed with code ${code}`));
        }
      });
      
      firebaseProcess.on('error', (error) => {
        reject(error);
      });
    });
  },

  createGenXFirebaseConfig() {
    const firebaseConfig = {
      genx_fx: {
        hosting: {
          public: "client/dist",
          ignore: ["firebase.json", "**/.*", "**/node_modules/**"],
          rewrites: [
            {
              source: "/api/**",
              destination: "/api/index.html"
            },
            {
              source: "**",
              destination: "/index.html"
            }
          ]
        },
        functions: {
          source: "api",
          runtime: "python39",
          environmentVariables: {
            GENX_ENV: "production"
          }
        },
        firestore: {
          rules: "firestore.rules",
          indexes: "firestore.indexes.json"
        }
      }
    };
    
    // Write enhanced Firebase config
    const configPath = path.join(process.cwd(), 'firebase.genx.json');
    fs.writeFileSync(configPath, JSON.stringify(firebaseConfig, null, 2));
    console.log(`✅ GenX Firebase config created: ${configPath}`);
  },

  showDeploymentInfo() {
    console.log('\n🎉 GenX FX Deployment Complete!');
    console.log('================================');
    console.log('🌐 Your trading platform is now live on Firebase');
    console.log('📊 Check Firebase Console for detailed metrics');
    console.log('⚡ Functions are ready for real-time trading signals');
    console.log('🔥 Firestore is configured for trading data storage');
  },

  showHelp() {
    console.log('🔥 Firebase Plugin for GenX FX Trading Platform');
    console.log('===============================================');
    console.log('');
    console.log('Usage: genx-cli firebase <command> [options]');
    console.log('');
    console.log('Commands:');
    console.log('  init [features...]     Initialize Firebase project');
    console.log('  deploy [target]        Deploy to Firebase (hosting, functions, firestore)');
    console.log('  hosting <action>       Manage Firebase Hosting');
    console.log('  functions <action>     Manage Cloud Functions');
    console.log('  firestore <action>     Manage Firestore database');
    console.log('  auth <action>          Manage Firebase Authentication');
    console.log('  status                 Show Firebase project status');
    console.log('  login                  Login to Firebase');
    console.log('  logout                 Logout from Firebase');
    console.log('');
    console.log('Examples:');
    console.log('  genx-cli firebase init hosting functions');
    console.log('  genx-cli firebase deploy');
    console.log('  genx-cli firebase hosting deploy');
    console.log('  genx-cli firebase functions logs');
    console.log('  genx-cli firebase status');
  }
};

export default firebasePlugin;