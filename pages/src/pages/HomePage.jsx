import { useNavigate } from 'react-router-dom';
import Threed from '../components/ui/Threed';
import Rondo from '../components/ui/Rondo';

import './HomePage.css'

const HomePage = () => {

  const navigate = useNavigate();

  const handleDemoClick = () => {
    const demoArticle = "Slovenian handball team makes it to Paris Olympics semifinal Lille, 8 August - Slovenia defeated Norway 33:28 in the Olympic men's handball tournament in Lille late on Wednesday to advance to the semifinal where they will face Denmark on Friday evening. This is the best result the team has so far achieved at the Olympic Games and one of the best performances in the history of Slovenia's team sports squads.";
    navigate('/video', { state: { text: demoArticle, type: 'demo' } });
  };

  return ( 
    <div>
    
      <div id="HomePage">

        <div id="Heading">
          <h1>NEWS TO REEL</h1>
        </div>

        <div id="Demo">
          <Threed handleDemoClick={handleDemoClick} />
        </div>

        <div id="Left">
          <Rondo />
        </div>

      </div>
  
    </div>
  )
};

export default HomePage;
