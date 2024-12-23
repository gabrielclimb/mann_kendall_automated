import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Navbar } from './components/layout/Navbar';
import { HomePage } from './pages/HomePage';
import { ProjectsPage } from './pages/ProjectsPage';
import { LoginPage } from './pages/LoginPage';
import { AnalysisPage } from './pages/AnalysisPage';
import { ProtectedRoute } from './components/routes/ProtectedRoute';

const queryClient = new QueryClient();

// function App() {
//     return (
//         <QueryClientProvider client={queryClient}>
//             <Router>
//                 <div className="min-h-screen bg-background text-foreground">
//                     <Navbar />
//                     <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
//                         <Routes>
//                             <Route path="/login" element={<LoginPage />} />
//                             <Route path="/" element={<HomePage />} />
//                             <Route path="/projects" element={<ProjectsPage />} />
//                             <Route path="/analysis" element={<AnalysisPage />} />
//                         </Routes>
//                     </main>
//                 </div>
//             </Router>
//             <ReactQueryDevtools initialIsOpen={false} />
//         </QueryClientProvider>
//     );
// }

function App() {
    return (
        <Router>
            <Routes>
                {/* Rota pública para login */}
                <Route path="/login" element={<LoginPage />} />

                {/* Rotas protegidas */}
                <Route
                    path="/"
                    element={
                        <ProtectedRoute>
                            <HomePage />
                        </ProtectedRoute>
                    }
                />
            </Routes>
        </Router>
    );
}

export default App;
