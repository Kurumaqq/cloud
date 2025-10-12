import { useNavigate } from "react-router-dom";

export default function useContextMenuHandler(
  path,
  setShowContext,
  setShowCreateDirPopup,
  setShowBlur,
  setCursorPos,
  setShowItemContext
) {
  const navigate = useNavigate();

  const handleBackContextMenu = () => {
    const backPath = path.split("/").slice(0, -1).join("/");
    navigate(`/root/${backPath}`);
    setShowContext(false);
  };

  const handleCreateDirContextMenu = () => {
    setShowCreateDirPopup(true);
    setShowContext(false);
    setShowBlur(true);
  };

  const handleContextMenu = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setShowItemContext(false);
    setCursorPos({ x: e.pageX, y: e.pageY });
    setShowContext(true);
  };

  return {
    handleBackContextMenu,
    handleCreateDirContextMenu,
    handleContextMenu,
  };
}
