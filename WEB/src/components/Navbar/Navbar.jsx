import { useEffect, useState } from "react";
import classes from "./Navbar.module.css";
import ButtonNav from "./ButtonNav";
import { useNavigate } from "react-router-dom";

export default function Navbar({
  path,
  setShowCreateDirPopup,
  setShowBlur,
  searchValue,
  setSearchValue,
  files,
  onChangeSearch,
}) {
  const [pathValue, setPath] = useState(path);
  const navigate = useNavigate();

  function handleBack() {
    path = path.split("/").slice(0, -1).join("/");
    console.log(path);
    navigate(`/${path}`);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") {
      pathValue === "" ? navigate("/root") : navigate(`/${pathValue}`);
    }
  }

  function handlePlus() {
    setShowCreateDirPopup(true);
    setShowBlur(true);
  }

  useEffect(() => {
    setPath(path);
  }, [path]);

  return (
    <nav className={classes.navbar}>
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
    </nav>
  );
}
