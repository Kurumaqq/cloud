import { useNavigate } from "react-router-dom";
import classes from "./Folder.module.css";
import { copyFile, deleteFile, moveFile } from "../../utils/api/files";
import { updateExplorer } from "../../utils/utils";
import { useState } from "react";
export default function Dir({
  name,
  icon,
  contextHandle,
  path,
  files,
  setFiles,
  setDirs,
  show,
  isFavourite,
  onClickStar,
}) {
  const [starShow, setStarShow] = useState(false);
  const [starActive, setStarActive] = useState(false);
  const icon_path = "/icons/folder";
  const navigate = useNavigate();

  function openFolder() {
    navigate(name);
  }

  return show ? (
    <div
      onMouseEnter={() => setStarShow(true)}
      onMouseLeave={() => setStarShow(false)}
      onClick={openFolder}
      draggable={true}
      onDragStart={(e) => {
        e.dataTransfer.setData(
          "text/plain",
          JSON.stringify({
            path: `${path}${name}`,
            type: "dir",
          })
        );
      }}
      onDragOver={(e) => {
        e.preventDefault();
      }}
      onDrop={async (e) => {
        e.preventDefault();
        const sourceFile = JSON.parse(
          e.dataTransfer.getData("text/plain")
        ).filename;
        try {
          await moveFile(sourceFile, `${path}${name}`);

          await updateExplorer(path, setDirs, setFiles, files, navigate);
        } catch (err) {
          console.error("Ошибка при drag & drop:", err);
        }
      }}
      onContextMenu={contextHandle}
      className={classes.folder}
    >
      <img draggable={false} src={`${icon_path}/${icon}`} alt="folder" />
      <div className={classes.foldername}>{name}</div>
      {starShow || isFavourite ? (
        <button
          onMouseEnter={() => setStarActive(true)}
          onMouseLeave={() => setStarActive(false)}
          onClick={(e) => {
            e.stopPropagation();
            onClickStar();
          }}
          className={classes.starBtn}
        >
          <img
            className={classes.starIcon}
            src={`/icons/${
              starActive || isFavourite ? "star-active" : "star-inactive"
            }.svg`}
            alt=""
          />
        </button>
      ) : null}
    </div>
  ) : null;
}
