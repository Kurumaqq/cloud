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
  const [constShowStar, setConstShowStar] = useState(isFavourite);
  //   if (filename === "hui.png") console.log(isFavourite);
  // const [constStarActive, setConstStarActive] = useState(false);

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
      onMouseEnter={() => (!starActive ? setStarShow(true) : null)}
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
      {starShow || constShowStar ? (
        <button
          onMouseEnter={() => setStarActive(true)}
          onMouseLeave={() => setStarActive(false)}
          className={classes.starBtn}
          onClick={(e) => {
            e.stopPropagation();
            onClickStar();
            if (constShowStar) {
              setStarShow(true);
              setConstShowStar(false);
            } else {
              setConstShowStar(true);
            }
            // else{ setConstShowStar(true)};
            // setConstShowStar(true);
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
