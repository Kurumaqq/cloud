import { uploadFiles } from "./fetch/files.js";
import { contextMenuEl } from "./elements/other.js";
import { updateContextMenu } from "./utils.js";
import { fetchAndRenderExplorer } from "./fetch/combined.js";

export function loadEventListeners() {
  document.querySelector(".main").addEventListener("click", (e) => {
    e.preventDefault();
    updateContextMenu();
  });

  const main = document.querySelector(".main");

  main.addEventListener("contextmenu", (e) => {
    const excludedClasses = [
      "file",
      "file-icon",
      "file-title",
      "dir",
      "dir-icon",
      "dir-title",
    ];
    const isExcluded = excludedClasses.some((className) =>
      e.target.classList.contains(className)
    );

    if (isExcluded) return;

    e.preventDefault();

    const existingMenu = document.querySelector(".contextMenu");
    existingMenu?.remove();
    const menu = contextMenuEl();
    document.querySelector(".main").appendChild(menu);
    menu.style.left = `${e.clientX}px`;
    menu.style.top = `${e.clientY}px`;
  });
  main.addEventListener("dragover", (e) => {
    if (e.dataTransfer.types.includes("Files")) {
      e.preventDefault();
      main.classList.add("drop");
    }
  });

  main.addEventListener("dragleave", (e) => {
    if (!e.currentTarget.contains(e.relatedTarget)) {
      e.preventDefault();
      main.classList.remove("drop");
    }
  });

  main.addEventListener("drop", async (e) => {
    if (e.dataTransfer.types.includes("Files")) {
      e.preventDefault();
      main.classList.remove("drop");
      uploadFiles(e);
    }
  });

  document
    .querySelector(".progressUpload-close")
    .addEventListener("click", () => {
      const progressUpload = document.querySelector(".progressUpload");
      progressUpload.classList.remove("progressBar-show");
    });
}
