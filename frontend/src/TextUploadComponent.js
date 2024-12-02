import React, { useState } from 'react';

const TextUploadComponent = ({ onTextSubmit }) => {
  const [inputText, setInputText] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!inputText.trim()) {
      setError('Please enter some text before submitting');
      return;
    }
    
    onTextSubmit(inputText);
    setError('');
  };

  return (
    <div style={{
      padding: '24px',
      backgroundColor: 'white',
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
    }}>
      <h2 style={{
        fontSize: '1.5rem',
        fontWeight: '600',
        marginBottom: '1rem'
      }}>Upload Medical Report</h2>
      
      {error && (
        <div style={{
          padding: '12px',
          marginBottom: '1rem',
          backgroundColor: '#fee2e2',
          color: '#dc2626',
          borderRadius: '4px',
          border: '1px solid #fca5a5'
        }}>
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        <textarea
          style={{
            width: '100%',
            height: '256px',
            padding: '12px',
            border: '1px solid #d1d5db',
            borderRadius: '4px',
            resize: 'vertical',
            fontFamily: 'inherit'
          }}
          placeholder="Paste your medical report text here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
        />
        
        <button
          type="submit"
          style={{
            padding: '8px 16px',
            backgroundColor: '#3b82f6',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer',
            fontWeight: '500',
            transition: 'background-color 0.2s'
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#2563eb'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#3b82f6'}
        >
          Submit Report
        </button>
      </form>
    </div>
  );
};

export default TextUploadComponent;