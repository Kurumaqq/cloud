import { uploadFiles } from "./fetch/files.js";
import { fetchAndRenderExplorer } from "./fetch/combined.js";

export function loadEventListeners() {
  document.querySelector(".main").addEventListener("click", (e) => {
    e.preventDefault();
    const contextFileMenu = document.querySelector(".contextFile");
    const contextDirMenu = document.querySelector(".contextDir");
    contextFileMenu ? contextFileMenu.remove() : null;
    contextDirMenu ? contextDirMenu.remove() : null;
  });

  document.querySelector(".main").addEventListener("dragover", (e) => {
    e.preventDefault();
    if (!e.classList.contains(".file")) {
      const main = document.querySelector(".main");
      main.classList.add("drop");
    }
  });

  document.querySelector(".main").addEventListener("dragleave", (e) => {
    e.preventDefault();
    if (!e.classList.contains(".file")) {
      const main = document.querySelector(".main");
      main.classList.remove("drop");
    }
  });

  document.querySelector(".main").addEventListener("drop", async (e) => {
    e.preventDefault();
    if (!e.classList.contains(".file")) {
      const main = document.querySelector(".main");
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

  (async () => {
    const container = document.querySelector(".explorer");
    fetchAndRenderExplorer(
      "http://kuruma.online:8001/combined/list",
      container
    );
  })();
}
