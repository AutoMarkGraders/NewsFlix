import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Auth from './components/Auth';
import HomePage from './pages/HomePage';
import VideoPage from './pages/VideoPage';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Auth />} />
        <Route path="/home" element={<HomePage />} />
        <Route path="/video" element={<VideoPage />} />
      </Routes>
    </Router>
  );
};

export default App;
