from app.models import Technology


def test_create_technology_returns_201(client):
    project = client.post("/projects", json={"name": "Web Platform"}).json()

    response = client.post(
        f"/projects/{project['id']}/technologies", json={"name": "FastAPI"}
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "FastAPI"
    assert body["project_id"] == project["id"]
    assert "created_at" in body


def test_create_technology_empty_name_returns_422(client):
    project = client.post("/projects", json={"name": "Web Platform"}).json()

    response = client.post(
        f"/projects/{project['id']}/technologies", json={"name": ""}
    )

    assert response.status_code == 422


def test_create_technology_project_not_found_returns_404(client):
    response = client.post("/projects/9999/technologies", json={"name": "FastAPI"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found"


def test_create_technology_appears_in_project_detail(client):
    project = client.post("/projects", json={"name": "Web Platform"}).json()
    client.post(
        f"/projects/{project['id']}/technologies", json={"name": "PostgreSQL"}
    )

    detail = client.get(f"/projects/{project['id']}").json()

    technologies = [tech["name"] for tech in detail["technologies"]]
    assert technologies == ["PostgreSQL"]


def test_update_technology_renames_technology(client):
    project = client.post("/projects", json={"name": "Web Platform"}).json()
    tech = client.post(
        f"/projects/{project['id']}/technologies", json={"name": "React"}
    ).json()

    response = client.patch(
        f"/projects/{project['id']}/technologies/{tech['id']}",
        json={"name": "Next.js"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Next.js"
    assert body["id"] == tech["id"]


def test_update_technology_not_found_returns_404(client):
    project = client.post("/projects", json={"name": "Web Platform"}).json()

    response = client.patch(
        f"/projects/{project['id']}/technologies/9999", json={"name": "Any"}
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Technology not found"


def test_delete_technology_removes_technology(client):
    project = client.post("/projects", json={"name": "Web Platform"}).json()
    tech = client.post(
        f"/projects/{project['id']}/technologies", json={"name": "Docker"}
    ).json()

    response = client.delete(f"/projects/{project['id']}/technologies/{tech['id']}")

    assert response.status_code == 204
    detail = client.get(f"/projects/{project['id']}").json()
    assert detail["technologies"] == []


def test_delete_technology_not_found_returns_404(client):
    project = client.post("/projects", json={"name": "Web Platform"}).json()

    response = client.delete(f"/projects/{project['id']}/technologies/9999")

    assert response.status_code == 404


def test_delete_project_cascades_technologies(client):
    project = client.post("/projects", json={"name": "Legacy System"}).json()
    tech = client.post(
        f"/projects/{project['id']}/technologies", json={"name": "COBOL"}
    ).json()

    assert client.delete(f"/projects/{project['id']}").status_code == 204

    db = client.app.state.session_factory()
    try:
        assert db.get(Technology, tech["id"]) is None
    finally:
        db.close()