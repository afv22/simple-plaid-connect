const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5001/api";

type HttpMethod =
  | "GET"
  | "POST"
  | "PUT"
  | "DELETE"
  | "PATCH"
  | "HEAD"
  | "OPTIONS";

class APIClient {
  async fetch(endpoint: string, method: HttpMethod, options = {}) {
    const normalizedEndpoint = endpoint.startsWith("/")
      ? endpoint
      : `/${endpoint}`;
    const url = `${API_BASE_URL}${normalizedEndpoint}`;

    return fetch(url, { ...options, method: method }).then((response) => {
      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }
      return response.json();
    });
  }

  async post(endpoint: string, options = {}) {
    return this.fetch(endpoint, "POST", options);
  }

  async get(endpoint: string, options = {}) {
    return this.fetch(endpoint, "GET", options);
  }
}

export default new APIClient();
