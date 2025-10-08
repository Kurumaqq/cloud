import {
  getFile,
  getVideoThumbnail,
  listFiles,
  uploadFileApi,
} from "./api/files";
import { listDirs } from "./api/dirs";

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

    // Сначала устанавливаем список файлов с актуальными favourite
    setFilesList(
      serverFiles.map((f) => ({
        name: f.name,
        icon: null,
        show:
          !searchValue ||
          f.name.toLowerCase().includes(searchValue.toLowerCase()),
        favourite: f.favourite,
      }))
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

export const updateDirs = (path, setDirs, navigate, searchValue) => {
  listDirs(path)
    .then((res) => {
      setDirs(
        res.data.dirs.map((d) => {
          const name = d.split("/").pop();

          const shouldShow =
            !searchValue ||
            name.toLowerCase().includes(searchValue.toLowerCase());

          return {
            name,
            icon: "folder-base.svg",
            show: shouldShow,
          };
        })
      );
    })
    .catch(() => navigate("/login"));
};

export const updateExplorer = async (
  path,
  setDirs,
  setFiles,
  files,
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
  setShowProgressFiles,
  searchValue
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
