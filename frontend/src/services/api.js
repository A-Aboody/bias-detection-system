import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    console.log('API Request:', config.method?.toUpperCase(), config.url);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    console.log('API Response:', response.status, response.config.url);
    return response;
  },
  (error) => {
    console.error('Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const biasDetectionAPI = {
  /**
   * Detect bias in text
   */
  detectBias: async (text, categories = null) => {
    try {
      const response = await api.post('/api/v1/detect', {
        text,
        categories,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Perform comprehensive analysis
   */
  analyzeText: async (text, modelName = null) => {
    try {
      const response = await api.post('/api/v1/analyze', {
        text,
        model_name: modelName,
      });
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Get available bias categories
   */
  getCategories: async () => {
    try {
      const response = await api.get('/api/v1/categories');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },

  /**
   * Health check
   */
  healthCheck: async () => {
    try {
      const response = await api.get('/api/v1/health');
      return response.data;
    } catch (error) {
      throw error.response?.data || error;
    }
  },
};

export default api;
