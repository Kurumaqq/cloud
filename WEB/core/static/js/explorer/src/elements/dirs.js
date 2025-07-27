import { contextDirDelete } from "../btnHandler/dirs.js";
import { contextDirRename } from "../btnHandler/dirs.js";
import { openDir } from "../btnHandler/dirs.js";
import { openContextMenu } from "../btnHandler/other.js";

export function contextDir(dirname) {
  const container = document.createElement("div");
  container.classList.add("contextDir");

  const deleteBtn = document.createElement("button");
  deleteBtn.classList.add("contextDir-delete");
  deleteBtn.onclick = async () => contextDirDelete(dirname);
  deleteBtn.textContent = "Delete";

  const renameBtn = document.createElement("button");
  renameBtn.classList.add("contextDir-rename");
  renameBtn.onclick = () => contextDirRename(dirname);
  renameBtn.textContent = "Rename";

  container.appendChild(deleteBtn);
  container.appendChild(renameBtn);

  return container;
}

export function dirEl(container, dirname) {
  const dirDiv = document.createElement("div");
  dirDiv.classList.add("dir");
  dirDiv.onclick = () => openDir(dirname);

  dirDiv.addEventListener("contextmenu", (e) => {
    openContextMenu(e, dirname, "dir");
  });

  const dirIcon = document.createElement("img");
  dirIcon.classList.add("dir-icon");
  dirIcon.src = "/static/img/document.svg";

  const dirTitle = document.createElement("span");
  dirTitle.classList.add("dir-title");
  dirTitle.textContent = dirname;

  dirDiv.appendChild(dirIcon);
  dirDiv.appendChild(dirTitle);
  container.appendChild(dirDiv);
}
