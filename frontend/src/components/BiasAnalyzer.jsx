import React, { useState } from 'react';
import { Send, FileText, Loader2, AlertCircle } from 'lucide-react';
import { biasDetectionAPI } from '../services/api';
import ResultsDisplay from './ResultsDisplay';

const BiasAnalyzer = () => {
  const [text, setText] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [analysisMode, setAnalysisMode] = useState('detect'); // 'detect' or 'comprehensive'

  const exampleTexts = [
    "The female nurse assisted the male doctor with the surgery.",
    "He is an excellent engineer, while she makes a great secretary.",
    "The inner-city youth were suspected of the crime.",
  ];

  const handleAnalyze = async () => {
    if (!text.trim()) {
      setError('Please enter some text to analyze');
      return;
    }

    setIsAnalyzing(true);
    setError(null);
    setResults(null);

    try {
      let data;
      if (analysisMode === 'comprehensive') {
        data = await biasDetectionAPI.analyzeText(text);
      } else {
        data = await biasDetectionAPI.detectBias(text);
      }
      setResults(data);
    } catch (err) {
      console.error('Analysis error:', err);
      setError(err.detail || 'Failed to analyze text. Please try again.');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleExampleClick = (exampleText) => {
    setText(exampleText);
    setResults(null);
    setError(null);
  };

  const handleClear = () => {
    setText('');
    setResults(null);
    setError(null);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-xl font-semibold text-gray-900 flex items-center">
                <FileText className="w-5 h-5 mr-2 text-primary-600" />
                Input Text
              </h2>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => setAnalysisMode('detect')}
                  className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                    analysisMode === 'detect'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  Quick
                </button>
                <button
                  onClick={() => setAnalysisMode('comprehensive')}
                  className={`px-3 py-1 rounded text-sm font-medium transition-colors ${
                    analysisMode === 'comprehensive'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                  }`}
                >
                  Detailed
                </button>
              </div>
            </div>

            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              placeholder="Enter or paste text to analyze for bias..."
              className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
              disabled={isAnalyzing}
            />

            <div className="flex items-center justify-between mt-4">
              <span className="text-sm text-gray-500">
                {text.length} characters
              </span>
              <div className="flex space-x-2">
                <button
                  onClick={handleClear}
                  className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-200 rounded-lg hover:bg-gray-300 transition-colors disabled:opacity-50"
                  disabled={isAnalyzing || !text}
                >
                  Clear
                </button>
                <button
                  onClick={handleAnalyze}
                  className="px-6 py-2 text-sm font-medium text-white bg-primary-600 rounded-lg hover:bg-primary-700 transition-colors disabled:opacity-50 flex items-center space-x-2"
                  disabled={isAnalyzing || !text.trim()}
                >
                  {isAnalyzing ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4" />
                      <span>Analyze</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>

          {/* Example Texts */}
          <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Try Example Texts
            </h3>
            <div className="space-y-2">
              {exampleTexts.map((example, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(example)}
                  className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg text-sm text-gray-700 transition-colors"
                  disabled={isAnalyzing}
                >
                  {example}
                </button>
              ))}
            </div>
          </div>

          {/* Info Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <div className="flex items-start">
              <AlertCircle className="w-5 h-5 text-blue-600 mr-3 mt-0.5 flex-shrink-0" />
              <div className="text-sm text-blue-800">
                <p className="font-medium mb-1">Detection Categories:</p>
                <ul className="list-disc list-inside space-y-1 text-blue-700">
                  <li>Gender bias</li>
                  <li>Racial/ethnic bias</li>
                  <li>Religious bias</li>
                  <li>Political bias</li>
                  <li>Socioeconomic bias</li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 fade-in">
              <div className="flex items-center">
                <AlertCircle className="w-5 h-5 text-red-600 mr-3" />
                <p className="text-sm text-red-800">{error}</p>
              </div>
            </div>
          )}

          {results && <ResultsDisplay results={results} mode={analysisMode} />}

          {!results && !error && !isAnalyzing && (
            <div className="bg-white rounded-lg shadow-md p-12 text-center">
              <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500 text-lg">
                Enter text to begin analysis
              </p>
              <p className="text-gray-400 text-sm mt-2">
                Results will appear here
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default BiasAnalyzer;
