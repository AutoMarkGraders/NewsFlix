import { useState } from 'react';
import { useLocation } from 'react-router-dom';
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
      setVideoUrl(`http://localhost:8000/news/demo?cb=${cacheBuster}`);
    }
    else {
      try {
        const response = await fetch('http://localhost:8000/news/text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: text }),
        });
        const blob = await response.blob();
        const videoObjectUrl = URL.createObjectURL(blob);
        setVideoUrl(videoObjectUrl);
      } catch (error) {
        console.error('Error fetching video:', error);
      }
    }

    setShowReelPlayer(true);
  };

  // const handleTextareaChange = (event) => {
  //   setText(event.target.value);
  // };

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