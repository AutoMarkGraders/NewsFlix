import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { API_URL } from '../api';
import { api } from '../api';
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { FaWhatsapp, FaFacebook, FaLink} from "react-icons/fa";
import { FaXTwitter } from "react-icons/fa6";
import './VideoPage.css';

const VideoPage = () => {
  const location = useLocation();
  const { text: initialText, type } = location.state || { text: '', type: 'notDemo' };
  const [text, setText] = useState(initialText);
  const [showReelPlayer, setShowReelPlayer] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');
  const [shareUrl, setShareUrl] = useState('https://res.cloudinary.com/news-to-reel/video/upload/v1738601524/qmcggdivy9soww6farbb.mp4');

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
        const blob = response.data;
        const videoObjectUrl = URL.createObjectURL(blob);
        setVideoUrl(videoObjectUrl);

        // Upload the video to Cloudinary
        const formData = new FormData();
        formData.append('file', blob);
        formData.append('upload_preset', 'upload_reels');

        const cloudinaryResponse = await fetch(`https://api.cloudinary.com/v1_1/news-to-reel/video/upload`,
          {method: 'POST', body: formData,}
        );

        const cloudinaryData = await cloudinaryResponse.json();
        setShareUrl(cloudinaryData.secure_url);

        alert('Reel Generated!');

      } catch (error) {
        alert('ERROR');
        console.error('Error fetching video:', error);
      }
    }

    setShowReelPlayer(true);
  };


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
          <div className="grid">

            <h2 className='headingg'>Generated News Reel</h2>

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
                onClick={() => window.open(`https://wa.me/?text=Check out this AI powered video generated using NewsToReel: ${shareUrl}`, "_blank")}
                style={{background: "none",border: "none",cursor: "pointer",fontSize: "40px",color: "#25D366",}}
              >
              <FaWhatsapp />
              </button>

              {/* Twitter Button */}
              <button
                onClick={() => window.open(`https://twitter.com/intent/tweet?url=${shareUrl}&text=Check out this AI powered video generated using NewsToReel!`, "_blank")}
                style={{background: "none",border: "none",cursor: "pointer",fontSize: "40px",color: "#000",}}
              >
              <FaXTwitter />
              </button>

              {/* Copy Link Button */}
              <button
                onClick={() => { navigator.clipboard.writeText(shareUrl); alert('Reel sharable link copied!'); }}
                style={{background: "white", border: "none", borderRadius: "50%", cursor: "pointer", fontSize: "25px", color: "#000", width: "40px", height: "40px", display: "flex", justifyContent: "center", alignItems: "center"}}
              >
              <FaLink />
              </button>
            </div>

          </div>
        )}
      </div>
      
    </div>
  );

};

export default VideoPage;