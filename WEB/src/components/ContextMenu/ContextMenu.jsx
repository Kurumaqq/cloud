import classes from "./ContextMenu.module.css";
import Button from "./Button";
import { useNavigate } from "react-router-dom";

export default function ContextMenu({
  show,
  x,
  y,
  path,
  onRefresh,
  onBack,
  onCreateDir,
}) {
  if (!show) return null;
  const navigate = useNavigate();

  const handleBack = () => {
    path = path.split("/").slice(0, -1).join("/");
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
        <Button icon={"./back.svg"} onClick={onBack}>
          Back
        </Button>
        <Button icon={"./refresh.svg"} onClick={onRefresh}>
          Refresh
        </Button>
        <Button icon={"./plus.svg"} onClick={onCreateDir}>
          Create dir
        </Button>
      </ul>
    </div>
  );
}
