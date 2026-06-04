import { useEffect, useState } from "react";
import classes from "./Navbar.module.css";
import ButtonNav from "./ButtonNav";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import config from "../../../public/config.json";

export default function Navbar({
  path,
  handlePlus,
  searchValue,
  onChangeSearch,
}) {
  const [pathValue, setPath] = useState(path);
  const [showLogoutBtn, setShowLogoutBtn] = useState(false);
  const navigate = useNavigate();

  function handleBack() {
    path = path.split("/").slice(0, -1).join("/");
    navigate(`/${path}`);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      pathValue === "" ? navigate("/root") : navigate(`/${pathValue}`);
    }
  }

  async function handleLeaveUser() {
    try {
      await axios.post(
        `${config.APIURL}/logout`,
        {},
        { withCredentials: true }
      );
      navigate("/login");
    } catch (err) {
      console.error("Ошибка при выходе:", err);
    }
  }

  useEffect(() => {
    setPath(path);
  }, [path]);

  return (
    <nav className={classes.navbar}>
      <button
        className={classes.settingsBtn}
        onClick={() => navigate("/settings")}
      >
        <img src="/icons/settings.svg" alt="settings" />
      </button>
      <div className={classes.containerCenter}>
        <ul>
          <li className={classes.li}>
            <ButtonNav onClick={handleBack} icon={"back.svg"} alt={"back"} />
          </li>
          <li className={classes.li}>
            <ButtonNav
              onClick={() => navigate("/root")}
              icon={"home.svg"}
              alt={"home"}
            />
          </li>
          <li className={classes.li}>
            <ButtonNav onClick={handlePlus} icon={"plus.svg"} alt={"plus"} />
          </li>
          <li className={classes.li}>
            <ButtonNav
              onClick={() => window.location.reload()}
              icon={"refresh.svg"}
              alt={"refresh"}
            />
          </li>
        </ul>
        <input
          onKeyDown={handleKeyDown}
          className={classes.path}
          value={pathValue}
          onChange={(e) => setPath(e.target.value)}
        ></input>
        <input
          onChange={onChangeSearch}
          className={classes.search}
          placeholder="search"
          value={searchValue}
        ></input>
      </div>
      <div className={classes.userProfile}>
        <button
          className={classes.profileBtn}
          onClick={() => setShowLogoutBtn((prev) => !prev)}
        >
          <img src="/icons/user.svg" alt="user" />
        </button>
        <button
          onClick={async () => await handleLeaveUser()}
          className={
            showLogoutBtn
              ? `${classes.logoutBtn} ${classes.show}`
              : classes.logoutBtn
          }
        >
          logout
        </button>{" "}
      </div>
    </nav>
  );
}
