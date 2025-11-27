/**
 * Main entry point - Simplified
 */

import { Application } from './core/Application.js';

class SpacecraftDynamicsApp {
  private application: Application;

  constructor() {
    this.application = new Application({
      rendering: {
        antialias: true,
        shadows: true
      },
      physics: {
        gravity: 9.81,
        timeScale: 1.0
      }
    });
  }

  async initialize() {
    try {
      await this.application.initialize();
      this.setupEventListeners();
      
      console.log('🎯 Spacecraft Dynamics 3D System Ready');
      
      // Auto-start for testing
      this.application.start();
      
    } catch (error) {
      console.error('❌ Failed to initialize application:', error);
      this.showError(error);
    }
  }

  private setupEventListeners() {
    // Listen to state changes
    this.application.onStateChange((state) => {
      console.log('Application state changed:', state);
    });

    // Setup basic UI controls
    this.setupBasicUI();
  }

  private setupBasicUI() {
    // Create basic controls
    const controls = document.createElement('div');
    controls.style.cssText = `
      position: fixed;
      top: 10px;
      right: 10px;
      background: rgba(0,0,0,0.8);
      color: white;
      padding: 10px;
      border-radius: 5px;
      z-index: 1000;
    `;
    
    controls.innerHTML = `
      <div style="margin-bottom: 10px;">
        <strong>Spacecraft Dynamics 3D</strong>
      </div>
      <button id="btn-start">Start</button>
      <button id="btn-stop">Stop</button>
      <button id="btn-reset">Reset</button>
    `;
    
    document.body.appendChild(controls);

    // Add event listeners
    document.getElementById('btn-start')?.addEventListener('click', () => {
      this.application.start();
    });

    document.getElementById('btn-stop')?.addEventListener('click', () => {
      this.application.stop();
    });

    document.getElementById('btn-reset')?.addEventListener('click', () => {
      console.log('Reset functionality to be implemented');
    });
  }

  private showError(error: any) {
    const errorDiv = document.createElement('div');
    errorDiv.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: #dc2626;
      color: white;
      padding: 2rem;
      border-radius: 8px;
      text-align: center;
      z-index: 10000;
    `;
    errorDiv.innerHTML = `
      <h2>🚨 Application Error</h2>
      <p>${error.message || 'Unknown error'}</p>
      <button onclick="this.parentElement.remove()" 
              style="margin-top: 1rem; padding: 0.5rem 1rem; background: white; color: #dc2626; border: none; border-radius: 4px; cursor: pointer;">
        Dismiss
      </button>
    `;
    document.body.appendChild(errorDiv);
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', async () => {
  const app = new SpacecraftDynamicsApp();
  await app.initialize();
});

export { SpacecraftDynamicsApp };
