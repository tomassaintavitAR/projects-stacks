let currentProjectId = null;

function $(selector) {
  return document.querySelector(selector);
}

function escapeHtml(value) {
  const div = document.createElement("div");
  div.textContent = value;
  return div.innerHTML;
}

function formatDate(value) {
  const date = new Date(value);
  return date.toLocaleDateString();
}

function showError(element, message) {
  element.textContent = message;
  element.hidden = false;
}

function hideError(element) {
  element.hidden = true;
}

function showView(projects = false) {
  $("#projects-view").hidden = !projects;
  $("#project-detail-view").hidden = projects;
}

async function loadProjects() {
  const errorEl = $("#projects-error");
  const emptyEl = $("#projects-empty");
  const tableEl = $("#projects-table");
  hideError(errorEl);
  try {
    const projects = await apiRequest("/projects");
    emptyEl.hidden = projects.length > 0;
    tableEl.hidden = projects.length === 0;
    const body = $("#projects-body");
    body.innerHTML = "";
    for (const project of projects) {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td><a href="#" data-action="open" data-id="${project.id}">${escapeHtml(project.name)}</a></td>
        <td>${formatDate(project.created_at)}</td>
        <td>
          <button type="button" data-action="rename" data-id="${project.id}">Renombrar</button>
          <button type="button" data-action="delete" data-id="${project.id}" class="danger">Eliminar</button>
        </td>`;
      body.appendChild(row);
    }
  } catch (error) {
    showError(errorEl, `No se pudieron cargar los proyectos: ${error.message}`);
  }
}

async function createProject(name) {
  const errorEl = $("#projects-error");
  hideError(errorEl);
  try {
    await apiRequest("/projects", {
      method: "POST",
      body: JSON.stringify({ name }),
    });
    $("#new-project-name").value = "";
    await loadProjects();
  } catch (error) {
    showError(errorEl, `No se pudo crear el proyecto: ${error.message}`);
  }
}

async function renameProject(id) {
  const errorEl = $("#projects-error");
  const current = await apiRequest(`/projects/${id}`);
  const name = window.prompt("Nuevo nombre del proyecto:", current.name);
  if (name === null) {
    return;
  }
  hideError(errorEl);
  try {
    await apiRequest(`/projects/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ name: name.trim() }),
    });
    await loadProjects();
  } catch (error) {
    showError(errorEl, `No se pudo renombrar el proyecto: ${error.message}`);
  }
}

async function deleteProject(id) {
  const errorEl = $("#projects-error");
  if (!window.confirm("¿Eliminar este proyecto y sus tecnologías?")) {
    return;
  }
  hideError(errorEl);
  try {
    await apiRequest(`/projects/${id}`, { method: "DELETE" });
    await loadProjects();
  } catch (error) {
    showError(errorEl, `No se pudo eliminar el proyecto: ${error.message}`);
  }
}

async function loadProjectDetail(id) {
  const errorEl = $("#detail-error");
  hideError(errorEl);
  try {
    const project = await apiRequest(`/projects/${id}`);
    currentProjectId = project.id;
    $("#detail-title").textContent = project.name;
    loadTechnologies(project.technologies);
    showView(false);
  } catch (error) {
    showError(errorEl, `No se pudo cargar el proyecto: ${error.message}`);
  }
}

function loadTechnologies(technologies) {
  const emptyEl = $("#techs-empty");
  const tableEl = $("#techs-table");
  emptyEl.hidden = technologies.length > 0;
  tableEl.hidden = technologies.length === 0;
  const body = $("#techs-body");
  body.innerHTML = "";
  for (const technology of technologies) {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${escapeHtml(technology.name)}</td>
      <td>${formatDate(technology.created_at)}</td>
      <td>
        <button type="button" data-action="rename-tech" data-id="${technology.id}">Editar</button>
        <button type="button" data-action="delete-tech" data-id="${technology.id}" class="danger">Eliminar</button>
      </td>`;
    body.appendChild(row);
  }
}

async function createTechnology(name) {
  const errorEl = $("#detail-error");
  hideError(errorEl);
  try {
    const project = await apiRequest(`/projects/${currentProjectId}/technologies`, {
      method: "POST",
      body: JSON.stringify({ name }),
    });
    $("#new-tech-name").value = "";
    await loadProjectDetail(project.project_id);
  } catch (error) {
    showError(errorEl, `No se pudo agregar la tecnología: ${error.message}`);
  }
}

async function renameTechnology(id) {
  const errorEl = $("#detail-error");
  const project = await apiRequest(`/projects/${currentProjectId}`);
  const technology = project.technologies.find((item) => item.id === id);
  const name = window.prompt("Nuevo nombre de la tecnología:", technology.name);
  if (name === null) {
    return;
  }
  hideError(errorEl);
  try {
    await apiRequest(
      `/projects/${currentProjectId}/technologies/${id}`,
      {
        method: "PATCH",
        body: JSON.stringify({ name: name.trim() }),
      }
    );
    await loadProjectDetail(currentProjectId);
  } catch (error) {
    showError(errorEl, `No se pudo editar la tecnología: ${error.message}`);
  }
}

async function deleteTechnology(id) {
  const errorEl = $("#detail-error");
  if (!window.confirm("¿Eliminar esta tecnología?")) {
    return;
  }
  hideError(errorEl);
  try {
    await apiRequest(`/projects/${currentProjectId}/technologies/${id}`, {
      method: "DELETE",
    });
    await loadProjectDetail(currentProjectId);
  } catch (error) {
    showError(errorEl, `No se pudo eliminar la tecnología: ${error.message}`);
  }
}

function goBack() {
  currentProjectId = null;
  showView(true);
  loadProjects();
}

function handleDocumentClick(event) {
  const element = event.target.closest("[data-action]");
  if (!element) {
    return;
  }
  const id = Number(element.dataset.id);
  switch (element.dataset.action) {
    case "open":
      event.preventDefault();
      loadProjectDetail(id);
      break;
    case "rename":
      renameProject(id);
      break;
    case "delete":
      deleteProject(id);
      break;
    case "rename-tech":
      renameTechnology(id);
      break;
    case "delete-tech":
      deleteTechnology(id);
      break;
  }
}

function handleDocumentSubmit(event) {
  if (event.target.id === "create-project-form") {
    event.preventDefault();
    const input = $("#new-project-name");
    createProject(input.value.trim());
  } else if (event.target.id === "create-tech-form") {
    event.preventDefault();
    const input = $("#new-tech-name");
    createTechnology(input.value.trim());
  }
}

document.addEventListener("click", handleDocumentClick);
document.addEventListener("submit", handleDocumentSubmit);
$("#back-button").addEventListener("click", goBack);

loadProjects();