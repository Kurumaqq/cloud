export function getPath(full_path) {
  return full_path.split("/").pop();
}

export function updateProgressBar(progressBar, loaded, total) {
  const percentComplete = (loaded / total) * 100;
  progressBar.textContent = `${percentComplete.toFixed(2)}%`;
  progressBar.style.width = `${percentComplete}%`;
}

export function updateContextMenu() {
  const oldContextFileMenu = document.querySelector(".contextFile");
  const oldContextDirMenu = document.querySelector(".contextDir");
  if (oldContextFileMenu) oldContextFileMenu.remove();
  if (oldContextDirMenu) oldContextDirMenu.remove();
}
