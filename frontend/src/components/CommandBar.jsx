import React, { useState } from "react";

export default function CommandBar({ onSendCommand, loading }) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    onSendCommand(prompt);
    setPrompt("");
  };

  return (
    <div style={{ background: "#1e1e2e", padding: "20px", borderRadius: "12px", marginBottom: "24px" }}>
      <h3 style={{ margin: "0 0 10px 0", color: "#cdd6f4" }}>🎙️ Natural Language Control Terminal</h3>
      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "10px" }}>
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g., Set studio lights to 30% and play Drake"
          disabled={loading}
          style={{
            flex: 1,
            padding: "12px 16px",
            borderRadius: "8px",
            border: "1px solid #45475a",
            background: "#181825",
            color: "#cdd6f4",
            fontSize: "15px",
            outline: "none"
          }}
        />
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: "12px 24px",
            borderRadius: "8px",
            border: "none",
            background: loading ? "#585b70" : "#89b4fa",
            color: "#11111b",
            fontWeight: "bold",
            cursor: loading ? "not-allowed" : "pointer",
            fontSize: "15px"
          }}
        >
          {loading ? "Processing..." : "Dispatch"}
        </button>
      </form>
    </div>
  );
}