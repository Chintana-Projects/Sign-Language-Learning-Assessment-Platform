
import axios from "axios";

// =====================================================
// AXIOS API INSTANCE
// =====================================================

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",

    headers: {
        "Content-Type": "application/json",
    },
});

// =====================================================
// REQUEST INTERCEPTOR
// Automatically attaches JWT token to every request
// =====================================================

api.interceptors.request.use(
    (config) => {

        const token =
            localStorage.getItem("signsync_access_token");

        if (token) {

            config.headers.Authorization =
                `Bearer ${token}`;

        }

        return config;
    },

    (error) => {

        return Promise.reject(error);

    }
);

// =====================================================
// EXPORT API
// =====================================================

export default api;

