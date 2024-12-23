import { api } from "../services/api";


export async function login(username: string, password: string) {
    try {
        const response = await api.post('/auth/login', { username, password });
        const { access_token } = response.data;
        localStorage.setItem('authToken', access_token); // Salvar o token
        return access_token;
    } catch (error) {
        console.error('Erro ao autenticar:', error);
        throw error;
    }
}

export function logout() {
    localStorage.removeItem('authToken');
    window.location.href = '/login'; // Redireciona após logout
}

export function isAuthenticated(): boolean {
    const token = localStorage.getItem('authToken');
    return !!token;
}
