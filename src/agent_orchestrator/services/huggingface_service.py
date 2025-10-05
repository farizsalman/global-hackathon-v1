import httpx
import os

class HuggingFaceService:
    def __init__(self):
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        self.base_url = os.getenv("HUGGINGFACE_API_URL", "https://api-inference.huggingface.co/models/")

    async def query_model(self, model: str, inputs: str):
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}{model}",
                headers=headers,
                json={"inputs": inputs}
            )
            response.raise_for_status()
            return response.json()
