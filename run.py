import asyncio
import uvicorn
import os
import sys
import signal
import psutil
import logging
from typing import List
from n8n_builder.app import app
from llm_integration import LLMClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def kill_processes_on_ports(ports: List[int]) -> None:
    """Kill any processes running on the specified ports."""
    for port in ports:
        try:
            for proc in psutil.process_iter(['pid', 'name', 'connections']):
                try:
                    # Skip system processes (PID 0, 4, etc.)
                    if proc.info['pid'] in [0, 4]:
                        continue
                    
                    # Check if process has connections
                    connections = proc.connections() if proc.info['connections'] is not None else []
                    
                    for conn in connections:
                        if hasattr(conn, 'laddr') and conn.laddr.port == port:
                            logger.info(f"Killing process {proc.info['pid']} ({proc.info['name']}) using port {port}")
                            try:
                                if sys.platform == 'win32':
                                    proc.terminate()
                                else:
                                    proc.terminate()
                                
                                # Wait for process to terminate
                                proc.wait(timeout=3)
                                logger.info(f"Successfully terminated process {proc.info['pid']}")
                            except (psutil.TimeoutExpired, psutil.AccessDenied) as e:
                                logger.warning(f"Could not terminate process {proc.info['pid']}: {e}")
                            except Exception as e:
                                logger.warning(f"Error terminating process {proc.info['pid']}: {e}")
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    # Process no longer exists or we don't have permission
                    continue
                except Exception as e:
                    logger.warning(f"Error checking process connections: {e}")
                    continue
                    
        except Exception as e:
            logger.warning(f"Error scanning processes for port {port}: {e}")
            continue

async def cleanup():
    """Cleanup resources before shutdown."""
    # Close the LLM client
    if hasattr(app.state, 'llm_client'):
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
        "n8n_builder.app:app",
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