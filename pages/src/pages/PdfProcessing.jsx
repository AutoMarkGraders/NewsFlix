import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState, useRef } from 'react';
import * as pdfjsLib from 'pdfjs-dist';
import styled from 'styled-components';
import { toast } from 'react-toastify';
import Slider from 'react-slick';
import Modal from 'react-modal';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';

pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).toString();

Modal.setAppElement('#root');

const PdfProcessing = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { pdfData, fileName } = location.state || {};

  const [images, setImages] = useState([]);
  const [selectedImage, setSelectedImage] = useState(null);
  const [modalIsOpen, setModalIsOpen] = useState(false);
  const [cropBox, setCropBox] = useState(null);
  const [croppedImage, setCroppedImage] = useState(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [startPos, setStartPos] = useState(null);
  const imageRef = useRef(null);

  useEffect(() => {
    if (!pdfData) {
      toast.error('No PDF file provided');
      navigate('/');
      return;
    }

    const extractImages = async () => {
      try {
        const pdfDoc = await pdfjsLib.getDocument({ data: pdfData.slice(0) }).promise;
        let extractedImages = [];

        for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
          const page = await pdfDoc.getPage(pageNum);
          const scale = 1;
          const viewport = page.getViewport({ scale });

          const canvas = document.createElement('canvas');
          const context = canvas.getContext('2d');
          canvas.width = viewport.width;
          canvas.height = viewport.height;

          await page.render({ canvasContext: context, viewport }).promise;
          extractedImages.push(canvas.toDataURL('image/png'));
        }

        setImages(extractedImages);
      } catch (error) {
        toast.error('Error processing PDF');
        console.error('PDF Processing Error:', error);
      }
    };

    extractImages();
  }, [pdfData, navigate]);

  const handleImageClick = (imageSrc) => {
    setSelectedImage(imageSrc);
    setModalIsOpen(true);
  };

  const handleMouseDown = (e) => {
    const rect = imageRef.current.getBoundingClientRect();
    setStartPos({ x: e.clientX - rect.left, y: e.clientY - rect.top });
    setIsDrawing(true);
    setCropBox(null);
  };

  const handleMouseMove = (e) => {
    if (!isDrawing || !startPos) return;
    const rect = imageRef.current.getBoundingClientRect();
    setCropBox({
      x: Math.min(startPos.x, e.clientX - rect.left),
      y: Math.min(startPos.y, e.clientY - rect.top),
      width: Math.abs(e.clientX - rect.left - startPos.x),
      height: Math.abs(e.clientY - rect.top - startPos.y),
    });
  };

  const handleMouseUp = () => {
    setIsDrawing(false);
  };

  const cropImage = async () => {
    if (!selectedImage || !cropBox || !imageRef.current) return;

    const img = new Image();
    img.src = selectedImage;
    await new Promise((resolve) => (img.onload = resolve));

    const rect = imageRef.current.getBoundingClientRect();
    const scaleX = img.width / rect.width;
    const scaleY = img.height / rect.height;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = cropBox.width * scaleX;
    canvas.height = cropBox.height * scaleY;

    ctx.drawImage(
      img,
      cropBox.x * scaleX, cropBox.y * scaleY, canvas.width, canvas.height,
      0, 0, canvas.width, canvas.height
    );

    setCroppedImage(canvas.toDataURL('image/png'));
  };

  return (
    <StyledContainer>
      <h2>Viewing: {fileName}</h2>
      <SliderContainer>
        <Slider dots={true} infinite={false} speed={500} slidesToShow={3} slidesToScroll={1}>
          {images.map((imageSrc, index) => (
            <ImageSlide key={index} onClick={() => handleImageClick(imageSrc)}>
              <img src={imageSrc} alt={`PDF Page ${index + 1}`} />
            </ImageSlide>
          ))}
        </Slider>
      </SliderContainer>

      <Modal isOpen={modalIsOpen} onRequestClose={() => setModalIsOpen(false)}>
        <CloseButton onClick={() => setModalIsOpen(false)}>✖</CloseButton>
        <h3>Zoom & Crop</h3>
        <CropContainer onMouseDown={handleMouseDown} onMouseMove={handleMouseMove} onMouseUp={handleMouseUp}>
          <img ref={imageRef} src={selectedImage} alt="Zoomed" style={{ width: '100%', height: 'auto' }} />
          {cropBox && (
            <CropOverlay style={{ left: cropBox.x, top: cropBox.y, width: cropBox.width, height: cropBox.height }} />
          )}
        </CropContainer>
        <CropButton onClick={cropImage}>Crop</CropButton>
        {croppedImage && <CroppedImage src={croppedImage} alt="Cropped" />}
      </Modal>
    </StyledContainer>
  );
};

const StyledContainer = styled.div` text-align: center; padding: 10px; `;
const SliderContainer = styled.div` margin: 10px auto; width: 90%; max-width: 1200px; `;
const ImageSlide = styled.div` text-align: center; padding: 5px; cursor: pointer; `;
const CropContainer = styled.div` position: relative; width: 100%; height: auto; background: #000; `;
const CropOverlay = styled.div` position: absolute; border: 2px dashed red; background: rgba(255, 0, 0, 0.2); `;
const CloseButton = styled.button`
  position: absolute;
  top: 10px;
  right: 10px;
  background: red;
  color: white;
  border: none;
  padding: 8px 12px;
  font-size: 18px;
  cursor: pointer;
  border-radius: 50%;
  z-index: 1000;
  transition: background 0.3s;

  &:hover {
    background: darkred;
  }
`;

const CropButton = styled.button` margin-top: 10px; padding: 10px; background: #28a745; color: white; border: none; cursor: pointer; `;
const CroppedImage = styled.img` display: block; margin-top: 10px; max-width: 100%; border: 2px solid #007bff; `;

export default PdfProcessing;
