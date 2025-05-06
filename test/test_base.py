def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 404  # No existe '/' si no se define

def test_register_route(client):
    response = client.get('/registro')
    assert response.status_code in [200, 302]  # Existe, puede redirigir o mostrarse

def test_pin_route(client):
    response = client.get('/verificar-pin')
    assert response.status_code in [200, 302]