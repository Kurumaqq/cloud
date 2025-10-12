import { renameDir } from "../utils/api/dirs";
import { renameFile } from "../utils/api/files";

export default function useRenameHandler(
  path,
  currentSelect,
  renamePopupValue,
  setShowRenamePopup,
  setShowBlur,
  refresh
) {
  const handleConfirm = () => {
    if (currentSelect.type == "file") {
      renameFile(
        currentSelect.path,
        `${path}/${renamePopupValue}`[0] != "/"
          ? `${path}/${renamePopupValue}`
          : renamePopupValue
      );
    } else if (currentSelect.type == "dir") {
      renameDir(
        currentSelect.path,
        `${path}/${renamePopupValue}`[0] != "/"
          ? `${path}/${renamePopupValue}`
          : renamePopupValue
      );
    }
    setShowRenamePopup(false);
    setShowBlur(false);
    refresh();
  };

  const handleCancelRename = () => {
    setShowRenamePopup(false);
    setShowBlur(false);
  };

  return { handleConfirm, handleCancelRename };q
}
