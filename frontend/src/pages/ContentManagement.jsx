import { useEffect, useState } from "react";
import "../styles/Layout.css";
import "../styles/Cards.css";

export default function ContentManagement() {
    const [lessons, setLessons] = useState([]);
    const [loading, setLoading] = useState(true);
    const [editingLesson, setEditingLesson] = useState(null);
const [saving, setSaving] = useState(false);

    // =========================================
    // LOAD LESSONS
    // =========================================

    async function loadLessons() {
        try {
            setLoading(true);

            const response = await fetch(
                "http://127.0.0.1:8000/lessons/"
            );

            if (!response.ok) {
                throw new Error("Unable to load lessons");
            }

            const data = await response.json();

            setLessons(data);
        } catch (error) {
            console.error(
                "Content loading error:",
                error
            );
        } finally {
            setLoading(false);
        }
    }

    // =========================================
    // LOAD ON PAGE OPEN
    // =========================================

    useEffect(() => {
        loadLessons();
    }, []);

    // =========================================
    // TOGGLE STATUS
    // =========================================

    async function toggleStatus(lesson) {
        try {
            const response = await fetch(
                `http://127.0.0.1:8000/lessons/${lesson.id}/status?is_active=${!lesson.is_active}`,
                {
                    method: "PATCH"
                }
            );

            if (!response.ok) {
                throw new Error(
                    "Unable to update lesson status"
                );
            }

            await loadLessons();
        } catch (error) {
            console.error(
                "Status update error:",
                error
            );
        }
    }

    async function saveLesson() {
    try {
        setSaving(true);

        const response = await fetch(
            `http://127.0.0.1:8000/lessons/${editingLesson.id}?title=${encodeURIComponent(editingLesson.title)}&description=${encodeURIComponent(editingLesson.description)}&category=${encodeURIComponent(editingLesson.category)}`,
            {
                method: "PUT"
            }
        );

        if (!response.ok) {
            throw new Error("Unable to update lesson");
        }

        setEditingLesson(null);

        await loadLessons();

    } catch (error) {
        console.error(
            "Lesson update error:",
            error
        );
    } finally {
        setSaving(false);
    }
}

    // =========================================
    // LOADING
    // =========================================

    if (loading) {
        return (
            <div
                style={{
                    padding: "40px",
                    textAlign: "center"
                }}
            >
                Loading content...
            </div>
        );
    }

    // =========================================
    // PAGE
    // =========================================

    return (
       <div
    style={{
        width: "100%",
        minHeight: "100vh",
        boxSizing: "border-box",
        background: "#F5F7FB",
        padding: "30px 40px"
    }}
>
            {/* HEADER */}

            <div
                style={{
                   width: "100%",
margin: "0 auto 25px"
                }}
            >
                <h1
                    style={{
                        margin: 0,
                        fontSize: "30px",
                        color: "#111827"
                    }}
                >
                    Content Management
                </h1>

                <p
                    style={{
                        marginTop: "6px",
                        color: "#6B7280"
                    }}
                >
                    Manage learning lessons available to learners.
                </p>
            </div>

            {/* CONTENT CARD */}

<div
    style={{
        width: "100%",
        background: "#FFFFFF",
        color: "#111827",
        borderRadius: "20px",
        padding: "25px",
        boxSizing: "border-box",
        boxShadow:
            "0 8px 30px rgba(15,23,42,0.08)"
    }}
> <div
                    style={{
                        overflowX: "auto"
                    }}
                >
                    <table
                        style={{
                            width: "100%",
                            borderCollapse: "collapse"
                        }}
                    >
                        <thead>
                            <tr
                                style={{
                                    borderBottom:
                                        "1px solid #E5E7EB",
                                    textAlign: "left"
                                }}
                            >
                                <th style={thStyle}>
                                    Letter
                                </th>

                                <th style={thStyle}>
                                    Title
                                </th>

                                <th style={thStyle}>
                                    Category
                                </th>

                                <th style={thStyle}>
                                    Status
                                </th>

                                <th style={thStyle}>
                                    Action
                                </th>
                            </tr>
                        </thead>

                        <tbody>
                            {lessons.map((lesson) => (
                                <tr
                                    key={lesson.id}
                                    style={{
                                        borderBottom:
                                            "1px solid #F1F5F9"
                                    }}
                                >
                                    <td style={tdStyle}>
                                        <strong
                                            style={{
                                                fontSize: "20px",
                                                color: "#4F46E5"
                                            }}
                                        >
                                            {lesson.sign}
                                        </strong>
                                    </td>

                                    <td style={tdStyle}>
                                        {lesson.title}
                                    </td>

                                    <td style={tdStyle}>
                                        {lesson.category}
                                    </td>

                                    <td style={tdStyle}>
                                        <span
                                            style={{
                                                padding:
                                                    "6px 12px",
                                                borderRadius:
                                                    "999px",
                                                fontSize:
                                                    "13px",
                                                fontWeight:
                                                    "600",
                                                background:
                                                    lesson.is_active
                                                        ? "#DCFCE7"
                                                        : "#FEE2E2",
                                                color:
                                                    lesson.is_active
                                                        ? "#15803D"
                                                        : "#B91C1C"
                                            }}
                                        >
                                            {lesson.is_active
                                                ? "Active"
                                                : "Inactive"}
                                        </span>
                                    </td>

                                    <td style={tdStyle}>
                                        <div
    style={{
        display: "flex",
        gap: "8px"
    }}
>
    <button
        onClick={() =>
            setEditingLesson({
                ...lesson
            })
        }
        style={{
            border: "none",
            borderRadius: "8px",
            padding: "8px 14px",
            cursor: "pointer",
            background: "#EEF2FF",
            color: "#4F46E5",
            fontWeight: "600"
        }}
    >
        Edit
    </button>

    <button
        onClick={() =>
            toggleStatus(lesson)
        }
        style={{
            border: "none",
            borderRadius: "8px",
            padding: "8px 14px",
            cursor: "pointer",
            background: lesson.is_active
                ? "#FEE2E2"
                : "#DCFCE7",
            color: lesson.is_active
                ? "#B91C1C"
                : "#15803D",
            fontWeight: "600"
        }}
    >
        {lesson.is_active
            ? "Deactivate"
            : "Activate"}
    </button>
</div>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
            {editingLesson && (
    <div
        style={{
            position: "fixed",
            inset: 0,
            background: "rgba(0,0,0,0.45)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 1000
        }}
    >
        <div
            style={{
                width: "500px",
                maxWidth: "90%",
                background: "#FFFFFF",
                borderRadius: "16px",
                padding: "25px",
                boxShadow:
                    "0 20px 50px rgba(0,0,0,0.2)"
            }}
        >
            <h2
    style={{
        marginTop: 0,
        color: "#111827",
        background: "#FFFFFF"
    }}
>
    Edit Lesson
</h2>

            <label style={labelStyle}>
                Title
            </label>

            <input
                value={editingLesson.title}
                onChange={(e) =>
                    setEditingLesson({
                        ...editingLesson,
                        title: e.target.value
                    })
                }
                style={inputStyle}
            />

            <label style={labelStyle}>
                Description
            </label>

            <textarea
                value={editingLesson.description || ""}
                onChange={(e) =>
                    setEditingLesson({
                        ...editingLesson,
                        description:
                            e.target.value
                    })
                }
                rows={4}
                style={inputStyle}
            />

            <label style={labelStyle}>
                Category
            </label>

            <input
                value={editingLesson.category || ""}
                onChange={(e) =>
                    setEditingLesson({
                        ...editingLesson,
                        category: e.target.value
                    })
                }
                style={inputStyle}
            />

            <div
                style={{
                    display: "flex",
                    justifyContent: "flex-end",
                    gap: "10px",
                    marginTop: "20px"
                }}
            >
                <button
                    onClick={() =>
                        setEditingLesson(null)
                    }
                    style={cancelButtonStyle}
                >
                    Cancel
                </button>

                <button
                    onClick={saveLesson}
                    disabled={saving}
                    style={saveButtonStyle}
                >
                    {saving
                        ? "Saving..."
                        : "Save"}
                </button>
            </div>
        </div>
    </div>
)}
        </div>
    );
}

// =========================================
// TABLE STYLES
// =========================================

const thStyle = {
    padding: "14px 16px",
    color: "#6B7280",
    fontSize: "14px",
    fontWeight: "600"
};

const tdStyle = {
    padding: "16px",
    color: "#374151",
    fontSize: "15px"
};
const labelStyle = {
    display: "block",
    marginBottom: "6px",
    marginTop: "15px",
    color: "#374151",
    background: "#FFFFFF",
    fontSize: "14px",
    fontWeight: "600"
};

const inputStyle = {
    width: "100%",
    boxSizing: "border-box",
    padding: "10px 12px",
    border: "1px solid #D1D5DB",
    borderRadius: "8px",
    fontSize: "14px",
    color: "#111827",
    background: "#FFFFFF",
    outline: "none"
};

const cancelButtonStyle = {
    border: "1px solid #D1D5DB",
    borderRadius: "8px",
    padding: "9px 16px",
    background: "#FFFFFF",
    color: "#374151",
    cursor: "pointer",
    fontWeight: "600"
};

const saveButtonStyle = {
    border: "none",
    borderRadius: "8px",
    padding: "9px 18px",
    background: "#4F46E5",
    color: "#FFFFFF",
    cursor: "pointer",
    fontWeight: "600"
};