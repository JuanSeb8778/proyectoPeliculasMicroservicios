import React, { useState, useEffect, useRef } from "react";
import "./ChatAgentePeliculas.css"; 

const ChatAgentePeliculas = () => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState("");
    const logContainerRef = useRef(null);

    useEffect(() => {
        logContainerRef.current?.scrollTo(0, logContainerRef.current.scrollHeight);
    }, [messages]);

    const sendMessage = async () => {
        if (!inputValue.trim()) return;

        const newMessage = { sender: "user", text: inputValue };
        setMessages((prev) => [...prev, newMessage]);
        setInputValue("");

        try {
            const res = await fetch("http://127.0.0.1:8000/query", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query: inputValue }),
            });
            const data = await res.json();

            let botText = data.response || data.error || "Error procesando la consulta.";

            if (botText.startsWith("TOOL[add_movie]")) {
                const match = botText.match(/title='([^']+)'/);
                const title = match ? match[1] : "la película";
                botText = `✅ Se ha agregado correctamente la película *${title}*.`;
            }

            const botMessage = { sender: "bot", text: botText };
            setMessages((prev) => [...prev, botMessage]);
        } catch (err) {
            setMessages((prev) => [
                ...prev,
                { sender: "bot", text: "Error de conexión con el servidor." },
            ]);
        }
    };

    return (
        <div className="chat-container">
            <div className="chat-log" ref={logContainerRef}>
                {messages.map((msg, i) => (
                    <div key={i} className={`msg ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
            </div>

            <div className="chat-input">
                <input
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                    placeholder="Escribe algo... Ej: Agrega Avengers: End Game"
                />
                <button onClick={sendMessage}>Enviar</button>
            </div>
        </div>
    );
};

export default ChatAgentePeliculas;
