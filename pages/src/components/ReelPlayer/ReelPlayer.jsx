import './ReelPlayer.css'

const ReelPlayer = () => {
  return (
    <div id="ReelPlayer">
      <h2>Your Generated Video:</h2>
      <video width="250" controls>
        <source src="http://localhost:8000/upload/demo" type="video/mp4" />
      </video>
    </div>
  );
};

export default ReelPlayer;
