#!/usr/bin/env python3
"""
Dynamic Multi-Model Orchestrator & Router Engine for UAO System
Automatically classifies incoming tasks and routes prompts to the optimal local LLM kernel:
  1. Llama-3.3-70B (Port 8090) -> System Architecture & Master Planning
  2. Qwen-2.5-Coder-32B (Port 8091) -> Python SDK, Android ADK & Network Code
  3. DeepSeek-R1-Distill-70B (Port 8092) -> Protocol Debugging & Math Reasoning
  4. Codestral-22B (Port 8093) -> Fast Subagent Background Execution
"""

import os
import sys
import json
import sqlite3
import re
import platform

# Model Routing Map Configuration
MODEL_ENDPOINTS = {
    "llama_3_3_70b": {
        "port": 8090,
        "endpoint": "http://localhost:8090/v1",
        "description": "Master Orchestrator, System Planning & Documentation"
    },
    "qwen_2_5_coder_32b": {
        "port": 8091,
        "endpoint": "http://localhost:8091/v1",
        "description": "Python SDK, Android ADK (Kotlin/Java), Network Sockets & API Schemas"
    },
    "deepseek_r1_70b": {
        "port": 8092,
        "endpoint": "http://localhost:8092/v1",
        "description": "Deep Reasoning, Complex Network Debugging & IPC Verification"
    },
    "codestral_22b": {
        "port": 8093,
        "endpoint": "http://localhost:8093/v1",
        "description": "Fast Subagent Execution, Unit Tests & Quick Refactoring"
    }
}

# Domain Intent Regex Patterns
PATTERNS = {
    "qwen_2_5_coder_32b": [
        re.compile(r"(?i)\b(sdk|adk|android|kotlin|java|gradle|ndk|pydantic|grpc|websocket|api contract|code gen)\b"),
        re.compile(r"(?i)\b(write code|implement function|class definition|type annotations)\b")
    ],
    "deepseek_r1_70b": [
        re.compile(r"(?i)\b(debug|race condition|deadlock|packet routing|stack trace|root cause|protocol verification)\b"),
        re.compile(r"(?i)\b(math proof|matrix inverse|quantum cirq|onemkl)\b")
    ],
    "codestral_22b": [
        re.compile(r"(?i)\b(unit test|lint fix|quick edit|refactor line|subagent task)\b")
    ]
}

def classify_prompt_intent(prompt_text):
    """Classifies prompt text and returns optimal target model and endpoint."""
    for model_key, regex_list in PATTERNS.items():
        for pattern in regex_list:
            if pattern.search(prompt_text):
                return model_key, MODEL_ENDPOINTS[model_key]
    
    # Default to Master Orchestrator Llama-3.3-70B
    return "llama_3_3_70b", MODEL_ENDPOINTS["llama_3_3_70b"]

def route_request(prompt_text):
    model_key, config = classify_prompt_intent(prompt_text)
    print(f"\n[+] PROMPT CLASSIFICATION RESULT:")
    print(f"  • Selected Model: {model_key.upper()}")
    print(f"  • Port Endpoint: {config['endpoint']}")
    print(f"  • Domain Target:  {config['description']}")
    return model_key, config

def main():
    print("=== DYNAMIC MULTI-MODEL ORCHESTRATOR & ROUTER ENGINE ===")
    test_prompts = [
        "Create a Python SDK client for our gRPC network protocol.",
        "Build an Android ADK app using Kotlin and native NDK bindings.",
        "Debug this asynchronous socket race condition and memory leak.",
        "Synthesize a high-level system architecture blueprint for multi-cloud DR."
    ]
    for prompt in test_prompts:
        print(f"\nPrompt: '{prompt}'")
        route_request(prompt)

if __name__ == "__main__":
    main()
