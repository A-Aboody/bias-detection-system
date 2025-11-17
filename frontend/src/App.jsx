import React, { useEffect, useState } from 'react';
import Header from './components/Header';
import BiasAnalyzer from './components/BiasAnalyzer';
import { biasDetectionAPI } from './services/api';
import { AlertCircle } from 'lucide-react';
import './index.css';

function App() {
  const [isBackendHealthy, setIsBackendHealthy] = useState(null);

  useEffect(() => {
    // Check backend health on mount
    const checkHealth = async () => {
      try {
        await biasDetectionAPI.healthCheck();
        setIsBackendHealthy(true);
      } catch (error) {
        console.error('Backend health check failed:', error);
        setIsBackendHealthy(false);
      }
    };

    checkHealth();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100">
      <Header />
      
      {isBackendHealthy === false && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-center">
            <AlertCircle className="w-5 h-5 text-red-600 mr-3 flex-shrink-0" />
            <div className="text-sm text-red-800">
              <p className="font-medium">Backend Connection Error</p>
              <p className="mt-1">
                Unable to connect to the backend server. Please ensure the backend is running at{' '}
                <code className="bg-red-100 px-1 py-0.5 rounded">http://localhost:8000</code>
              </p>
            </div>
          </div>
        </div>
      )}
      
      <BiasAnalyzer />
      
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 mt-12">
        <div className="border-t border-gray-200 pt-8 text-center">
          <p className="text-sm text-gray-600">
            University of Michigan - Dearborn | CIS 411 Final Project
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Team: Abdula Ameen, Ali Zahr, Chance Inosencio, Ghina Albabbili
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;
