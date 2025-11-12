import React from "react";
import ChatAgentePeliculas from "./components/ChatAgentePeliculas"; 
import "./App.css"; 

function App() {
  return (
    <div className="app-wrapper">
      <h1 className="app-title">AI Agent Peliculist</h1>
      <ChatAgentePeliculas />
    </div>
  );
}

export default App;
