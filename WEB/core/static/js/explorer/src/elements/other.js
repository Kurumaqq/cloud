import { renameConfirm, renameCancel } from "../btnHandler/other.js";

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
