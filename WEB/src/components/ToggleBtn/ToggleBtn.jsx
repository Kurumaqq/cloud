import { useState } from "react";
import classes from "./ToggleBtn.module.css";

export default function ToggleBtn({ onEnable, onDisable }) {
  const [checked, setChecked] = useState(false);

  const handleChange = (e) => {
    const curr = e.target.checked;
    setChecked(curr);

    if (curr) onEnable();
    else onDisable();
  };

  return (
    <label className={classes.switch}>
      <input type="checkbox" checked={checked} onChange={handleChange} />
      <span className={`${classes.slider} ${classes.round}`}></span>
    </label>
  );
}
