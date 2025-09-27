import { listFiles, uploadFileApi } from "./api/files";
import { listDirs } from "./api/dirs";

export const updateFiles = (path, setFiles) =>
  listFiles(path)
    .then((res) =>
      setFiles(
        res.data.files.map((f) => ({
          name: f.split("/").pop(),
          icon: "zip.svg",
        }))
      )
    )
    .catch(console.error);

export const updateDirs = (path, setDirs) =>
  listDirs(path)
    .then((res) =>
      setDirs(
        res.data.dirs.map((d) => ({
          name: d.split("/").pop(),
          icon: "folder-base.svg",
        }))
      )
    )
    .catch(console.error);

export const updateExplorer = async (path, setDirs, setFiles) => {
  await Promise.all([updateDirs(path, setDirs), updateFiles(path, setFiles)]);
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
