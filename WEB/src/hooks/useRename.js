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
  const handleConfirm = async () => {
    if (currentSelect.type == "file") {
      await renameFile(
        currentSelect.path,
        `${path}/${renamePopupValue}`[0] != "/"
          ? `${path}/${renamePopupValue}`
          : renamePopupValue
      );
    } else if (currentSelect.type == "dir") {
      await renameDir(
        currentSelect.path,
        `${path}/${renamePopupValue}`[0] != "/"
          ? `${path}/${renamePopupValue}`
          : renamePopupValue
      );
    }
    setShowRenamePopup(false);
    setShowBlur(false);
    await refresh();
  };

  const handleCancelRename = () => {
    setShowRenamePopup(false);
    setShowBlur(false);
  };

  return { handleConfirm, handleCancelRename };
  q;
}
