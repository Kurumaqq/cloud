import classes from "./ContextMenu.module.css";
import Button from "./Button";
import { useNavigate } from "react-router-dom";

export default function ContextMenu({
  show,
  setShow,
  x,
  y,
  path,
  setShowCreateDir,
  setShowBlur,
}) {
  if (!show) return null;
  const navigate = useNavigate();

  const handleRefresh = () => {
    window.location.reload();
    setShow(false);
  };

  const handleBack = () => {
    console.log(path);
    path = path.split("/").slice(0, -1).join("/");
    console.log(path);
    navigate(`/root/${path}`);
    setShow(false);
  };

  const handleCreateDir = () => {
    setShowCreateDir(true);
    setShow(false);
    setShowBlur(true);
  };

  return (
    <div
      className={classes.contextMenu}
      style={{ insetInlineStart: x, insetBlockStart: y }}
    >
      <ul className={classes.ul}>
        <Button icon={"./paste.svg"}>Paste</Button>
        <Button icon={"./back.svg"} onClick={handleBack}>
          Back
        </Button>
        <Button icon={"./refresh.svg"} onClick={handleRefresh}>
          Refresh
        </Button>
        <Button icon={"./plus.svg"} onClick={handleCreateDir}>
          Create dir
        </Button>
      </ul>
    </div>
  );
}
