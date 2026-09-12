const API_URL = "http://127.0.0.1:8000/lessons";

export const getLessons = async () => {
    const res = await fetch(`${API_URL}/`);
    return await res.json();
};

export const createLesson = async (lesson) => {
    const res = await fetch(`${API_URL}/`, {
        method: "POST",
        headers: {
            "Content-Type":
                "application/json"
        },
        body: JSON.stringify(lesson)
    });

    return await res.json();
};

export const updateLesson = async (
    id,
    lesson
) => {
    const params =
        new URLSearchParams({
            title: lesson.title,
            description:
                lesson.description,
            category:
                lesson.category
        });

    const res = await fetch(
        `${API_URL}/${id}?${params}`,
        {
            method: "PUT"
        }
    );

    return await res.json();
};

export const updateLessonStatus =
    async (id, isActive) => {

        const res = await fetch(
            `${API_URL}/${id}/status?is_active=${isActive}`,
            {
                method: "PATCH"
            }
        );

        return await res.json();
    };