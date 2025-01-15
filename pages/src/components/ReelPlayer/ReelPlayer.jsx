import './ReelPlayer.css'

const ReelPlayer = ({ type }) => {

  // Generate a cache-busting query parameter
  const cacheBuster = new Date().getTime();

  const videoUrl = type === 'demo'
    ? `http://localhost:8000/upload/demo?cb=${cacheBuster}`
    : `http://localhost:8000/upload/text?cb=${cacheBuster}`;

  return (
    <div id="ReelPlayer">
      <h2>Your Generated Video:</h2>
      <video width="250" controls>
        <source src={videoUrl} type="video/mp4" />
      </video>
    </div>
  );
};

export default ReelPlayer;
