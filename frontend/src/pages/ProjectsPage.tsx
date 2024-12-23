
import { PlusCircle, FileSpreadsheet } from 'lucide-react';
import { useProjects, useCreateProject } from '../hooks/useApi';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";



export const ProjectsPage = () => {
    const { data: projects, isLoading, error } = useProjects();
    const createProject = useCreateProject();

    const handleNewProject = () => {
        createProject.mutate({
            name: "New Project",
            description: "Description for new project"
        });
    };

    if (isLoading) {
        return (
            <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
            </div>
        );
    }

    if (error) {
        return (
            <Alert variant="destructive">
                <AlertTitle>Error</AlertTitle>
                <AlertDescription>
                    {error instanceof Error ? error.message : 'Failed to load projects'}
                </AlertDescription>
            </Alert>
        );
    }

    return (
        <div>
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
                <button
                    onClick={handleNewProject}
                    disabled={createProject.isPending}
                    className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                >
                    <PlusCircle className="h-5 w-5 mr-2" />
                    New Project
                </button>
            </div>

            <div className="bg-white shadow overflow-hidden sm:rounded-md">
                <ul className="divide-y divide-gray-200">
                    {projects?.map((project) => (
                        <li key={project.id}>
                            <div className="px-4 py-4 sm:px-6">
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center">
                                        <FileSpreadsheet className="h-5 w-5 text-gray-400 mr-3" />
                                        <p className="text-sm font-medium text-blue-600 truncate">{project.name}</p>
                                    </div>
                                </div>
                                <div className="mt-2 sm:flex sm:justify-between">
                                    <div className="sm:flex">
                                        <p className="flex items-center text-sm text-gray-500">
                                            Last updated {new Date(project.updated_at).toLocaleDateString()}
                                        </p>
                                    </div>
                                    <div className="text-sm text-gray-500">
                                        Owner: {project.owner}
                                    </div>
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
            </div>

            {createProject.error && (
                <Alert variant="destructive" className="mt-4">
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>
                        Failed to create project: {createProject.error instanceof Error ? createProject.error.message : 'Unknown error'}
                    </AlertDescription>
                </Alert>
            )}
        </div>
    );
};
