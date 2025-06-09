from typing import Dict
from .n8n_builder import WorkflowPattern

class CodeGenerationPatterns:
    patterns: Dict[str, WorkflowPattern] = {
        "file_trigger": WorkflowPattern(
            name="file_trigger",
            description="Trigger workflow when a file is created or modified",
            template="""
            {
                "nodes": [
                    {
                        "parameters": {
                            "path": "{{$node["File Trigger"].json["path"]}}",
                            "options": {
                                "watch": true
                            }
                        },
                        "name": "File Trigger",
                        "type": "n8n-nodes-base.files",
                        "typeVersion": 1,
                        "position": [250, 300]
                    }
                ]
            }
            """,
            common_use_cases=[
                "File monitoring",
                "Document processing",
                "Backup triggers"
            ]
        ),
        "email_notification": WorkflowPattern(
            name="email_notification",
            description="Send an email notification",
            template="""
            {
                "nodes": [
                    {
                        "parameters": {
                            "fromEmail": "{{$node["Email"].json["fromEmail"]}}",
                            "toEmail": "{{$node["Email"].json["toEmail"]}}",
                            "subject": "{{$node["Email"].json["subject"]}}",
                            "text": "{{$node["Email"].json["text"]}}"
                        },
                        "name": "Email",
                        "type": "n8n-nodes-base.emailSend",
                        "typeVersion": 1,
                        "position": [450, 300]
                    }
                ]
            }
            """,
            common_use_cases=[
                "Alert notifications",
                "Report distribution",
                "Status updates"
            ]
        )
    } 