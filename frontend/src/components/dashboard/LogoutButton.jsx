import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

export default function LogoutButton() {

    const navigate = useNavigate();
    const { logout } = useAuth();

    const handleLogout = () => {

        console.log("LOGOUT CLICKED");

        logout();

        navigate("/", { replace: true });

    };

    return (
        <button
            className="logout-button"
            onClick={handleLogout}
        >
            Logout
        </button>
    );
}