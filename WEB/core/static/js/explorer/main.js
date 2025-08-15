import { loadEventListeners } from "./src/event.js";
import { Config } from "./src/config/config.js";
import { fetchAndRenderExplorer } from "./src/fetch/combined.js";

export let copy = {};
export const copyWrapper = {
  get value() {
    const data = sessionStorage.getItem("copyData");
    return data ? JSON.parse(data) : null;
  },
  set value(newVal) {
    sessionStorage.setItem("copyData", JSON.stringify(newVal));
  },
};

loadEventListeners();
(async () => {
  const apiUrl = await Config.getValue("apiUrl");
  const container = document.querySelector(".explorer");
  //   console.log("HUIQWEQE");
  await fetchAndRenderExplorer(`${apiUrl}/combined/list`);
})();
