import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
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
    } else {
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

  const handleChange = (event) => {
    setText(event.target.value);
  };

  return (
    <div className="video-page-container">

      <div className="left-half">
        <div className="grid w-full gap-1.5">
          <Label htmlFor="article">Preview the News Article</Label>
          <Textarea
            placeholder="Paste an article here."
            value={text}
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
            <video width="300" controls>
              <source src={videoUrl} type="video/mp4" />
            </video>
          </div>
        )}
      </div>
      
    </div>
  );

};

export default VideoPage;