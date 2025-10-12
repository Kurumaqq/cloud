import { useRef } from "react";
import { useEffect } from "react";
import classes from "./NamePopup.module.css";
import ButtonCancel from "../ButtonCancel/ButtonCancel";
import ButtonConfirm from "../ButtonConfirm/ButtonConfirm";

export default function NamePopup({
  show,
  title,
  value,
  onChange,
  onConfirm,
  onCancel,
}) {
  const inputRef = useRef(null);
  useEffect(() => {
    if (show) {
      inputRef.current.select();
    }
  }, [show]);

  function handleKeyDown(e) {
    if (e.key === "Escape") onCancel();
    if (e.key === "Enter") onConfirm();
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
        <ButtonCancel onClick={onCancel}></ButtonCancel>
        <ButtonConfirm onClick={onConfirm}></ButtonConfirm>
      </div>
    </div>
  ) : (
    <></>
  );
}
