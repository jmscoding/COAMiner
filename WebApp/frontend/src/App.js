import Topbar from "./components/topbar/Topbar";
import Sidebar from "./components/sidebar/sidebar"
import Home from "./pages/home/Home";
import relevantArticle from "./pages/relevantArticle/relevantArticle";
import UserList from "./pages/userList/UserList";
import "./App.css"
import {BrowserRouter as Router, Routes, Route} from "react-router-dom"

function App() {
  return (
    <Router>
      <Topbar/>
      <div className="container">
        <Sidebar/>
        <Routes>
          <Route exact path="/" element={<Home />}  />
          {/*<Route path="/coa" element={<COA />} /> */}        
          <Route path="/relevant" element={<relevantArticle />} />       
          <Route path="/userList" element={<UserList />} />
        </Routes>
        
      </div>
    </Router>
  );
}

export default App;
