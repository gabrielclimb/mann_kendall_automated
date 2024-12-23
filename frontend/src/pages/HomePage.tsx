import { PlusCircle, FileSpreadsheet, TrendingUp } from 'lucide-react';
import { QuickActionCard } from '../components/features/home/QuickActionCard';

export const HomePage = () => {
    return (
        <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-8">
                Welcome to Mann Kendall Automated
            </h1>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <QuickActionCard
                    title="Create New Project"
                    description="Start a new analysis project"
                    icon={<PlusCircle className="h-6 w-6 text-blue-600" />}
                    href="/projects/new"
                />
                <QuickActionCard
                    title="Upload Dataset"
                    description="Add new data for analysis"
                    icon={<FileSpreadsheet className="h-6 w-6 text-blue-600" />}
                    href="/analysis/new"
                />
                <QuickActionCard
                    title="View Results"
                    description="Check your analysis results"
                    icon={<TrendingUp className="h-6 w-6 text-blue-600" />}
                    href="/analysis"
                />
            </div>
        </div>
    );
};
