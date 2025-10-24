import React, { useEffect } from "react";
import { useAuthStore } from "./stores/authStore";
import { LoginForm } from "./components/LoginForm";
import { UploadForm } from "./components/UploadForm";
import "./App.css";

function App() {
  const screen = useAuthStore((state) => state.screen);
  const token = useAuthStore((state) => state.token);
  const getProject = useAuthStore((state) => state.getProject);

  useEffect(() => {
    if (token) {
      getProject().catch(console.error);
    }
  }, [token]);

  return (
    <div className="app">
      {screen === "login" ? (
        <LoginForm onLoginSuccess={() => {}} />
      ) : (
        <UploadForm />
      )}
    </div>
  );
}

export default App;
