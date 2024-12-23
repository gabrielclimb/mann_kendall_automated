import { Link } from 'react-router-dom';

interface QuickActionCardProps {
    title: string;
    description: string;
    icon: React.ReactNode;
    href: string;
}

export const QuickActionCard = ({ title, description, icon, href }: QuickActionCardProps) => (
    <div className="bg-white overflow-hidden shadow rounded-lg">
        <div className="p-5">
            <div className="flex items-center">
                <div className="flex-shrink-0">{icon}</div>
                <div className="ml-5">
                    <h3 className="text-lg font-medium text-gray-900">{title}</h3>
                    <p className="mt-1 text-sm text-gray-500">{description}</p>
                </div>
            </div>
        </div>
        <div className="bg-gray-50 px-5 py-3">
            <Link
                to={href}
                className="text-sm font-medium text-blue-600 hover:text-blue-500"
            >
                Get started →
            </Link>
        </div>
    </div>
);
