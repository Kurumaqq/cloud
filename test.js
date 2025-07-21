document.getElementById("drop-area").addEventListener("drop", (e) => {
  e.preventDefault();
  const files = e.dataTransfer.files;
  console.log(files);
});

document.getElementById("drop-area").addEventListener("dragover", (e) => {
  e.preventDefault();
});
