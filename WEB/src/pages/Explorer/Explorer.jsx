import { useCallback, useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import Navbar from "../../components/Navbar/Navbar";
import ProgressBar from "../../components/ProgressBar/ProgressBar";
import classes from "./Explorer.module.css";
import ItemContext from "../../components/ContextMenu/ItemContext";
import NamePopup from "../../components/NamePopup/NamePopup";
import BlurBg from "../../components/Blurbg/Blurbg";
import ContextMenu from "../../components/ContextMenu/ContextMenu";
import ConfirmPopup from "../../components/ConfirmPopup/ConfirmPopup";
import FullScreenVideo from "../../components/FullScreenVideo/FullScreenVideo";
import { renderDirs, renderFiles, updateExplorer } from "../../utils/utils";
import useMainHandlers from "../../hooks/useMain";
import useNavBarHandler from "../../hooks/useNavbar";
import useContextMenuHandler from "../../hooks/useContextMenu";
import useRenameHandler from "../../hooks/useRename";
import useCreateDirHandler from "../../hooks/useCreateDir";
import useDeleteHandler from "../../hooks/useDelete";
import useItemContext from "../../hooks/useItemContext";
import useFileHandler from "../../hooks/useFile";
import FullScreenImg from "../../components/FullScreenImg/FullScreenImg";

export let currentSelect = { path: "", type: "" };
export function Explorer() {
  const location = useLocation();
  const path = location.pathname
    .replace("/root/", "")
    .replace(/\/{2,}/g, "/")
    .replace("/root", "");
  const [searchValue, setSearchValue] = useState("");
  const [progressFiles, setProgressFiles] = useState([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const [showProgressFiles, setShowProgressFiles] = useState(false);
  const [cursorPos, setCursorPos] = useState({ x: 0, y: 0 });
  const [showItemContext, setShowItemContext] = useState(false);
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

  const refresh = useCallback(
    (value) => {
      const effectiveValue = value !== undefined ? value : searchValue;
      updateExplorer(path, setDirs, setFiles, effectiveValue);
    },
    [path, searchValue]
  );

  const {
    handleClick: handleOnClickMain,
    handleDragOver: handleDragOverMain,
    handleDragLeave: handleDragLeaveMain,
    handleDrop: handleDropMain,
  } = useMainHandlers(
    setShowItemContext,
    setShowContext,
    setIsDragOver,
    path,
    setProgressFiles,
    setShowProgressFiles,
    setDirs,
    setFiles,
    refresh
  );

  const { handlePlus: handlePlusNavbar, onChangeSearch } = useNavBarHandler(
    searchValue,
    setSearchValue,
    setShowCreateDirPopup,
    setShowBlur,
    refresh
  );

  const {
    handleBackContextMenu,
    handleCreateDirContextMenu,
    handleContextMenu,
  } = useContextMenuHandler(
    path,
    setShowContext,
    setShowCreateDirPopup,
    setShowBlur,
    setCursorPos,
    setShowItemContext
  );

  const { handleConfirm: handleConfirmRename, handleCancelRename } =
    useRenameHandler(
      path,
      currentSelect,
      renamePopupValue,
      setShowRenamePopup,
      setShowBlur,
      refresh
    );

  const { handleCreateDirConfirm, handleCreateDirCancel } = useCreateDirHandler(
    path,
    setShowCreateDirPopup,
    setShowBlur,
    setCreateDirPopupValue,
    createDirPopupValue,
    refresh
  );

  const { handleDeleteConfirm, handleDeleteCancel } = useDeleteHandler(
    setShowBlur,
    setShowConfirmPopup,
    currentSelect,
    refresh
  );

  const {
    handleCopy: handleCopyItemContext,
    handleDelete: handleDeleteItemContext,
    handleDownload: handleDownloadItemContext,
    contextHandle: contextItemHandle,
    handleRename: handleRenameItemContext,
  } = useItemContext(
    setShowItemContext,
    setShowRenamePopup,
    setShowBlur,
    setShowConfirmPopup,
    setShowContext,
    setCursorPos,
    setRenamePopupValue,
    currentSelect,
    path
  );

  const { handleOnClickFile } = useFileHandler({
    setFullScreenImgSrc,
    setFullScreenImgName,
    setShowBlur,
    setShowFullScreenImg,
    setFullScreenVideoSrc,
    setShowFullScreenVideo,
    path,
    currentSelect,
  });

  const onCloseProgressBar = () => {
    setProgressFiles([]);
    setShowProgressFiles(false);
  };

  useEffect(() => {
    if (showFullScreenImg || showFullScreenVideo) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
  }, [showFullScreenImg, showFullScreenVideo]);

  useEffect(() => {
    updateExplorer(path, setDirs, setFiles, searchValue);
  }, [location.pathname]);

  return (
    <>
      <BlurBg show={showBlur}></BlurBg>
      <main
        onContextMenu={(e) => handleContextMenu(e)}
        className={`${classes.main} ${isDragOver ? classes.dragOver : ""}`}
        onClick={handleOnClickMain}
        onDragOver={(e) => handleDragOverMain(e)}
        onDragLeave={(e) => handleDragLeaveMain(e)}
        onDrop={handleDropMain}
      >
        <Navbar
          handlePlus={handlePlusNavbar}
          path={`root/${decodeURIComponent(path)}`}
          searchValue={searchValue}
          onChangeSearch={(e) => onChangeSearch(e)}
        />
        <div className={classes.fileContainer}>
          {/* TODO: Take out in const renderDirs and renderFiles */}
          {renderDirs(dirs, setDirs, files, setFiles, path, contextItemHandle)}
          {renderFiles(
            files,
            setFiles,
            path,
            contextItemHandle,
            handleOnClickFile
          )}
        </div>
        <ProgressBar
          show={showProgressFiles}
          files={progressFiles}
          onClose={onCloseProgressBar}
        />
      </main>
      <ContextMenu
        show={showContext}
        path={path}
        x={cursorPos.x}
        y={cursorPos.y}
        onBack={handleBackContextMenu}
        onRefresh={() => window.location.reload()}
        onCreateDir={handleCreateDirContextMenu}
      ></ContextMenu>
      <NamePopup
        title={"Rename"}
        value={renamePopupValue}
        show={showRenamePopup}
        onChange={(e) => setRenamePopupValue(e.target.value)}
        onConfirm={handleConfirmRename}
        onCancel={handleCancelRename}
      ></NamePopup>
      <NamePopup
        title={"Name directory"}
        value={createDirPopupValue}
        show={showCreateDirPopup}
        onChange={(e) => setCreateDirPopupValue(e.target.value)}
        onConfirm={handleCreateDirConfirm}
        onCancel={handleCreateDirCancel}
      ></NamePopup>
      <ConfirmPopup
        show={showConfirmPopup}
        title={"Are you sure delete "}
        highlight={currentSelect.path.split("/").pop()}
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
      ></ConfirmPopup>
      <ItemContext
        x={cursorPos.x}
        y={cursorPos.y}
        show={showItemContext}
        onRename={handleRenameItemContext}
        onCopy={handleCopyItemContext}
        onDelete={handleDeleteItemContext}
        onDownload={async () => handleDownloadItemContext()}
      ></ItemContext>
      <FullScreenImg
        src={fullScreenImgSrc}
        name={fullScreenImgName}
        setName={setFullScreenImgName}
        show={showFullScreenImg}
        setShowBlur={setShowBlur}
        setShow={setShowFullScreenImg}
        files={files}
        setSrc={setFullScreenImgSrc}
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
