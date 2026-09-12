import api from "./api";


// =====================================================
// INSTRUCTOR DASHBOARD
// =====================================================

export async function getInstructorDashboard() {

    const response = await api.get(
        "/instructor/dashboard"
    );

    return response.data;
}


// =====================================================
// ALL INSTRUCTOR STUDENTS
// =====================================================

export async function getInstructorStudents() {

    const response = await api.get(
        "/instructor/students"
    );

    return response.data;
}


// =====================================================
// INDIVIDUAL STUDENT DETAILS
// =====================================================

export async function getStudentDetails(studentId) {

    const response = await api.get(
        `/instructor/students/${studentId}`
    );

    return response.data;
}   