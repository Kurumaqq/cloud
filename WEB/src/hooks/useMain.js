import { useCallback } from "react";
import { uploadFile } from "../utils/utils";

export default function useMainHandlers(
  setShowItemContext,
  setShowContext,
  setIsDragOver,
  path,
  setProgressFiles,
  setShowProgressFiles,
  setDirs,
  setFiles,
  refresh
) {
  const handleClick = useCallback(() => {
    setShowItemContext(false);
    setShowContext(false);
  }, [setShowItemContext, setShowContext]);

  const handleDragOver = useCallback(
    (e) => {
      e.preventDefault();
      if (e.dataTransfer.types.includes("Files")) setIsDragOver(true);
    },
    [setIsDragOver]
  );

  const handleDragLeave = useCallback(
    (e) => {
      e.preventDefault();
      if (e.dataTransfer.types.includes("Files")) setIsDragOver(false);
    },
    [setIsDragOver]
  );

  const handleDrop = async (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const files = e.dataTransfer.files;
    await Promise.all(
      Array.from(files).map((f) =>
        uploadFile(
          f,
          path,
          setProgressFiles,
          setShowProgressFiles,
          setDirs,
          setFiles
        )
      )
    );
    refresh();
  };

  return { handleClick, handleDragOver, handleDragLeave, handleDrop };
}
