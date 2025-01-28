import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { API_URL } from '../api';
import { api } from '../api';
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { FaWhatsapp, FaFacebook } from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";
import './VideoPage.css';

const VideoPage = () => {
  const location = useLocation();
  const { text: initialText, type } = location.state || { text: '', type: 'notDemo' };
  const [text, setText] = useState(initialText);
  const [showReelPlayer, setShowReelPlayer] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');

  const handleGenerateClick = async () => {
    const cacheBuster = new Date().getTime();

    if (type === 'demo') {
      setVideoUrl(`${API_URL}/news/demo?cb=${cacheBuster}`);
      alert('Reel Generated!');
    }
    else {
      try {
        alert('Generating Reel. Please wait...');
        const response = await api.post('/news/text', { text }, { responseType: 'blob' });
        const videoObjectUrl = URL.createObjectURL(response.data);
        setVideoUrl(videoObjectUrl);
        alert('Reel Generated!');

      } catch (error) {
        alert('ERROR');
        console.error('Error fetching video:', error);
      }
    }

    setShowReelPlayer(true);
  };

 // TODO set as url to vid uploaded in cloud  
  const shareUrl = window.location.href;

  return (
    <div id="vp-container">

      <div id="lhs">
        <div className="grid w-full gap-1.5">
          <h2 className='headingg'>Preview the News Article</h2>
          <Textarea id="article"
            placeholder="Paste an article here."
            value={text}
            onChange={(event) => setText(event.target.value)}
          />
          <Button onClick={handleGenerateClick}>Generate</Button>
        </div>
      </div>

      <div id="rhs">
        {showReelPlayer && (
          <div id="ReelPlayer">

            <h2 className='headingg'>Generated Video:</h2>

            <video controls>
              <source src={videoUrl} type="video/mp4" />
            </video>

            <div id='socials'>
              {/* Facebook Button */}
              <button
                onClick={() => window.open(`https://www.facebook.com/sharer/sharer.php?u=${shareUrl}`, "_blank")}
                style={{background: "white",border: "none",borderRadius: "50%",cursor: "pointer",fontSize: "40px",color: "#4267B2",}}
              >
              <FaFacebook />
              </button>

              {/* WhatsApp Button */}
              <button
                onClick={() => window.open(`https://wa.me/?text=Check out this video: ${shareUrl}`, "_blank")}
                style={{background: "none",border: "none",cursor: "pointer",fontSize: "40px",color: "#25D366",}}
              >
              <FaWhatsapp />
              </button>

              {/* Twitter Button */}
              <button
                onClick={() => window.open(`https://twitter.com/intent/tweet?url=${shareUrl}&text=Check out this video!`, "_blank")}
                style={{background: "none",border: "none",cursor: "pointer",fontSize: "40px",color: "#000",}}
              >
              <FaXTwitter />
              </button>
            </div>

          </div>
        )}
      </div>
      
    </div>
  );

};

export default VideoPage;