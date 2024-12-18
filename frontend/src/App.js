// App.js
import './App.css';
import ChatPlugin from './ChatbotButton';
import Dashboard from './dashboard';
import LoginPage from './LoginPage';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { useState } from 'react';

function App() {
  const [isViewingSample, setIsViewingSample] = useState(false);
  
  // console.log('App - isViewingSample:', isViewingSample);

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route 
            path="/" 
            element={
              <LoginPage 
                setIsViewingSample={setIsViewingSample} 
              />
            } 
          />
          <Route 
            path="/dashboard" 
            element={
              <>
                <Dashboard isViewingSample={isViewingSample} />
              </>
            } 
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
