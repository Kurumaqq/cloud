import { fetchAndRender } from "./src/fetch.js";
import { Config } from "./src/config/config.js";
// TODO: REFACTORING (RENAME FUNCS AND OTHER THINGS)
// TODO: REMOVE SIDEBAR
// TODO: MAKE JUST WIN EXPLORER

document.querySelector(".explorer").addEventListener("drop", async (e) => {
  e.preventDefault();
  const files = e.dataTransfer.files;
  if (files.length === 0) return;

  const file = files[0]; // Берём первый файл из списка
  const formData = new FormData();
  formData.append("file", file, file.name);

  try {
    const response = await fetch("http://kuruma.online:8001/files/upload", {
      method: "POST",
      headers: {
        Authorization: "1682",
      },
      body: formData,
    });

    const result = await response.json();
    console.log("Успешно загружено:", result);
  } catch (err) {
    console.error("Ошибка загрузки:", err);
  }
});
document.querySelector(".explorer").addEventListener("dragover", (e) => {
  e.preventDefault();
});

(async () => {
  const container = document.querySelector(".explorer");
  fetchAndRender("http://kuruma.online:8001/combined/list", container);
})();
