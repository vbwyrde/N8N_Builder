import json
import uuid
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime

class MessageType(Enum):
    """Types of messages that can be exchanged between agents."""
    WORKFLOW_REQUEST = "workflow_request"
    WORKFLOW_RESPONSE = "workflow_response"
    ERROR = "error"
    STATUS_UPDATE = "status_update"
    DATA_TRANSFER = "data_transfer"
    COMMAND = "command"
    EVENT = "event"

class MessagePriority(Enum):
    """Priority levels for message processing."""
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class AgentMessage:
    """Base class for all agent communication messages."""
    
    def __init__(
        self,
        message_type: MessageType,
        sender: str,
        recipient: str,
        content: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        correlation_id: Optional[str] = None,
        parent_message_id: Optional[str] = None
    ):
        self.message_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat()
        self.message_type = message_type
        self.sender = sender
        self.recipient = recipient
        self.content = content
        self.priority = priority
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.parent_message_id = parent_message_id
        self.metadata: Dict[str, Any] = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary format."""
        return {
            "message_id": self.message_id,
            "timestamp": self.timestamp,
            "message_type": self.message_type.value,
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "priority": self.priority.value,
            "correlation_id": self.correlation_id,
            "parent_message_id": self.parent_message_id,
            "metadata": self.metadata
        }
    
    def to_json(self) -> str:
        """Convert message to JSON string."""
        return json.dumps(self.to_dict())
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMessage':
        """Create message from dictionary."""
        message = cls(
            message_type=MessageType(data["message_type"]),
            sender=data["sender"],
            recipient=data["recipient"],
            content=data["content"],
            priority=MessagePriority(data["priority"]),
            correlation_id=data["correlation_id"],
            parent_message_id=data.get("parent_message_id")
        )
        message.message_id = data["message_id"]
        message.timestamp = data["timestamp"]
        message.metadata = data.get("metadata", {})
        return message
    
    @classmethod
    def from_json(cls, json_str: str) -> 'AgentMessage':
        """Create message from JSON string."""
        return cls.from_dict(json.loads(json_str))

class WorkflowRequest(AgentMessage):
    """Message for requesting workflow processing."""
    
    def __init__(
        self,
        sender: str,
        recipient: str,
        workflow_data: Dict[str, Any],
        priority: MessagePriority = MessagePriority.NORMAL,
        correlation_id: Optional[str] = None,
        parent_message_id: Optional[str] = None
    ):
        super().__init__(
            message_type=MessageType.WORKFLOW_REQUEST,
            sender=sender,
            recipient=recipient,
            content={"workflow_data": workflow_data},
            priority=priority,
            correlation_id=correlation_id,
            parent_message_id=parent_message_id
        )

class WorkflowResponse(AgentMessage):
    """Message for workflow processing results."""
    
    def __init__(
        self,
        sender: str,
        recipient: str,
        workflow_result: Dict[str, Any],
        success: bool,
        error: Optional[str] = None,
        correlation_id: Optional[str] = None,
        parent_message_id: Optional[str] = None
    ):
        super().__init__(
            message_type=MessageType.WORKFLOW_RESPONSE,
            sender=sender,
            recipient=recipient,
            content={
                "workflow_result": workflow_result,
                "success": success,
                "error": error
            },
            priority=MessagePriority.NORMAL,
            correlation_id=correlation_id,
            parent_message_id=parent_message_id
        )

class StatusUpdate(AgentMessage):
    """Message for agent status updates."""
    
    def __init__(
        self,
        sender: str,
        recipient: str,
        status: str,
        details: Dict[str, Any],
        correlation_id: Optional[str] = None,
        parent_message_id: Optional[str] = None
    ):
        super().__init__(
            message_type=MessageType.STATUS_UPDATE,
            sender=sender,
            recipient=recipient,
            content={
                "status": status,
                "details": details
            },
            priority=MessagePriority.LOW,
            correlation_id=correlation_id,
            parent_message_id=parent_message_id
        )

class ErrorMessage(AgentMessage):
    """Message for error reporting."""
    
    def __init__(
        self,
        sender: str,
        recipient: str,
        error: str,
        error_type: str,
        details: Dict[str, Any],
        correlation_id: Optional[str] = None,
        parent_message_id: Optional[str] = None
    ):
        super().__init__(
            message_type=MessageType.ERROR,
            sender=sender,
            recipient=recipient,
            content={
                "error": error,
                "error_type": error_type,
                "details": details
            },
            priority=MessagePriority.HIGH,
            correlation_id=correlation_id,
            parent_message_id=parent_message_id
        ) 