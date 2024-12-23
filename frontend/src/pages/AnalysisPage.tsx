// src/pages/AnalysisPage.tsx
import React, { useState } from 'react';
import { FileSpreadsheet } from 'lucide-react';
import { useProjects, useUploadDataset, useAnalyzeDataset } from '../hooks/useApi';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';

export const AnalysisPage = () => {
    const [file, setFile] = useState<File | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const { data: projects } = useProjects();
    const uploadDataset = useUploadDataset();
    const analyzeDataset = useAnalyzeDataset();

    const handleDragOver = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        setIsDragging(false);

        const droppedFile = e.dataTransfer.files[0];
        if (isValidFileType(droppedFile)) {
            setFile(droppedFile);
        }
    };

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const selectedFile = e.target.files?.[0];
        if (selectedFile && isValidFileType(selectedFile)) {
            setFile(selectedFile);
        }
    };

    const handleUpload = async () => {
        if (!file || !projects?.[0]) return;

        try {
            // Upload the dataset
            const dataset = await uploadDataset.mutateAsync({
                projectId: projects[0].id,
                name: file.name,
                file: file
            });

            // Start analysis
            await analyzeDataset.mutateAsync(dataset.id);

            // Clear the file
            setFile(null);
        } catch (error) {
            console.error('Upload failed:', error);
        }
    };

    const isValidFileType = (file: File) => {
        const validTypes = [
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        ];
        return validTypes.includes(file.type);
    };

    return (
        <div>
            <h1 className="text-2xl font-bold text-gray-900 mb-6">Analysis</h1>
            <div className="bg-white shadow sm:rounded-lg">
                <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-lg leading-6 font-medium text-gray-900">
                        Upload Dataset for Analysis
                    </h3>
                    <div className="mt-2 max-w-xl text-sm text-gray-500">
                        <p>Upload your Excel file containing time series data for analysis.</p>
                    </div>
                    <div className="mt-5">
                        <div
                            className="flex items-center justify-center w-full"
                            onDragOver={handleDragOver}
                            onDragLeave={handleDragLeave}
                            onDrop={handleDrop}
                        >
                            <label className={`flex flex-col items-center justify-center w-full h-64 border-2 border-dashed rounded-lg cursor-pointer ${isDragging
                                    ? 'border-blue-500 bg-blue-50'
                                    : 'border-gray-300 bg-gray-50 hover:bg-gray-100'
                                }`}>
                                <div className="flex flex-col items-center justify-center pt-5 pb-6">
                                    <FileSpreadsheet className="w-10 h-10 mb-3 text-gray-400" />
                                    <p className="mb-2 text-sm text-gray-500">
                                        <span className="font-semibold">Click to upload</span> or drag and drop
                                    </p>
                                    <p className="text-xs text-gray-500">
                                        Excel files only (XLSX, XLS)
                                    </p>
                                    {file && (
                                        <p className="mt-2 text-sm text-blue-600">
                                            Selected: {file.name}
                                        </p>
                                    )}
                                </div>
                                <input
                                    type="file"
                                    className="hidden"
                                    accept=".xlsx,.xls"
                                    onChange={handleFileChange}
                                />
                            </label>
                        </div>
                    </div>

                    {file && (
                        <div className="mt-4">
                            <button
                                onClick={handleUpload}
                                disabled={uploadDataset.isPending || analyzeDataset.isPending}
                                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                            >
                                {uploadDataset.isPending || analyzeDataset.isPending ?
                                    'Processing...' : 'Start Analysis'}
                            </button>
                        </div>
                    )}

                    {uploadDataset.error && (
                        <Alert variant="destructive" className="mt-4">
                            <AlertTitle>Upload Error</AlertTitle>
                            <AlertDescription>
                                {uploadDataset.error instanceof Error
                                    ? uploadDataset.error.message
                                    : 'Failed to upload dataset'}
                            </AlertDescription>
                        </Alert>
                    )}

                    {analyzeDataset.error && (
                        <Alert variant="destructive" className="mt-4">
                            <AlertTitle>Analysis Error</AlertTitle>
                            <AlertDescription>
                                {analyzeDataset.error instanceof Error
                                    ? analyzeDataset.error.message
                                    : 'Failed to analyze dataset'}
                            </AlertDescription>
                        </Alert>
                    )}
                </div>
            </div>
        </div>
    );
};
