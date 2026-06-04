import ToggleBtn from "../../components/ToggleBtn/ToggleBtn";
import classes from "./Settings.module.css";
import ButtonConfirm from "../../components/ButtonConfirm/ButtonConfirm";

export default function General() {
  return (
    <div className={classes.container}>
      <div className={classes.settingsPart}>
        <span className={classes.settingsDesc}>Restart QCloud</span>
        <ButtonConfirm> Restart</ButtonConfirm>
      </div>
      <div className={classes.settingsPart}>
        <span className={classes.settingsDesc}>Toggle star</span>
        <ToggleBtn></ToggleBtn>
      </div>
      <div className={classes.settingsPart}>
        <span className={classes.settingsDesc}> Data path</span>
        <input className={classes.inputData} type="text" />
      </div>
      <div className={classes.settingsPart}>
        <span className={classes.settingsDesc}>Api URL</span>
        <input className={classes.inputData} type="text" />
      </div>
      <div className={classes.settingsChangePassword}>
        <span className={classes.settingsDesc}>
          Change password for kurumaqq
        </span>
        <div className={classes.passwordSection}>
          <span>Current password</span>
          <input className={classes.inputData} type="text" />
        </div>
        <div className={classes.passwordSection}>
          <span>New password</span>
          <input className={classes.inputData} type="text" />
        </div>
      </div>
    </div>
  );
}
