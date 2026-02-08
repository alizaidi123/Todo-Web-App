/**
 * API Base URL Configuration
 *
 * Provides canonical API base URL resolution with environment-specific behavior:
 * - Production: Requires NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL (throws error if missing)
 * - Development: Falls back to localhost:8000 if not configured
 */

/**
 * Get the API base URL based on environment
 * @returns Base URL without trailing slash
 * @throws Error in production if NEXT_PUBLIC_API_BASE_URL and NEXT_PUBLIC_API_URL are both missing
 */
export function getApiBase(): string {
  // Try primary env var first, then fallback var
  const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || process.env.NEXT_PUBLIC_API_URL;

  if (apiBaseUrl) {
    // Normalize: strip trailing slash if present
    return apiBaseUrl.endsWith('/') ? apiBaseUrl.slice(0, -1) : apiBaseUrl;
  }

  // No environment variable set - behavior depends on environment
  if (process.env.NODE_ENV === 'production') {
    // Production MUST have explicit configuration
    throw new Error(
      'Error: API base URL not configured for production. ' +
      'Please set NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL environment variable. ' +
      `Current NODE_ENV: ${process.env.NODE_ENV}`
    );
  }

  // Development: use localhost fallback with warning
  if (typeof console !== 'undefined' && console.warn) {
    console.warn(
      'Warning: API base URL not configured, using development default: http://127.0.0.1:8000. ' +
      'Set NEXT_PUBLIC_API_BASE_URL or NEXT_PUBLIC_API_URL to override.'
    );
  }

  return 'http://127.0.0.1:8000';
}
