import classes from "./ContextMenu.module.css";
import Button from "./Button";
import { currentSelect } from "../../pages/Explorer/Explorer";
import { downloadFile } from "../../utils/api/files";

export default function ItemContext({
  show,
  x,
  y,
  onRename,
  onCopy,
  onDelete,
  onDownload,
}) {
//   function handleRename() {
//     setShowContext(false);
//     setShowRenamePopup(true);
//     setShowBlur(true);
//   }

//   function handleCopy() {
//     setShowContext(false);
//     localStorage.setItem("copy", JSON.stringify(currentSelect));
//   }

//   function handleDelete() {
//     setShowContext(false);
//     setShowConfirmPopup(true);
//     setShowBlur(true);
//   }

//   const handleDownload = async () => {
//     setShowContext(false);
//     await downloadFile(currentSelect.path);
//   };
  return show ? (
    <div
      className={classes.contextMenu}
      style={{ insetInlineStart: x, insetBlockStart: y }}
    >
      <ul className={classes.ul}>
        <Button onClick={onCopy} icon={"copy.svg"}>
          Сopy
        </Button>
        <Button onClick={onRename} icon={"rename.svg"}>
          Rename
        </Button>
        <Button onClick={onDownload} icon={"download.svg"}>
          Download
        </Button>
        <Button onClick={onDelete} icon={"delete.svg"}>
          Delete
        </Button>
      </ul>
    </div>
  ) : (
    <></>
  );
}
