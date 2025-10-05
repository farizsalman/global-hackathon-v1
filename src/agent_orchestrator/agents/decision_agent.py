from typing import Any, Dict, Optional, List
from src.agent_orchestrator.api.models import AgentTask, AgentResult

class DecisionAgent:
    def __init__(self, hithreshold: float = 0.7, lothreshold: float = 0.4):
        self.confidence_high = hithreshold
        self.confidence_low = lothreshold

    async def execute(self, task: AgentTask) -> AgentResult:
        # task.params expected to have keys: "research" (ResearchAgent), "analysis" (AnalysisAgent)
        try:
            research = task.params.get("research", {})
            analysis = task.params.get("analysis", {})
            research_score = research.get("score", 0)
            analysis_score = analysis.get("score", 0)
            insights = analysis.get("insights", [])

            avg_confidence = (research_score + analysis_score) / 2

            # Recommendation logic
            if avg_confidence >= self.confidence_high:
                rec = "Confidently recommend proceeding based on available evidence and analysis."
            elif avg_confidence <= self.confidence_low:
                rec = "Confidence is low; escalate for human review/approval."
            else:
                rec = "Proceed with caution; partial human review suggested."

            return AgentResult(
                agent_id=task.agent_id,
                success=True,
                result={
                    "decision": rec,
                    "avg_confidence": avg_confidence,
                    "human_review": avg_confidence <= self.confidence_low,
                    "details": {
                        "research_score": research_score,
                        "analysis_score": analysis_score,
                        "insights": insights,
                    }
                },
                error=None
            )
        except Exception as e:
            return self.handle_error(e)

    def handle_error(self, error: Exception) -> AgentResult:
        return AgentResult(agent_id="decision", success=False, result=None, error=str(error))
