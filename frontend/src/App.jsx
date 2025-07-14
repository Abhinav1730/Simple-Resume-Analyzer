import "./App.css";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import UploadResume from "./components/UploadResume";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadResume />} />
      </Routes>
    </Router>
  );
}

export default App;
