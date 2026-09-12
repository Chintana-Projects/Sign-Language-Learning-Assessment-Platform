import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import "../styles/ProfilePage.css";

export default function ProfilePage() {

    const navigate = useNavigate();

    const { user, logout, setUser } = useAuth();

    const photoStorageKey =
        `profile_photo_${user?.id}`;

    const [name, setName] = useState(
        user?.full_name || ""
    );

    const [photo, setPhoto] = useState(
        localStorage.getItem(
            photoStorageKey
        ) || null
    );

    /* =====================================
       PHOTO UPLOAD
    ===================================== */

    const handlePhotoChange = (e) => {

        const file = e.target.files[0];

        if (!file) return;

        const reader = new FileReader();

        reader.onloadend = () => {

            setPhoto(
                reader.result
            );

            localStorage.setItem(
                photoStorageKey,
                reader.result
            );

        };

        reader.readAsDataURL(file);

    };

    /* =====================================
       LOGOUT
    ===================================== */

    const handleLogout = () => {

        logout();

        navigate("/");

    };

    /* =====================================
       SAVE CHANGES
    ===================================== */

    const handleSave = () => {

        const updatedUser = {

            ...user,

            full_name: name,

            profile_photo: photo

        };

        setUser(
            updatedUser
        );

        localStorage.setItem(

            "signsync_user",

            JSON.stringify(
                updatedUser
            )

        );

        alert(
            "Profile updated successfully!"
        );

    };

    /* =====================================
       RESET PROGRESS
    ===================================== */

    const handleReset = () => {

        const confirmReset = window.confirm(

            "Are you sure you want to reset all progress?"

        );

        if (!confirmReset) return;

        localStorage.removeItem(
            photoStorageKey
        );

        setPhoto(
            null
        );

        alert(
            "Progress reset feature will be connected to backend later."
        );

    };

    /* =====================================
       UI
    ===================================== */

    return (

        <div className="profile-page">

            <div className="profile-card">

                <h1 className="profile-title">
                    Profile
                </h1>

                {/* PROFILE PHOTO */}

                {photo ? (

                    <img
                        src={photo}
                        alt="Profile"
                        className="profile-image"
                    />

                ) : (

                    <div className="profile-avatar">

                        {name
                            ?.split(" ")
                            ?.map(
                                word => word[0]
                            )
                            ?.join("")
                            ?.substring(0, 2)
                            ?.toUpperCase()}

                    </div>

                )}

                {/* FILE INPUT */}

                <input
                    type="file"
                    accept="image/*"
                    id="profile-photo"
                    hidden
                    onChange={
                        handlePhotoChange
                    }
                />

                {/* FORM */}

                <div className="profile-form">

                    <label>
                        Name
                    </label>

                    <input
                        value={name}
                        onChange={(e) =>
                            setName(
                                e.target.value
                            )
                        }
                    />

                    <label>
                        Role
                    </label>

                    <input
                        value="Learner"
                        disabled
                    />

                </div>

                {/* ACTION BUTTONS */}

                <div className="profile-actions">

                    <label
                        htmlFor="profile-photo"
                        className="profile-btn upload-btn"
                    >
                        Upload Photo
                    </label>

                    <button
                        className="profile-btn save-btn"
                        onClick={
                            handleSave
                        }
                    >
                        Save Changes
                    </button>

                    <button
                        className="profile-btn reset-btn"
                        onClick={
                            handleReset
                        }
                    >
                        Reset Progress
                    </button>

                </div>

                {/* LOGOUT */}

                <button
                    className="logout-btn"
                    onClick={
                        handleLogout
                    }
                >
                    Logout
                </button>

            </div>

        </div>

    );

}