import { useState } from 'react';
import { useAnalyzeDataset, useUploadDataset } from '../hooks/useApi';
import { Alert, AlertDescription, AlertTitle, Button, Card, CardContent, CardHeader, CardTitle, Label, Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui';
import { FileUploader } from '../components/FileUploader';

export const AnalysisPage = () => {
    const [file, setFile] = useState<File | null>(null);
    const [analysisType, setAnalysisType] = useState('mann-kendall');
    const uploadDataset = useUploadDataset();
    const analyzeDataset = useAnalyzeDataset();

    const handleFileChange = (selectedFile: File) => {
        setFile(selectedFile);
    };

    const handleUpload = async () => {
        if (file) {
            try {
                const uploadResult = await uploadDataset.mutateAsync({
                    projectId: 'your-project-id', // You need to provide the project ID
                    name: file.name,
                    file: file
                });
                if (uploadResult.id) {
                    await analyzeDataset.mutateAsync(uploadResult.id);
                }
            } catch (error) {
                console.error('Error during upload or analysis:', error);
            }
        }
    };

    return (
        <div className="container mx-auto px-4 py-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-6">Data Analysis</h1>

            <Tabs defaultValue="upload" className="space-y-4">
                <TabsList>
                    <TabsTrigger value="upload">Upload Dataset</TabsTrigger>
                    <TabsTrigger value="results">Analysis Results</TabsTrigger>
                </TabsList>

                <TabsContent value="upload">
                    <Card>
                        <CardHeader>
                            <CardTitle>Upload New Dataset</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="space-y-4">
                                <FileUploader onFileSelect={handleFileChange} />

                                <div className="space-y-2">
                                    <Label htmlFor="analysis-type">Analysis Type</Label>
                                    <select
                                        id="analysis-type"
                                        value={analysisType}
                                        onChange={(e) => setAnalysisType(e.target.value)}
                                        className="w-full p-2 border rounded"
                                    >
                                        <option value="mann-kendall">Mann-Kendall Test</option>
                                        <option value="linear-regression">Linear Regression</option>
                                        <option value="time-series">Time Series Analysis</option>
                                    </select>
                                </div>

                                <Button
                                    onClick={handleUpload}
                                    disabled={!file || uploadDataset.isPending || analyzeDataset.isPending}
                                    className="w-full"
                                >
                                    {uploadDataset.isPending || analyzeDataset.isPending ? 'Processing...' : 'Start Analysis'}
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="results">
                    <Card>
                        <CardHeader>
                            <CardTitle>Analysis Results</CardTitle>
                        </CardHeader>
                        <CardContent>
                            {analyzeDataset.data ? (
                                <div>
                                    <h3 className="text-lg font-semibold mb-2">Results for Dataset {analyzeDataset.data.dataset}</h3>
                                    <pre className="bg-gray-100 p-4 rounded overflow-x-auto">
                                        {JSON.stringify(analyzeDataset.data.results, null, 2)}
                                    </pre>
                                </div>
                            ) : (
                                <p>No analysis results available. Please upload and analyze a dataset.</p>
                            )}
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>

            {(uploadDataset.error || analyzeDataset.error) && (
                <Alert variant="destructive" className="mt-4">
                    <AlertTitle>Error</AlertTitle>
                    <AlertDescription>
                        {uploadDataset.error instanceof Error
                            ? uploadDataset.error.message
                            : analyzeDataset.error instanceof Error
                                ? analyzeDataset.error.message
                                : 'An error occurred during the process'}
                    </AlertDescription>
                </Alert>
            )}
        </div>
    );
};

