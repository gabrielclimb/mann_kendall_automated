
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { projectsApi, datasetsApi, analysisApi, Project, Dataset, AnalysisResult } from '../services/api';

// Projects hooks
export const useProjects = () => {
    return useQuery<Project[]>({
        queryKey: ['projects'],
        queryFn: projectsApi.getAll
    });
};

export const useProject = (id: string) => {
    return useQuery<Project>({
        queryKey: ['projects', id],
        queryFn: () => projectsApi.getById(id),
        enabled: !!id
    });
};

export const useCreateProject = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: projectsApi.create,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['projects'] });
        }
    });
};

export const useUpdateProject = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ id, data }: { id: string; data: Partial<Project> }) =>
            projectsApi.update(id, data),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: ['projects'] });
            queryClient.invalidateQueries({ queryKey: ['projects', variables.id] });
        }
    });
};

export const useDeleteProject = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: projectsApi.delete,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['projects'] });
        }
    });
};

// Datasets hooks
export const useProjectDatasets = (projectId: string) => {
    return useQuery<Dataset[]>({
        queryKey: ['datasets', projectId],
        queryFn: () => datasetsApi.getByProject(projectId),
        enabled: !!projectId
    });
};

export const useUploadDataset = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: ({ projectId, name, file }: { projectId: string; name: string; file: File }) =>
            datasetsApi.upload(projectId, name, file),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: ['datasets', variables.projectId] });
        }
    });
};

export const useAnalyzeDataset = () => {
    const queryClient = useQueryClient();

    return useMutation({
        mutationFn: datasetsApi.analyze,
        onSuccess: (_, datasetId) => {
            queryClient.invalidateQueries({ queryKey: ['analyses', datasetId] });
        }
    });
};

// Analysis hooks
export const useDatasetAnalyses = (datasetId: string) => {
    return useQuery<AnalysisResult[]>({
        queryKey: ['analyses', datasetId],
        queryFn: () => analysisApi.getByDataset(datasetId),
        enabled: !!datasetId
    });
};
