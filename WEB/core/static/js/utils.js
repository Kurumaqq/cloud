export function getFullPath(buttonElement) {
  let fullPath = buttonElement.innerText.trim();
  let current = buttonElement.closest(".dir")?.parentElement;

  while (current) {
    const parentDir = current.closest(".dir");
    if (!parentDir) break;
    const parentButton = parentDir.querySelector("button");
    if (parentButton) {
      fullPath = `${parentButton.innerText.trim()}/${fullPath}`;
    }
    current = parentDir.parentElement;
  }

  return fullPath;
}
