import { renameDir } from "../fetch/dirs.js";
import { renameFile } from "../fetch/files.js";
import { updateContextMenu } from "../utils.js";
import { contextFile } from "../elements/files.js";
import { contextDir } from "../elements/dirs.js";

export async function renameConfirm(textArea, dirname, type) {
  let newPath = textArea.value;
  let path = window.location.pathname.slice(1);
  const fullPath = `${path}${dirname}`;
  const fullNewPath = `${path}${newPath}`;
  if (!newPath) return;
  if (type === "file") await renameFile(fullPath, fullNewPath);
  else if (type === "dir") await renameDir(fullPath, fullNewPath);
  else throw new Error("Invalid type");
  location.reload();
}

export function renameCancel() {
  const renamePopup = document.querySelector(".renamePopup");
  renamePopup.remove();
}

export function openContextMenu(e, name, type) {
  e.preventDefault();
  updateContextMenu();
  let contextMenu;

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
