""" LLM Chat Payload Dataclass """
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

@dataclass
class ChatPayload:
    model: str
    temperature: float
    top_k: int
    top_p: float
    repeat_penalty: float
    seed: int
    messages: List[Dict[str, str]] = field(default_factory=list)
    images: Optional[List[str]] = None
    stream: Optional[bool] = False

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "repeat_penalty": self.repeat_penalty,
            "seed": self.seed,
            "messages": self.messages,
        }
        if self.images:
            payload["images"] = self.images
        if self.stream is not None:
            payload["stream"] = self.stream
        return payload
