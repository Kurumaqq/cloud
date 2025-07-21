export function getPath(full_path) {
  const path = window.location.pathname;
  const a = full_path.split("/").pop();
  return a;
}
