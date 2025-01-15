import { useState } from 'react'
import { useNavigate } from 'react-router-dom';
import './HomePage.css'
import Heading from '../components/Heading/Heading';
import Right from '../components/Right/Right';
import Rondo from '../components/ui/Rondo';

//import ReelPlayer from '../components/ReelPlayer/ReelPlayer';
//import Card from '../components/ui/Card';

const HomePage = () => {
  //const [showVideo, setShowVideo] = useState(false);

  const navigate = useNavigate();

  const handleDemoClick = () => {
    const demoArticle = "Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads.";
    navigate('/video', { state: { message: demoArticle, type: 'demo' } });
  };

  return ( 
    <div>
    
      <div id="HomePage">
        <Heading />
        <Right handleDemoClick={handleDemoClick} />
        <div id="Left">
          <Rondo />
        </div>
      </div>
  
    </div>
  )
};

export default HomePage;
