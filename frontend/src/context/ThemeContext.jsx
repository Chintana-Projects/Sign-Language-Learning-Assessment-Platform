import { createContext, useContext, useEffect, useState } from "react";

const ThemeContext = createContext();

export function ThemeProvider({ children }) {

    const [theme, setTheme] = useState(
        localStorage.getItem("theme") || "light"
    );

    useEffect(() => {

        document.body.className = theme;

        localStorage.setItem("theme", theme);

    }, [theme]);

    function toggleTheme() {

        setTheme(prev =>
            prev === "light" ? "dark" : "light"
        );

    }

    return (

        <ThemeContext.Provider
            value={{
                theme,
                toggleTheme
            }}
        >

            {children}

        </ThemeContext.Provider>

    );

}

export function useTheme() {

    return useContext(ThemeContext);

}