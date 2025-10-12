import { getFile } from "../utils/api/files";
import config from "../../public/config.json";

export default function useFileHandler({
  setFullScreenImgSrc,
  setFullScreenImgName,
  setShowBlur,
  setShowFullScreenImg,
  setFullScreenVideoSrc,
  setShowFullScreenVideo,
  path,
  currentSelect,
}) {
  const handleOnClickFile = (filename) => {
    currentSelect.path = path ? path + "/" + filename : filename;
    const picExt = ["jpg", "jpeg", "png", "gif", "bmp", "svg"];
    const videoExt = ["mp4", "webm", "ogg", "mkv"];
    const ext = filename.split(".").pop().toLowerCase();
    if (picExt.includes(ext)) {
      setFullScreenImgSrc("");
      setFullScreenImgName(filename);
      setShowBlur(true);
      setShowFullScreenImg(true);
      getFile(`${path}/${filename}`).then(setFullScreenImgSrc);
    } else if (videoExt.includes(ext)) {
      setFullScreenVideoSrc("");
      setFullScreenImgName(filename);
      setShowBlur(true);
      setShowFullScreenVideo(true);
      const curr_path = path ? path + "/" : "";
      const videoUrl = `${config.APIURL}/files/get/${curr_path}${filename}`;
      setFullScreenVideoSrc(videoUrl);
    }
  };

  return { handleOnClickFile };
}
