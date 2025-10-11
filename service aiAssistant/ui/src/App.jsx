import React from "react";
import ChatAgentePeliculas from "./components/ChatAgentePeliculas"; // 👈 Importa tu componente principal
import "./App.css"; // Opcional: si quieres estilos globales simples

function App() {
  return (
    <div className="app-wrapper">
      <h1 className="app-title">🎬 Chat Agente de Películas</h1>
      <ChatAgentePeliculas />
    </div>
  );
}

export default App;
