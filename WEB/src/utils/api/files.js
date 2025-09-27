import axios from "axios";

const API_BASE = "http://127.0.0.1:8001";

export const listFiles = (path) =>
  axios.get(`${API_BASE}/files/list/${path}`, {
    headers: {
      Authorization: localStorage.getItem("accessToken"),
    },
  });

export const uploadFileApi = (path, file, onProgress) => {
  const formData = new FormData();
  formData.append("file", file, file.name);

  return axios.post(`${API_BASE}/files/upload?path=${path}`, formData, {
    headers: {
      Authorization: localStorage.getItem("accessToken"),
    },
    onUploadProgress: (progressEvent) => {
      if (progressEvent.total && onProgress) {
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        onProgress(percentCompleted);
      }
    },
  });
};

export const renameFile = async (path, new_name) => {
  return axios.post(
    `${API_BASE}/files/rename`,
    {},
    {
      params: { path: path, new_name: new_name },
      headers: {
        Authorization: localStorage.getItem("accessToken"),
      },
    }
  );
};

export const deleteFile = async (path) => {
  return axios.delete(`${API_BASE}/files/delete`, {
    params: { path: path },
    headers: {
      Authorization: localStorage.getItem("accessToken"),
    },
  });
};

export const downloadFile = async (path) => {
  const response = await axios.get(`/files/download/${path}`, {
    headers: {
      Authorization: localStorage.getItem("accessToken") || "",
    },
    responseType: "blob",
  });

  const url = URL.createObjectURL(response.data);
  const a = document.createElement("a");
  a.href = url;
  a.download = path.split("/").pop();
  a.click();
  URL.revokeObjectURL(url);
};
