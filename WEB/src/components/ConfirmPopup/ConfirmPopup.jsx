import classes from "./ConfirmPopup.module.css";
import ButtonCancel from "../ButtonCancel/ButtonCancel";
import ButtonConfirm from "../ButtonConfirm/ButtonConfirm";

export default function ConfirmPopup({
  show,
  title,
  highlight,
  setShow,
  onConfirm,
  setShowBlur,
}) {
  function handleCancel() {
    setShow(false);
    setShowBlur(false);
  }

  function handleConfirm() {
    onConfirm();
    setShow(false);
    setShowBlur(false);
  }

  return show ? (
    <div className={classes.popup}>
      <p className={classes.title}>
        {title}
        <strong>{highlight.toUpperCase()}</strong>?
      </p>
      <div className={classes.actions}>
        <ButtonCancel onClick={handleCancel}>No</ButtonCancel>
        <ButtonConfirm onClick={handleConfirm}></ButtonConfirm>
      </div>
    </div>
  ) : null;
}
