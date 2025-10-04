import { useNavigate } from "react-router-dom";
import classes from "./Folder.module.css";
import { copyFile, deleteFile, moveFile } from "../../utils/api/files";
import { updateExplorer } from "../../utils/utils";
export default function Dir({
  name,
  icon,
  contextHandle,
  path,
  files,
  setFiles,
  setDirs,
}) {
  const icon_path = "/icons/folder";
  const navigate = useNavigate();
  path ? (path += "/") : null;

  function openFolder() {
    navigate(name);
  }

  return (
    <div
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
        // debugger;
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
    </div>
  );
}
