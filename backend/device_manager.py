from typing import List, Dict, Any
from pydantic import BaseModel
from llm_service import DeviceCommand

class ExecutedCommandResult(BaseModel):
    command: DeviceCommand
    status: str  # "executed" or "rejected"
    message: str

class DeviceManager:
    def __init__(self):
        self.devices: Dict[str, Dict[str, Any]] = {
            "studio_light": {
                "id": "studio_light",
                "name": "Studio Lights",
                "type": "light",
                "location": "studio",
                "supported_actions": ["turn_on", "turn_off", "set_brightness"],
                "state": {"power": "on", "brightness": "100%"}
            },
            "studio_music": {
                "id": "studio_music",
                "name": "Studio Audio Monitors",
                "type": "music",
                "location": "studio",
                "supported_actions": ["play_track", "pause"],
                "state": {"status": "paused", "current_track": "None"}
            },
            "living_room_light": {
                "id": "living_room_light",
                "name": "Living Room Lights",
                "type": "light",
                "location": "living_room",
                "supported_actions": ["turn_on", "turn_off", "set_brightness"],
                "state": {"power": "off", "brightness": "100%"}
            },
            "living_room_thermostat": {
                "id": "living_room_thermostat",
                "name": "Main AC Thermostat",
                "type": "thermostat",
                "location": "living_room",
                "supported_actions": ["set_temp"],
                "state": {"temperature": "22C"}
            }
        }

    def get_all_devices(self) -> List[Dict[str, Any]]:
        return list(self.devices.values())

    def _normalize_location(self, loc: str) -> str:
        loc = loc.lower().strip()
        for term in [" lights", " light", " music", " room", " thermostat"]:
            loc = loc.replace(term, "")
        return loc

    def validate_and_execute(self, commands: List[DeviceCommand]) -> List[ExecutedCommandResult]:
        execution_results = []

        for cmd in commands:
            cmd_loc = self._normalize_location(cmd.target_location)

            # Match target location and device type
            target_devices = [
                dev for dev in self.devices.values()
                if (cmd_loc == "all" or dev["location"] == cmd_loc or cmd_loc in dev["id"])
                and dev["type"] == cmd.device_type
            ]

            if not target_devices:
                execution_results.append(ExecutedCommandResult(
                    command=cmd,
                    status="rejected",
                    message=f"Context Guardrail: No '{cmd.device_type}' device found in location '{cmd.target_location}'."
                ))
                continue

            for dev in target_devices:
                if cmd.action not in dev["supported_actions"]:
                    execution_results.append(ExecutedCommandResult(
                        command=cmd,
                        status="rejected",
                        message=f"Capability Guardrail: Device '{dev['name']}' does not support action '{cmd.action}'."
                    ))
                    continue

                # Execute state updates
                if cmd.action in ["turn_on", "turn_off"]:
                    dev["state"]["power"] = "on" if cmd.action == "turn_on" else "off"
                elif cmd.action == "set_brightness" and cmd.value:
                    dev["state"]["brightness"] = cmd.value
                    dev["state"]["power"] = "on"
                elif cmd.action == "play_track" and cmd.value:
                    dev["state"]["status"] = "playing"
                    dev["state"]["current_track"] = cmd.value
                elif cmd.action == "pause":
                    dev["state"]["status"] = "paused"
                elif cmd.action == "set_temp" and cmd.value:
                    dev["state"]["temperature"] = cmd.value

                execution_results.append(ExecutedCommandResult(
                    command=cmd,
                    status="executed",
                    message=f"Success: Executed '{cmd.action}' on '{dev['name']}'."
                ))

        return execution_results