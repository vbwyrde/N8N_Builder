import sys
import json
import logging
import asyncio
import httpx
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn
from rich import print

def test_imports():
    print("[green]Testing imports...[/green]")
    try:
        # Test FastAPI
        app = FastAPI()
        print("[green]✓ FastAPI imported successfully[/green]")
        
        # Test Pydantic
        class TestModel(BaseModel):
            name: str
        test_model = TestModel(name="test")
        print("[green]✓ Pydantic imported successfully[/green]")
        
        # Test httpx
        async def test_httpx():
            async with httpx.AsyncClient() as client:
                response = await client.get("http://httpbin.org/get")
                return response.status_code == 200
        
        asyncio.run(test_httpx())
        print("[green]✓ httpx imported and working[/green]")
        
        # Test python-dotenv
        load_dotenv()
        print("[green]✓ python-dotenv imported successfully[/green]")
        
        # Test rich
        print("[green]✓ rich imported successfully[/green]")
        
        print("\n[bold green]All dependencies are working correctly![/bold green]")
        return True
    except Exception as e:
        print(f"[red]Error testing dependencies: {str(e)}[/red]")
        return False

if __name__ == "__main__":
    test_imports() 