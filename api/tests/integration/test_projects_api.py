def test_create_project_returns_201_and_project(client):
    response = client.post("/projects", json={"name": "E-commerce Platform"})

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "E-commerce Platform"
    assert body["id"] > 0
    assert "created_at" in body


def test_create_project_empty_name_returns_422(client):
    response = client.post("/projects", json={"name": ""})

    assert response.status_code == 422


def test_list_projects_empty_returns_empty_list(client):
    response = client.get("/projects")

    assert response.status_code == 200
    assert response.json() == []


def test_list_projects_returns_all_projects(client):
    client.post("/projects", json={"name": "Mobile App"})
    client.post("/projects", json={"name": "Data Pipeline"})

    response = client.get("/projects")

    assert response.status_code == 200
    names = [project["name"] for project in response.json()]
    assert names == ["Mobile App", "Data Pipeline"]


def test_get_project_returns_detail(client):
    created = client.post("/projects", json={"name": "Analytics Dashboard"}).json()

    response = client.get(f"/projects/{created['id']}")

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == created["id"]
    assert body["name"] == "Analytics Dashboard"
    assert body["technologies"] == []


def test_get_project_not_found_returns_404(client):
    response = client.get("/projects/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_update_project_renames_project(client):
    created = client.post("/projects", json={"name": "Old Name"}).json()

    response = client.patch(f"/projects/{created['id']}", json={"name": "New Name"})

    assert response.status_code == 200
    assert response.json()["name"] == "New Name"


def test_update_project_not_found_returns_404(client):
    response = client.patch("/projects/9999", json={"name": "Any Name"})

    assert response.status_code == 404


def test_delete_project_removes_project(client):
    created = client.post("/projects", json={"name": "Temporary Project"}).json()

    response = client.delete(f"/projects/{created['id']}")

    assert response.status_code == 204
    assert client.get(f"/projects/{created['id']}").status_code == 404


def test_delete_project_not_found_returns_404(client):
    response = client.delete("/projects/9999")

    assert response.status_code == 404