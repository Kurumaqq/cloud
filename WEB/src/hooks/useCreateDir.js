import { createDir } from "../utils/api/dirs";

export default function useCreateDirHandler(
  path,
  setShowCreateDirPopup,
  setShowBlur,
  setCreateDirPopupValue,
  createDirPopupValue,
  refresh
) {
  const handleCreateDirConfirm = async () => {
    setShowCreateDirPopup(false);
    setShowBlur(false);
    await createDir(`${path}/${createDirPopupValue}`);
    setCreateDirPopupValue("");
    refresh();
  };

  const handleCreateDirCancel = () => {
    setShowCreateDirPopup(false);
    setShowBlur(false);
  };

  return {
    handleCreateDirConfirm,
    handleCreateDirCancel,
  };
}
