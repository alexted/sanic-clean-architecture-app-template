import pytest

pytestmark = pytest.mark.anyio


async def test_sum(client) -> None:
    response = await client.post("/v1/summarise", json={"x": 4, "y": 6})

    assert response.status_code == 200
    assert response.json() == {"sum": 10}


async def test_sub(client) -> None:
    response = await client.get("/v1/subtract", params={"minuend": 9, "subtrahend": 4})

    assert response.status_code == 200
    assert response.json() == {"result": 5}


async def test_multi(client) -> None:
    response = await client.put("/v1/multiply", json={"x": 3, "y": 3})

    assert response.status_code == 200
    assert response.json() == {"result": 9}


async def test_div(client) -> None:
    response = await client.delete("/v1/divide", params={"dividend": 9, "divisor": 3})

    assert response.status_code == 200
    assert response.json() == {"result": 3}
