import api from "./api";


// =========================================
// LOGIN
// =========================================

export const loginUser = async (data) => {

    const response = await api.post(
        "/auth/login",
        data
    );

    return response.data;
};


// =========================================
// REGISTER USER
// =========================================

export const registerUser = async (data) => {

    const response = await api.post(
        "/auth/register",
        data
    );

    return response.data;
};


// =========================================
// GET ALL USERS
// =========================================

export const getAllUsers = async () => {

    const response = await api.get(
        "/users/"
    );

    return response.data;
};


// =========================================
// UPDATE USER
// =========================================

export const updateUser = async (
    userId,
    data
) => {

    const response = await api.put(
        `/users/${userId}`,
        null,
        {
            params: {
                full_name: data.full_name,
                email: data.email,
                role: data.role
            }
        }
    );

    return response.data;
};


// =========================================
// ACTIVATE / DEACTIVATE USER
// =========================================

export const updateUserStatus = async (
    userId,
    isActive
) => {

    const response = await api.patch(
        `/users/${userId}/status`,
        null,
        {
            params: {
                is_active: isActive
            }
        }
    );

    return response.data;
};