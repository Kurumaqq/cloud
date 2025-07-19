import { getFullPath } from "./utils.js";

export function updateFileExplorer(buttonElement) {
  const parentDiv = buttonElement.parentElement.querySelector(".dir-content");
  if (!parentDiv) return;
  parentDiv.innerHTML = "";

  const fullPath = getFullPath(buttonElement);
  toggleDir(buttonElement);

  fetch(`http://localhost:8000/combined/list/${fullPath}`, {
    headers: {
      "Content-Type": "application/json",
      Authorization: "1682",
    },
  })
    .then((response) => {
      if (!response.ok)
        throw new Error(`HTTP error! status: ${response.status}`);
      return response.json();
    })
    .then((data) => {
      if (!data.dirs && !data.files) return;

      (data.dirs || []).forEach((dir) => {
        parentDiv.appendChild(createDirElement(dir, buttonElement));
      });

      (data.files || []).forEach((file) => {
        parentDiv.appendChild(createFileElement(file, buttonElement));
      });
    })
    .catch((error) => {
      console.error("Ошибка:", error);
      parentDiv.textContent = "Ошибка загрузки данных";
    });
}

function toggleDir(buttonElement) {
  const isClosed = buttonElement.classList.toggle("dir-close");
  buttonElement.classList.toggle("dir-open", !isClosed);
  const content = buttonElement.nextElementSibling;
  if (content) content.style.display = isClosed ? "none" : "flex";
}

function createDirElement(dir, buttonElement) {
  const dirDiv = document.createElement("div");
  const currTextIndent = parseInt(
    window.getComputedStyle(buttonElement).textIndent,
    10
  );
  dirDiv.className = "dir";
  const button = document.createElement("button");
  button.textContent = dir.split("/").pop();
  button.className = "dir-button dir-close";
  button.style.textIndent = `${currTextIndent + 7}px`;

  const dirContent = document.createElement("div");
  dirContent.className = "dir-content";

  dirDiv.append(button, dirContent);
  return dirDiv;
}

function createFileElement(file, buttonElement) {
  const fileBtn = document.createElement("button");
  const currTextIndent = parseInt(
    window.getComputedStyle(buttonElement).textIndent,
    10
  );
  fileBtn.className = "files";
  fileBtn.textContent = file.split("/").pop();
  fileBtn.style.textIndent = `${currTextIndent + 7}px`;
  return fileBtn;
}

document.addEventListener("click", (event) => {
  const btn = event.target.closest(".dir-button");
  if (btn) updateFileExplorer(btn);
});
