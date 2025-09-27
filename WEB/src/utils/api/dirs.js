import axios from "axios";

const API_BASE = "http://127.0.0.1:8001";

export const listDirs = (path) =>
  axios.get(`${API_BASE}/dirs/list/${path}`, {
    headers: {
      Authorization: localStorage.getItem("accessToken"),
    },
  });

export const createDir = async (path) => {
  if (path[0] === "/") path = path.slice(1);
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
