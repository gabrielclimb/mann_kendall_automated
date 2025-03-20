import { useState } from 'react';
import { PlusCircle, Search, Filter } from 'lucide-react';
import { useProjects, useCreateProject } from '../hooks/useApi';
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";

export const ProjectsPage = () => {
    const { data: projects, isLoading, error } = useProjects();
    const createProject = useCreateProject();
    const [searchTerm, setSearchTerm] = useState('');

    const handleNewProject = () => {
        createProject.mutate({
            name: "New Project",
            description: "Description for new project",
            processed: false
        });
    };

    const filteredProjects = projects?.filter(project =>
        project.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (project.description && project.description.toLowerCase().includes(searchTerm.toLowerCase()))
    );

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
        <div className="container mx-auto px-4 py-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
                <Button onClick={handleNewProject} disabled={createProject.isPending}>
                    <PlusCircle className="h-5 w-5 mr-2" />
                    New Project
                </Button>
            </div>

            <Card className="mb-6">
                <CardHeader>
                    <CardTitle>Project List</CardTitle>
                </CardHeader>
                <CardContent>
                    <div className="flex space-x-2 mb-4">
                        <div className="relative flex-grow">
                            <Search className="absolute left-2 top-2.5 h-4 w-4 text-gray-500" />
                            <Input
                                type="text"
                                placeholder="Search projects..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="pl-8"
                            />
                        </div>
                        <Button variant="outline">
                            <Filter className="h-4 w-4 mr-2" />
                            Filter
                        </Button>
                    </div>

                    <Table>
                        <TableHeader>
                            <TableRow>
                                <TableHead>Name</TableHead>
                                <TableHead>Description</TableHead>
                                <TableHead>Created At</TableHead>
                                <TableHead>Status</TableHead>
                            </TableRow>
                        </TableHeader>
                        <TableBody>
                            {filteredProjects?.map((project) => (
                                <TableRow key={project.id}>
                                    <TableCell className="font-medium">{project.name}</TableCell>
                                    <TableCell>{project.description}</TableCell>
                                    <TableCell>{new Date(project.created_at).toLocaleDateString()}</TableCell>
                                    <TableCell>
                                        <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${project.processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'
                                            }`}>
                                            {project.processed ? 'Completed' : 'Pending'}
                                        </span>
                                    </TableCell>
                                </TableRow>
                            ))}
                        </TableBody>
                    </Table>
                </CardContent>
            </Card>

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

