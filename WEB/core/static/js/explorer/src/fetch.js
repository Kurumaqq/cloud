import { Config } from "./config/config.js";
import { getPath } from "./utils.js";
import { fileEl } from "./elements.js";

export async function fetchAndRender(url, container) {
  try {
    const path = window.location.pathname;
    const response = await fetch(`${url}${path}`, {
      headers: {
        "Content-Type": "application/json",
        Authorization: "1682",
      },
    });

    if (!response.ok) throw new Error(response.status);
    const data = await response.json();
    if (!data?.dirs && !data?.files) return;

    console.log(data.all);

    data.all.forEach((e) => {
      fileEl(container, getPath(e));
    });
  } catch (e) {
    console.error("Ошибка:", e);
    container.textContent = "Ошибка загрузки данных";
  }
}
