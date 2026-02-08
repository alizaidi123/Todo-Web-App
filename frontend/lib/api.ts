import { authenticatedFetch } from './auth-utils';
import { getApiBase } from './apiBase';

class ApiClient {
  private baseUrl: string;

  constructor() {
    // getApiBase() already strips trailing slash, no need to do it again
    this.baseUrl = getApiBase();
  }

  private async request(endpoint: string, options: RequestInit = {}) {
    // Ensure proper URL joining by removing leading slash from endpoint if baseUrl ends with slash
    // and ensure endpoint starts with slash if baseUrl doesn't end with slash
    let normalizedEndpoint = endpoint.startsWith('/') ? endpoint : '/' + endpoint;
    const url = `${this.baseUrl}${normalizedEndpoint}`;

    const response = await authenticatedFetch(url, options);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // Handle 204 No Content responses and other responses that may have empty bodies
    if (response.status === 204 || response.headers.get('Content-Length') === '0') {
      return null;
    }

    // For other successful responses, check if there's content before parsing JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const text = await response.text();
      return text ? JSON.parse(text) : null;
    }

    // If not JSON, try to return the text content
    return await response.text();
  }

  get<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, { method: 'GET' });
  }

  post<T>(endpoint: string, data?: any): Promise<T> {
    return this.request(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  put<T>(endpoint: string, data?: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  patch<T>(endpoint: string, data?: any): Promise<T> {
    return this.request(endpoint, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  delete<T>(endpoint: string): Promise<T> {
    return this.request(endpoint, {
      method: 'DELETE',
    });
  }
}

export const apiClient = new ApiClient();