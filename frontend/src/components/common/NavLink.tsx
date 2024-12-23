import { Link, useLocation } from 'react-router-dom';

interface NavLinkProps {
    to: string;
    children: React.ReactNode;
}

export const NavLink = ({ children, to }: NavLinkProps) => {
    const location = useLocation();
    const isActive = location.pathname === to;

    return (
        <Link
            to={to}
            className={`inline-flex items-center px-1 pt-1 text-sm font-medium border-b-2 ${isActive
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                }`}
        >
            {children}
        </Link>
    );
};
