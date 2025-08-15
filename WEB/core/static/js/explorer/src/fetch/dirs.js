import { Config } from "../config/config.js";

export async function listDirs(path) {
  try {
    const token = await Config.getValue("token");
    const apiUrl = await Config.getValue("apiUrl");

    const response = await fetch(`${apiUrl}/dirs/list/${path}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    });

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}

export async function sizeDir(path) {
  try {
    const token = await Config.getValue("token");
    const apiUrl = await Config.getValue("apiUrl");

    const response = await fetch(`${apiUrl}/dirs/size/${path}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    });

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}
export async function createDir(path) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");

    const response = await fetch(`${apiUrl}/dirs/create?path=${path}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: token,
      },
    });

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}

export async function copyDir(path, new_path) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");

    const response = await fetch(
      `${apiUrl}/dirs/copy?dir_path=${path}&copy_path=${new_path}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token,
        },
      }
    );

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}

export async function renameDir(path, new_name) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");
    const response = await fetch(
      `${apiUrl}/dirs/rename?path=${path}&new_name=${new_name}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: token,
        },
      }
    );

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}

export async function deleteDir(path) {
  try {
    const apiUrl = await Config.getValue("apiUrl");
    const token = await Config.getValue("token");

    const response = await fetch(`${apiUrl}/dirs/delete?path=${path}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "Aplication/json",
        Authorization: token,
      },
    });

    if (!response.ok) throw new Error(response.status);

    const data = await response.json();
    return data;
  } catch (e) {
    console.log(e);
  }
}
