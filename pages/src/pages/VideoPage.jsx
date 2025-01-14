import { useLocation } from 'react-router-dom';
import { Textarea } from "@/components/ui/textarea"
import { Label } from "@/components/ui/label"
import ReelPlayer from '../components/ReelPlayer/ReelPlayer';
import './VideoPage.css';

const VideoPage = () => {
    const location = useLocation();
    const { message } = location.state || { message: '' };

    return (
        <div className="video-page-container">
            <div className="left-half">
                <div className="grid w-full gap-1.5">
                <Label htmlFor="article">Preview the News Article</Label>
                <Textarea placeholder="Paste an article here." value={message} id="article" readOnly />
                </div>
            </div>
            <div className="right-half">
                <ReelPlayer />
            </div>
        </div>
    );
};

export default VideoPage;