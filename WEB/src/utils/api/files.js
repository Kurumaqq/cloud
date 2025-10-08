import axios from "axios";
import config from "../../../public/config.json";
import { getCookie } from "../utils";

const API_BASE = config.APIURL;
const CHUNK_SIZE = 5 * 1024 * 1024;

export const listFiles = async (path) =>
  axios.get(`${API_BASE}/files/list/${encodeURIComponent(path)}`, {
    withCredentials: true,
    headers: {
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
  });

export const addFavFile = async (path) => {
  axios.post(
    `${API_BASE}/files/add-favourite?path=${path}`,
    {},
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    }
  );
};

export const rmFavFile = async (path) => {
  axios.post(
    `${API_BASE}/files/rm-favourite?path=${path}`,
    {},
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    }
  );
};

export const getFile = async (path) => {
  const response = await axios.get(`${API_BASE}/files/get/${path}`, {
    withCredentials: true,
    headers: {
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
    responseType: "blob",
  });
  const blob = response.data;
  const url = URL.createObjectURL(blob);
  return url;
};

export const copyFile = async (path, copy_path) => {
  await axios.post(
    `${API_BASE}/files/copy?file_path=${path}&copy_path=${copy_path}`,
    {},
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    }
  );
};

export const getVideoThumbnail = async (path, time = 0.5) => {
  const response = await axios.get(`${API_BASE}/files/thumbnail/${path}`, {
    params: { time },
    withCredentials: true,
    headers: {
      "X-CSRF-TOKEN": getCookie("csrf_access_token"),
    },
    responseType: "blob",
  });

  return URL.createObjectURL(response.data);
};

export const moveFile = async (path, movePath) => {
  const response = await axios.post(
    `${API_BASE}/files/move`,
    { path: path, move_path: movePath },
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    }
  );
};

export const uploadFileApi = async (path, file, onProgress) => {
  const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
  const uploadId = Date.now() + "-" + file.name;

  let uploadedBytes = 0;

  for (let chunkIndex = 0; chunkIndex < totalChunks; chunkIndex++) {
    const start = chunkIndex * CHUNK_SIZE;
    const end = Math.min(start + CHUNK_SIZE, file.size);
    const chunk = file.slice(start, end);

    const formData = new FormData();
    formData.append("file", chunk, file.name);
    formData.append("upload_id", String(uploadId));
    formData.append("chunk_index", String(chunkIndex));
    formData.append("total_chunks", totalChunks);
    formData.append("filename", file.name);
    formData.append("path", path);

    await axios.post(`${API_BASE}/files/upload`, formData, {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const chunkProgress = progressEvent.loaded / progressEvent.total;
          const totalProgress =
            ((uploadedBytes + progressEvent.loaded) / file.size) * 100;
          onProgress(Math.min(100, Math.round(totalProgress)));
        }
      },
    });

    uploadedBytes += chunk.size;
  }
  const formData = new FormData();
  formData.append("upload_id", uploadId);
  formData.append("total_chunks", totalChunks);
  formData.append("filename", file.name);
  formData.append("path", path);

  const response = await axios.post(
    `${API_BASE}/files/complete-upload`,
    formData,
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    }
  );

  if (onProgress) onProgress(100);

  return response.data;
};

export const renameFile = async (path, newName) => {
  return axios.post(
    `${API_BASE}/files/rename`,
    { path: path, new_name: newName },
    {
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    }
  );
};

export const deleteFile = async (path) => {
  try {
    await axios.delete(`${API_BASE}/files/delete`, {
      params: { path },
      withCredentials: true,
      headers: {
        "X-CSRF-TOKEN": getCookie("csrf_access_token"),
      },
    });
  } catch (err) {
    console.error("Ошибка deleteFile:", err);
  }
};

export const downloadFile = async (path) => {
  const a = document.createElement("a");
  a.href = `${API_BASE}/files/download/${path}`;
  a.download = path.split("/").pop();
  a.click();
};
