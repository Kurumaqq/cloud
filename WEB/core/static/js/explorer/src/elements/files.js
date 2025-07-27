import { contextFileDel, contextFileRename } from "../btnHandler/files.js";
import { openContextMenu } from "../btnHandler/other.js";

export function contextFile(filename) {
  const container = document.createElement("div");
  container.classList.add("contextFile");

  const deleteBtn = document.createElement("button");
  deleteBtn.classList.add("contextFile-delete");
  deleteBtn.textContent = "Delete";
  deleteBtn.onclick = async () => await contextFileDel(filename);

  const renameBtn = document.createElement("button");
  renameBtn.classList.add("contextFile-rename");
  renameBtn.onclick = () => contextFileRename(filename);
  renameBtn.textContent = "Rename";

  container.appendChild(deleteBtn);
  container.appendChild(renameBtn);

  return container;
}

export function fileEl(container, filename) {
  const fileDiv = document.createElement("div");
  fileDiv.classList.add("file");
  fileDiv.draggable = true;

  fileDiv.addEventListener("contextmenu", (e) => {
    openContextMenu(e, filename, "file");
  });

  const fileIcon = document.createElement("img");
  fileIcon.classList.add("file-icon");
  fileIcon.src = "/static/img/document.svg";

  const fileTitle = document.createElement("span");
  fileTitle.classList.add("file-title");
  fileTitle.textContent = filename;

  fileDiv.appendChild(fileIcon);
  fileDiv.appendChild(fileTitle);
  container.appendChild(fileDiv);
}
