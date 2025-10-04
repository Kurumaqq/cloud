import {
  getFile,
  getVideoThumbnail,
  listFiles,
  uploadFileApi,
} from "./api/files";
import { listDirs } from "./api/dirs";
import config from "../../public/config.json";
import { useNavigate } from "react-router-dom";

export const updateFiles = async (path, setFilesList) => {
  try {
    const res = await listFiles(path);
    const serverFiles = (res.data.files ?? []).map((f) => f.split("/").pop());

    setFilesList((prev) => {
      const updated = [];

      for (const name of serverFiles) {
        const existing = prev.find((file) => file.name === name);
        if (existing) {
          updated.push(existing);
        } else {
          updated.push({ name, icon: null });
        }
      }

      return updated;
    });

    for (const name of serverFiles) {
      const icon = await getIcon(name, path);
      setFilesList((prev) =>
        prev.map((file) =>
          file.name === name && file.icon === null ? { ...file, icon } : file
        )
      );
    }
  } catch (err) {
    console.error(err);
  }
};

export const updateDirs = (path, setDirs, navigate) => {
  listDirs(path)
    .then((res) =>
      setDirs(
        res.data.dirs.map((d) => ({
          name: d.split("/").pop(),
          icon: "folder-base.svg",
        }))
      )
    )
    .catch(() => navigate("/login"));
};

export const updateExplorer = async (
  path,
  setDirs,
  setFiles,
  files,
  navigate
) => {
  await Promise.all([
    updateDirs(path, setDirs, navigate),
    updateFiles(path, setFiles, files),
  ]);
};

export const uploadFile = async (
  file,
  path,
  setProgressFiles,
  setShowProgressFiles
) => {
  try {
    setShowProgressFiles(true);
    setProgressFiles((prev) => [
      ...prev,
      {
        name: file.name,
        icon: `${file.name.split(".").pop()}.svg`,
        percent: 0,
      },
    ]);

    await uploadFileApi(path, file, (percent) => {
      setProgressFiles((prev) =>
        prev.map((f) => (f.name === file.name ? { ...f, percent } : f))
      );
    });
  } catch (err) {
    console.error("Ошибка загрузки", err);
  }
};

export const getIcon = async (filename, path = "") => {
  if (!filename || typeof filename !== "string") {
    return "/icons/files/document.svg";
  }

  const picExt = ["jpg", "jpeg", "png", "gif", "bmp", "svg"];
  const videoExt = ["mp4", "webm", "ogg"];
  if (path) path += "/";

  const ext = filename.split(".").pop().toLowerCase();

  if (picExt.includes(ext)) {
    return await getFile(`${path}${filename}`);
  } else if (videoExt.includes(ext)) {
    return `${config.APIURL}/files/thumbnail/${path}${filename}?time=0.5`;
  } else {
    return `/icons/files/${ext}.svg`;
  }
};
