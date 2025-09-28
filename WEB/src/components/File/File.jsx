import classes from "./File.module.css";
import docIcon from "/src/assets/icons/files/document.svg";

export default function File({ text, icon, contextHandle }) {
  const icon_path = "/icons/files";

  return (
    <div
      onDragStart={(e) => {
        e.dataTransfer.setData("text/plain", text);
      }}
      onContextMenu={contextHandle}
      draggable={true}
      className={classes.file}
    >
      <img
        draggable={false}
        src={`${icon_path}/${icon}`}
        alt="file"
        onError={(e) => {
          e.target.src = docIcon;
        }}
      />
      <div className={classes.filename}>{text}</div>
    </div>
  );
}
