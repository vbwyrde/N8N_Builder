"""
Workflow Iteration Agent - Handles workflow modification and iteration requests.
"""

import json
import logging
from typing import Dict, Any
from datetime import datetime

from .base_agent import BaseAgent, AgentConfig, AgentResult

logger = logging.getLogger(__name__)

class WorkflowIterationAgent(BaseAgent):
    """Agent responsible for iterating and modifying existing N8N workflows."""
    
    def __init__(self, config: AgentConfig):
        super().__init__(config)
        self.supported_operations = [
            "modify_workflow",
            "iterate_workflow", 
            "analyze_workflow",
            "suggest_improvements"
        ]
    
    async def process(self, request: Dict[str, Any]) -> AgentResult:
        """Process a workflow iteration request."""
        try:
            operation = request.get("operation")
            if operation not in self.supported_operations:
                return AgentResult(
                    success=False,
                    error=f"Unsupported operation: {operation}. Supported: {self.supported_operations}"
                )
            
            if operation == "modify_workflow":
                return await self._modify_workflow(request)
            elif operation == "iterate_workflow":
                return await self._iterate_workflow(request)
            elif operation == "analyze_workflow":
                return await self._analyze_workflow(request)
            elif operation == "suggest_improvements":
                return await self._suggest_improvements(request)
            
        except Exception as e:
            self.logger.error(f"Error processing workflow iteration: {str(e)}")
            return AgentResult(
                success=False,
                error=str(e),
                metadata={"operation": request.get("operation")}
            )
    
    async def _modify_workflow(self, request: Dict[str, Any]) -> AgentResult:
        """Modify an existing workflow based on the request."""
        try:
            existing_workflow = request.get("existing_workflow")
            modification_request = request.get("modification_description")
            
            if not existing_workflow or not modification_request:
                return AgentResult(
                    success=False,
                    error="Missing required fields: existing_workflow, modification_description"
                )
            
            # Parse existing workflow
            if isinstance(existing_workflow, str):
                workflow_data = json.loads(existing_workflow)
            else:
                workflow_data = existing_workflow
            
            # Analyze current workflow
            analysis = self._analyze_workflow_structure(workflow_data)
            
            # Generate modification plan
            modification_plan = self._create_modification_plan(
                workflow_data, 
                analysis, 
                modification_request
            )
            
            # Apply modifications
            modified_workflow = self._apply_modifications(workflow_data, modification_plan)
            
            return AgentResult(
                success=True,
                data={
                    "modified_workflow": modified_workflow,
                    "modification_plan": modification_plan,
                    "original_analysis": analysis,
                    "workflow_id": request.get("workflow_id")
                },
                metadata={
                    "operation": "modify_workflow",
                    "nodes_before": len(workflow_data.get("nodes", [])),
                    "nodes_after": len(modified_workflow.get("nodes", [])),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                error=f"Failed to modify workflow: {str(e)}"
            )
    
    async def _iterate_workflow(self, request: Dict[str, Any]) -> AgentResult:
        """Iterate on a workflow based on testing feedback."""
        try:
            existing_workflow = request.get("existing_workflow")
            feedback = request.get("testing_feedback")
            additional_requirements = request.get("additional_requirements", "")
            
            # Combine feedback and requirements
            combined_request = f"""
            Testing Feedback: {feedback}
            
            Additional Requirements: {additional_requirements}
            
            Please address the feedback and incorporate the additional requirements.
            """
            
            # Use modify workflow with the combined request
            modification_request = {
                **request,
                "operation": "modify_workflow",
                "modification_description": combined_request.strip()
            }
            
            result = await self._modify_workflow(modification_request)
            
            if result.success:
                result.metadata["operation"] = "iterate_workflow"
                result.metadata["iteration_type"] = "feedback_based"
            
            return result
            
        except Exception as e:
            return AgentResult(
                success=False,
                error=f"Failed to iterate workflow: {str(e)}"
            )
    
    async def _analyze_workflow(self, request: Dict[str, Any]) -> AgentResult:
        """Analyze a workflow structure and provide insights."""
        try:
            workflow = request.get("workflow")
            if isinstance(workflow, str):
                workflow_data = json.loads(workflow)
            else:
                workflow_data = workflow
            
            analysis = self._analyze_workflow_structure(workflow_data)
            
            return AgentResult(
                success=True,
                data={"analysis": analysis},
                metadata={
                    "operation": "analyze_workflow",
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                error=f"Failed to analyze workflow: {str(e)}"
            )
    
    async def _suggest_improvements(self, request: Dict[str, Any]) -> AgentResult:
        """Suggest improvements for a workflow."""
        try:
            workflow = request.get("workflow")
            if isinstance(workflow, str):
                workflow_data = json.loads(workflow)
            else:
                workflow_data = workflow
            
            analysis = self._analyze_workflow_structure(workflow_data)
            suggestions = self._generate_improvement_suggestions(workflow_data, analysis)
            
            return AgentResult(
                success=True,
                data={
                    "suggestions": suggestions,
                    "analysis": analysis
                },
                metadata={
                    "operation": "suggest_improvements",
                    "suggestion_count": len(suggestions),
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        except Exception as e:
            return AgentResult(
                success=False,
                error=f"Failed to generate suggestions: {str(e)}"
            )
    
    def _analyze_workflow_structure(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze workflow structure and components."""
        analysis = {
            "node_count": len(workflow.get("nodes", [])),
            "node_types": [],
            "triggers": [],
            "actions": [],
            "connections": workflow.get("connections", {}),
            "connection_count": 0,
            "potential_issues": [],
            "complexity_score": 0
        }
        
        # Analyze nodes
        for node in workflow.get("nodes", []):
            node_type = node.get("type", "unknown")
            analysis["node_types"].append(node_type)
            
            # Categorize nodes
            if any(trigger_keyword in node_type.lower() 
                   for trigger_keyword in ["trigger", "webhook", "schedule"]):
                analysis["triggers"].append({
                    "id": node.get("id"),
                    "name": node.get("name"),
                    "type": node_type
                })
            else:
                analysis["actions"].append({
                    "id": node.get("id"),
                    "name": node.get("name"),
                    "type": node_type
                })
        
        # Count connections
        for source_node, connections in analysis["connections"].items():
            for connection_type, targets in connections.items():
                for target_list in targets:
                    analysis["connection_count"] += len(target_list)
        
        # Calculate complexity score
        analysis["complexity_score"] = (
            analysis["node_count"] * 1 +
            analysis["connection_count"] * 0.5 +
            len(analysis["triggers"]) * 2
        )
        
        # Identify potential issues
        if len(analysis["triggers"]) == 0:
            analysis["potential_issues"].append("No trigger nodes found - workflow may not start")
        
        if analysis["connection_count"] == 0 and analysis["node_count"] > 1:
            analysis["potential_issues"].append("Nodes are not connected")
        
        if analysis["node_count"] > 20:
            analysis["potential_issues"].append("High complexity - consider breaking into smaller workflows")
        
        return analysis
    
    def _create_modification_plan(self, workflow: Dict[str, Any], 
                                analysis: Dict[str, Any], 
                                request: str) -> Dict[str, Any]:
        """Create a plan for modifying the workflow."""
        # This is a simplified version - in a real implementation,
        # you'd use the LLM to generate a more sophisticated plan
        plan = {
            "modifications": [],
            "reasoning": f"Addressing request: {request}",
            "estimated_complexity": "medium"
        }
        
        # Simple heuristics for common requests
        request_lower = request.lower()
        
        if "email" in request_lower and not any("email" in node_type.lower() 
                                               for node_type in analysis["node_types"]):
            plan["modifications"].append({
                "action": "add_node",
                "node_type": "n8n-nodes-base.emailSend",
                "reasoning": "Adding email functionality as requested"
            })
        
        if "database" in request_lower and not any("postgres" in node_type.lower() or "mysql" in node_type.lower()
                                                  for node_type in analysis["node_types"]):
            plan["modifications"].append({
                "action": "add_node", 
                "node_type": "n8n-nodes-base.postgres",
                "reasoning": "Adding database connectivity as requested"
            })
        
        if "schedule" in request_lower and len(analysis["triggers"]) == 0:
            plan["modifications"].append({
                "action": "add_node",
                "node_type": "n8n-nodes-base.scheduleTrigger", 
                "reasoning": "Adding schedule trigger to automate workflow"
            })
        
        return plan
    
    def _apply_modifications(self, workflow: Dict[str, Any], 
                           plan: Dict[str, Any]) -> Dict[str, Any]:
        """Apply the modification plan to the workflow."""
        # Deep copy the workflow
        modified_workflow = json.loads(json.dumps(workflow))
        
        for modification in plan["modifications"]:
            action = modification["action"]
            
            if action == "add_node":
                new_node = {
                    "id": str(len(modified_workflow["nodes"]) + 1),
                    "name": modification.get("name", f"New {modification['node_type'].split('.')[-1]}"),
                    "type": modification["node_type"],
                    "parameters": modification.get("parameters", {}),
                    "position": [0, 0]
                }
                modified_workflow["nodes"].append(new_node)
            
            # Add more modification types as needed
        
        return modified_workflow
    
    def _generate_improvement_suggestions(self, workflow: Dict[str, Any], 
                                        analysis: Dict[str, Any]) -> list:
        """Generate improvement suggestions based on workflow analysis."""
        suggestions = []
        
        # Performance suggestions
        if analysis["node_count"] > 15:
            suggestions.append({
                "type": "performance",
                "priority": "medium",
                "suggestion": "Consider breaking this workflow into smaller, more focused workflows",
                "reason": f"Current workflow has {analysis['node_count']} nodes, which may impact performance"
            })
        
        # Error handling suggestions
        if analysis["connection_count"] > 0:
            suggestions.append({
                "type": "reliability",
                "priority": "high", 
                "suggestion": "Add error handling nodes to catch and handle failures",
                "reason": "Error handling improves workflow reliability"
            })
        
        # Security suggestions
        suggestions.append({
            "type": "security",
            "priority": "medium",
            "suggestion": "Review node parameters for sensitive data and use environment variables",
            "reason": "Protects sensitive information like API keys and passwords"
        })
        
        # Monitoring suggestions
        if analysis["complexity_score"] > 10:
            suggestions.append({
                "type": "monitoring",
                "priority": "low",
                "suggestion": "Add logging/notification nodes to track workflow execution",
                "reason": "Complex workflows benefit from execution monitoring"
            })
        
        return suggestions 