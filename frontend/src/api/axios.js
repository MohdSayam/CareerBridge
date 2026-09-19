import axios from "axios";

const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api",
    timeout: 15000 // 15 second timeout
})

// Auto-attach JWT token to every request
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("access_token")
    if (token) {
        config.headers.Authorization = `Bearer ${token}`
    }
    return config
}, (error) => Promise.reject(error))

// Global 401 handler — clear session and redirect to login
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            const isAuthEndpoint = error.config?.url?.includes("/auth/")
            if (!isAuthEndpoint) {
                localStorage.clear()
                window.location.href = "/login"
            }
        }
        return Promise.reject(error)
    }
)

export default api