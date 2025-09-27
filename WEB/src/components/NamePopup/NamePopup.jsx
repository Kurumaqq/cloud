import { useRef } from "react";
import { useEffect } from "react";
import classes from "./NamePopup.module.css";
import ButtonCancel from "../ButtonCancel/ButtonCancel";
import ButtonConfirm from "../ButtonConfirm/ButtonConfirm";

export default function NamePopup({
  show,
  setShow,
  value,
  onChange,
  setShowBlur,
  title,
  onConfirm,
}) {
  const inputRef = useRef(null);
  useEffect(() => {
    if (show) {
      inputRef.current.select();
    }
  }, [show]);

  function handleConfirm() {
    setShow(false);
    setShowBlur(false);
    onConfirm();
  }
  function handleCancel() {
    setShow(false);
    setShowBlur(false);
  }

  function handleKeyDown(e) {
    if (e.key === "Escape") handleCancel();
    if (e.key === "Enter") handleConfirm();
  }

  return show ? (
    <div onKeyDown={handleKeyDown} className={classes.renamePopup}>
      <p>{title}</p>
      <input
        ref={inputRef}
        onKeyDown={handleKeyDown}
        onChange={onChange}
        value={value}
        type="text"
        className={classes.input}
      />
      <div className={classes.btnContainer}>
        <ButtonCancel onClick={handleCancel}></ButtonCancel>
        <ButtonConfirm onClick={handleConfirm}></ButtonConfirm>
      </div>
    </div>
  ) : (
    <></>
  );
}
