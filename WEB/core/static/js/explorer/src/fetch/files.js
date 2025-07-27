import { updateProgressBar } from "../utils.js";
import { Config } from "../config/config.js";
import { progressBarEl } from "../elements/other.js";
import { fileEl } from "../elements/files.js";
// import progressBarEl
// import {  fileEl} from " fileEl";
export async function listFiles(path) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");

    const response = await fetch(`${apiUrl}/files/list/${path}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    });

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}

export async function downloadFile(path) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");

    const response = await fetch(`${apiUrl}/files/download/${path}`, {
      method: "GET",
      headers: { Authorization: token },
    });

    if (!response.ok) throw new Error(response.status);

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = path.split("/").pop() || "file";
    a.click();
    URL.revokeObjectURL(url);
  } catch (e) {
    console.error("Ошибка скачивания:", e);
  }
}

export async function readFile(path) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");

    const response = await fetch(`${apiUrl}/files/read/${path}`, {
      method: "GET",
      headers: {
        "Content-Type": "aplication/json",
        Authorization: token,
      },
    });

    if (!response.ok) throw new Error(response.status);

    const data = response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}

export function uploadFiles(e) {
  e.preventDefault();

  const progressUpload = document.querySelector(".progressUpload");
  progressUpload.classList.add("progressBar-show");

  const main = document.querySelector(".main");
  main.classList.remove("drop");

  const files = e.dataTransfer.files;
  if (files.length === 0) return;

  Array.from(files).forEach((file) => uploadFile(file));
}

export async function renameFile(path, new_name) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");

    const response = await fetch(
      `${apiUrl}/files/rename?path=${path}&new_name=${new_name}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "aplication/json",
          Authorization: token,
        },
      }
    );

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}

export function uploadFile(file) {
  const path = window.location.pathname.slice(1);
  const progressUpload = document.querySelector(".progressUpload");
  const progressElement = progressBarEl();
  progressElement.querySelector(".progressUpload-filename").textContent =
    file.name;
  progressUpload.appendChild(progressElement);

  const progressBar = progressElement.querySelector(".progress");

  const formData = new FormData();
  formData.append("file", file, file.name);

  const xhr = new XMLHttpRequest();
  xhr.open("POST", `http://kuruma.online:8001/files/upload?path=${path}`, true);
  xhr.setRequestHeader("Authorization", "1682");

  xhr.upload.addEventListener("progress", (event) => {
    if (event.lengthComputable) {
      updateProgressBar(progressBar, event.loaded, event.total);
    }
  });

  xhr.onload = () => {
    if (xhr.status >= 200 && xhr.status < 300) {
      const container = document.querySelector(".explorer");
      const fileNames = document.querySelectorAll(".file-title");

      const isFileAlreadyExist = Array.from(fileNames).some(
        (el) => el.textContent === file.name
      );

      isFileAlreadyExist ? null : fileEl(container, file.name);
    } else {
      console.error("Ошибка загрузки:", xhr.statusText);
    }
  };

  xhr.onerror = () => {
    console.error("Ошибка сети при загрузке файла");
  };

  xhr.send(formData);
}

export async function deleteFile(path) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");

    const response = await fetch(`${apiUrl}/files/delete?path=${path}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    });

    if (!response.ok) throw new Error(response.status);

    const data = response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}
