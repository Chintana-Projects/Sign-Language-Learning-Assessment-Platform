
import {
    createContext,
    useContext,
    useEffect,
    useState
} from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {

    const [user, setUser] = useState(() => {

        const savedUser =
            localStorage.getItem("signsync_user");

        if (!savedUser) {
            return null;
        }

        try {
            return JSON.parse(savedUser);
        } catch (error) {

            console.error(
                "Unable to load saved user:",
                error
            );

            return null;
        }
    });


    const [accessToken, setAccessToken] = useState(() => {

        return localStorage.getItem(
            "signsync_access_token"
        );
    });


    // =====================================================
    // LOGIN
    // =====================================================

    const login = (token, userData) => {

        console.log(
            "AUTH LOGIN USER:",
            userData
        );

        setAccessToken(token);
        setUser(userData);

        localStorage.setItem(
            "signsync_access_token",
            token
        );

        localStorage.setItem(
            "signsync_user",
            JSON.stringify(userData)
        );
    };


    // =====================================================
    // LOGOUT
    // =====================================================

    const logout = () => {

        setUser(null);
        setAccessToken(null);

        localStorage.removeItem(
            "signsync_user"
        );

        localStorage.removeItem(
            "signsync_access_token"
        );
    };


    // =====================================================
    // AUTH STATE
    // =====================================================

    useEffect(() => {

        if (user) {

            localStorage.setItem(
                "signsync_user",
                JSON.stringify(user)
            );

        }

    }, [user]);


    return (
        <AuthContext.Provider
            value={{
                user,
                setUser,

                accessToken,

                login,
                logout,

                isAuthenticated:
                    !!user && !!accessToken
            }}
        >
            {children}
        </AuthContext.Provider>
    );
}


// =========================================================
// USE AUTH
// =========================================================

export function useAuth() {

    const context =
        useContext(AuthContext);

    if (!context) {

        throw new Error(
            "useAuth must be used inside AuthProvider"
        );

    }

    return context;
}

