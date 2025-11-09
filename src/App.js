import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import Home from './components/Home/Home';
import Login from './components/Auth/Login';
import SignUp from './components/Auth/SignUp';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css'; // <-- ADD THIS LINE

function App() {
  return (
    <Router>
      <AuthProvider>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/" element={<Home />} />
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}

export default App;
