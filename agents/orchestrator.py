from dataclasses import dataclass
from typing import Dict, Any, List

@dataclass
class AgentResult:
    name: str
    payload: Dict[str, Any]

class Orchestrator:
    def __init__(self, agents: List[object]):
        self.agents = agents

    def run(self, context: Dict[str, Any]) -> List[AgentResult]:
        results = []
        for agent in self.agents:
            try:
                output = agent.run(context)
                results.append(AgentResult(name=agent.name, payload=output))
                # Merge context with outputs so downstream agents can use it
                context.update(output or {})
            except Exception as e:
                results.append(AgentResult(name=agent.name, payload={"error": str(e)}))
        return results
