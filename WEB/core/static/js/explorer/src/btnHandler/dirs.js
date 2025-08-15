import { deleteDir } from "../fetch/dirs.js";
import { renameEl } from "../elements/other.js";

export function contextDirRename(dirname) {
  const main = document.querySelector(".main");
  const rename = renameEl(dirname, "dir");
  main.appendChild(rename);
}

export function openDir(dirname) {
  const path = window.location.href;
  window.location.href = `${path}${dirname}`;
}

export async function contextDirDelete(dirname) {
  const path = window.location.pathname.slice(1);
  const fullPath = `${path}${dirname}`;
  await deleteDir(fullPath);
  const names = document.querySelectorAll(`.dir-title`);
  names.forEach((e) => {
    if (e.textContent === dirname) {
      e.parentElement.remove();
    }
  });
}
