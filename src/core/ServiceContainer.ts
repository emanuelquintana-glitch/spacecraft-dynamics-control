/**
 * Simple Dependency Injection Container
 */

export type ServiceFactory<T = any> = () => T;

export class ServiceContainer {
  private services: Map<string, ServiceFactory> = new Map();
  private instances: Map<string, any> = new Map();

  /**
   * Register a singleton service
   */
  registerSingleton<T>(token: string, factory: ServiceFactory<T>): void {
    this.services.set(token, factory);
  }

  /**
   * Register a transient service
   */
  registerTransient<T>(token: string, factory: ServiceFactory<T>): void {
    this.services.set(token, factory);
  }

  /**
   * Resolve a service
   */
  resolve<T>(token: string): T {
    // Check if we already have an instance for singleton
    if (this.instances.has(token)) {
      return this.instances.get(token);
    }

    const factory = this.services.get(token);
    if (!factory) {
      throw new Error(`Service not registered: ${token}`);
    }

    const instance = factory();
    
    // Store instance for singleton services
    this.instances.set(token, instance);
    
    return instance;
  }

  /**
   * Check if service is registered
   */
  has(token: string): boolean {
    return this.services.has(token);
  }

  /**
   * Dispose all services
   */
  dispose(): void {
    this.instances.clear();
    this.services.clear();
  }
}

// Global container instance
export const container = new ServiceContainer();
