const API_URL = "http://localhost:8000";


export async function getStudentProgress(studentId) {
    try {
        const response = await fetch(
            `${API_URL}/api/dashboard/progress/${studentId}`
        );

        if (!response.ok) {
            throw new Error("Failed to fetch progress");
        }

        return await response.json();

    } catch (error) {
        console.error("Progress API Error:", error);
        return null;
    }
}


export async function getRecommendations(studentId) {
    try {
        const response = await fetch(
            `${API_URL}/api/dashboard/recommendations/${studentId}`
        );

        if (!response.ok) {
            throw new Error("Failed to fetch recommendations");
        }

        return await response.json();

    } catch(error){
        console.error("Recommendation API Error:", error);
        return null;
    }
}