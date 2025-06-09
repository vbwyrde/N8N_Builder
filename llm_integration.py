import aiohttp
import json
import logging
import re
import asyncio
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMConfig:
    def __init__(self, endpoint: str, api_key: Optional[str] = None, model: str = "mimo-vl-7b",
                 temperature: float = 0.7, max_tokens: int = 2000, timeout: int = 30,
                 headers: Dict[str, str] = None, is_local: bool = True):
        self.endpoint = endpoint
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.headers = headers or {}
        self.is_local = is_local

class LLMClient:
    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig(
            endpoint="http://localhost:1234/v1/chat/completions",
            model="mimo-vl-7b",
            is_local=True
        )
        self.session = None
        logger.info(f"LLM Config: endpoint={self.config.endpoint}, is_local={self.config.is_local}, model={self.config.model}")

    async def _ensure_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    def _create_prompt(self, description: str) -> str:
        return f"""You are an expert N8N workflow generator. Create a valid N8N workflow JSON based on this description: {description}

CRITICAL INSTRUCTIONS:
1. Return ONLY the JSON workflow, no explanations, no thinking process, no markdown
2. Do not include any text before or after the JSON
3. Do not include any code blocks or backticks
4. The response must be a single valid JSON object
5. Do not include any comments or notes
6. Do not include any markdown formatting
7. Do not include any thinking process or analysis
8. Do not include any usage instructions or notes
9. Do not include any key features or setup instructions
10. The response must start with {{ and end with }}
11. Do not include any <think> tags or thinking process
12. Do not include any example usage or setup instructions
13. Do not include any best practices or notes
14. Do not include any explanations or comments
15. Do not include any markdown code blocks
16. Do not include any thinking process or analysis
17. Do not include any usage instructions or notes
18. Do not include any key features or setup instructions
19. Do not include any example usage or setup instructions
20. Do not include any best practices or notes
21. Do not include any thinking process or analysis
22. Do not include any usage instructions or notes
23. Do not include any key features or setup instructions
24. Do not include any example usage or setup instructions
25. Do not include any best practices or notes

Example of correct response format:
{{
    "nodes": [
        {{
            "parameters": {{}},
            "name": "Start",
            "type": "n8n-nodes-base.start",
            "typeVersion": 1,
            "position": [0, 0]
        }}
    ],
    "connections": {{}}
}}"""

    def _extract_json(self, content: str) -> Dict[str, Any]:
        """Extract JSON from the LLM response by finding all JSON blocks and using the first valid one."""
        # First try direct JSON parsing in case the response is clean
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            pass

        # Find all potential JSON blocks in the content
        json_blocks = []
        
        # Look for JSON in code blocks first
        code_blocks = re.findall(r'```(?:json)?\s*(\{[\s\S]*?\})\s*```', content)
        json_blocks.extend(code_blocks)
        
        # Look for any JSON object in the content, handling nested objects
        # This regex looks for the outermost { and } pair
        json_objects = []
        stack = []
        start = -1
        for i, char in enumerate(content):
            if char == '{':
                if not stack:  # This is the start of a new object
                    start = i
                stack.append(char)
            elif char == '}':
                if stack:
                    stack.pop()
                    if not stack and start != -1:  # We found a complete object
                        json_objects.append(content[start:i+1])
                        start = -1
        
        json_blocks.extend(json_objects)
        
        # Try each block until we find valid JSON
        for block in json_blocks:
            try:
                # Clean up the block
                cleaned = block.strip()
                
                # Find the first { and last } in the cleaned string
                start = cleaned.find('{')
                end = cleaned.rfind('}') + 1
                if start >= 0 and end > start:
                    cleaned = cleaned[start:end]
                
                # Try to parse the cleaned JSON
                try:
                    parsed = json.loads(cleaned)
                    # Verify this is a complete workflow with correct structure
                    if not isinstance(parsed, dict):
                        continue
                    if 'nodes' not in parsed or 'connections' not in parsed:
                        continue
                    
                    # Validate node types and structure
                    valid_nodes = True
                    for node in parsed['nodes']:
                        if not all(k in node for k in ['parameters', 'name', 'type', 'typeVersion', 'position']):
                            valid_nodes = False
                            break
                        # Ensure correct node types and parameters
                        if node['type'] in ['n8n-community-folder-monitor', 'n8n-nodes-base.watch-folder', 'n8n-nodes-base.watch-files', 'n8n-nodes-base.watchFiles']:
                            node['type'] = 'n8n-community.file-system'
                            # Convert parameters to expected format
                            if 'path' in node['parameters']:
                                node['parameters']['watchDirectory'] = node['parameters'].pop('path')
                            elif 'watchPath' in node['parameters']:
                                node['parameters']['watchDirectory'] = node['parameters'].pop('watchPath')
                            if 'filter' in node['parameters']:
                                node['parameters']['fileExtensions'] = [ext.strip('*.') for ext in node['parameters'].pop('filter').split(',')]
                            elif 'fileTypes' in node['parameters']:
                                node['parameters']['fileExtensions'] = node['parameters'].pop('fileTypes')
                            node['parameters']['triggerOnNewFiles'] = True
                            # Remove unnecessary parameters
                            for param in ['watch', 'recursive', 'interval', 'triggerOnNewFile']:
                                node['parameters'].pop(param, None)
                        elif node['type'] in ['n8n-nodes-base.email', 'n8n-nodes-base.sendEmail']:
                            # Ensure email parameters are correct
                            if 'recipient' in node['parameters']:
                                node['parameters']['emailAddress'] = node['parameters'].pop('recipient')
                            elif 'emailTo' in node['parameters']:
                                node['parameters']['emailAddress'] = node['parameters'].pop('emailTo')
                            if 'message' in node['parameters']:
                                node['parameters']['body'] = node['parameters'].pop('message')
                            elif 'htmlBody' in node['parameters']:
                                node['parameters']['body'] = node['parameters'].pop('htmlBody')
                            # Remove unnecessary parameters
                            for param in ['smtpServer', 'port', 'authenticationType', 'username', 'password']:
                                node['parameters'].pop(param, None)
                    
                    if not valid_nodes:
                        continue
                    
                    # Ensure proper connections
                    if 'connections' not in parsed or not parsed['connections']:
                        # Create default connections if none exist
                        parsed['connections'] = {'main': []}
                        node_names = [node['name'] for node in parsed['nodes']]
                        for i in range(len(node_names) - 1):
                            parsed['connections']['main'].append([
                                {
                                    'node': node_names[i],
                                    'type': 'outputData',
                                    'index': -1
                                },
                                {
                                    'node': node_names[i + 1],
                                    'type': 'inputData',
                                    'index': 0
                                }
                            ])
                    elif isinstance(parsed['connections'], dict):
                        # Convert to expected format if needed
                        if 'main' not in parsed['connections']:
                            new_connections = {'main': []}
                            for node_name, connections in parsed['connections'].items():
                                for conn in connections:
                                    if isinstance(conn, dict) and 'from' in conn and 'to' in conn:
                                        new_conn = [
                                            {
                                                'node': node_name,
                                                'type': 'outputData',
                                                'index': -1
                                            },
                                            {
                                                'node': conn['to'].split('.')[0],
                                                'type': 'inputData',
                                                'index': 0
                                            }
                                        ]
                                        new_connections['main'].append(new_conn)
                            parsed['connections'] = new_connections
                        else:
                            # Fix connection node names to match actual node names
                            for conn_list in parsed['connections']['main']:
                                for conn in conn_list:
                                    if conn['node'] == 'Folder Monitor':
                                        conn['node'] = next((node['name'] for node in parsed['nodes'] if node['type'] == 'n8n-community.file-system'), conn['node'])
                                    elif conn['node'] == 'Trigger':
                                        conn['node'] = next((node['name'] for node in parsed['nodes'] if node['type'] == 'n8n-nodes-base.email'), conn['node'])
                    
                    return parsed
                except json.JSONDecodeError:
                    # If that fails, try to fix common JSON issues
                    cleaned = re.sub(r',\s*}', '}', cleaned)  # Remove trailing commas
                    cleaned = re.sub(r',\s*]', ']', cleaned)  # Remove trailing commas in arrays
                    cleaned = re.sub(r'}\s*{', '},{', cleaned)  # Fix missing commas between objects
                    cleaned = re.sub(r'}\s*]', '}]', cleaned)  # Fix missing commas before array end
                    cleaned = re.sub(r']\s*}', ']}', cleaned)  # Fix missing commas after array end
                    cleaned = re.sub(r'"\s*:\s*"', '":"', cleaned)  # Fix missing spaces in key-value pairs
                    cleaned = re.sub(r'"\s*,\s*"', '","', cleaned)  # Fix missing spaces in arrays
                    parsed = json.loads(cleaned)
                    
                    # Apply the same validation and fixes as above
                    if not isinstance(parsed, dict):
                        continue
                    if 'nodes' not in parsed or 'connections' not in parsed:
                        continue
                    
                    # Validate node types and structure
                    valid_nodes = True
                    for node in parsed['nodes']:
                        if not all(k in node for k in ['parameters', 'name', 'type', 'typeVersion', 'position']):
                            valid_nodes = False
                            break
                        # Ensure correct node types and parameters
                        if node['type'] in ['n8n-community-folder-monitor', 'n8n-nodes-base.watch-folder', 'n8n-nodes-base.watch-files', 'n8n-nodes-base.watchFiles']:
                            node['type'] = 'n8n-community.file-system'
                            # Convert parameters to expected format
                            if 'path' in node['parameters']:
                                node['parameters']['watchDirectory'] = node['parameters'].pop('path')
                            elif 'watchPath' in node['parameters']:
                                node['parameters']['watchDirectory'] = node['parameters'].pop('watchPath')
                            if 'filter' in node['parameters']:
                                node['parameters']['fileExtensions'] = [ext.strip('*.') for ext in node['parameters'].pop('filter').split(',')]
                            elif 'fileTypes' in node['parameters']:
                                node['parameters']['fileExtensions'] = node['parameters'].pop('fileTypes')
                            node['parameters']['triggerOnNewFiles'] = True
                            # Remove unnecessary parameters
                            for param in ['watch', 'recursive', 'interval', 'triggerOnNewFile']:
                                node['parameters'].pop(param, None)
                        elif node['type'] in ['n8n-nodes-base.email', 'n8n-nodes-base.sendEmail']:
                            # Ensure email parameters are correct
                            if 'recipient' in node['parameters']:
                                node['parameters']['emailAddress'] = node['parameters'].pop('recipient')
                            elif 'emailTo' in node['parameters']:
                                node['parameters']['emailAddress'] = node['parameters'].pop('emailTo')
                            if 'message' in node['parameters']:
                                node['parameters']['body'] = node['parameters'].pop('message')
                            elif 'htmlBody' in node['parameters']:
                                node['parameters']['body'] = node['parameters'].pop('htmlBody')
                            # Remove unnecessary parameters
                            for param in ['smtpServer', 'port', 'authenticationType', 'username', 'password']:
                                node['parameters'].pop(param, None)
                    
                    if not valid_nodes:
                        continue
                    
                    # Ensure proper connections
                    if 'connections' not in parsed or not parsed['connections']:
                        # Create default connections if none exist
                        parsed['connections'] = {'main': []}
                        node_names = [node['name'] for node in parsed['nodes']]
                        for i in range(len(node_names) - 1):
                            parsed['connections']['main'].append([
                                {
                                    'node': node_names[i],
                                    'type': 'outputData',
                                    'index': -1
                                },
                                {
                                    'node': node_names[i + 1],
                                    'type': 'inputData',
                                    'index': 0
                                }
                            ])
                    elif isinstance(parsed['connections'], dict):
                        # Convert to expected format if needed
                        if 'main' not in parsed['connections']:
                            new_connections = {'main': []}
                            for node_name, connections in parsed['connections'].items():
                                for conn in connections:
                                    if isinstance(conn, dict) and 'from' in conn and 'to' in conn:
                                        new_conn = [
                                            {
                                                'node': node_name,
                                                'type': 'outputData',
                                                'index': -1
                                            },
                                            {
                                                'node': conn['to'].split('.')[0],
                                                'type': 'inputData',
                                                'index': 0
                                            }
                                        ]
                                        new_connections['main'].append(new_conn)
                            parsed['connections'] = new_connections
                        else:
                            # Fix connection node names to match actual node names
                            for conn_list in parsed['connections']['main']:
                                for conn in conn_list:
                                    if conn['node'] == 'Folder Monitor':
                                        conn['node'] = next((node['name'] for node in parsed['nodes'] if node['type'] == 'n8n-community.file-system'), conn['node'])
                                    elif conn['node'] == 'Trigger':
                                        conn['node'] = next((node['name'] for node in parsed['nodes'] if node['type'] == 'n8n-nodes-base.email'), conn['node'])
                    
                    return parsed
            except json.JSONDecodeError:
                continue

        raise ValueError("No valid workflow JSON found in response")

    async def _call_llm(self, prompt: str, max_retries: int = 3) -> Dict[str, Any]:
        """Call the LLM API with retries and proper error handling."""
        retry_count = 0
        last_error = None
        
        while retry_count < max_retries:
            try:
                await self._ensure_session()
                logger.info(f"Calling LLM API with is_local={self.config.is_local} (attempt {retry_count + 1}/{max_retries})")
                
                payload = {
                    "model": self.config.model,
                    "messages": [
                        {"role": "system", "content": "You are an expert N8N workflow generator. Return ONLY valid JSON, no other text. No thinking process, no explanations, no markdown, no code blocks, no usage instructions, no best practices, no notes. The response must be a single valid JSON object starting with { and ending with }. Do not include any thinking process or analysis. Do not include any <think> tags or thinking process. Do not include any example usage or setup instructions. Do not include any best practices or notes. Do not include any explanations or comments. Do not include any markdown code blocks. Do not include any thinking process or analysis. Do not include any usage instructions or notes. Do not include any key features or setup instructions. Do not include any example usage or setup instructions. Do not include any best practices or notes."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": self.config.temperature,
                    "max_tokens": self.config.max_tokens
                }

                async with self.session.post(
                    self.config.endpoint,
                    json=payload,
                    headers=self.config.headers,
                    timeout=self.config.timeout
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"LLM API error: {response.status} - {error_text}")
                    
                    result = await response.json()
                    content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                    
                    # Try to extract and parse JSON
                    try:
                        workflow = self._extract_json(content)
                        return workflow
                    except Exception as e:
                        logger.error(f"Failed to parse LLM response as JSON: {e}")
                        logger.error(f"Raw response content: {content}")
                        raise ValueError("LLM response was not valid JSON")
                    
            except asyncio.TimeoutError as e:
                last_error = e
                retry_count += 1
                if retry_count < max_retries:
                    logger.warning(f"Timeout on attempt {retry_count}, retrying...")
                    await asyncio.sleep(1)  # Wait 1 second before retrying
                continue
            except Exception as e:
                logger.error(f"Error calling LLM API: {e}", exc_info=True)
                raise
        
        # If we get here, all retries failed
        error_message = f"Failed to generate workflow after {max_retries} attempts. Last error: {str(last_error)}"
        logger.error(error_message)
        raise ValueError(error_message)

    async def generate_workflow(self, description: str) -> Dict[str, Any]:
        """Generate an N8N workflow from a description."""
        try:
            prompt = self._create_prompt(description)
            workflow = await self._call_llm(prompt)
            return workflow
        except Exception as e:
            logger.error(f"Error generating workflow: {str(e)}")
            # Return a basic error workflow
            return {
                "nodes": [
                    {
                        "parameters": {},
                        "name": "Error",
                        "type": "n8n-nodes-base.start",
                        "typeVersion": 1,
                        "position": [0, 0]
                    }
                ],
                "connections": {},
                "error": str(e)
            } 