export default async function Test() {
  try {
    const res = await fetch("/config.json");
    const data = await res.json();
    return data;
  } catch (err) {
    console.error(err);
  }
}
