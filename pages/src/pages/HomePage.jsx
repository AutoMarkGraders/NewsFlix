import { useState } from 'react'
import './HomePage.css'
import Heading from '../components/Heading/Heading';
import Left from '../components/Left/Left';
import Right from '../components/Right/Right';
import ReelPlayer from '../components/ReelPlayer/ReelPlayer';
//import Card from '../components/ui/Card';

const HomePage = () => {
  const [showVideo, setShowVideo] = useState(false);

  const handleGenerateClick = () => {
    setShowVideo(true);
  };

  return ( 
    <div>
    {!showVideo ? (
      <div id="HomePage">
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

export default HomePage;
