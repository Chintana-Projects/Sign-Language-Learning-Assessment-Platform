import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import "../styles/Login.css";

function Register() {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    role: "learner",
  });

  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleRegister = async (e) => {
    e.preventDefault();

    setError("");

    if (
      !formData.fullName ||
      !formData.email ||
      !formData.password ||
      !formData.confirmPassword
    ) {
      setError("Please fill all fields.");
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    const requestBody = {
      full_name: formData.fullName,
      email: formData.email,
      password: formData.password,
      role: formData.role,
    };

    console.log("Sending Registration Data:");
    console.log(JSON.stringify(requestBody, null, 2));

    try {
      setLoading(true);

      const response = await fetch(
        "http://127.0.0.1:8000/auth/register",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestBody),
        }
      );

      let data = {};

      try {
        data = await response.json();
      } catch {
        data = {};
      }

      if (!response.ok) {
        throw new Error(
          data.detail || "Registration Failed"
        );
      }

      alert("Registration Successful!");

      navigate("/login");

    } catch (err) {
      console.error(err);
      setError(
        err.message || "Registration Failed"
      );
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

      {/* Registration Card */}
      <div className="login-wrapper register-wrapper">

        <div className="login-card register-card">

          {/* Header */}
          <div className="login-card-header register-header">

            <div className="register-logo">
              🤟
            </div>

            <h2>
              Create your SignSync Account
            </h2>

            <p>
              Join SignSync and start learning sign language.
            </p>

          </div>


          {/* Role Selector */}
          <div className="role-selector">

            <button
              type="button"
              className={
                formData.role === "learner"
                  ? "role-btn active"
                  : "role-btn"
              }
              onClick={() =>
                setFormData((prev) => ({
                  ...prev,
                  role: "learner",
                }))
              }
            >
              <span>🎓</span>
              <span>Learner</span>
            </button>


            <button
              type="button"
              className={
                formData.role === "instructor"
                  ? "role-btn active"
                  : "role-btn"
              }
              onClick={() =>
                setFormData((prev) => ({
                  ...prev,
                  role: "instructor",
                }))
              }
            >
              <span>👨‍🏫</span>
              <span>Instructor</span>
            </button>


            <button
              type="button"
              className={
                formData.role === "accessibility_trainer"
                  ? "role-btn active"
                  : "role-btn"
              }
              onClick={() =>
                setFormData((prev) => ({
                  ...prev,
                  role: "accessibility_trainer",
                }))
              }
            >
              <span>♿</span>
              <span>Accessibility Trainer</span>
            </button>


            <button
              type="button"
              className={
                formData.role === "administrator"
                  ? "role-btn active"
                  : "role-btn"
              }
              onClick={() =>
                setFormData((prev) => ({
                  ...prev,
                  role: "administrator",
                }))
              }
            >
              <span>⚙️</span>
              <span>Administrator</span>
            </button>

          </div>


          {/* Registration Form */}
          <form onSubmit={handleRegister}>

            {/* Full Name */}
            <div className="input-group">

              <label>
                Full Name
              </label>

              <input
                type="text"
                name="fullName"
                placeholder="Enter your full name"
                value={formData.fullName}
                onChange={handleChange}
                required
              />

            </div>


            {/* Email */}
            <div className="input-group">

              <label>
                Email Address
              </label>

              <input
                type="email"
                name="email"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
                required
              />

            </div>


            {/* Password Row */}
            <div className="input-row">

              <div className="input-group">

                <label>
                  Password
                </label>

                <input
                  type="password"
                  name="password"
                  placeholder="Create password"
                  value={formData.password}
                  onChange={handleChange}
                  required
                />

              </div>


              <div className="input-group">

                <label>
                  Confirm Password
                </label>

                <input
                  type="password"
                  name="confirmPassword"
                  placeholder="Confirm password"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />

              </div>

            </div>


            {/* Error */}
            {error && (
              <div className="register-error">
                ⚠️ {error}
              </div>
            )}


            {/* Register Button */}
            <button
              type="submit"
              className="register-button"
              disabled={loading}
            >
              {loading ? (
                <>
                  <span className="spinner"></span>
                  Creating Account...
                </>
              ) : (
                <>
                  Create Account
                </>
              )}
            </button>

          </form>


          {/* Login */}
          <div className="register-login">

            Already have an account?

            <Link to="/login">
              Login
            </Link>

          </div>

        </div>

      </div>

    </div>
  );
}

export default Register;