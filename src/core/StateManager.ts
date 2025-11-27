/**
 * Simple State Management
 */

export interface StateAction<T = any> {
  type: string;
  payload?: T;
}

export class StateManager<T extends object> {
  private state: T;
  private listeners: Set<(state: T) => void> = new Set();

  constructor(initialState: T) {
    this.state = { ...initialState };
  }

  /**
   * Get current state
   */
  getState(): T {
    return this.state;
  }

  /**
   * Update state
   */
  dispatch(action: StateAction): void {
    // Simple reducer pattern - in real app, you'd have proper reducers
    const newState = { ...this.state } as any;
    
    switch (action.type) {
      case 'SET_STATE':
        Object.assign(newState, action.payload);
        break;
      default:
        // For other actions, just merge the payload
        if (action.payload) {
          Object.assign(newState, action.payload);
        }
    }
    
    this.state = newState;
    this.notifyListeners();
  }

  /**
   * Subscribe to state changes
   */
  subscribe(listener: (state: T) => void): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  private notifyListeners(): void {
    for (const listener of this.listeners) {
      try {
        listener(this.state);
      } catch (error) {
        console.error('Error in state listener:', error);
      }
    }
  }
}
