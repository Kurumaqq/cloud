import { useState } from "react";
import classes from "./ProgressBar.module.css";

export default function ProgressBar({
  files,
  show,
  setShow,
  setProgressFiles,
}) {
  const iconDir = "/src/assets/icons/files";
  return (
    <>
      {show ? (
        <div className={classes.main}>
          <div className={classes.header}>
            <p>Upload files</p>
            <button
              className={classes.closeBtn}
              onClick={() => {
                setProgressFiles([]);
                setShow(false);
              }}
            >
              <img
                className={classes.closeIcon}
                src={"/src/assets/icons/close.svg"}
                alt="close"
              />
            </button>
          </div>
          <ul className={classes.Filelist}>
            {files
              .slice()
              .reverse()
              .map((e, i) => (
                <li key={i}>
                  <div className={classes.fileProgressBar}>
                    <div className={classes.fileTitle}>
                      <img
                        className={classes.fileIcon}
                        src={`${iconDir}/${e.name.split(".").pop()}.svg`}
                        alt="file"
                        onError={(e) => {
                          e.target.src = "/src/assets/icons/files/document.svg";
                        }}
                      />
                      <p>{e.name}</p>
                    </div>
                    <div
                      className={classes.progressBar}
                      style={{
                        background: `conic-gradient(#2a6f97 0% ${e.percent}%, #ddd 0% 100%)`,
                      }}
                    ></div>
                  </div>
                </li>
              ))}
          </ul>
        </div>
      ) : (
        <></>
      )}
    </>
  );
}
