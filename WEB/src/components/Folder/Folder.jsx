import { useLocation, useNavigate } from "react-router-dom";
import classes from "./Folder.module.css";
export default function Dir({ text, icon, contextHandle }) {
  const icon_path = "/icons/folder";
  const navigate = useNavigate();
  const location = useLocation();

  function openFolder() {
    navigate(text);
  }

  return (
    <div
      onClick={openFolder}
      onDragStart={(e) => {
        e.dataTransfer.setData("text/plain", text);
      }}
      onDragOver={(e) => {
        e.preventDefault();
      }}
      onDrop={(e) => {
        e.preventDefault();
        const sourceFile = e.dataTransfer.getData("text/plain");
        console.log(text, sourceFile);
      }}
      onContextMenu={contextHandle}
      className={classes.folder}
    >
      <img draggable={false} src={`${icon_path}/${icon}`} alt="folder" />
      <div className={classes.foldername}>{text}</div>
    </div>
  );
}
