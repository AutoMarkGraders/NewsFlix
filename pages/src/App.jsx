import { useState } from 'react'
import './App.css'
import Heading from './components/Heading/Heading';
import Left from './components/Left/Left';
import Right from './components/Right/Right';
import ReelPlayer from './components/ReelPlayer/ReelPlayer';
import Card from './components/ui/Card';

const App = () => {
  const [showVideo, setShowVideo] = useState(false);

  const handleGenerateClick = () => {
    setShowVideo(true);
  };

  return ( 
    <div>
    {!showVideo ? (
      <div id="App">
        <Heading />
        <Right handleGenerateClick={handleGenerateClick} />
        <Left />
      </div>
    ) : (
      <ReelPlayer />
    )}
    </div>
  )
};

export default App
