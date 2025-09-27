import classes from "./ButtonCancel.module.css";

export default function ({ onClick }) {
  return (
    <button onClick={onClick} className={classes.cancel}>
      Cancel
    </button>
  );
}
