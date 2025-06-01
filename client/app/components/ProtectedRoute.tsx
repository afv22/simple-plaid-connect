import { ReactNode } from 'react';
import { useAuth } from '../context/AuthContext';
import Login from './Login';

interface ProtectedRouteProps {
  children: ReactNode;
}

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  const { currentUser } = useAuth();
  
  if (!currentUser) {
    return <Login onLoginSuccess={() => {}} />;
  }
  
  return <>{children}</>;
};

export default ProtectedRoute;