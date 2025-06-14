import sys
import requests
from dotenv import load_dotenv
import os
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel
import json

def test_imports():
    print("✅ All required packages imported successfully")
    
def test_dotenv():
    load_dotenv()
    print("✅ python-dotenv loaded successfully")
    
def test_requests():
    try:
        response = requests.get("https://httpbin.org/get")
        print(f"✅ Requests test successful - Status code: {response.status_code}")
    except Exception as e:
        print(f"❌ Requests test failed: {str(e)}")
        
def test_fastapi():
    app = FastAPI()
    
    class TestModel(BaseModel):
        name: str
        
    @app.get("/test")
    async def test_endpoint():
        return {"status": "ok"}
    
    print("✅ FastAPI and Pydantic initialized successfully")
    
def main():
    print("\n=== Testing Environment Setup ===\n")
    print(f"Python Version: {sys.version}")
    print(f"Python Path: {sys.executable}\n")
    
    try:
        test_imports()
        test_dotenv()
        test_requests()
        test_fastapi()
        print("\n✅ All tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        
if __name__ == "__main__":
    main() 