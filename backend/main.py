from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# OpenTelemetry Imports
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from llm_service import LLMService, IntentResponse
from device_manager import DeviceManager, ExecutedCommandResult

# --- OpenTelemetry Configuration ---
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer("ai-smart-home-engine")

app = FastAPI(
    title="AI Smart Home NLP Engine",
    description="Low-latency FastAPI NLP intent router with OpenTelemetry Tracing.",
    version="1.0.0"
)

# Instrument FastAPI to capture HTTP metrics automatically
FastAPIInstrumentor.instrument_app(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_service = LLMService()
device_manager = DeviceManager()

class ParseRequest(BaseModel):
    prompt: str

class PipelineResponse(BaseModel):
    intent_analysis: IntentResponse
    execution_results: List[ExecutedCommandResult]
    updated_devices: List[Dict[str, Any]]

@app.get("/")
def health_check():
    return {"status": "online", "system": "AI Smart Home NLP Engine"}

@app.get("/api/devices")
def get_devices():
    return device_manager.get_all_devices()

@app.post("/api/parse-command", response_model=PipelineResponse)
def parse_and_execute_command(request: ParseRequest):
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Command prompt cannot be empty.")
    
    # Span 1: Track LLM Intent Parsing Latency
    with tracer.start_as_current_span("llm_intent_parsing") as span:
        span.set_attribute("user.prompt", request.prompt)
        intent_res = llm_service.parse_intent(request.prompt)
        span.set_attribute("llm.parsed_successfully", intent_res.parsed_successfully)
        span.set_attribute("llm.command_count", len(intent_res.commands))

    # Span 2: Track Context Guardrail & Validation Latency
    execution_results = []
    if intent_res.parsed_successfully:
        with tracer.start_as_current_span("context_guardrail_validation") as span:
            execution_results = device_manager.validate_and_execute(intent_res.commands)
            span.set_attribute("guardrail.executed_count", len(execution_results))

    return PipelineResponse(
        intent_analysis=intent_res,
        execution_results=execution_results,
        updated_devices=device_manager.get_all_devices()
    )