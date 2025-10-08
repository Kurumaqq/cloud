import {
  getFile,
  getVideoThumbnail,
  listFiles,
  uploadFileApi,
} from "./api/files";
import { listDirs } from "./api/dirs";
import config from "../../public/config.json";

let currentPath = null;
let currentSearchValue = null;

const iconCache = new Map();

const getCachedIcon = async (name, path) => {
  const key = `${path}/${name}`;

  if (iconCache.has(key)) {
    return iconCache.get(key);
  }

  const icon = await getIcon(name, path);

  iconCache.set(key, icon);

  return icon;
};

export const updateFiles = async (path, setFilesList, searchValue) => {
  currentPath = path;
  currentSearchValue = searchValue;

  try {
    const res = await listFiles(path);
    const serverFiles = (res.data.files ?? []).map((f) => ({
      name: f.name.split("/").pop(),
      favourite: f.favourite,
      size: f.size,
    }));

    if (currentPath !== path || currentSearchValue != searchValue) return;

    setFilesList(
      serverFiles.map((f) => {
        const shouldShow =
          !searchValue ||
          f.name.toLowerCase().includes(searchValue.toLowerCase());
        return {
          name: f.name,
          icon: null,
          favourite: f.favourite,
          show: shouldShow,
        };
      })
    );

    for (const f of serverFiles) {
      const icon = await getCachedIcon(f.name, path);
      setFilesList((prev) =>
        prev.map((file) =>
          file.name === f.name
            ? { ...file, icon, favourite: f.favourite }
            : file
        )
      );
    }
  } catch (err) {
    console.error(err);
  }
};

export const updateDirs = async (path, setDirs, navigate, searchValue) => {
  try {
    const res = await listDirs(path);
    const dirs = (res.data.dirs ?? []).map((d) => ({
      name: d.name.split("/").pop(),
      favourite: d.favourite,
      size: d.size,
    }));
    console.log(dirs);
    setDirs(
      dirs.map((d) => {
        console.log(d.favourite);
        const shouldShow =
          !searchValue ||
          d.name.toLowerCase().includes(searchValue.toLowerCase());
        return {
          name: d.name,
          icon: "folder-base.svg",
          favourite: d.favourite,
          show: shouldShow,
        };
      })
    );
  } catch (e) {
    console.log(e);
  }
};

export const updateExplorer = async (
  path,
  setDirs,
  setFiles,
  navigate,
  searchValue
) => {
  await Promise.all([
    updateDirs(path, setDirs, navigate, searchValue),
    updateFiles(path, setFiles, searchValue),
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
  const videoExt = ["mp4", "webm", "ogg", "mkv"];
  if (path) path += "/";

  const ext = filename.split(".").pop().toLowerCase();

  if (picExt.includes(ext)) {
    return await getFile(`${path}${filename}`);
  } else if (videoExt.includes(ext)) {
    return await getVideoThumbnail(`${path}${filename}`);
  } else {
    return `/icons/files/${ext}.svg`;
  }
};

export function getCookie(name) {
  const match = document.cookie.match(new RegExp("(^| )" + name + "=([^;]+)"));
  if (match) return match[2];
  return null;
}
