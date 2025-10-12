import classes from "./ConfirmPopup.module.css";
import ButtonCancel from "../ButtonCancel/ButtonCancel";
import ButtonConfirm from "../ButtonConfirm/ButtonConfirm";

export default function ConfirmPopup({
  show,
  title,
  highlight,
  onConfirm,
  onCancel,
}) {
  return show ? (
    <div className={classes.popup}>
      <p className={classes.title}>
        {title}
        <strong>{highlight.toUpperCase()}</strong>?
      </p>
      <div className={classes.actions}>
        <ButtonCancel onClick={onCancel}>No</ButtonCancel>
        <ButtonConfirm onClick={onConfirm}></ButtonConfirm>
      </div>
    </div>
  ) : null;
}
