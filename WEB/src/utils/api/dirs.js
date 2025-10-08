import axios from "axios";
import config from "../../../public/config.json";
import { getCookie } from "../utils.js";

const API_BASE = config.APIURL;

export const listDirs = async (path) =>
  axios.get(`${API_BASE}/dirs/list/${encodeURIComponent(path)}`, {
    withCredentials: true,
    headers: {
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
  });

export const createDir = async (path) => {
  return axios.post(
    `${API_BASE}/dirs/create?path=${encodeURIComponent(path)}`,
    {},
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    }
  );
};

export const renameDir = (path, new_name) => {
  return axios.post(
    `${API_BASE}/dirs/rename`,
    {},
    {
      params: { path: path, new_name: new_name },
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    }
  );
};

export const deleteDir = async (path) => {
  return axios.delete(`${API_BASE}/dirs/delete`, {
    params: { path },
    withCredentials: true,
    headers: {
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
  });
};
