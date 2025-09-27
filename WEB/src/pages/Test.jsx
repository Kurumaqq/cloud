import { useState } from "react";

export default function Test() {
  const [files, setFiles] = useState([1, 2]);

  function add() {
    setFiles([...files, files.length + 1]);
  }

  return (
    <>
      {files.map((file, index) => (
        <h1 key={index}>{file}</h1>
      ))}
      <button onClick={add}>add</button>
    </>
  );
}
