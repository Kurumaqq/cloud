import {
  renameConfirm,
  renameCancel,
  createDirConfirm,
  createDirCancel,
  paste,
} from "../btnHandler/other.js";

export function progressBarEl() {
  const progressBar = document.createElement("div");
  progressBar.classList.add("progressBar");

  const filename = document.createElement("span");
  filename.classList.add("progressUpload-filename");

  const progress = document.createElement("div");
  progress.classList.add("progress");
  progress.textContent = "0%";

  progressBar.appendChild(filename);
  progressBar.appendChild(progress);
  return progressBar;
}

export function renameEl(name, type) {
  const container = document.createElement("div");
  container.classList.add("renamePopup");

  const renameTextArea = document.createElement("textarea");
  renameTextArea.classList.add("renamePopup-textArea");
  renameTextArea.placeholder = "Enter filename";
  renameTextArea.value = name;

  const containerBtn = document.createElement("div");
  containerBtn.classList.add("renamePopup-containerBtn");

  const cancelBtn = document.createElement("button");
  cancelBtn.classList.add("renamePopup-cancelBtn");
  cancelBtn.textContent = "Cancel";
  cancelBtn.onclick = renameCancel;

  const confirmBtn = document.createElement("button");
  confirmBtn.classList.add("renamePopup-confirmBtn");
  confirmBtn.textContent = "Confirm";
  confirmBtn.onclick = async () =>
    await renameConfirm(renameTextArea, name, type);

  containerBtn.appendChild(cancelBtn);
  containerBtn.appendChild(confirmBtn);

  container.appendChild(renameTextArea);
  container.appendChild(containerBtn);

  return container;
}

export function contextMenuEl() {
  const container = document.createElement("div");
  container.classList.add("contextMenu");

  const refreshBtn = document.createElement("button");
  refreshBtn.classList.add("contextMenu-refreshBtn");
  refreshBtn.textContent = "Refresh";
  refreshBtn.onclick = () => location.reload();

  const createDirBtn = document.createElement("button");
  createDirBtn.classList.add("contextMenu-pasteBtn");
  createDirBtn.textContent = "Create dir";
  createDirBtn.onclick = () => {
    const explorer = document.querySelector(".explorer");
    explorer.prepend(createDirEl());
  };

  const pasteBtn = document.createElement("button");
  pasteBtn.classList.add("contextMenu-pasteBtn");
  pasteBtn.textContent = "Paste";
  pasteBtn.onclick = async () => await paste();

  container.appendChild(refreshBtn);
  container.appendChild(createDirBtn);
  container.appendChild(pasteBtn);

  return container;
}

export function createDirEl() {
  const container = document.createElement("div");
  container.classList.add("createDirPopup");

  const createDirTextArea = document.createElement("textarea");
  createDirTextArea.classList.add("createDirPopup-textArea");
  createDirTextArea.placeholder = "Enter filename";

  const containerBtn = document.createElement("div");
  containerBtn.classList.add("createDirPopup-containerBtn");

  const cancelBtn = document.createElement("button");
  cancelBtn.classList.add("createDirPopup-cancelBtn");
  cancelBtn.textContent = "Cancel";
  cancelBtn.onclick = createDirCancel;

  const confirmBtn = document.createElement("button");
  confirmBtn.classList.add("createDirPopup-confirmBtn");
  confirmBtn.textContent = "Confirm";
  confirmBtn.onclick = async () => {
    const name = createDirTextArea.value;
    await createDirConfirm(name);
  };

  containerBtn.appendChild(cancelBtn);
  containerBtn.appendChild(confirmBtn);

  container.appendChild(createDirTextArea);
  container.appendChild(containerBtn);

  return container;
}
