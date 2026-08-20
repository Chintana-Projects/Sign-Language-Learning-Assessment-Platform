import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import api from "../services/api";
import "../styles/Login.css";

export default function Login() {
    const navigate = useNavigate();
    const { login } = useAuth();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("learner");
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    const handleLogin = async (e) => {
        e.preventDefault();

        setError("");
        setLoading(true);

        try {
            const response = await api.post("/auth/login", {
                email: email,
                password: password,
                role: role,
            });

            const data = response.data;

            login(
                data.access_token,
                data.user
            );

            switch (data.user.role) {
                case "learner":
                    navigate("/dashboard");
                    break;

                case "instructor":
                    navigate("/instructor/dashboard");
                    break;

                case "administrator":
                    navigate("/admin/dashboard");
                    break;

                case "accessibility_trainer":
                    navigate("/trainer/dashboard");
                    break;

                default:
                    navigate("/");
            }

        } catch (error) {
            console.error("Login error:", error);

            if (error.response) {
                setError(
                    error.response.data?.detail ||
                    "Invalid email or password."
                );
            } else {
                setError(
                    "Unable to connect to the server."
                );
            }

        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">

            {/* Decorative background */}
            <div className="login-decoration decoration-one"></div>
            <div className="login-decoration decoration-two"></div>
            <div className="login-decoration decoration-three"></div>

            <div className="login-wrapper">

                {/* LEFT BRANDING SECTION */}
                <div className="login-brand-section">

                    <div className="brand-icon">
                        ✋
                    </div>

                    <h1>SignSync</h1>

                    <h2>
                        Learn. Practice. Communicate.
                    </h2>

                    <p>
                        An AI-powered sign language learning
                        platform designed to make communication
                        more accessible and engaging.
                    </p>

                    <div className="brand-features">

                        <div className="brand-feature">
                            <span>🤖</span>
                            <div>
                                <strong>AI Recognition</strong>
                                <small>
                                    Practice signs with intelligent
                                    gesture recognition.
                                </small>
                            </div>
                        </div>

                        <div className="brand-feature">
                            <span>📚</span>
                            <div>
                                <strong>Interactive Learning</strong>
                                <small>
                                    Build your sign language skills
                                    step by step.
                                </small>
                            </div>
                        </div>

                        <div className="brand-feature">
                            <span>📊</span>
                            <div>
                                <strong>Track Progress</strong>
                                <small>
                                    Monitor your accuracy and
                                    learning performance.
                                </small>
                            </div>
                        </div>

                    </div>

                </div>


                {/* LOGIN CARD */}
                <div className="login-card">

                    <div className="login-card-header">

                        <div className="mobile-brand-icon">
                            ✋
                        </div>

                        <h2>
                            Welcome back 👋
                        </h2>

                        <p>
                            Sign in to continue your SignSync journey.
                        </p>

                    </div>


                    <form onSubmit={handleLogin}>

                        {/* EMAIL */}
                        <div className="input-group">

                            <label htmlFor="email">
                                Email
                            </label>

                            <div className="input-wrapper">

                                <span className="input-icon">
                                    ✉️
                                </span>

                                <input
                                    id="email"
                                    type="email"
                                    placeholder="Enter your email"
                                    value={email}
                                    onChange={(e) =>
                                        setEmail(e.target.value)
                                    }
                                    required
                                />

                            </div>

                        </div>


                        {/* PASSWORD */}
                        <div className="input-group">

                            <label htmlFor="password">
                                Password
                            </label>

                            <div className="input-wrapper">

                                <span className="input-icon">
                                    🔒
                                </span>

                                <input
                                    id="password"
                                    type={
                                        showPassword
                                            ? "text"
                                            : "password"
                                    }
                                    placeholder="Enter your password"
                                    value={password}
                                    onChange={(e) =>
                                        setPassword(e.target.value)
                                    }
                                    required
                                />

                                <button
                                    type="button"
                                    className="password-toggle"
                                    onClick={() =>
                                        setShowPassword(
                                            !showPassword
                                        )
                                    }
                                >
                                    {showPassword
                                        ? "🙈"
                                        : "👁️"}
                                </button>

                            </div>

                        </div>


                        {/* ROLE */}
                        <div className="input-group">

                            <label htmlFor="role">
                                Login as
                            </label>

                            <div className="input-wrapper">

                                <span className="input-icon">
                                    👤
                                </span>

                                <select
                                    id="role"
                                    value={role}
                                    onChange={(e) =>
                                        setRole(e.target.value)
                                    }
                                >
                                    <option value="learner">
                                        Learner
                                    </option>

                                    <option value="instructor">
                                        Instructor
                                    </option>

                                    <option value="accessibility_trainer">
                                        Accessibility Trainer
                                    </option>

                                    <option value="administrator">
                                        Administrator
                                    </option>

                                </select>

                            </div>

                        </div>


                        {/* ERROR */}
                        {error && (
                            <div className="login-error">
                                <span>⚠️</span>
                                <p>{error}</p>
                            </div>
                        )}


                        {/* LOGIN BUTTON */}
                        <button
                            type="submit"
                            className="login-button"
                            disabled={loading}
                        >

                            {loading ? (
                                <>
                                    <span className="spinner"></span>
                                    Logging in...
                                </>
                            ) : (
                                <>
                                    Login
                                    <span>→</span>
                                </>
                            )}

                        </button>

                    </form>


                    {/* REGISTER */}
                    <div className="register-section">

                        <div className="divider">
                            <span></span>
                            <p>New to SignSync?</p>
                            <span></span>
                        </div>

                        <Link
                            to="/register"
                            className="create-account-link"
                        >
                            Create Account
                        </Link>

                    </div>

                </div>

            </div>

            <div className="login-footer">
                © 2026 SignSync · AI Powered Sign Language Learning
            </div>

        </div>
    );
}