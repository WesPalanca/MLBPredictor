import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./Pages/Home";
import LoginSignup from "./Pages/LoginSignup";
import Predict from './Pages/Predict';

const App = () =>{
  return(
    <Router>
      <Routes>
        <Route path='/' element={<Home />} />
        <Route path="/auth" element={<LoginSignup />} />
        <Route path='/predict' element={<Predict/>} />
      </Routes>
    </Router>
  )
}


export default App;