"""AgentManager — CRUD for agent profiles stored on disk."""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from app.models.agent_profile import AgentProfile

log = logging.getLogger(__name__)


class AgentManager:
    def __init__(self, agents_dir: Path):
        self._dir = agents_dir
        self._dir.mkdir(parents=True, exist_ok=True)
        self._agents: Dict[str, AgentProfile] = {}
        self._load_all()
        if not self._agents:
            self._create_defaults()

    def _load_all(self):
        for path in self._dir.glob("*.json"):
            try:
                a = AgentProfile.load(path)
                self._agents[a.id] = a
            except Exception as e:
                log.warning("Could not load agent %s: %s", path.name, e)

    def _create_defaults(self):
        defaults = [
            AgentProfile(
                name="General Assistant",
                description="A helpful, general-purpose assistant.",
                system_prompt="You are a helpful, harmless, and honest assistant.",
                icon="🤖",
                execution_mode="executor",
                reasoning_mode="normal",
            ),
            AgentProfile(
                name="Code Reviewer",
                description="Reviews code for bugs, style, and security issues.",
                system_prompt=(
                    "You are an expert code reviewer. Analyze code for:\n"
                    "1. Bugs and logical errors\n2. Security vulnerabilities\n"
                    "3. Performance issues\n4. Style and readability\n"
                    "Provide specific, actionable feedback."
                ),
                icon="🔍",
                execution_mode="executor",
                reasoning_mode="thinking",
            ),
            AgentProfile(
                name="Research Planner",
                description="Breaks down complex research tasks into steps.",
                system_prompt=(
                    "You are a research coordinator. When given a topic:\n"
                    "1. Identify key questions to answer\n"
                    "2. Break down into subtasks\n"
                    "3. Suggest methodology\n"
                    "4. Synthesize information clearly."
                ),
                icon="📚",
                execution_mode="planner",
                reasoning_mode="plan",
            ),
        ]
        for agent in defaults:
            self._agents[agent.id] = agent
            agent.save(self._dir)

    def create(self, **kwargs) -> AgentProfile:
        a = AgentProfile(**kwargs)
        self._agents[a.id] = a
        a.save(self._dir)
        return a

    def get(self, agent_id: str) -> Optional[AgentProfile]:
        return self._agents.get(agent_id)

    def list_all(self) -> List[AgentProfile]:
        return sorted(self._agents.values(), key=lambda a: a.name)

    def update(self, agent: AgentProfile):
        self._agents[agent.id] = agent
        agent.save(self._dir)

    def delete(self, agent_id: str) -> bool:
        a = self._agents.pop(agent_id, None)
        if a:
            path = self._dir / f"{agent_id}.json"
            if path.exists():
                path.unlink()
            return True
        return False

    def duplicate(self, agent_id: str) -> Optional[AgentProfile]:
        import copy, uuid
        src = self._agents.get(agent_id)
        if not src:
            return None
        new_a = copy.deepcopy(src)
        new_a.id = str(uuid.uuid4())
        new_a.name = f"{src.name} (copy)"
        self._agents[new_a.id] = new_a
        new_a.save(self._dir)
        return new_a

    def import_from_file(self, path: Path) -> AgentProfile:
        import uuid
        a = AgentProfile.load(path)
        a.id = str(uuid.uuid4())
        self._agents[a.id] = a
        a.save(self._dir)
        return a

    def export_to_file(self, agent_id: str, path: Path) -> bool:
        a = self._agents.get(agent_id)
        if not a:
            return False
        try:
            import json
            with open(path, "w", encoding="utf-8") as f:
                json.dump(a.to_dict(), f, indent=2)
            return True
        except Exception as e:
            log.error("Agent export failed: %s", e)
            return False
