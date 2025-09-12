#!/usr/bin/env python3
"""
Test script para verificar se o MCP server está funcionando corretamente
e usando os modelos do VS Code.
"""

import asyncio
import json
import aiohttp
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MCPServerTester:
    def __init__(self, base_url: str = "http://localhost:8122"):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def test_health(self) -> bool:
        """Test if the server is responding"""
        try:
            async with self.session.get(f"{self.base_url}/sse") as response:
                if response.status == 200:
                    logger.info("✅ Server is responding")
                    return True
                else:
                    logger.error(f"❌ Server returned status {response.status}")
                    return False
        except Exception as e:
            logger.error(f"❌ Failed to connect to server: {e}")
            return False

    async def test_mcp_tools(self) -> Dict[str, Any]:
        """Test available MCP tools"""
        try:
            # MCP tools list request
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/list"
            }
            
            async with self.session.post(
                f"{self.base_url}/messages",
                json=mcp_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("✅ MCP tools request successful")
                    return result
                else:
                    logger.error(f"❌ MCP tools request failed with status {response.status}")
                    text = await response.text()
                    logger.error(f"Response: {text}")
                    return {}
        except Exception as e:
            logger.error(f"❌ Failed to test MCP tools: {e}")
            return {}

    async def test_add_episode(self) -> Dict[str, Any]:
        """Test adding an episode to verify VS Code models are working"""
        try:
            # Test add_episode tool
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": "add_episode",
                    "arguments": {
                        "name": "VS Code Test Episode",
                        "content": "Testing if VS Code models are working correctly in Docker. This should test both LLM and embedder integration."
                    }
                }
            }
            
            logger.info("🧪 Testing add_episode with VS Code models...")
            async with self.session.post(
                f"{self.base_url}/messages",
                json=mcp_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("✅ add_episode request successful")
                    return result
                else:
                    logger.error(f"❌ add_episode request failed with status {response.status}")
                    text = await response.text()
                    logger.error(f"Response: {text}")
                    return {}
        except Exception as e:
            logger.error(f"❌ Failed to test add_episode: {e}")
            return {}

    async def test_search(self) -> Dict[str, Any]:
        """Test search functionality to verify embedder is working"""
        try:
            # Test search tool
            mcp_request = {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "search",
                    "arguments": {
                        "query": "VS Code models test",
                        "limit": 5
                    }
                }
            }
            
            logger.info("🔍 Testing search with VS Code embedder...")
            async with self.session.post(
                f"{self.base_url}/messages",
                json=mcp_request,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info("✅ Search request successful")
                    return result
                else:
                    logger.error(f"❌ Search request failed with status {response.status}")
                    text = await response.text()
                    logger.error(f"Response: {text}")
                    return {}
        except Exception as e:
            logger.error(f"❌ Failed to test search: {e}")
            return {}

async def main():
    logger.info("🚀 Starting MCP Server Tests...")
    
    async with MCPServerTester() as tester:
        # Test 1: Health check
        logger.info("\n📡 Test 1: Server Health Check")
        health_ok = await tester.test_health()
        
        if not health_ok:
            logger.error("❌ Server is not responding. Aborting tests.")
            return
        
        # Test 2: MCP Tools
        logger.info("\n🛠️  Test 2: MCP Tools List")
        tools_result = await tester.test_mcp_tools()
        if tools_result:
            if 'result' in tools_result and 'tools' in tools_result['result']:
                tools = tools_result['result']['tools']
                logger.info(f"✅ Found {len(tools)} MCP tools:")
                for tool in tools[:5]:  # Show first 5 tools
                    logger.info(f"   - {tool.get('name', 'unknown')}: {tool.get('description', 'no description')[:60]}...")
            else:
                logger.info(f"Tools response: {json.dumps(tools_result, indent=2)}")
        
        # Test 3: Add Episode (tests LLM)
        logger.info("\n📝 Test 3: Add Episode (LLM Test)")
        episode_result = await tester.test_add_episode()
        if episode_result:
            if 'result' in episode_result:
                logger.info("✅ Episode added successfully - VS Code LLM is working!")
                logger.info(f"Result: {json.dumps(episode_result['result'], indent=2)}")
            else:
                logger.info(f"Episode response: {json.dumps(episode_result, indent=2)}")
        
        # Test 4: Search (tests Embedder)
        logger.info("\n🔍 Test 4: Search (Embedder Test)")
        search_result = await tester.test_search()
        if search_result:
            if 'result' in search_result:
                logger.info("✅ Search completed successfully - VS Code Embedder is working!")
                logger.info(f"Result: {json.dumps(search_result['result'], indent=2)}")
            else:
                logger.info(f"Search response: {json.dumps(search_result, indent=2)}")

    logger.info("\n🎉 MCP Server Tests Completed!")

if __name__ == "__main__":
    asyncio.run(main())