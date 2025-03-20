import { Plus, FileSpreadsheet, TrendingUp, BarChart2 } from 'lucide-react';

interface ActionCardProps {
    title: string;
    description: string;
    icon: React.ReactNode;
    href: string;
}

const ActionCard = ({ title, description, icon, href }: ActionCardProps) => (
    <a
        href={href}
        className="block p-6 transition-all duration-200 bg-gray-800 rounded-lg hover:bg-gray-700 group"
    >
        <div className="flex items-center space-x-4">
            <div className="p-2 bg-gray-700 rounded-lg group-hover:bg-gray-600">
                {icon}
            </div>
            <div>
                <h3 className="text-lg font-semibold text-gray-100">{title}</h3>
                <p className="text-gray-400">{description}</p>
            </div>
        </div>
        <div className="mt-4">
            <span className="inline-flex items-center text-sm font-medium text-blue-400 group-hover:text-blue-300">
                Get started
                <svg className="w-4 h-4 ml-2" viewBox="0 0 16 16" fill="none">
                    <path d="M6.667 12.667L12 7.333L6.667 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
            </span>
        </div>
    </a>
);

interface RecentProjectProps {
    name: string;
    timeAgo: string;
}

const RecentProject = ({ name, timeAgo }: RecentProjectProps) => (
    <div className="flex items-center justify-between py-3 border-b border-gray-700">
        <span className="text-gray-300">{name}</span>
        <span className="text-sm text-gray-500">{timeAgo}</span>
    </div>
);

export function HomePage() {
    const actions = [
        {
            title: "Create New Project",
            description: "Start a new analysis project",
            icon: <Plus className="w-6 h-6 text-blue-400" />,
            href: "/projects/new"
        },
        {
            title: "Upload Dataset",
            description: "Add new data for analysis",
            icon: <FileSpreadsheet className="w-6 h-6 text-green-400" />,
            href: "/analysis/new"
        },
        {
            title: "View Results",
            description: "Check your analysis results",
            icon: <TrendingUp className="w-6 h-6 text-purple-400" />,
            href: "/analysis"
        },
        {
            title: "Visualize Data",
            description: "Create charts and graphs",
            icon: <BarChart2 className="w-6 h-6 text-orange-400" />,
            href: "/visualize"
        }
    ];

    return (
        <div className="min-h-screen bg-gray-900">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                <div className="space-y-12">
                    {/* Header */}
                    <div>
                        <h1 className="text-4xl font-bold text-white">
                            Welcome to Mann Kendall Automated
                        </h1>
                        <p className="mt-4 text-xl text-gray-400">
                            Analyze your data with advanced statistical methods
                        </p>
                    </div>

                    {/* Action Cards */}
                    <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
                        {actions.map((action) => (
                            <ActionCard key={action.title} {...action} />
                        ))}
                    </div>

                    {/* Recent Projects */}
                    <div className="bg-gray-800 rounded-lg p-6">
                        <h2 className="text-xl font-semibold text-white mb-4">Recent Projects</h2>
                        <div className="space-y-1">
                            <RecentProject name="Project A" timeAgo="2 days ago" />
                            <RecentProject name="Project B" timeAgo="1 week ago" />
                            <RecentProject name="Project C" timeAgo="2 weeks ago" />
                        </div>
                        <a
                            href="/projects"
                            className="inline-flex items-center mt-4 text-sm font-medium text-blue-400 hover:text-blue-300"
                        >
                            View all projects
                            <svg className="w-4 h-4 ml-2" viewBox="0 0 16 16" fill="none">
                                <path d="M6.667 12.667L12 7.333L6.667 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                            </svg>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    );
}

