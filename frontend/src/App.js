// App.js
import './App.css';
import ChatPlugin from './ChatbotButton';
import Dashboard from './dashboard';

function App() {
  return (
    <div className="App">
      <Dashboard /> {/* This will render the dashboard in the background */}
      <ChatPlugin /> {/* This will render the chatbot button on top of the dashboard */}
    </div>
  );
}

export default App;
