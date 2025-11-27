/**
 * Main Application Controller - Simplified and Working Version
 */

import { ServiceContainer, container } from './ServiceContainer';
import { EventBus, eventBus } from './EventBus';
import { StateManager } from './StateManager';

export interface ApplicationConfig {
  rendering: {
    antialias: boolean;
    shadows: boolean;
  };
  physics: {
    gravity: number;
    timeScale: number;
  };
}

export interface ApplicationState {
  isInitialized: boolean;
  isRunning: boolean;
  currentScene: string;
}

export class Application {
  private config: ApplicationConfig;
  private stateManager: StateManager<ApplicationState>;
  private serviceContainer: ServiceContainer;
  private eventBus: EventBus;
  private animationFrameId: number | null = null;

  constructor(config: Partial<ApplicationConfig> = {}) {
    this.config = {
      rendering: {
        antialias: true,
        shadows: true,
        ...config.rendering
      },
      physics: {
        gravity: 9.81,
        timeScale: 1.0,
        ...config.physics
      }
    };
    
    this.serviceContainer = container;
    this.eventBus = eventBus;
    this.stateManager = new StateManager<ApplicationState>({
      isInitialized: false,
      isRunning: false,
      currentScene: 'default'
    });

    this.registerCoreServices();
  }

  /**
   * Initialize the application
   */
  async initialize(): Promise<void> {
    if (this.stateManager.getState().isInitialized) {
      console.warn('Application already initialized');
      return;
    }

    try {
      console.log('🚀 Initializing Spacecraft Dynamics Application...');

      // Initialize core systems would go here
      await this.initializeCoreSystems();

      // Update state
      this.stateManager.dispatch({
        type: 'SET_STATE',
        payload: { isInitialized: true }
      });

      console.log('✅ Application initialized successfully');

    } catch (error) {
      console.error('❌ Failed to initialize application:', error);
      throw error;
    }
  }

  /**
   * Start the application
   */
  start(): void {
    const state = this.stateManager.getState();
    
    if (!state.isInitialized) {
      throw new Error('Application must be initialized before starting');
    }

    if (state.isRunning) {
      console.warn('Application is already running');
      return;
    }

    this.stateManager.dispatch({
      type: 'SET_STATE',
      payload: { isRunning: true }
    });

    this.animationFrameId = requestAnimationFrame(this.loop.bind(this));

    console.log('🎬 Application started');
  }

  /**
   * Stop the application
   */
  stop(): void {
    if (this.animationFrameId) {
      cancelAnimationFrame(this.animationFrameId);
      this.animationFrameId = null;
    }

    this.stateManager.dispatch({
      type: 'SET_STATE',
      payload: { isRunning: false }
    });

    console.log('🛑 Application stopped');
  }

  /**
   * Get application state
   */
  getState(): ApplicationState {
    return this.stateManager.getState();
  }

  /**
   * Subscribe to state changes
   */
  onStateChange(listener: (state: ApplicationState) => void): () => void {
    return this.stateManager.subscribe(listener);
  }

  /**
   * Get service container
   */
  getServiceContainer(): ServiceContainer {
    return this.serviceContainer;
  }

  /**
   * Get event bus
   */
  getEventBus(): EventBus {
    return this.eventBus;
  }

  /**
   * Cleanup resources
   */
  dispose(): void {
    this.stop();
    this.serviceContainer.dispose();
    this.eventBus.clear();
    console.log('🧹 Application disposed');
  }

  private registerCoreServices(): void {
    this.serviceContainer.registerSingleton('Application', () => this);
    this.serviceContainer.registerSingleton('EventBus', () => this.eventBus);
    this.serviceContainer.registerSingleton('ServiceContainer', () => this.serviceContainer);
  }

  private async initializeCoreSystems(): Promise<void> {
    // Systems initialization will be added here
    await Promise.resolve();
  }

  private loop(): void {
    this.animationFrameId = requestAnimationFrame(this.loop.bind(this));
    
    // Main application loop
    this.eventBus.emit('RENDER_FRAME', { timestamp: Date.now() });
  }
}
