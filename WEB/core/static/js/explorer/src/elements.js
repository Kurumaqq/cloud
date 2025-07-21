export function fileEl(container, fileName) {
  const path = window.location.href;

  const fileDiv = document.createElement("div");
  fileDiv.classList.add("file");
  fileDiv.onclick = () => {
    window.location.href = `${path}${fileName}`;
  };

  fileDiv.addEventListener("contextmenu", (event) => {
    event.preventDefault();
    console.log("ПКМ нажата на кнопку!");
  });

  const fileIcon = document.createElement("img");
  fileIcon.classList.add("file-icon");
  fileIcon.src = "/static/img/document.svg";

  const fileTitle = document.createElement("span");
  fileTitle.classList.add("file-title");
  fileTitle.textContent = fileName;

  fileDiv.appendChild(fileIcon);
  fileDiv.appendChild(fileTitle);
  container.appendChild(fileDiv);
}
