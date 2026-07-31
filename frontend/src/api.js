const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function fetchDevices() {
  const response = await fetch(`${API_BASE_URL}/devices`);
  if (!response.ok) throw new Error("Failed to fetch devices");
  return await response.json();
}

export async function sendCommand(prompt) {
  const response = await fetch(`${API_BASE_URL}/parse-command`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  if (!response.ok) throw new Error("Failed to send command");
  return await response.json();
}