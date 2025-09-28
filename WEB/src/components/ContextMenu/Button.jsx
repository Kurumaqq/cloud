import classes from "./ContextMenu.module.css";

export default function Button({ children, icon, onClick }) {
  const baseDir = "/icons";
  return (
    <button onClick={onClick} className={classes.button}>
      <img className={classes.icon} src={`${baseDir}/${icon}`} alt="" />
      <span className={classes.title}>{children}</span>
    </button>
  );
}
