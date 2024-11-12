import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '@mui/material/Button';

function LoginButton() {
  const navigate = useNavigate();
  const isLoggedIn = localStorage.getItem('authToken');

  const handleClick = () => {
    if (isLoggedIn) {
      localStorage.removeItem('authToken'); // Log out user
      alert('Logged out successfully');
      navigate('/'); // Redirect to main page
    } else {
      navigate('/login');
    }
  };

  return (
    <Button
      variant="contained"
      color="primary"
      style={{ position: 'absolute', top: 20, left: 20 }}
      onClick={handleClick}
    >
      {isLoggedIn ? 'Logout' : 'Login'}
    </Button>
  );
}

export default LoginButton;
