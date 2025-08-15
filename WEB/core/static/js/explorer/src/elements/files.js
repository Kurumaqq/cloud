import { contextFileDel, contextFileRename } from "../btnHandler/files.js";
import { openContextMenu } from "../btnHandler/other.js";
import { copyWrapper } from "../../main.js";
import { getFile } from "../fetch/files.js";

export function contextFile(filename) {
  const container = document.createElement("div");
  container.classList.add("contextFile");

  const copyBtn = document.createElement("button");
  copyBtn.classList.add("contextFile-copy");
  const path = (location.pathname + filename).slice(1);
  copyBtn.onclick = () => {
    copyWrapper.value = { path: path, type: "file" };
  };
  copyBtn.textContent = "Copy";

  const renameBtn = document.createElement("button");
  renameBtn.classList.add("contextFile-rename");
  renameBtn.onclick = () => contextFileRename(filename);
  renameBtn.textContent = "Rename";

  const deleteBtn = document.createElement("button");
  deleteBtn.classList.add("contextFile-delete");
  deleteBtn.onclick = async () => await contextFileDel(filename);
  deleteBtn.textContent = "Delete";

  container.appendChild(copyBtn);
  container.appendChild(renameBtn);
  container.appendChild(deleteBtn);

  return container;
}

export function fileEl(filename) {
  const ext = filename.split(".").pop();
  const fileDiv = document.createElement("div");
  fileDiv.classList.add("file");
  fileDiv.draggable = true;

  fileDiv.addEventListener("contextmenu", (e) => {
    e.preventDefault();
    openContextMenu(e, fileDiv, "file");
  });

  fileDiv.addEventListener("dragstart", (e) => {
    const fileData = {
      name: filename,
      path: "/current/path/" + filename,
      type: "file",
    };
    e.dataTransfer.setData("application/json", JSON.stringify(fileData));
  });

  fileDiv.addEventListener("dragend", () => {
    fileDiv.classList.remove("dragging");
  });

  const fileIcon = document.createElement("img");

  const imgExt = [
    "jpg",
    "jpeg",
    "png",
    "gif",
    "bmp",
    "tiff",
    "webp",
    "ico",
    ".svg",
    "pdf",
  ];
  if (imgExt.includes(ext)) {
    (async () => {
      const blob = await getFile(`${location.pathname.slice(1)}${filename}`);
      const url = URL.createObjectURL(blob);

      fileIcon.style.objectFit = "cover";
      fileIcon.style.overflow = "hidden";
      fileIcon.src = url;
    })();
  } else {
    fileIcon.src = "/static/img/document.svg";
  }
  fileIcon.classList.add("file-icon");
  fileIcon.draggable = false;
  fileIcon.alt = "File icon";

  const fileTitle = document.createElement("span");
  fileTitle.classList.add("file-title");
  fileTitle.textContent = filename;

  fileDiv.appendChild(fileIcon);
  fileDiv.appendChild(fileTitle);

  return fileDiv;
}
