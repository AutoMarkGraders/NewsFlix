import { useNavigate } from 'react-router-dom';
import Threed from '@/components/ui/Threed';
import Rondo from '@/components/ui/Rondo';

import './HomePage.css'

const HomePage = () => {

  const navigate = useNavigate();

  const handleDemoClick = () => {
    const demoArticle = "In recent years, there has been a growing global push to protect biodiversity as the impacts of habitat loss, pollution, and climate change drive species closer to extinction. Governments and organizations worldwide have launched initiatives to conserve biodiversity hotspots, restore damaged ecosystems, and establish new protected areas. The Kunming-Montreal Global Biodiversity Framework, adopted in 2022, aims to halt biodiversity loss by 2030, setting targets like protecting 30% of land and marine areas and restoring 20% of degraded ecosystems. Countries such as Brazil are intensifying efforts to reduce Amazon deforestation, while the U.S. has launched the “America the Beautiful” initiative to protect 30% of its lands and waters. In addition, corporations and NGOs are adopting sustainable practices and supporting reforestation projects. However, challenges such as funding, enforcement, and conflicting land-use priorities remain. Conservationists believe that a shift toward viewing ecological health as essential to economic resilience is crucial for achieving lasting impact.";
    navigate('/video', { state: { text: demoArticle, type: 'demo' } });
  };

  return ( 
    <div>
    
      <div id="HomePage">

        <div id="Heading">
          <h1>NewsToReel</h1>
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
