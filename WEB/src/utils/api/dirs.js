import axios from "axios";
import config from "../../../public/config.json";

const API_BASE = config.APIURL;

export const listDirs = (path) =>
  axios.get(`${API_BASE}/dirs/list/${path}`, {
    headers: {
      Authorization: localStorage.getItem("accessToken"),
    },
  });

export const createDir = async (path) => {
  //   if (path[0] === "/") path = path.slice(1);
  return axios.post(
    `${API_BASE}/dirs/create`,
    {},
    {
      params: { path },
      headers: {
        Authorization: localStorage.getItem("accessToken"),
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
      headers: {
        Authorization: localStorage.getItem("accessToken"),
      },
    }
  );
};

export const deleteDir = async (path) => {
  return axios.delete(`${API_BASE}/dirs/delete`, {
    params: { path },
    headers: {
      Authorization: localStorage.getItem("accessToken"),
    },
  });
};
