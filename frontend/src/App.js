// App.js
import './App.css';
import ChatPlugin from './ChatbotButton';
import Dashboard from './dashboard';
import LoginPage from './LoginPage';
import LoginButton from './LoginButton';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <div className="App">
        <LoginButton />
        <Routes>
          <Route path="/" element={<Dashboard />} /> {/* Home route for your dashboard */}
          <Route path="/login" element={<LoginPage />} /> {/* Route for your login page */}
        </Routes>
        <ChatPlugin /> {/* This will render the chatbot button */}
      </div>
    </Router>
  );
}

export default App;
