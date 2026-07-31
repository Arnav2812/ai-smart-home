import React from "react";

export default function DeviceGrid({ devices }) {
  const getDeviceIcon = (type) => {
    switch (type) {
      case "light": return "💡";
      case "music": return "🎵";
      case "thermostat": return "❄️";
      default: return "🔌";
    }
  };

  return (
    <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(240px, 1fr))", gap: "16px", marginBottom: "24px" }}>
      {devices.map((device) => (
        <div
          key={device.id}
          style={{
            background: "#1e1e2e",
            border: "1px solid #313244",
            borderRadius: "12px",
            padding: "16px",
            color: "#cdd6f4"
          }}
        >
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
            <span style={{ fontSize: "24px" }}>{getDeviceIcon(device.type)}</span>
            <span style={{ fontSize: "11px", textTransform: "uppercase", background: "#313244", padding: "4px 8px", borderRadius: "6px", color: "#a6adc8" }}>
              {device.location}
            </span>
          </div>
          <h4 style={{ margin: "0 0 8px 0", fontSize: "16px" }}>{device.name}</h4>
          
          <div style={{ fontSize: "13px", color: "#bac2de", marginTop: "8px", background: "#181825", padding: "8px", borderRadius: "6px" }}>
            {Object.entries(device.state).map(([key, val]) => (
              <div key={key} style={{ display: "flex", justifyContent: "space-between", textTransform: "capitalize" }}>
                <span>{key}:</span>
                <strong style={{ color: "#a6e3a1" }}>{String(val)}</strong>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}