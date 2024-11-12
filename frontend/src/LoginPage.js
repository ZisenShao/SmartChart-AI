import React, { useState } from 'react';
import { TextField, Button, Container, Typography, Box } from '@mui/material';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function LoginPage() {
  const [isSignUp, setIsSignUp] = useState(false); // Toggle between sign in and sign up
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

const handleSubmit = async (e) => {
    e.preventDefault();
    try {
        const baseUrl = 'http://localhost:8000';

        if (isSignUp) {
            const response = await axios.post(`${baseUrl}/api/register/`, formData);
            alert('Sign up successful. Please log in.');
            setIsSignUp(false);
        } else {
            const { email, password } = formData;
            const response = await axios.post(`${baseUrl}/api/login/`, { email, password });
            localStorage.setItem('authToken', response.data.token);
            alert('Login successful');
            navigate('/');
        }
    } catch (error) {
        if (error.response && error.response.data && error.response.data.error) {
            alert(error.response.data.error);
        } else {
            console.error('Error:', error);
            alert('An error occurred. Please try again.');
        }
    }
};

  return (
    <Container maxWidth="sm">
      <Box
        display="flex"
        flexDirection="column"
        alignItems="center"
        mt={5}
        p={3}
        borderRadius={5}
        boxShadow={3}
      >
        <Typography variant="h4" gutterBottom>
          {isSignUp ? 'Sign Up' : 'Sign In'}
        </Typography>
        <form onSubmit={handleSubmit}>
          {isSignUp && (
            <TextField
              label="Name"
              name="name"
              variant="outlined"
              fullWidth
              margin="normal"
              value={formData.name}
              onChange={handleChange}
            />
          )}
          <TextField
            label="Email"
            name="email"
            variant="outlined"
            fullWidth
            margin="normal"
            value={formData.email}
            onChange={handleChange}
          />
          <TextField
            label="Password"
            name="password"
            type="password"
            variant="outlined"
            fullWidth
            margin="normal"
            value={formData.password}
            onChange={handleChange}
          />
          <Button type="submit" variant="contained" color="primary" fullWidth style={{ marginTop: '20px' }}>
            {isSignUp ? 'Sign Up' : 'Sign In'}
          </Button>
        </form>
        <Button
          color="secondary"
          onClick={() => setIsSignUp(!isSignUp)}
          style={{ marginTop: '10px' }}
        >
          {isSignUp ? 'Already have an account? Sign In' : "Don't have an account? Sign Up"}
        </Button>
      </Box>
    </Container>
  );
}

export default LoginPage;
