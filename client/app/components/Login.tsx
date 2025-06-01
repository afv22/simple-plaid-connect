import { useState } from 'react';
import { Box, Button, Typography, Paper, Container } from '@mui/material';
import { signInWithGoogle } from '../services/firebase';

type LoginProps = {
  onLoginSuccess: () => void;
};

const Login = ({ onLoginSuccess }: LoginProps) => {
  const [error, setError] = useState<string | null>(null);

  const handleGoogleSignIn = async () => {
    try {
      await signInWithGoogle();
      onLoginSuccess();
    } catch (err) {
      console.error('Login failed:', err);
      setError('Failed to sign in with Google. Please try again.');
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ 
        mt: 8, 
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}>
        <Paper elevation={3} sx={{ p: 4, width: '100%' }}>
          <Typography component="h1" variant="h5" align="center" gutterBottom>
            Plaid Connect
          </Typography>
          <Typography variant="body1" align="center" sx={{ mb: 3 }}>
            Sign in to access your accounts
          </Typography>
          
          <Button
            fullWidth
            variant="contained"
            color="primary"
            size="large"
            onClick={handleGoogleSignIn}
            sx={{ mt: 2 }}
          >
            Sign in with Google
          </Button>
          
          {error && (
            <Typography color="error" align="center" sx={{ mt: 2 }}>
              {error}
            </Typography>
          )}
        </Paper>
      </Box>
    </Container>
  );
};

export default Login;