import api from "./api";

export async function getInstructorDashboard() {

    const response = await api.get("/instructor/dashboard");

    return response.data;

}