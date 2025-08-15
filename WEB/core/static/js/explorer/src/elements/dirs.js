import { contextDirDelete } from "../btnHandler/dirs.js";
import { contextDirRename } from "../btnHandler/dirs.js";
import { openDir } from "../btnHandler/dirs.js";
import { openContextMenu } from "../btnHandler/other.js";
import { copy, copyWrapper } from "../../main.js";

export function contextDir(dirname) {
  const container = document.createElement("div");
  container.classList.add("contextDir");

  const copyBtn = document.createElement("button");
  copyBtn.classList.add("contextFile-copy");
  copyBtn.onclick = () => {
    const path = (location.pathname + dirname).slice(1);
    copyWrapper.value = { path: path, type: "dir" };
  };
  copyBtn.textContent = "Copy";

  const deleteBtn = document.createElement("button");
  deleteBtn.classList.add("contextDir-delete");
  deleteBtn.onclick = async () => contextDirDelete(dirname);
  deleteBtn.textContent = "Delete";

  const renameBtn = document.createElement("button");
  renameBtn.classList.add("contextDir-rename");
  renameBtn.onclick = () => contextDirRename(dirname);
  renameBtn.textContent = "Rename";

  container.appendChild(copyBtn);
  container.appendChild(renameBtn);
  container.appendChild(deleteBtn);

  return container;
}

export function dirEl(dirname) {
  const dirDiv = document.createElement("div");
  dirDiv.classList.add("dir");
  dirDiv.onclick = () => openDir(dirname);

  dirDiv.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = "move";
  });

  dirDiv.addEventListener("drop", (e) => {
    e.preventDefault();
    const fileData = JSON.parse(e.dataTransfer.getData("application/json"));
    console.log(`Файл "${fileData.name}" перемещён в папку "${dirname}"`);
    console.log(fileData.type);
  });
  dirDiv.addEventListener("contextmenu", (e) => {
    openContextMenu(e, dirDiv, "dir");
  });

  const dirIcon = document.createElement("img");
  dirIcon.classList.add("dir-icon");
  dirIcon.draggable = false;
  dirIcon.src = "/static/img/document.svg";

  const dirTitle = document.createElement("span");
  dirTitle.classList.add("dir-title");
  dirTitle.textContent = dirname;

  dirDiv.appendChild(dirIcon);
  dirDiv.appendChild(dirTitle);

  return dirDiv;
}
