import { downloadFile } from "../utils/api/files";

export default function useItemContext(
  setShowItemContext,
  setShowRenamePopup,
  setShowBlur,
  setShowConfirmPopup,
  setShowContext,
  setCursorPos,
  setRenamePopupValue,
  currentSelect,
  path
) {
  const handleRename = () => {
    setShowItemContext(false);
    setShowRenamePopup(true);
    setShowBlur(true);
  };

  const handleCopy = () => {
    setShowItemContext(false);
    localStorage.setItem("copy", JSON.stringify(currentSelect));
  };

  const handleDelete = () => {
    setShowItemContext(false);
    setShowConfirmPopup(true);
    setShowBlur(true);
  };

  const handleDownload = async () => {
    setShowItemContext(false);
    await downloadFile(currentSelect.path);
  };

  const contextHandle = (e, name, type) => {
    e.preventDefault();
    e.stopPropagation();
    currentSelect.path = path != "" ? `${path}/${name}` : name;
    currentSelect.type = type;
    setRenamePopupValue(currentSelect.path.split("/").pop());
    setCursorPos({ x: e.pageX, y: e.pageY });
    setShowContext(false);
    setShowItemContext(true);
  };

  return {
    handleRename,
    handleCopy,
    handleDelete,
    handleDownload,
    contextHandle,
  };
}
