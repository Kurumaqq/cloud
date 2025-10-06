import axios from "axios";
import config from "../../../public/config.json";

const API_BASE = config.APIURL;
const CHUNK_SIZE = 5 * 1024 * 1024;

export const listFiles = async (path) =>
  axios.get(`${API_BASE}/files/list/${path}`, {
    headers: {
      Authorization: localStorage.getItem("accessToken"),
    },
  });

export const addFavFile = async (path) => {
  axios.post(
    `${API_BASE}/files/add-favourite?path=${path}`,
    {},
    {
      headers: {
        Authorization: localStorage.getItem("accessToken"),
      },
    }
  );
};

export const rmFavFile = async (path) => {
  axios.post(
    `${API_BASE}/files/rm-favourite?path=${path}`,
    {},
    {
      headers: {
        Authorization: localStorage.getItem("accessToken"),
      },
    }
  );
};

export const getFile = async (path) => {
  const response = await axios.get(
    `${API_BASE}/files/get/${path}?token=${localStorage.getItem(
      "accessToken"
    )}`,
    {
      responseType: "blob",
    }
  );
  const blob = response.data;
  const url = URL.createObjectURL(blob);
  return url;
};

export const copyFile = async (path, copy_path) => {
  await axios.post(
    `${API_BASE}/files/copy?file_path=${path}&copy_path=${copy_path}`,
    {},
    {
      headers: {
        Authorization: localStorage.getItem("accessToken"),
      },
    }
  );
};

export const getVideoThumbnail = async (path, time = 0.5) => {
  const response = await axios.get(
    `${API_BASE}/files/thumbnail/${path}?time=${time}`,
    {
      headers: {
        Authorization: localStorage.getItem("accessToken"),
      },
      responseType: "blob",
    }
  );

  return URL.createObjectURL(response.data);
};

export const moveFile = async (path, move_path) => {
  console.log("Запрос на перемещение файла:", { path, move_path });

  try {
    const response = await axios.post(
      `${API_BASE}/files/move?path=${encodeURIComponent(
        path
      )}&move_path=${encodeURIComponent(move_path)}`,
      {},
      {
        headers: {
          Authorization: localStorage.getItem("accessToken"),
        },
      }
    );

    console.log("Ответ от сервера:", response.data);
    return response.data;
  } catch (error) {
    console.error("Ошибка при перемещении файла:", error);
    throw error;
  }
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
    formData.append("uploadId", uploadId);
    formData.append("chunkIndex", chunkIndex);
    formData.append("totalChunks", totalChunks);
    formData.append("filename", file.name);
    formData.append("path", path);

    await axios.post(`${API_BASE}/files/upload`, formData, {
      headers: {
        Authorization: localStorage.getItem("accessToken"),
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

  const response = await axios.get(`${API_BASE}/files/complete-upload`, {
    headers: {
      Authorization: localStorage.getItem("accessToken"),
    },
    params: {
      uploadId,
      totalChunks,
      filename: file.name,
      path,
    },
  });

  if (onProgress) onProgress(100);

  return response.data;
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
  try {
    await axios.delete(`${API_BASE}/files/delete`, {
      params: { path },
      headers: {
        Authorization: localStorage.getItem("accessToken"),
      },
    });
  } catch (err) {
    console.error("Ошибка deleteFile:", err);
  }
};

export const downloadFile = async (path) => {
  const a = document.createElement("a");
  a.href = `${API_BASE}/files/download/${path}?token=${localStorage.getItem(
    "accessToken"
  )}`;
  a.download = path.split("/").pop();
  a.click();
};
