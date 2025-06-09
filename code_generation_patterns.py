from typing import Dict, List
from dataclasses import dataclass

@dataclass
class WorkflowPattern:
    name: str
    description: str
    template: str
    common_use_cases: List[str]

class CodeGenerationPatterns:
    @staticmethod
    def _get_basic_code_gen_template() -> str:
        return '''{
            "name": "Code Generation Workflow",
            "nodes": [
                {
                    "parameters": {
                        "prompt": "={{ $json.prompt }}",
                        "model": "mimo-vl-7b"
                    },
                    "name": "Mimo VL 7B",
                    "type": "n8n-nodes-base.mimo",
                    "position": [250, 300],
                    "id": "1"
                },
                {
                    "parameters": {
                        "values": {
                            "string": [
                                {
                                    "name": "generated_code",
                                    "value": "={{ $json.response }}"
                                }
                            ]
                        }
                    },
                    "name": "Set",
                    "type": "n8n-nodes-base.set",
                    "position": [450, 300],
                    "id": "2"
                }
            ],
            "connections": {
                "1": {
                    "main": [
                        [
                            {
                                "node": "2",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            },
            "settings": {},
            "tags": [],
            "active": false
        }'''

    @staticmethod
    def _get_code_review_template() -> str:
        return '''{
            "name": "Code Review Workflow",
            "nodes": [
                {
                    "parameters": {
                        "prompt": "={{ $json.code }}"
                    },
                    "name": "Mimo VL 7B",
                    "type": "n8n-nodes-base.mimo",
                    "position": [250, 300],
                    "id": "1"
                },
                {
                    "parameters": {
                        "values": {
                            "string": [
                                {
                                    "name": "review_comments",
                                    "value": "={{ $json.response }}"
                                }
                            ]
                        }
                    },
                    "name": "Set",
                    "type": "n8n-nodes-base.set",
                    "position": [450, 300],
                    "id": "2"
                }
            ],
            "connections": {
                "1": {
                    "main": [
                        [
                            {
                                "node": "2",
                                "type": "main",
                                "index": 0
                            }
                        ]
                    ]
                }
            },
            "settings": {},
            "tags": [],
            "active": false
        }'''

    @property
    def patterns(self) -> Dict[str, WorkflowPattern]:
        return {
            "BasicCodeGen": WorkflowPattern(
                name="Basic Code Generation",
                description="Generates code based on natural language description",
                template=self._get_basic_code_gen_template(),
                common_use_cases=[
                    "Generate function from description",
                    "Create class structure",
                    "Implement interface"
                ]
            ),
            "CodeReview": WorkflowPattern(
                name="Code Review Generation",
                description="Generates code review workflow",
                template=self._get_code_review_template(),
                common_use_cases=[
                    "Review code changes",
                    "Generate review comments",
                    "Suggest improvements"
                ]
            )
        } 