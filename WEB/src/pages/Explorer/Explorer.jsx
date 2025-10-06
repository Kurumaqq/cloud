import { useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";
import File from "../../components/File/File";
import ProgressBar from "../../components/ProgressBar/ProgressBar";
import Dir from "../../components/Folder/Folder";
import classes from "./Explorer.module.css";
import ContextMenu from "../../components/ContextMenu/ContextMenu";
import NamePopup from "../../components/NamePopup/NamePopup";
import BlurBg from "../../components/Blurbg/Blurbg";
import { createDir, deleteDir } from "../../utils/api/dirs";
import {
  addFavFile,
  deleteFile,
  getFile,
  renameFile,
  rmFavFile,
} from "../../utils/api/files";
import { renameDir } from "../../utils/api/dirs";
import ConfirmPopup from "../../components/ConfirmPopup/ConfirmPopup";
import FullScreenImg from "../../components/FullScreenImg/FullScreenImg";
import FullScreenVideo from "../../components/FullScreenVideo/FullScreenVideo";
import config from "../../../public/config.json";
import {
  getIcon,
  updateExplorer,
  updateFiles,
  uploadFile,
} from "../../utils/utils";
// import { useNavigate } from "react-router-dom";

export let currentSelect = { path: "", type: "" };
export function Explorer() {
  const location = useLocation();
  const path = location.pathname
    .replace("/root/", "")
    .replace(/\/{2,}/g, "/")
    .replace("/root", "");
  const navigate = useNavigate();
  const [searchValue, setSearchValue] = useState("");
  const [progressFiles, setProgressFiles] = useState([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showProgressFiles, setShowProgressFiles] = useState(false);
  const [cursorPos, setCursorPos] = useState({ x: 0, y: 0 });
  const [showContext, setShowContext] = useState(false);
  const [showRenamePopup, setShowRenamePopup] = useState(false);
  const [showCreateDirPopup, setShowCreateDirPopup] = useState(false);
  const [renamePopupValue, setRenamePopupValue] = useState(currentSelect.path);
  const [createDirPopupValue, setCreateDirPopupValue] = useState("");
  const [showFullScreenImg, setShowFullScreenImg] = useState(false);
  const [showFullScreenVideo, setShowFullScreenVideo] = useState(false);
  const [fullScreenImgSrc, setFullScreenImgSrc] = useState("");
  const [fullScreenVideoSrc, setFullScreenVideoSrc] = useState("");
  const [fullScreenImgName, setFullScreenImgName] = useState("");
  const [showConfirmPopup, setShowConfirmPopup] = useState(false);
  const [showBlur, setShowBlur] = useState(false);
  const [files, setFiles] = useState([]);
  const [dirs, setDirs] = useState([]);

  //   console.log(files);
  const contextHandle = (e, name, type) => {
    e.preventDefault();
    currentSelect.path = path != "" ? `${path}/${name}` : name;
    currentSelect.type = type;
    setRenamePopupValue(currentSelect.path.split("/").pop());
    setCursorPos({ x: e.pageX, y: e.pageY });
    setShowContext(true);
  };

  const handleCreateDir = async () => {
    await createDir(`${path}/${createDirPopupValue}`);
    setCreateDirPopupValue("");
    updateExplorer(path, setDirs, setFiles, files, navigate);
  };

  const handleOnClickFile = (filename) => {
    const picExt = ["jpg", "jpeg", "png", "gif", "bmp", "svg"];
    const videoExt = ["mp4", "webm", "ogg", "mkv"];
    const ext = filename.split(".").pop().toLowerCase();
    if (picExt.includes(ext)) {
      setFullScreenImgSrc("");
      setFullScreenImgName(filename);
      setShowBlur(true);
      setShowFullScreenImg(true);
      getIcon(filename, path).then(setFullScreenImgSrc);
    } else if (videoExt.includes(ext)) {
      setFullScreenVideoSrc("");
      setFullScreenImgName(filename);
      setShowBlur(true);
      setShowFullScreenVideo(true);
      const curr_path = path ? path + "/" : "";
      const videoUrl = `${
        config.APIURL
      }/files/get/${curr_path}${filename}?token=${localStorage.getItem(
        "accessToken"
      )}`;
      setFullScreenVideoSrc(videoUrl);
    }
  };

  const handleRename = async () => {
    if (currentSelect.type == "file") {
      await renameFile(
        currentSelect.path,
        `${path}/${renamePopupValue}`[0] != "/"
          ? `${path}/${renamePopupValue}`
          : renamePopupValue
      );
    } else if (currentSelect.type == "dir") {
      await renameDir(
        currentSelect.path,
        `${path}/${renamePopupValue}`[0] != "/"
          ? `${path}/${renamePopupValue}`
          : renamePopupValue
      );
    }
    updateExplorer(path, setDirs, setFiles, files, navigate);
  };

  const handleDelete = async () => {
    if (currentSelect.type == "file") {
      await deleteFile(currentSelect.path);
    } else if (currentSelect.type == "dir") {
      await deleteDir(currentSelect.path);
    }
    updateExplorer(path, setDirs, setFiles, files, navigate);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    await Promise.all(
      Array.from(files).map((f) =>
        uploadFile(
          f,
          path,
          setProgressFiles,
          setShowProgressFiles,
          setDirs,
          setFiles
        )
      )
    );
    updateExplorer(path, setDirs, setFiles, files, navigate, searchValue);
  };

  useEffect(() => {
    if (showFullScreenImg || showFullScreenVideo) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
  }, [showFullScreenImg, showFullScreenVideo]);

  useEffect(() => {
    updateExplorer(path, setDirs, setFiles, files, navigate);
  }, [location.pathname]);
  return (
    <>
      <BlurBg show={showBlur}></BlurBg>
      <main
        className={`${classes.main} ${isDragOver ? classes.dragOver : ""}`}
        onClick={() => setShowContext(false)}
        onDragOver={(e) => {
          e.preventDefault();
          if (e.dataTransfer.types.includes("Files")) setIsDragOver(true);
        }}
        onDragLeave={(e) => {
          e.preventDefault();
          setIsDragOver(false);
        }}
        onDrop={handleDrop}
      >
        <Navbar
          setShowCreateDirPopup={setShowCreateDirPopup}
          setShowBlur={setShowBlur}
          path={`root/${decodeURIComponent(path)}`}
          searchValue={searchValue}
          setSearchValue={setSearchValue}
          onChangeSearch={(e) => {
            setSearchValue(e.target.value);
            updateExplorer(
              path,
              setDirs,
              setFiles,
              files,
              navigate,
              e.target.value
            );
          }}
          files={files}
        />
        <div className={classes.fileContainer}>
          {dirs.map((f, i) => (
            <Dir
              contextHandle={(e) => contextHandle(e, f.name, "dir")}
              key={i}
              path={path}
              name={f.name}
              icon={f.icon}
              setDirs={setDirs}
              setFiles={setFiles}
              files={files}
              show={f.show}
            />
          ))}
          {files.map((f, i) => {
            return (
              <File
                contextHandle={(e) => contextHandle(e, f.name, "file")}
                onClick={() => handleOnClickFile(f.name)}
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
          })}
        </div>
        <ProgressBar
          setShow={setShowProgressFiles}
          show={showProgressFiles}
          files={progressFiles}
          setProgressFiles={setProgressFiles}
        />
      </main>
      <NamePopup
        title={"Rename"}
        value={renamePopupValue}
        show={showRenamePopup}
        onChange={(e) => setRenamePopupValue(e.target.value)}
        setShow={setShowRenamePopup}
        setShowBlur={setShowBlur}
        onConfirm={handleRename}
      ></NamePopup>
      <NamePopup
        title={"Name directory"}
        value={createDirPopupValue}
        onChange={(e) => setCreateDirPopupValue(e.target.value)}
        show={showCreateDirPopup}
        setShow={setShowCreateDirPopup}
        setShowBlur={setShowBlur}
        onConfirm={handleCreateDir}
      ></NamePopup>
      <ConfirmPopup
        show={showConfirmPopup}
        title={"Are you sure delete "}
        highlight={currentSelect.path.split("/").pop()}
        setShow={setShowConfirmPopup}
        setShowBlur={setShowBlur}
        onConfirm={handleDelete}
      ></ConfirmPopup>
      <ContextMenu
        x={cursorPos.x}
        y={cursorPos.y}
        setShowContext={setShowContext}
        setShowBlur={setShowBlur}
        setShowRenamePopup={setShowRenamePopup}
        show={showContext}
        setShowConfirmPopup={setShowConfirmPopup}
      ></ContextMenu>
      <FullScreenImg
        src={fullScreenImgSrc}
        setSrc={setFullScreenImgSrc}
        show={showFullScreenImg}
        setShow={setShowFullScreenImg}
        setShowBlur={setShowBlur}
        files={files}
        name={fullScreenImgName}
        setName={setFullScreenImgName}
        setFullScreenImgSrc={setFullScreenImgSrc}
        path={path}
      ></FullScreenImg>
      <FullScreenVideo
        src={fullScreenVideoSrc}
        setShow={setShowFullScreenVideo}
        setShowBlur={setShowBlur}
        show={showFullScreenVideo}
      />
    </>
  );
}
