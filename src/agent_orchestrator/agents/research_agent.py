import os
import httpx
import asyncio
from typing import Any, Dict, Optional
from src.agent_orchestrator.api.models import AgentTask, AgentResult

class ResearchAgent:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.api_url = os.getenv("HUGGINGFACE_API_URL", "https://api-inference.huggingface.co/models/")
        self.model = os.getenv("RESEARCH_AGENT_MODEL", "google-bert/bert-base-uncased")
        self.max_retries = 3
        self.timeout = 20

    async def execute(self, task: AgentTask) -> AgentResult:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"inputs": task.query}
        url = f"{self.api_url}{self.model}"
        result = None
        error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(url, headers=headers, json=data)
                    response.raise_for_status()
                    result = response.json()
                    break
            except httpx.HTTPStatusError as e:
                error = f"HTTP {e.response.status_code}: {e.response.text}"
                if e.response.status_code == 429:
                    await asyncio.sleep(2 * attempt)  # Backoff for rate limit
                else:
                    break
            except Exception as e:
                error = str(e)
                await asyncio.sleep(1 * attempt)

        citations = self.extract_citations(result)
        score = self.get_confidence(result, citations)

        return AgentResult(
            agent_id=task.agent_id,
            success=bool(result),
            result={"output": result, "citations": citations, "score": score},
            error=error,
        )

    def extract_citations(self, result: Optional[Any]) -> list:
        # Custom citation/source extraction (adjust based on output schema)
        if not result:
            return []
        if isinstance(result, list) and 'sources' in result[0]:
            return result[0]['sources']
        elif isinstance(result, dict) and 'citations' in result:
            return result['citations']
        return []

    def get_confidence(self, result: Optional[Any], citations: list) -> float:
        # Example: combine citation count, recency, key attributes
        score = 0.5
        if not result:
            return 0.0
        if citations:
            score += 0.3 * min(len(citations), 3)
            recency_boost = 0
            for c in citations:
                date = c.get("date") if isinstance(c, dict) else None
                if date and str(date).startswith("202"):
                    recency_boost += 0.1
            score += min(recency_boost, 0.3)
        return min(score, 1.0)

    def handle_error(self, error: Exception) -> Dict[str, Any]:
        return {
            "success": False,
            "result": None,
            "error": str(error)
        }
