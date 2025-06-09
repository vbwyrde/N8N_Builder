import asyncio
import uvicorn
import os
import sys
import signal
import psutil
import logging
from typing import List
from main import app
from llm_integration import LLMClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kill_processes_on_ports(ports: List[int]) -> None:
    """Kill any processes running on the specified ports."""
    for port in ports:
        for proc in psutil.process_iter(['pid', 'name', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        logger.info(f"Killing process {proc.pid} ({proc.name()}) using port {port}")
                        if sys.platform == 'win32':
                            os.kill(proc.pid, signal.SIGTERM)
                        else:
                            proc.terminate()
                        proc.wait(timeout=3)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                pass

async def cleanup():
    """Cleanup resources before shutdown."""
    # Close the LLM client
    await app.state.llm_client.close()

async def main():
    # Kill any existing processes on our ports
    kill_processes_on_ports([8002, 8080])
    
    # Store the LLM client in the app state
    app.state.llm_client = LLMClient()
    
    # Register cleanup on shutdown
    @app.on_event("shutdown")
    async def shutdown_event():
        await cleanup()
    
    # Start the FastAPI server
    config = uvicorn.Config(
        "main:app",
        host="127.0.0.1",
        port=8002,
        log_level="info",
        reload=True
    )
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
    except Exception as e:
        logger.error(f"Error running server: {e}")
        sys.exit(1) 