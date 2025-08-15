import { copyDir, createDir, renameDir } from "../fetch/dirs.js";
import { copyFile, renameFile } from "../fetch/files.js";
import { updateContextMenu } from "../utils.js";
import { contextFile, fileEl } from "../elements/files.js";
import { contextDir, dirEl } from "../elements/dirs.js";
import { copyWrapper } from "../../main.js";

export async function renameConfirm(textArea, name, type) {
  let ext = "";
  if (type === "file") {
    console.log(name);
    ext = textArea.value.includes(".") ? "" : "." + name.split(".").pop();
    console.log(ext);
    console.log(textArea.value);
  } else if (type === "dir") {
    ext = "";
  }
  let newPath = `${textArea.value}${ext}`;
  let path = window.location.pathname.slice(1);
  const fullPath = `${path}${name}`;
  const fullNewPath = `${path}${textArea.value}`;
  if (!newPath) return;
  if (type === "file") await renameFile(fullPath, fullNewPath);
  else if (type === "dir") await renameDir(fullPath, fullNewPath);
  else throw new Error("Invalid type");
  const names = document.querySelectorAll(`.${type}-title`);
  names.forEach((e) => {
    if (e.textContent === name) {
      renameCancel();
      e.textContent = newPath;
    }
  });
}

export function renameCancel() {
  const renamePopup = document.querySelector(".renamePopup");
  renamePopup.remove();
}

export function createDirCancel() {
  const renamePopup = document.querySelector(".createDirPopup");
  renamePopup.remove();
}

export function openContextMenu(e, div, type) {
  e.preventDefault();
  updateContextMenu();
  let contextMenu;
  const titleElement = div.querySelector(`.${type}-title`);
  const name = titleElement.textContent;

  if (type === "file") {
    contextMenu = contextFile(name);
  } else if (type === "dir") {
    contextMenu = contextDir(name);
  }
  const main = document.querySelector(".main");
  main.appendChild(contextMenu);

  contextMenu.style.left = `${e.clientX}px`;
  contextMenu.style.top = `${e.clientY}px`;
}

export async function createDirConfirm(name) {
  const path = location.pathname.slice(1);
  if (name) {
    await createDir(`${path}${name}`);
    const explorer = document.querySelector(".explorer");
    const popup = document.querySelector(".createDirPopup");
    explorer.prepend(dirEl(name));
    popup.remove();
  }
}

export async function paste() {
  const path = location.pathname.slice(1);
  console.log(copyWrapper.value);
  if (copyWrapper.value.type === "file") {
    const data = await copyFile(copyWrapper.value.path, path);
    const explorer = document.querySelector(".explorer");
    explorer.appendChild(fileEl(data.name));
  } else if (copyWrapper.value.type === "dir") {
    const data = await copyDir(copyWrapper.value.path, path);
    console.log(data);
    const explorer = document.querySelector(".explorer");
    explorer.appendChild(dirEl(data.name));
  }
}
