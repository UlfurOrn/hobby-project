async def test_get_pokemon(api_client):
    response = await api_client.get("/pokemon")

    assert response.status_code == 200
    assert response.json() == []
