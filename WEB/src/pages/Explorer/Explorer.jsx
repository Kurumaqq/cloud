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
import { deleteFile, renameFile } from "../../utils/api/files";
import { renameDir } from "../../utils/api/dirs";
import ConfirmPopup from "../../components/ConfirmPopup/ConfirmPopup";
import { updateExplorer, uploadFile } from "../../utils/utils";

export let currentSelect = { path: "", type: "" };
export function Explorer() {
  const location = useLocation();
  const path = location.pathname
    .replace("/root/", "")
    .replace(/\/{2,}/g, "/")
    .replace("/root", "");

  const [progressFiles, setProgressFiles] = useState([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showProgressFiles, setShowProgressFiles] = useState(false);
  const [cursorPos, setCursorPos] = useState({ x: 0, y: 0 });
  const [showContext, setShowContext] = useState(false);
  const [showRenamePopup, setShowRenamePopup] = useState(false);
  const [showCreateDirPopup, setShowCreateDirPopup] = useState(false);
  const [renamePopupValue, setRenamePopupValue] = useState(currentSelect.path);
  const [createDirPopupValue, setCreateDirPopupValue] = useState("");
  const [showConfirmPopup, setShowConfirmPopup] = useState(false);
  const [showBlur, setShowBlur] = useState(false);
  const [files, setFiles] = useState([]);
  const [dirs, setDir] = useState([]);

  const contextHandle = (e, name, type) => {
    e.preventDefault();
    currentSelect.path = path != "" ? `${path}/${name}` : name;
    currentSelect.type = type;
    setRenamePopupValue(currentSelect.path.split("/").pop());
    console.log(currentSelect.path);
    setCursorPos({ x: e.pageX, y: e.pageY });
    setShowContext(true);
  };

  const handleCreateDir = async () => {
    await createDir(`${path}/${createDirPopupValue}`);
    setCreateDirPopupValue("");
    updateExplorer(path, setDir, setFiles);
  };

  const handleRename = async () => {
    if (currentSelect.type == "file") {
      await renameFile(currentSelect.path, `${path}/${renamePopupValue}`);
    } else if (currentSelect.type == "dir") {
      await renameDir(currentSelect.path, renamePopupValue);
    }
    updateExplorer(path, setDir, setFiles);
  };

  const handleDelete = async () => {
    if (currentSelect.type == "file") {
      await deleteFile(currentSelect.path);
    } else if (currentSelect.type == "dir") {
      await deleteDir(currentSelect.path);
    }
    updateExplorer(path, setDir, setFiles);
  };

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragOver(false);

    const files = e.dataTransfer.files;
    Array.from(files).forEach(async (f) => {
      await uploadFile(f, path, setProgressFiles, setShowProgressFiles);
      updateExplorer(path, setDir, setFiles);
    });
  };

  useEffect(() => {
    updateExplorer(path, setDir, setFiles);
  }, [path, showBlur]);

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
          path={`root/${path}`}
        />
        <div className={classes.fileContainer}>
          {dirs.map((f, i) => (
            <Dir
              contextHandle={(e) => contextHandle(e, f.name, "dir")}
              key={i}
              text={f.name}
              icon={f.icon}
            />
          ))}
          {files.map((f, i) => (
            <File
              contextHandle={(e) => contextHandle(e, f.name, "file")}
              key={i}
              text={f.name}
              icon={`${f.name.split(".").pop()}.svg`}
            />
          ))}
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
    </>
  );
}
