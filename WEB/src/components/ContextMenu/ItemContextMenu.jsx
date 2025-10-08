import classes from "./ContextMenu.module.css";
import Button from "./Button";
import { currentSelect } from "../../pages/Explorer/Explorer";
import { downloadFile } from "../../utils/api/files";

export default function ItemContextMenu({
  show,
  x,
  y,
  setShowRenamePopup,
  setShowBlur,
  setShowContext,
  setShowConfirmPopup,
}) {
  function handleRename() {
    setShowContext(false);
    setShowRenamePopup(true);
    setShowBlur(true);
  }

  function handleCopy() {
    setShowContext(false);
    localStorage.setItem("copy", JSON.stringify(currentSelect));
  }

  function handleDelete() {
    setShowContext(false);
    setShowConfirmPopup(true);
    setShowBlur(true);
  }

  const handleDownload = async () => {
    setShowContext(false);
    console.log(await downloadFile(currentSelect.path));
  };
  return show ? (
    <div
      className={classes.contextMenu}
      style={{ insetInlineStart: x, insetBlockStart: y }}
    >
      <ul className={classes.ul}>
        <Button onClick={handleCopy} icon={"copy.svg"}>
          Сopy
        </Button>
        <Button onClick={handleRename} icon={"rename.svg"}>
          Rename
        </Button>
        <Button onClick={handleDownload} icon={"download.svg"}>
          Download
        </Button>
        <Button onClick={handleDelete} icon={"delete.svg"}>
          Delete
        </Button>
      </ul>
    </div>
  ) : (
    <></>
  );
}
