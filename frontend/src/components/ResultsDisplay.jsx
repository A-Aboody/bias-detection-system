import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle,
  XCircle,
  TrendingUp,
  Eye,
  Lightbulb,
  BarChart3,
} from 'lucide-react';

const ResultsDisplay = ({ results, mode }) => {
  const [showHighlights, setShowHighlights] = useState(true);

  // Get severity color and icon
  const getSeverityInfo = (severity) => {
    switch (severity) {
      case 'severe':
        return {
          color: 'red',
          bgColor: 'bg-red-100',
          textColor: 'text-red-800',
          borderColor: 'border-red-300',
          icon: XCircle,
        };
      case 'moderate':
        return {
          color: 'yellow',
          bgColor: 'bg-yellow-100',
          textColor: 'text-yellow-800',
          borderColor: 'border-yellow-300',
          icon: AlertTriangle,
        };
      case 'mild':
        return {
          color: 'blue',
          bgColor: 'bg-blue-100',
          textColor: 'text-blue-800',
          borderColor: 'border-blue-300',
          icon: AlertTriangle,
        };
      default:
        return {
          color: 'green',
          bgColor: 'bg-green-100',
          textColor: 'text-green-800',
          borderColor: 'border-green-300',
          icon: CheckCircle,
        };
    }
  };

  const getCategoryColor = (category) => {
    const colors = {
      gender: 'bg-pink-100 text-pink-800 border-pink-300',
      race: 'bg-purple-100 text-purple-800 border-purple-300',
      religion: 'bg-indigo-100 text-indigo-800 border-indigo-300',
      political: 'bg-orange-100 text-orange-800 border-orange-300',
      socioeconomic: 'bg-teal-100 text-teal-800 border-teal-300',
      age: 'bg-cyan-100 text-cyan-800 border-cyan-300',
    };
    return colors[category] || 'bg-gray-100 text-gray-800 border-gray-300';
  };

  // Extract data based on mode
  const hasBias = mode === 'comprehensive' 
    ? results.bias_analysis?.has_bias 
    : results.has_bias;
  
  const severity = mode === 'comprehensive'
    ? results.bias_analysis?.severity
    : results.severity;
  
  const categories = mode === 'comprehensive'
    ? results.bias_analysis?.categories || []
    : results.bias_categories || [];
  
  const scores = mode === 'comprehensive'
    ? results.bias_analysis?.scores || {}
    : results.bias_scores || {};
  
  const overallScore = mode === 'comprehensive'
    ? results.bias_analysis?.overall_score
    : results.overall_score;

  const severityInfo = getSeverityInfo(severity);
  const SeverityIcon = severityInfo.icon;

  const renderTextWithHighlights = () => {
    if (!results.highlights || results.highlights.length === 0) {
      return <p className="text-gray-700 whitespace-pre-wrap">{results.text}</p>;
    }

    const text = results.text;
    const highlights = [...results.highlights].sort((a, b) => a.start - b.start);
    const parts = [];
    let lastIndex = 0;

    highlights.forEach((highlight, index) => {
      // Add text before highlight
      if (highlight.start > lastIndex) {
        parts.push(
          <span key={`text-${index}`}>
            {text.substring(lastIndex, highlight.start)}
          </span>
        );
      }

      // Add highlighted term
      const categoryColor = getCategoryColor(highlight.category);
      parts.push(
        <span
          key={`highlight-${index}`}
          className={`highlight-term ${categoryColor} border font-medium`}
          title={`${highlight.category} bias`}
        >
          {highlight.term}
        </span>
      );

      lastIndex = highlight.end;
    });

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push(
        <span key="text-end">{text.substring(lastIndex)}</span>
      );
    }

    return <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{parts}</p>;
  };

  return (
    <div className="space-y-6 fade-in">
      {/* Overall Status Card */}
      <div className={`${severityInfo.bgColor} border ${severityInfo.borderColor} rounded-lg p-6`}>
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-3">
            <SeverityIcon className={`w-6 h-6 ${severityInfo.textColor} mt-1`} />
            <div>
              <h3 className={`text-lg font-semibold ${severityInfo.textColor}`}>
                {hasBias ? 'Bias Detected' : 'No Significant Bias Detected'}
              </h3>
              <p className={`text-sm ${severityInfo.textColor} mt-1`}>
                {hasBias
                  ? `Severity: ${severity.charAt(0).toUpperCase() + severity.slice(1)}`
                  : 'The text appears to be balanced and neutral'}
              </p>
            </div>
          </div>
          {overallScore !== undefined && overallScore !== null && (
            <div className="text-right">
              <div className={`text-3xl font-bold ${severityInfo.textColor}`}>
                {(overallScore * 100).toFixed(0)}%
              </div>
              <div className={`text-xs ${severityInfo.textColor}`}>Overall Score</div>
            </div>
          )}
        </div>
      </div>

      {/* Bias Categories */}
      {hasBias && categories.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <TrendingUp className="w-5 h-5 mr-2 text-primary-600" />
            Detected Bias Categories
          </h3>
          <div className="space-y-3">
            {categories.map((category) => (
              <div key={category} className="flex items-center justify-between">
                <span className={`px-3 py-1 rounded-full text-sm font-medium border ${getCategoryColor(category)}`}>
                  {category.charAt(0).toUpperCase() + category.slice(1)}
                </span>
                {scores[category] !== undefined && (
                  <div className="flex items-center space-x-2">
                    <div className="w-32 bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full transition-all"
                        style={{ width: `${scores[category] * 100}%` }}
                      />
                    </div>
                    <span className="text-sm font-medium text-gray-700 w-12 text-right">
                      {(scores[category] * 100).toFixed(0)}%
                    </span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Text with Highlights */}
      {results.highlights && results.highlights.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 flex items-center">
              <Eye className="w-5 h-5 mr-2 text-primary-600" />
              Text Analysis
            </h3>
            <button
              onClick={() => setShowHighlights(!showHighlights)}
              className="text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              {showHighlights ? 'Hide' : 'Show'} Highlights
            </button>
          </div>
          {showHighlights && (
            <div className="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
              {renderTextWithHighlights()}
            </div>
          )}
          <div className="mt-4 flex flex-wrap gap-2">
            {Object.keys(scores).map((category) => (
              <span
                key={category}
                className={`px-2 py-1 rounded text-xs border ${getCategoryColor(category)}`}
              >
                {category}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Comprehensive Mode: Statistics */}
      {mode === 'comprehensive' && results.statistics && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <BarChart3 className="w-5 h-5 mr-2 text-primary-600" />
            Text Statistics
          </h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {results.statistics.word_count}
              </div>
              <div className="text-xs text-gray-600 mt-1">Words</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {results.statistics.char_count}
              </div>
              <div className="text-xs text-gray-600 mt-1">Characters</div>
            </div>
            <div className="text-center p-3 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-gray-900">
                {results.statistics.sentence_count}
              </div>
              <div className="text-xs text-gray-600 mt-1">Sentences</div>
            </div>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {mode === 'comprehensive' && results.recommendations && results.recommendations.length > 0 && (
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
            <Lightbulb className="w-5 h-5 mr-2 text-yellow-500" />
            Recommendations
          </h3>
          <ul className="space-y-2">
            {results.recommendations.map((rec, index) => (
              <li key={index} className="flex items-start space-x-2">
                <span className="text-primary-600 mt-1">•</span>
                <span className="text-sm text-gray-700">{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Timestamp */}
      <div className="text-xs text-gray-500 text-center">
        Analysis completed at {new Date(results.timestamp).toLocaleString()}
      </div>
    </div>
  );
};

export default ResultsDisplay;
