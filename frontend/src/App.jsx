import React, { useEffect, useState } from "react";
import { fetchDevices, sendCommand } from "./api";
import CommandBar from "./components/CommandBar";
import DeviceGrid from "./components/DeviceGrid";

export default function App() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [pipelineLogs, setPipelineLogs] = useState(null);

  useEffect(() => {
    loadDevices();
  }, []);

  const loadDevices = async () => {
    try {
      const data = await fetchDevices();
      setDevices(data);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSendCommand = async (prompt) => {
    setLoading(true);
    try {
      const res = await sendCommand(prompt);
      setPipelineLogs(res);
      setDevices(res.updated_devices);
    } catch (err) {
      alert("Error sending command to LLM engine.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "#11111b", color: "#cdd6f4", fontFamily: "sans-serif", padding: "40px 20px" }}>
      <div style={{ maxWidth: "900px", margin: "0 auto" }}>
        
        {/* Header */}
        <div style={{ marginBottom: "30px", borderBottom: "1px solid #313244", pb: "10px" }}>
          <h1 style={{ margin: 0, color: "#89b4fa" }}>AI Smart Home Engine</h1>
          <p style={{ color: "#a6adc8", margin: "6px 0 0 0" }}>
            Decoupled LLM Intent Routing & Context Guardrail Dashboard
          </p>
        </div>

        {/* Command Input */}
        <CommandBar onSendCommand={handleSendCommand} loading={loading} />

        {/* Device State Grid */}
        <h3 style={{ color: "#cdd6f4", marginBottom: "12px" }}>🌐 Active Edge Devices</h3>
        <DeviceGrid devices={devices} />

        {/* LLM & Guardrail Pipeline Logs */}
        {pipelineLogs && (
          <div style={{ background: "#1e1e2e", border: "1px solid #313244", borderRadius: "12px", padding: "20px" }}>
            <h3 style={{ margin: "0 0 12px 0", color: "#f9e2af" }}>🔍 Pipeline Inspection Log</h3>
            
            <p style={{ fontSize: "14px", color: "#bac2de" }}>
              <strong>LLM Reasoning:</strong> {pipelineLogs.intent_analysis.reasoning}
            </p>

            <h4 style={{ color: "#cdd6f4", marginTop: "16px", marginBottom: "8px" }}>Guardrail Results:</h4>
            <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
              {pipelineLogs.execution_results.map((res, idx) => (
                <li
                  key={idx}
                  style={{
                    padding: "10px",
                    borderRadius: "6px",
                    marginBottom: "8px",
                    background: res.status === "executed" ? "rgba(166, 227, 161, 0.1)" : "rgba(243, 139, 168, 0.1)",
                    borderLeft: `4px solid ${res.status === "executed" ? "#a6e3a1" : "#f38ba8"}`
                  }}
                >
                  <strong style={{ color: res.status === "executed" ? "#a6e3a1" : "#f38ba8", textTransform: "uppercase" }}>
                    [{res.status}]
                  </strong>{" "}
                  {res.message}
                </li>
              ))}
            </ul>
          </div>
        )}

      </div>
    </div>
  );
}