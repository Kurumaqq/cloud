import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/Login/Login";
import { Explorer } from "./pages/Explorer/Explorer";
import Redirect from "./pages/Redirect";
export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/root/*" element={<Explorer />} />
        <Route path="/login" element={<Login />} />
        <Route path="/download" element={<div />} />
        <Route path="/" element={<Redirect />} />
      </Routes>
    </Router>
  );
}
