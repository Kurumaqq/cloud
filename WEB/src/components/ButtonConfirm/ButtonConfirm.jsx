import classes from "./ButtonConfirm.module.css";

export default function ({ onClick }) {
  return (
    <button onClick={onClick} className={classes.confirm}>
      Confirm
    </button>
  );
}
