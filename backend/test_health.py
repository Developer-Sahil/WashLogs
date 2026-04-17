import asyncio
import httpx
from src.main import app
async def test():
    async with httpx.AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/health")
        print(r.status_code, r.text)

if __name__ == "__main__":
    asyncio.run(test())
