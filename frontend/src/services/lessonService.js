import api from "./api";

// =========================================
// GET ALL LESSONS
// =========================================

export const getAllLessons = async () => {
    const response = await api.get("/lessons/");
    return response.data;
};


// =========================================
// GET LESSON BY ID
// =========================================

export const getLessonById = async (lessonId) => {
    const response = await api.get(`/lessons/${lessonId}`);
    return response.data;
};