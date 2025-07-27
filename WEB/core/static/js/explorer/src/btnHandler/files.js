import { renameEl } from "../elements/other.js";
import { deleteFile } from "../fetch/files.js";

export async function contextFileDel(filename) {
  const path = window.location.pathname.slice(1);
  const fullPath = `${path}${filename}`;
  console.log(fullPath);
  await deleteFile(fullPath);
  location.reload();
}

export function contextFileRename(filename) {
  const main = document.querySelector(".main");
  const rename = renameEl(filename, "file");
  main.appendChild(rename);
}
