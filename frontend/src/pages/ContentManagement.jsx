import { useEffect, useState } from "react";
import "../styles/Layout.css";
import "../styles/Cards.css";

import {
    getLessons,
    createLesson,
    updateLesson,
    updateLessonStatus
} from "../services/lessonService";

export default function ContentManagement() {

    const [lessons, setLessons] = useState([]);
    const [loading, setLoading] = useState(true);

    const [editingLesson, setEditingLesson] =
        useState(null);

    const [saving, setSaving] =
        useState(false);

    const [showAddModal, setShowAddModal] =
        useState(false);

    const [newLesson, setNewLesson] =
        useState({
            title: "",
            description: "",
            category: "",
            sign: "",
            image_url: "",
            video_url: ""
        });

    // =========================================
    // LOAD LESSONS
    // =========================================

    const loadLessons = async () => {

        try {

            setLoading(true);

            const data =
                await getLessons();

            setLessons(data);

        } catch (error) {

            console.error(
                "Failed to load lessons",
                error
            );

        } finally {

            setLoading(false);

        }
    };

    // =========================================
    // PAGE LOAD
    // =========================================

    useEffect(() => {

        loadLessons();

    }, []);

    // =========================================
    // ACTIVATE / DEACTIVATE
    // =========================================

    const toggleStatus = async (
        lesson
    ) => {

        try {

            await updateLessonStatus(
                lesson.id,
                !lesson.is_active
            );

            await loadLessons();

        } catch (error) {

            console.error(
                "Status update error",
                error
            );
        }
    };

    // =========================================
    // SAVE EDIT
    // =========================================

    const saveLesson = async () => {

        try {

            setSaving(true);

            await updateLesson(
                editingLesson.id,
                {
                    title:
                        editingLesson.title,

                    description:
                        editingLesson.description,

                    category:
                        editingLesson.category
                }
            );

            setEditingLesson(null);

            await loadLessons();

        } catch (error) {

            console.error(
                "Lesson update error",
                error
            );

        } finally {

            setSaving(false);

        }
    };

    // =========================================
    // CREATE LESSON
    // =========================================

    const handleAddLesson = async () => {

        try {

            await createLesson(
                newLesson
            );

            setShowAddModal(false);

            setNewLesson({
                title: "",
                description: "",
                category: "",
                sign: "",
                image_url: "",
                video_url: ""
            });

            await loadLessons();

        } catch (error) {

            console.error(
                "Create lesson error",
                error
            );
        }
    };

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

    return (
        <div
            style={{
                width: "100%",
                minHeight: "100vh",
                background: "#F5F7FB",
                padding: "30px 40px",
                boxSizing: "border-box"
            }}
        >

            <div
                style={{
                    marginBottom: "25px"
                }}
            >
                <h1
                    style={{
                        margin: 0,
                        fontSize: "30px"
                    }}
                >
                    Content Management
                </h1>

                <p
                    style={{
                        color: "#6B7280"
                    }}
                >
                    Manage learning lessons.
                </p>

                <button
                    onClick={() =>
                        setShowAddModal(true)
                    }
                    style={{
                        marginTop: "15px",
                        background: "#4F46E5",
                        color: "#FFF",
                        border: "none",
                        padding: "10px 18px",
                        borderRadius: "8px",
                        cursor: "pointer",
                        fontWeight: "600"
                    }}
                >
                    + Add Lesson
                </button>
            </div>

            <div
                style={{
                    background: "#FFF",
                    padding: "25px",
                    borderRadius: "20px",
                    boxShadow:
                        "0 8px 30px rgba(0,0,0,0.08)"
                }}
            >

                <table
                    style={{
                        width: "100%",
                        borderCollapse:
                            "collapse"
                    }}
                >
                    <thead>
                        <tr>
                            <th style={thStyle}>
                                Sign
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
                                Actions
                            </th>
                        </tr>
                    </thead>

                    <tbody>

                        {lessons.map(
                            (lesson) => (

                                <tr
                                    key={
                                        lesson.id
                                    }
                                >

                                    <td style={tdStyle}>
                                        {
                                            lesson.sign
                                        }
                                    </td>

                                    <td style={tdStyle}>
                                        {
                                            lesson.title
                                        }
                                    </td>

                                    <td style={tdStyle}>
                                        {
                                            lesson.category
                                        }
                                    </td>

                                    <td style={tdStyle}>
                                        <span
                                            style={{
                                                color:
                                                    lesson.is_active
                                                        ? "green"
                                                        : "red"
                                            }}
                                        >
                                            {
                                                lesson.is_active
                                                    ? "Active"
                                                    : "Inactive"
                                            }
                                        </span>
                                    </td>

                                    <td style={tdStyle}>
                                        <button
                                            onClick={() =>
                                                setEditingLesson(
                                                    {
                                                        ...lesson
                                                    }
                                                )
                                            }
                                            style={
                                                editBtn
                                            }
                                        >
                                            Edit
                                        </button>

                                        <button
                                            onClick={() =>
                                                toggleStatus(
                                                    lesson
                                                )
                                            }
                                            style={
                                                statusBtn
                                            }
                                        >
                                            {
                                                lesson.is_active
                                                    ? "Deactivate"
                                                    : "Activate"
                                            }
                                        </button>
                                    </td>

                                </tr>
                            )
                        )}

                    </tbody>

                </table>

            </div>

            {/* ADD MODAL */}

            {showAddModal && (

                <div
                    style={
                        modalOverlay
                    }
                >
                    <div
                        style={
                            modalBox
                        }
                    >

                        <h2>
                            Add Lesson
                        </h2>

                        <input
                            placeholder="Title"
                            value={
                                newLesson.title
                            }
                            onChange={(e) =>
                                setNewLesson({
                                    ...newLesson,
                                    title:
                                        e.target
                                            .value
                                })
                            }
                            style={
                                inputStyle
                            }
                        />

                        <input
                            placeholder="Sign"
                            value={
                                newLesson.sign
                            }
                            onChange={(e) =>
                                setNewLesson({
                                    ...newLesson,
                                    sign:
                                        e.target
                                            .value
                                })
                            }
                            style={
                                inputStyle
                            }
                        />

                        <input
                            placeholder="Category"
                            value={
                                newLesson.category
                            }
                            onChange={(e) =>
                                setNewLesson({
                                    ...newLesson,
                                    category:
                                        e.target
                                            .value
                                })
                            }
                            style={
                                inputStyle
                            }
                        />

                        <textarea
                            placeholder="Description"
                            rows={4}
                            value={
                                newLesson.description
                            }
                            onChange={(e) =>
                                setNewLesson({
                                    ...newLesson,
                                    description:
                                        e.target
                                            .value
                                })
                            }
                            style={
                                inputStyle
                            }
                        />

                        <div
                            style={{
                                display:
                                    "flex",
                                justifyContent:
                                    "flex-end",
                                gap: "10px",
                                marginTop:
                                    "20px"
                            }}
                        >

                            <button
                                onClick={() =>
                                    setShowAddModal(
                                        false
                                    )
                                }
                                style={
                                    cancelButtonStyle
                                }
                            >
                                Cancel
                            </button>

                            <button
                                onClick={
                                    handleAddLesson
                                }
                                style={
                                    saveButtonStyle
                                }
                            >
                                Create
                            </button>

                        </div>

                    </div>
                </div>
            )}

            {/* EDIT MODAL */}

            {editingLesson && (

                <div
                    style={
                        modalOverlay
                    }
                >
                    <div
                        style={
                            modalBox
                        }
                    >

                        <h2>
                            Edit Lesson
                        </h2>

                        <input
                            value={
                                editingLesson.title
                            }
                            onChange={(e) =>
                                setEditingLesson(
                                    {
                                        ...editingLesson,
                                        title:
                                            e
                                                .target
                                                .value
                                    }
                                )
                            }
                            style={
                                inputStyle
                            }
                        />

                        <textarea
                            rows={4}
                            value={
                                editingLesson.description
                            }
                            onChange={(e) =>
                                setEditingLesson(
                                    {
                                        ...editingLesson,
                                        description:
                                            e
                                                .target
                                                .value
                                    }
                                )
                            }
                            style={
                                inputStyle
                            }
                        />

                        <input
                            value={
                                editingLesson.category
                            }
                            onChange={(e) =>
                                setEditingLesson(
                                    {
                                        ...editingLesson,
                                        category:
                                            e
                                                .target
                                                .value
                                    }
                                )
                            }
                            style={
                                inputStyle
                            }
                        />

                        <div
                            style={{
                                display:
                                    "flex",
                                justifyContent:
                                    "flex-end",
                                gap: "10px",
                                marginTop:
                                    "20px"
                            }}
                        >

                            <button
                                onClick={() =>
                                    setEditingLesson(
                                        null
                                    )
                                }
                                style={
                                    cancelButtonStyle
                                }
                            >
                                Cancel
                            </button>

                            <button
                                onClick={
                                    saveLesson
                                }
                                disabled={
                                    saving
                                }
                                style={
                                    saveButtonStyle
                                }
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

const thStyle = {
    padding: "12px",
    textAlign: "left"
};

const tdStyle = {
    padding: "12px"
};

const editBtn = {
    marginRight: "10px",
    padding: "8px 12px",
    border: "none",
    background: "#EEF2FF",
    color: "#4F46E5",
    borderRadius: "6px",
    cursor: "pointer"
};

const statusBtn = {
    padding: "8px 12px",
    border: "none",
    background: "#F3F4F6",
    borderRadius: "6px",
    cursor: "pointer"
};

const modalOverlay = {
    position: "fixed",
    inset: 0,
    background:
        "rgba(0,0,0,0.45)",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    zIndex: 1000
};

const modalBox = {
    width: "500px",
    background: "#FFF",
    padding: "25px",
    borderRadius: "16px"
};

const inputStyle = {
    width: "100%",
    marginTop: "10px",
    padding: "10px",
    border: "1px solid #D1D5DB",
    borderRadius: "8px",
    boxSizing: "border-box"
};

const cancelButtonStyle = {
    padding: "10px 16px",
    border: "1px solid #D1D5DB",
    background: "#FFF",
    borderRadius: "8px",
    cursor: "pointer"
};

const saveButtonStyle = {
    padding: "10px 16px",
    border: "none",
    background: "#4F46E5",
    color: "#FFF",
    borderRadius: "8px",
    cursor: "pointer"
};