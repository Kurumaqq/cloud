import { useEffect, useRef } from "react";
import classes from "./FullScreenVideo.module.css";

export default function FullScreenVideo({ show, setShow, src, setShowBlur }) {
  const modal = useRef(null);

  const handleClose = () => {
    setShow(false);
    setShowBlur(false);
  };

  const handleKeyDown = (e) => {
    e.preventDefault();
    if (e.key === "Escape") handleClose();
  };

  useEffect(() => {
    if (show && modal.current) {
      modal.current.focus();
    }
  }, [show]);

  return show ? (
    <>
      <button onClick={handleClose} className={classes.close}>
        <img className={classes.iconClose} src="/icons/close.svg" alt="close" />
      </button>
      <div
        ref={modal}
        tabIndex={0}
        onKeyDown={handleKeyDown}
        className={classes.modal}
      >
        <video className={classes.video} controls autoPlay src={src}></video>
      </div>
    </>
  ) : null;
}
