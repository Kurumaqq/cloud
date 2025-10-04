import classes from "./File.module.css";

export default function File({ filename, icon, contextHandle, onClick, path }) {
  path ? (path += "/") : null;
  const isUrl =
    icon?.startsWith("blob:http") || icon?.startsWith("http") ? true : false;

  return (
    <div
      onDragStart={(e) => {
        e.dataTransfer.setData(
          "text/plain",
          JSON.stringify({
            filename: `${path}${filename}`,
            type: "file",
          })
        );
      }}
      onContextMenu={contextHandle}
      draggable={true}
      className={classes.file}
      onClick={onClick}
    >
      <img
        className={isUrl ? classes.pic : classes.icon}
        draggable={false}
        src={icon ? icon : `/icons/files/${filename.split(".").pop()}.svg`}
        alt="file"
        onError={(e) => {
          e.target.src = `/icons/files/document.svg`;
        }}
      />
      <div className={classes.filename}>{filename}</div>
    </div>
  );
}
