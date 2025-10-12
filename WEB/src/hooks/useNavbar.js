import { useEffect } from "react";

export default function useNavBarHandler(
  searchValue,
  setSearchValue,
  setShowCreateDirPopup,
  setShowBlur,
  refresh
) {
  const handlePlus = () => {
    setShowCreateDirPopup(true);
    setShowBlur(true);
  };

  const onChangeSearch = async (e) => {
    const newValue = e.target.value;
    setSearchValue(newValue);
    refresh(newValue);
  };

  return { handlePlus, onChangeSearch };
}
