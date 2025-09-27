import classes from "./BlurBg.module.css";

export default function BlurBg({ show }) {
  return show ? <div className={classes.blur}></div> : null;
}
