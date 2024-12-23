import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const getAuthToken = () => localStorage.getItem('authToken') || '';


// Create axios instance with default config
export const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${getAuthToken()}`, // Inclua o token aqui
    },
    withCredentials: true, // Para cookies de sessão, se necessário
});


api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if (error.response?.status === 401) {
            console.error('Autenticação falhou. Redirecionando para login.');
            window.location.href = '/login'; // Redirecione para a página de login
        }
        return Promise.reject(error);
    }
);


// Types
export interface Project {
    id: string;
    name: string;
    description: string | null;
    owner: string;
    created_at: string;
    updated_at: string;
}

export interface Dataset {
    id: string;
    project: string;
    name: string;
    file: string;
    uploaded_at: string;
    processed: boolean;
}

export interface AnalysisResult {
    id: string;
    dataset: string;
    well_name: string;
    parameter: string;
    trend: string;
    statistic: number;
    coefficient_variation: number;
    confidence_factor: number;
    data_points: number;
    minimum_value: number;
    maximum_value: number;
    mean_value: number;
    analysis_date: string;
}

// API functions
export const projectsApi = {
    // Get all projects
    getAll: () => api.get<Project[]>('/projects/').then(res => res.data),

    // Get single project
    getById: (id: string) => api.get<Project>(`/projects/${id}/`).then(res => res.data),

    // Create new project
    create: (data: Omit<Project, 'id' | 'owner' | 'created_at' | 'updated_at'>) =>
        api.post<Project>('/projects/', data).then(res => res.data),

    // Update project
    update: (id: string, data: Partial<Project>) =>
        api.patch<Project>(`/projects/${id}/`, data).then(res => res.data),

    // Delete project
    delete: (id: string) => api.delete(`/projects/${id}/`)
};

export const datasetsApi = {
    // Get all datasets
    getAll: () => api.get<Dataset[]>('/datasets/').then(res => res.data),

    // Get datasets for a project
    getByProject: (projectId: string) =>
        api.get<Dataset[]>('/datasets/', { params: { project: projectId } })
            .then(res => res.data),

    // Upload new dataset
    upload: (projectId: string, name: string, file: File) => {
        const formData = new FormData();
        formData.append('project', projectId);
        formData.append('name', name);
        formData.append('file', file);

        return api.post<Dataset>('/datasets/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        }).then(res => res.data);
    },

    // Start analysis for a dataset
    analyze: (datasetId: string) =>
        api.post<{ message: string; results_count: number }>(`/datasets/${datasetId}/analyze/`)
            .then(res => res.data)
};

export const analysisApi = {
    // Get all analyses
    getAll: () => api.get<AnalysisResult[]>('/analyses/').then(res => res.data),

    // Get analyses for a dataset
    getByDataset: (datasetId: string) =>
        api.get<AnalysisResult[]>('/analyses/dataset_results/', {
            params: { dataset_id: datasetId }
        }).then(res => res.data)
};

// Error handling
api.interceptors.response.use(
    response => response,
    error => {
        // Handle different error types
        if (error.response?.status === 401) {
            // Handle unauthorized - maybe redirect to login
            window.location.href = '/login';
        }

        return Promise.reject(error);
    }
);
