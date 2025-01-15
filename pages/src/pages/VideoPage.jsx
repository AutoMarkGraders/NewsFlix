import { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import { Button } from "@/components/ui/button"
import ReelPlayer from '../components/ReelPlayer/ReelPlayer';
import './VideoPage.css';

const VideoPage = () => {
    const location = useLocation();
    const { message, type } = location.state || { message: '', type: 'text' };
    const [showReelPlayer, setShowReelPlayer] = useState(false);

    const handleGenerateClick = () => {
        setShowReelPlayer(true);
    };

    return (
        <div className="video-page-container">
            <div className="left-half">
                <div className="grid w-full gap-1.5">
                <Label htmlFor="article">Preview the News Article</Label>
                <Textarea placeholder="Paste an article here." value={message} id="article" />
                <Button onClick={handleGenerateClick}>Generate</Button>
                </div>
            </div>
            <div className="right-half">
                {showReelPlayer && <ReelPlayer type={type} />}
            </div>
        </div>
    );
};

export default VideoPage;