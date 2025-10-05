import pandas as pd
import numpy as np
import asyncio
from typing import Any, Dict, Optional, List
from src.agent_orchestrator.api.models import AgentTask, AgentResult

class AnalysisAgent:
    def __init__(self):
        pass

    async def execute(self, task: AgentTask) -> AgentResult:
        try:
            df = self.preprocess_data(task.params or task.query)
            if df is None or df.empty:
                raise ValueError("No valid data for analysis.")

            stats = self.compute_statistics(df)
            trends = self.detect_trends(df)
            insights = self.extract_insights(df, stats, trends)
            score = self.get_confidence(df, stats, trends, insights)

            return AgentResult(
                agent_id=task.agent_id,
                success=True,
                result={"stats": stats, "trends": trends, "insights": insights, "score": score},
                error=None
            )
        except Exception as e:
            return self.handle_error(e)

    def preprocess_data(self, data: Any) -> Optional[pd.DataFrame]:
        # Accepts DataFrame, list/dict, JSON. Handles missing/bad input.
        try:
            if isinstance(data, pd.DataFrame):
                df = data
            elif isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            elif isinstance(data, str):
                try:
                    df = pd.read_json(data)
                except:
                    df = pd.DataFrame([data])
            else:
                return None
            df = df.dropna(axis=1, thresh=int(0.3 * len(df)))
            df = df.dropna(axis=0, thresh=int(0.3 * len(df.columns)))
            return df
        except Exception:
            return None

    def compute_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        stats = {}
        for col in df.select_dtypes(include=np.number).columns:
            stats[col] = {
                "mean": float(df[col].mean()),
                "std": float(df[col].std()),
                "min": float(df[col].min()),
                "max": float(df[col].max()),
            }
        return stats

    def detect_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        trends = {}
        for col in df.select_dtypes(include=np.number).columns:
            arr = df[col].values
            if len(arr) >= 2:
                trend_corr = np.corrcoef(np.arange(len(arr)), arr)[0, 1]
                trends[col] = {
                    "trend": ("upward" if trend_corr > 0.35 else "downward" if trend_corr < -0.35 else "neutral"),
                    "corr": float(trend_corr)
                }
        return trends

    def extract_insights(self, df: pd.DataFrame, stats: Dict[str, Any], trends: Dict[str, Any]) -> List[str]:
        insights = []
        for col, s in stats.items():
            if s["mean"] > s["std"]:
                insights.append(f"{col} is relatively high and stable.")
            if col in trends and trends[col]["trend"] == "upward":
                insights.append(f"{col} is trending upward.")
            if col in trends and trends[col]["trend"] == "downward":
                insights.append(f"{col} is trending downward.")
        return insights

    def get_confidence(self, df, stats, trends, insights) -> float:
        completeness = 1.0 - df.isnull().mean().mean()
        insight_bonus = min(0.3, 0.05 * len(insights))
        confidence = min(1.0, 0.4 + 0.25 * (len(df) > 10) + 0.3 * completeness + insight_bonus)
        return confidence

    def handle_error(self, error: Exception) -> AgentResult:
        return AgentResult(agent_id="analysis", success=False, result=None, error=str(error))
