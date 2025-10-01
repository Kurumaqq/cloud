import classes from "./File.module.css";

export default function File({ filename, icon, contextHandle, onClick }) {
  let icon_path = "";
  const isUrl =
    icon?.startsWith("blob:http") || icon?.startsWith("data:image/png")
      ? true
      : false;

  return (
    <div
      onDragStart={(e) => {
        e.dataTransfer.setData("text/plain", filename);
      }}
      onContextMenu={contextHandle}
      draggable={true}
      className={classes.file}
      onClick={onClick}
    >
      <img
        className={isUrl ? classes.pic : classes.icon}
        draggable={false}
        src={`${icon_path}${icon}`}
        alt="file"
        onError={(e) => {
          e.target.src = `/icons/files/${filename.split(".").pop()}.svg`;
        }}
      />
      <div className={classes.filename}>{filename}</div>
    </div>
  );
}
