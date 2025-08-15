export class Config {
  static #config = null;

  static async #loadConfig() {
    if (!this.#config) {
      try {
        const response = await fetch(
          "/static/js/explorer/src/config/config.json"
        );
        if (!response.ok) throw new Error("Network response was not ok");
        this.#config = await response.json();
      } catch (error) {
        console.error("Failed to load config:", error);
        this.#config = {};
      }
    }
    return this.#config;
  }

  static async getValue(key) {
    await this.#loadConfig();
    return this.#config[key];
  }
}
