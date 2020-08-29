from gcloud.aio.auth.token import Token
from typing import Optional


class TokenGenerator:
    def __init__(self, path: str) -> None:
        self.generator = Token(service_file=path, scopes=["https://www.googleapis.com/auth/cloud-platform"])

    async def get(self) -> Optional[str]:
        return await self.generator.get()
