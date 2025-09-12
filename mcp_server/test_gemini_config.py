#!/usr/bin/env python3
"""
Test script to verify Gemini configuration in Graphiti MCP Server
"""

import os
import sys
from pathlib import Path

# Add the mcp_server directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from graphiti_mcp_server import GraphitiLLMConfig, GraphitiEmbedderConfig

def test_gemini_configuration():
    """Test Gemini configuration detection and client creation."""
    
    print("Testing Gemini Configuration...")
    print("-" * 50)
    
    # Test 1: Default configuration (should use Gemini)
    print("Test 1: Default configuration")
    
    # Clear environment variables to test defaults
    old_google_key = os.environ.get('GOOGLE_API_KEY')
    old_openai_key = os.environ.get('OPENAI_API_KEY')
    
    os.environ['GOOGLE_API_KEY'] = 'test_key'
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    
    try:
        llm_config = GraphitiLLMConfig.from_env()
        print(f"  Provider: {llm_config.provider}")
        print(f"  Model: {llm_config.model}")
        print(f"  Small Model: {llm_config.small_model}")
        
        embedder_config = GraphitiEmbedderConfig.from_env()
        print(f"  Embedder Provider: {embedder_config.provider}")
        print(f"  Embedder Model: {embedder_config.model}")
        
        # Test client creation (this will fail without a real API key, but should not crash)
        try:
            llm_client = llm_config.create_client()
            print("  ✓ LLM client creation successful")
        except ValueError as e:
            if "GOOGLE_API_KEY" in str(e):
                print("  ✓ LLM client creation properly validates API key")
            else:
                print(f"  ✗ Unexpected error: {e}")
        
        try:
            embedder_client = embedder_config.create_client()
            print("  ✓ Embedder client creation successful")
        except Exception as e:
            print(f"  ✗ Embedder client error: {e}")
            
    finally:
        # Restore original environment
        if old_google_key:
            os.environ['GOOGLE_API_KEY'] = old_google_key
        elif 'GOOGLE_API_KEY' in os.environ:
            del os.environ['GOOGLE_API_KEY']
            
        if old_openai_key:
            os.environ['OPENAI_API_KEY'] = old_openai_key
    
    print("\n✓ Configuration test completed!")

if __name__ == "__main__":
    test_gemini_configuration()
