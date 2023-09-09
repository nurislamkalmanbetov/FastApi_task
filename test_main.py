import httpx
from main import app
import pytest 


@pytest.mark.asyncio
async def test_read_root():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Hello": "World"}
