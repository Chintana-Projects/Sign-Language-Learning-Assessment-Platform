import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({
    children,
    allowedRole
}) {

    const {
        isAuthenticated,
        user
    } = useAuth();

    console.log("PROTECTED ROUTE");
    console.log("isAuthenticated =", isAuthenticated);
    console.log("user =", user);
    console.log("allowedRole =", allowedRole);

    if (!isAuthenticated) {
        console.log("REDIRECTING TO LOGIN");
        return <Navigate to="/" replace />;
    }

    if (
        allowedRole &&
        user?.role !== allowedRole
    ) {
        console.log(
            "ROLE MISMATCH:",
            user?.role,
            allowedRole
        );

        if (user?.role === "learner") {
            return <Navigate to="/dashboard" replace />;
        }

        if (user?.role === "instructor") {
            return <Navigate to="/instructor/dashboard" replace />;
        }

        if (user?.role === "administrator") {
            return <Navigate to="/admin/dashboard" replace />;
        }

        return <Navigate to="/" replace />;
    }

    return children;
}