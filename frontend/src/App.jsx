import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Layout from './components/Layout';
import Home from './pages/Home';
import './index.css';

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/planets" element={<div className="p-10"><h1>Planets Page</h1></div>} />
          <Route path="/planets/:slug" element={<div className="p-10"><h1>Planet Detail</h1></div>} />
          <Route path="/flights" element={<div className="p-10"><h1>Flights Page</h1></div>} />
          <Route path="/login" element={<div className="p-10"><h1>Login Page</h1></div>} />
          <Route path="/register" element={<div className="p-10"><h1>Register Page</h1></div>} />
          <Route path="/dashboard" element={<div className="p-10"><h1>Dashboard</h1></div>} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </Router>
  );
}

export default App;
