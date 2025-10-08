import { useState } from "react";
import classes from "./File.module.css";

export default function File({
  filename,
  icon,
  contextHandle,
  onClick,
  path,
  show,
  isFavourite,
  onClickStar,
}) {
  path ? (path += "/") : null;
  const isUrl =
    icon?.startsWith("blob:http") || icon?.startsWith("http") ? true : false;

  const [starShow, setStarShow] = useState(false);
  const [starActive, setStarActive] = useState(isFavourite);
  return show ? (
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
      onMouseEnter={() => setStarShow(true)}
      onMouseLeave={() => setStarShow(false)}
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
      {starShow || isFavourite ? (
        <button
          className={classes.starBtn}
          onMouseEnter={() => setStarActive(true)}
          onMouseLeave={() => setStarActive(false)}
          onClick={(e) => {
            e.stopPropagation();
            onClickStar();
          }}
        >
          <img
            className={classes.starIcon}
            src={`/icons/${
              isFavourite || starActive ? "star-active" : "star-inactive"
            }.svg`}
            alt=""
          />
        </button>
      ) : null}
    </div>
  ) : null;
}
