import pytest

from httpx import AsyncClient

headers = {"Authorization": ""}


@pytest.mark.asyncio
async def test_health_check_ok_status_200(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health-check/", headers=headers)
    assert response.status_code == 200
    assert response.json() == "Ok!"


@pytest.mark.asyncio
async def test_health_check_error_status_404(client: AsyncClient) -> None:
    response = await client.get("/health-check/", headers=headers)
    assert response.status_code == 404
