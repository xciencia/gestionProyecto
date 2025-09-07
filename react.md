## FrontEnd React

- React.js: La librería principal.
- Material-UI (MUI): Para los componentes visuales.
- React Router DOM: Para la navegación.
- Context API: Para la gestión de estado simple (para la autenticación, y quizás para los datos de la lista de proyectos, tareas). Para una aplicación más grande, Redux sería una opción, pero Context es más rápido de implementar para un ejemplo y suele ser suficiente.
- Axios: Para realizar peticiones HTTP a tu API de Django.

```
npx create-react-app gestion-proyectos-frontend
cd gestion-proyectos-frontend
```

### Instala las dependencias necesarias:

```
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material react-router-dom axios
```


#### AuthContext para manejar el estado de autenticación (usuario logueado, tokens JWT).

1. src/index.js (punto de entrada)

```
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import { BrowserRouter } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <AuthProvider>
        <App />
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
```

2. src/context/AuthContext.js (Contexto de Autenticación)

```
import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import axios from 'axios';
import { jwtDecode } from 'jwt-decode'; // Importa jwtDecode desde el nuevo paquete

// Instalar con: npm install jwt-decode
// O si es create-react-app más reciente: npm install @types/jwt-decode
// Asegúrate de que estás importando correctamente, podría ser `import jwt_decode from 'jwt-decode';`
// o `import { jwtDecode } from 'jwt-decode';` dependiendo de la versión del paquete.
// Para `jwt-decode` v3.1.2 en adelante, es `import { jwtDecode } from 'jwt-decode';`

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [authTokens, setAuthTokens] = useState(() =>
        localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null
    );
    const [user, setUser] = useState(() =>
        localStorage.getItem('authTokens') ? jwtDecode(JSON.parse(localStorage.getItem('authTokens')).access) : null
    );
    const [loading, setLoading] = useState(true);

    const API_BASE_URL = 'http://127.0.0.1:8000/api/'; // Tu URL base de la API de Django

    const loginUser = async (username, password) => {
        try {
            const response = await axios.post(`${API_BASE_URL}token/`, {
                username,
                password,
            });

            if (response.status === 200) {
                setAuthTokens(response.data);
                setUser(jwtDecode(response.data.access));
                localStorage.setItem('authTokens', JSON.stringify(response.data));
                return true;
            }
        } catch (error) {
            console.error('Login failed:', error);
            // Puedes manejar errores específicos aquí (ej. credenciales inválidas)
            return false;
        }
    };

    const logoutUser = useCallback(() => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
    }, []);

    const updateToken = useCallback(async () => {
        if (!authTokens?.refresh) {
            setLoading(false);
            return;
        }

        try {
            const response = await axios.post(`${API_BASE_URL}token/refresh/`, {
                refresh: authTokens.refresh,
            });

            if (response.status === 200) {
                setAuthTokens(response.data);
                setUser(jwtDecode(response.data.access));
                localStorage.setItem('authTokens', JSON.stringify(response.data));
            } else {
                logoutUser();
            }
        } catch (error) {
            console.error('Failed to refresh token:', error);
            logoutUser();
        } finally {
            setLoading(false);
        }
    }, [authTokens, logoutUser]);

    useEffect(() => {
        const fiveMinutes = 1000 * 60 * 5; // 5 minutos para refrescar el token
        const interval = setInterval(() => {
            if (authTokens) {
                updateToken();
            }
        }, fiveMinutes);

        // Llamar updateToken una vez al inicio para verificar token existente
        if (loading) {
            updateToken();
        }

        return () => clearInterval(interval);
    }, [authTokens, loading, updateToken]);


    const contextData = {
        user,
        authTokens,
        loginUser,
        logoutUser,
        API_BASE_URL
    };

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? <p>Cargando...</p> : children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
```