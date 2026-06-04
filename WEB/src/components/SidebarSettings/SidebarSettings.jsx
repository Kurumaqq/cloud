import classes from "./SidebarSettings.module.css";

export default function SidebarSettings({ children, onClick }) {
  return (
    <button onClick={onClick} className={classes.btn}>
      {children}
    </button>
  );
}
