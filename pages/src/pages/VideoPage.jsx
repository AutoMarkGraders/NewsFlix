import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import './VideoPage.css';

const VideoPage = () => {
  const location = useLocation();
  const { message: initialMessage, type } = location.state || { message: '', type: 'text' };
  const [message, setMessage] = useState(initialMessage);
  const [showReelPlayer, setShowReelPlayer] = useState(false);
  const [videoUrl, setVideoUrl] = useState('');

  const handleGenerateClick = async () => {
    const cacheBuster = new Date().getTime();

    if (type === 'demo') {
      setVideoUrl(`http://localhost:8000/news/demo?cb=${cacheBuster}`);
    } else {
      try {
        const response = await fetch('http://localhost:8000/news/text', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: message }),
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

  const handleChange = (event) => {
    setMessage(event.target.value);
  };

  return (
    <div className="video-page-container">
      <div className="left-half">
        <div className="grid w-full gap-1.5">
          <Label htmlFor="article">Preview the News Article</Label>
          <Textarea
            placeholder="Paste an article here."
            value={message}
            id="article"
            onChange={handleChange}
          />
          <Button onClick={handleGenerateClick}>Generate</Button>
        </div>
      </div>
      <div className="right-half">
        {showReelPlayer && (
          <div id="ReelPlayer">
            <h2>Your Generated Video:</h2>
            <video width="250" controls>
              <source src={videoUrl} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
          </div>
        )}
      </div>
    </div>
  );

};

export default VideoPage;