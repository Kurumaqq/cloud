import classes from "./Navbar.module.css";

export default function ButtonNav({ onClick, icon, alt }) {
  const baseDir = "/src/assets/icons";
  return (
    <button onClick={onClick} className={classes.btn}>
      <img
        className={classes.icon}
        draggable={false}
        src={`${baseDir}/${icon}`}
        alt={alt}
      />
    </button>
  );
}
