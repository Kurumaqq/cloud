import { getPath } from "../utils.js";
import { fileEl } from "../elements/files.js";
import { dirEl } from "../elements/dirs.js";

// TODO: DISK

export async function fetchAndRenderExplorer(url) {
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

    const explorer = document.querySelector(".explorer");
    data.dirs.forEach((e) => {
      console.log("HUIQWEQE");
      explorer.appendChild(dirEl(getPath(e)));
    });

    data.files.forEach((e) => {
      console.log("HUIQWEQE");
      explorer.appendChild(fileEl(getPath(e)));
    });
  } catch (e) {
    console.error("Ошибка:", e);
  }
}
