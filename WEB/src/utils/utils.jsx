import {
  addFavFile,
  getFile,
  getVideoThumbnail,
  listFiles,
  rmFavFile,
  uploadFileApi,
} from "./api/files";
import { addFavDir, listDirs, rmFavDir } from "./api/dirs";
import config from "../../public/config.json";
import Dir from "../components/Folder/Folder";
import File from "../components/File/File";

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

const MAX_ICON_CACHE = 400;
let batchSize = 3;

const maintainCacheLimit = () => {
  const keys = Array.from(iconCache.keys());
  if (keys.length > MAX_ICON_CACHE) {
    const toDelete = keys.length - MAX_ICON_CACHE;
    for (let i = 0; i < toDelete; i++) {
      iconCache.delete(keys[i]);
    }
  }
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

    if (currentPath !== path || currentSearchValue !== searchValue) return;

    setFilesList((prev) =>
      serverFiles.map((f) => {
        const shouldShow =
          !searchValue ||
          f.name.toLowerCase().includes(searchValue.toLowerCase());

        const existing = prev.find((p) => p.name === f.name);

        return {
          name: f.name,
          icon: existing?.icon ?? null,
          favourite: f.favourite,
          show: shouldShow,
        };
      })
    );

    for (let i = 0; i < serverFiles.length; i += batchSize) {
      if (currentPath !== path || currentSearchValue !== searchValue) return;

      const videoExt = ["mp4", "mov", "avi", "mkv", "wmv", "flv", "webm"];
      const ext = serverFiles[i]["name"].split(".").pop().toLowerCase();
      batchSize = videoExt.includes(ext) ? 1 : 3;

      const batch = serverFiles.slice(i, i + batchSize);
      const icons = await Promise.all(
        batch.map((f) => getCachedIcon(f.name, path))
      );

      maintainCacheLimit();

      if (currentPath !== path || currentSearchValue !== searchValue) return;

      setFilesList((prev) =>
        prev.map((file) => {
          const match = batch.find((b) => b.name === file.name);
          if (!match || file.icon) return file;
          const icon = icons[batch.indexOf(match)];
          return { ...file, icon, favourite: match.favourite };
        })
      );

      await new Promise((r) => setTimeout(r, 10));
    }
  } catch (err) {
    console.error(err);
  }
};

export const updateDirs = async (path, setDirs, searchValue) => {
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

export const updateExplorer = async (path, setDirs, setFiles, searchValue) => {
  await Promise.all([
    updateDirs(path, setDirs, searchValue),
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
    return await getFile(`${path}${filename}`, 240);
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

export const renderFiles = (files, setFiles, path, onContext, onClick) =>
  files.map((f, i) => {
    return (
      <File
        contextHandle={(e) => onContext(e, f.name, "file")}
        onClick={() => onClick(f.name)}
        key={i}
        path={path}
        filename={f.name}
        icon={f.icon}
        show={f.show}
        isFavourite={f.favourite}
        onClickStar={async () => {
          const curr_path = path ? path + "/" : "";
          if (!f.favourite) {
            await addFavFile(`${curr_path}${f.name}`);
          } else if (f.favourite) {
            await rmFavFile(`${curr_path}${f.name}`);
          }
          setFiles((prev) =>
            prev.map((file) =>
              file.name === f.name
                ? { ...file, favourite: !file.favourite }
                : file
            )
          );
        }}
      />
    );
  });

export const renderDirs = (dirs, setDirs, files, setFiles, path, onContext) =>
  dirs.map((d, i) => (
    <Dir
      contextHandle={(e) => onContext(e, d.name, "dir")}
      key={i}
      path={path}
      name={d.name}
      icon={d.icon}
      setDirs={setDirs}
      setFiles={setFiles}
      files={files}
      show={d.show}
      isFavourite={d.favourite}
      onClickStar={async () => {
        const curr_path = path ? path + "/" : "";
        if (!d.favourite) {
          await addFavDir(`${curr_path}${d.name}`);
        } else if (d.favourite) {
          await rmFavDir(`${curr_path}${d.name}`);
        }
        setDirs((prev) =>
          prev.map((dir) =>
            dir.name === d.name ? { ...dir, favourite: !dir.favourite } : dir
          )
        );
      }}
    />
  ));
