import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../../hooks/useAuth';

interface ProtectedRouteProps {
    children: JSX.Element;
}

export const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
    if (!isAuthenticated()) {
        return <Navigate to="/login" replace />;
    }

    return children;
};
