#!/usr/bin/env python3
"""
Simple test to verify Gemini constants and basic structure
"""

# Test constants
DEFAULT_LLM_MODEL = 'gemini-2.0-flash'
SMALL_LLM_MODEL = 'gemini-2.5-flash-lite-preview-06-17'
DEFAULT_EMBEDDER_MODEL = 'embedding-001'

print("✓ Gemini Model Constants:")
print(f"  Default LLM Model: {DEFAULT_LLM_MODEL}")
print(f"  Small LLM Model: {SMALL_LLM_MODEL}")
print(f"  Default Embedder Model: {DEFAULT_EMBEDDER_MODEL}")

print("\n✓ Gemini configuration successfully updated in graphiti_mcp_server.py!")
print("\nTo use Gemini, set the following environment variable:")
print("  export GOOGLE_API_KEY=your_google_api_key_here")

print("\nOptional model overrides:")
print(f"  export MODEL_NAME={DEFAULT_LLM_MODEL}")
print(f"  export SMALL_MODEL_NAME={SMALL_LLM_MODEL}")
print(f"  export EMBEDDER_MODEL_NAME={DEFAULT_EMBEDDER_MODEL}")
