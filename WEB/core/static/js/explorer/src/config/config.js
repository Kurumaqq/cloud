export class Config {
  static #config = null;

  static async headers() {
    await this.#load();
    return this.#config.headers;
  }

  static async apiUrl() {
    await this.#load();
    return this.#config.apiUrl;
  }

  static async #load() {
    if (this.#config == null) {
      try {
        const response = await (
          await fetch("../static/js/explorer/src/config/config.json")
        ).json();
        this.#config = response;
      } catch (e) {
        console.error("Error fetching config:", e);
        return;
      }
    }
  }
}
