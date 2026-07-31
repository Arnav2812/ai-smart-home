import os
import json
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class DeviceCommand(BaseModel):
    device_type: Literal["light", "music", "thermostat", "lock"] = Field(
        description="Target category of device"
    )
    target_location: str = Field(
        description="Target room name only (e.g., 'studio', 'living_room', 'all')"
    )
    action: Literal["turn_on", "turn_off", "set_brightness", "play_track", "pause", "set_temp"] = Field(
        description="The action to execute"
    )
    value: Optional[str] = Field(
        default=None, 
        description="Value parameter (e.g., '30%', 'Drake', '22C')"
    )

class IntentResponse(BaseModel):
    raw_prompt: str
    parsed_successfully: bool
    commands: List[DeviceCommand]
    reasoning: str = Field(description="Explanation of intent parsing")

class LLMService:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set in the .env file.")
        self.client = Groq(api_key=api_key)

    def parse_intent(self, user_prompt: str) -> IntentResponse:
        system_prompt = """
        You are an intelligent NLP parser for an enterprise IoT smart home network.
        Convert human spoken commands into a JSON array of device instructions.
        
        Rules:
        1. Extract target_location ONLY as the room name (e.g., use "studio", NOT "studio lights").
        2. If location is omitted in a continuous command (e.g. "play Drake"), inherit the location from the preceding command in the prompt or use "all".
        3. Format strictly as JSON:
        {
            "parsed_successfully": true,
            "reasoning": "Parsed studio light brightness and studio music track.",
            "commands": [
                {
                    "device_type": "light",
                    "target_location": "studio",
                    "action": "set_brightness",
                    "value": "30%"
                },
                {
                    "device_type": "music",
                    "target_location": "studio",
                    "action": "play_track",
                    "value": "Drake"
                }
            ]
        }
        """

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Parse this command: '{user_prompt}'"}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )

            raw_content = response.choices[0].message.content
            parsed_json = json.loads(raw_content)

            return IntentResponse(
                raw_prompt=user_prompt,
                parsed_successfully=parsed_json.get("parsed_successfully", True),
                commands=[DeviceCommand(**cmd) for cmd in parsed_json.get("commands", [])],
                reasoning=parsed_json.get("reasoning", "Successfully extracted intent.")
            )
        except Exception as e:
            return IntentResponse(
                raw_prompt=user_prompt,
                parsed_successfully=False,
                commands=[],
                reasoning=f"Parsing error: {str(e)}"
            )