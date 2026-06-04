import classes from "./ButtonConfirm.module.css";

export default function ({ children, onClick }) {
  return (
    <button onClick={onClick} className={classes.confirm}>
      {children || "Confirm"}
    </button>
  );
}
