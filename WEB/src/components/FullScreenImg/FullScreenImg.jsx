import { useState, useRef, useEffect } from "react";
import classes from "./FullScreenImg.module.css";
import { getIcon } from "../../utils/utils";

export default function FullScreenImg({
  src,
  name,
  setName,
  show,
  setShow,
  setShowBlur,
  files,
  setSrc,
  path,
}) {
  const [scale, setScale] = useState(1);
  const [position, setPosition] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [start, setStart] = useState({ x: 0, y: 0 });
  const [loaded, setLoaded] = useState(false);
  const modalRef = useRef(null);

  const handleNext = () => {
    const currentIndex = files.findIndex((f) => f.name === name);
    const picExt = ["jpg", "jpeg", "png", "gif", "bmp", "svg"];

    let nextImg = null;
    if (currentIndex !== -1) {
      for (let i = currentIndex + 1; i < files.length; i++) {
        nextImg = files.slice(currentIndex + 1).find((f) => {
          const ext = f.name.split(".").pop().toLowerCase();
          return picExt.includes(ext);
        });
        if (nextImg) {
          break;
        }
      }
      modalRef.current.focus();

      if (nextImg) {
        setScale(1);
        setPosition({ x: 0, y: 0 });

        getIcon(nextImg.name, path).then((src) => {
          setSrc(src);
          setName(nextImg.name);
        });
      }
    }
  };

  const handlePrevios = () => {
    const currentIndex = files.findIndex((f) => f.name === name);
    const picExt = ["jpg", "jpeg", "png", "gif", "bmp", "svg"];

    let prevImg = null;
    if (currentIndex !== -1) {
      for (let i = currentIndex - 1; i >= 0; i--) {
        prevImg = files
          .slice(0, currentIndex)
          .reverse()
          .find((f) => {
            const ext = f.name.split(".").pop().toLowerCase();
            console.log(picExt.includes(ext));
            return picExt.includes(ext);
          });
        if (prevImg) {
          break;
        }
      }
      modalRef.current.focus();

      if (prevImg) {
        setScale(1);
        setPosition({ x: 0, y: 0 });

        getIcon(prevImg.name, path).then((src) => {
          setSrc(src);
          setName(prevImg.name);
        });
      }
    }
  };

  const handleKeyDown = (e) => {
    e.preventDefault();
    if (e.key === "Escape") handleClose();
  };

  const handleClose = () => {
    setShow(false);
    setShowBlur(false);
    setScale(1);
    setPosition({ x: 0, y: 0 });
  };

  const handleWheel = (e) => {
    e.preventDefault();
    if (e.deltaY < 0) {
      setScale((prev) => prev + 0.3);
    } else {
      setScale((prev) => Math.max(0.3, prev - 0.3));
    }
  };

  const handleMouseDown = (e) => {
    e.preventDefault();
    setIsDragging(true);
    setStart({
      x: e.clientX - position.x,
      y: e.clientY - position.y,
    });
  };

  const handleMouseMove = (e) => {
    if (!isDragging) return;
    setPosition({
      x: e.clientX - start.x,
      y: e.clientY - start.y,
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };
  useEffect(() => {
    if (show && modalRef.current) {
      modalRef.current.focus();
    }
  }, [show, name]);

  useEffect(() => {
    if (!show) {
      setScale(0.5);
      setPosition({ x: 0, y: 0 });
    }
  }, [show]);

  useEffect(() => {
    setLoaded(false);
  }, [src]);
  return show ? (
    <>
      <button onClick={handleClose} className={classes.close}>
        <img className={classes.iconClose} src="/icons/close.svg" alt="close" />
      </button>
      <button onClick={handleNext} className={classes.next}>
        <img
          className={classes.iconNext}
          src="/icons/arrow-right.svg"
          alt="next"
        />
      </button>
      <button onClick={handlePrevios} className={classes.previos}>
        <img
          className={classes.iconPrev}
          src="/icons/arrow-left.svg"
          alt="prev"
        />
      </button>
      <div
        ref={modalRef}
        tabIndex={0}
        className={classes.modal}
        onWheel={handleWheel}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseLeave={handleMouseUp}
        onKeyDown={handleKeyDown}
      >
        <img
          src={src}
          alt="img"
          style={{
            display: loaded ? "block" : "none",
            transform: `translate(${position.x}px, ${position.y}px) scale(${scale})`,
            cursor: isDragging ? "grabbing" : "grab",
            transition: isDragging ? "none" : "transform 0.2s",
          }}
          onLoad={() => setLoaded(true)}
          onMouseDown={handleMouseDown}
        />
      </div>
    </>
  ) : null;
}
