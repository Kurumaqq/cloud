import axios from "axios";
import config from "../../../public/config.json";
import { getCookie } from "../utils.js";

const API_BASE = config.APIURL;

export const listDirs = async (path) =>
  axios.get(`${API_BASE}/dirs/list/${path}`, {
    withCredentials: true,
    headers: {
      "X-CSRF-TOKEN": getCookie("CSRF_ACCES_TOKEN"),
    },
  });

export const addFavDir = async (path) => {
  axios.post(
    `${API_BASE}/dirs/add-favourite?path=${path}`,
    {},
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("CSRF_ACCES_TOKEN"),
      },
    }
  );
};

export const rmFavDir = async (path) => {
  await axios.post(
    `${API_BASE}/dirs/rm-favourite?path=${encodeURIComponent(path)}`,
    {},
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("CSRF_ACCES_TOKEN"),
      },
    }
  );
};

export const createDir = async (path) => {
  return axios.post(
    `${API_BASE}/dirs/create?path=${encodeURIComponent(path)}`,
    {},
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("CSRF_ACCES_TOKEN"),
      },
    }
  );
};

export const renameDir = (path, new_name) => {
  return axios.post(
    `${API_BASE}/dirs/rename`,
    { path: path, new_name: new_name },
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("CSRF_ACCES_TOKEN"),
      },
    }
  );
};

export const deleteDir = async (path) => {
  return axios.delete(`${API_BASE}/dirs/delete`, {
    params: { path },
    withCredentials: true,
    headers: {
      "X-CSRF-TOKEN": getCookie("CSRF_ACCES_TOKEN"),
    },
  });
};
