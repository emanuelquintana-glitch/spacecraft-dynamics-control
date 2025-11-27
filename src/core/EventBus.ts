/**
 * Simple Event Bus System
 */

export type EventHandler<T = any> = (event: T) => void;

export interface EventSubscription {
  unsubscribe: () => void;
}

export class EventBus {
  private handlers: Map<string, EventHandler[]> = new Map();

  /**
   * Subscribe to an event
   */
  on<T = any>(eventType: string, handler: EventHandler<T>): EventSubscription {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, []);
    }

    const handlers = this.handlers.get(eventType)!;
    handlers.push(handler as EventHandler);

    return {
      unsubscribe: () => {
        const index = handlers.indexOf(handler as EventHandler);
        if (index > -1) {
          handlers.splice(index, 1);
        }
      }
    };
  }

  /**
   * Emit an event
   */
  emit<T = any>(eventType: string, event: T): void {
    const handlers = this.handlers.get(eventType) || [];
    
    for (const handler of handlers) {
      try {
        handler(event);
      } catch (error) {
        console.error(`Error in event handler for ${eventType}:`, error);
      }
    }
  }

  /**
   * Remove all handlers for event type
   */
  off(eventType: string): void {
    this.handlers.delete(eventType);
  }

  /**
   * Clear all events
   */
  clear(): void {
    this.handlers.clear();
  }
}

// Global event bus instance
export const eventBus = new EventBus();
