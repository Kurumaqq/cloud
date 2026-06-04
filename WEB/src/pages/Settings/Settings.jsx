import { useState } from "react";
import SidebarSettings from "../../components/SidebarSettings/SidebarSettings";
import classes from "./Settings.module.css";
import General from "./General";
import Users from "./User";
import ToggleBtn from "../../components/ToggleBtn/ToggleBtn";

export default function Settings() {
  const [state, setState] = useState("general");
  const stateMap = { general: <General />, users: <Users /> };

  return (
    <div className={classes.container}>
      <div className={classes.sideBar}>
        <h2>Settings</h2>
        <SidebarSettings onClick={() => setState("general")}>
          General
        </SidebarSettings>
        <SidebarSettings onClick={() => setState("users")}>
          Users
        </SidebarSettings>
        <SidebarSettings onClick={() => setState("statistics")}>
          Statistics
        </SidebarSettings>
        <SidebarSettings onClick={() => setState("apearence")}>
          Appearance
        </SidebarSettings>
      </div>
      <div className={classes.content}>{stateMap[state]}</div>
    </div>
  );
}
