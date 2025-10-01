import { getFile, listFiles, uploadFileApi } from "./api/files";
import { listDirs } from "./api/dirs";

export const updateFiles = async (path, setFiles) => {
  try {
    const res = await listFiles(path);

    const files = res.data.files.map((f) => ({
      name: f.split("/").pop(),
      icon: null,
    }));
    setFiles(files);

    for (const f of res.data.files) {
      const curr_path = location.pathname
        .replace("/root/", "")
        .replace(/\/{2, }/g, "/")
        .replace("/root", "");
      const name = f.split("/").pop();
      if (curr_path !== path) continue;
      const icon = await getIcon(name, path);
      setFiles((prev) =>
        prev.map((file) => (file.name === name ? { ...file, icon } : file))
      );
    }
  } catch (err) {
    console.error(err);
  }
};

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
    const videoUrl = await getFile(`${path}${filename}`);
    return await getVideoThumbnail(videoUrl);
  } else {
    return `/icons/files/${ext}.svg`;
  }
};

export const getVideoThumbnail = async (videoUrl) => {
  return new Promise((resolve, reject) => {
    const video = document.createElement("video");
    video.src = videoUrl;
    video.crossOrigin = "anonymous";
    video.muted = true;
    video.currentTime = 0.1;

    video.addEventListener("loadeddata", () => {
      video.addEventListener("canplay", () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        const thumbnail = canvas.toDataURL("image/png");
        resolve(thumbnail);
      });
    });

    video.addEventListener("error", (e) => {
      reject("Ошибка при загрузке видео: " + e);
    });
  });
};
