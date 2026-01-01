import pytest

from tests.data.mock_data import items
from tests.data.expected_data import created_item

pytestmark = pytest.mark.anyio


async def test_create_item(client) -> None:
    response = await client.post(
        "/v1/items", json={"name": "Item 4", "description": "This is awesome item!", "price": 400}
    )

    assert response.status_code == 201
    assert response.json() == created_item


async def test_get_item(seed_items, client) -> None:
    response = await client.get("/v1/items/102")

    assert response.status_code == 200
    assert response.json() == items[1]
