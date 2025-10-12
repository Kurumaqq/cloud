import { deleteFile } from "../utils/api/files";
import { deleteDir } from "../utils/api/dirs";

export default function useDeleteHandler(
  setShowBlur,
  setShowConfirmPopup,
  currentSelect,
  refresh
) {
  const handleDeleteConfirm = async () => {
    setShowBlur(false);
    setShowConfirmPopup(false);
    if (currentSelect.type == "file") {
      await deleteFile(currentSelect.path);
    } else if (currentSelect.type == "dir") {
      await deleteDir(currentSelect.path);
    }
    refresh();
  };

  const handleDeleteCancel = () => {
    setShowConfirmPopup(false);
    setShowBlur(false);
  };

  return {
    handleDeleteConfirm,
    handleDeleteCancel,
  };
}
