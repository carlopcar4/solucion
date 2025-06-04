import CouncilList from './pages/Councils';
import Login from './pages/Login';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CreateAccount from './pages/CreateAccount';
import CreateCouncil from './pages/CreateCouncil';
import ContentCouncil from './pages/Council.jsx'

import './App.css'

function App() {
  return (
    <Routes>
      <Route path='/' element={<CouncilList />} />
      <Route path='/login' element={<Login />} />
      <Route path='/createAccount' element={<CreateAccount />} />
      <Route path='/CreateCouncil' element={<CreateCouncil />} />
      <Route path='/councils/:id' element={<ContentCouncil />} />
    </Routes>
  );
}

export default App;