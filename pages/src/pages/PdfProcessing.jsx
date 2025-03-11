import { useLocation, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist';
import styled from 'styled-components';
import { toast } from 'react-toastify';

// Ensure the correct worker path
pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url
).toString();

const PdfProcessing = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { pdfData, fileName } = location.state || {};

  const [images, setImages] = useState([]);

  useEffect(() => {
    if (!pdfData) {
      toast.error('No PDF file provided');
      navigate('/');
      return;
    }

    const extractImages = async () => {
      try {
        const pdfDoc = await pdfjsLib.getDocument({ data: new Uint8Array(pdfData) }).promise;
        let extractedImages = [];

        for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
          const page = await pdfDoc.getPage(pageNum);
          const scale = 2;
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

  const handleImageSelection = (imageSrc) => {
    navigate('/video', { state: { text: imageSrc, type: 'notDemo' } });
  };

  return (
    <StyledContainer>
      <h2>Processing: {fileName}</h2>
      <p>Click on an image to proceed.</p>
      <div className="images-container">
        {images.length > 0 ? (
          images.map((imageSrc, index) => (
            <img
              key={index}
              src={imageSrc}
              alt={`PDF Page ${index + 1}`}
              onClick={() => handleImageSelection(imageSrc)}
            />
          ))
        ) : (
          <p>Extracting pages...</p>
        )}
      </div>
    </StyledContainer>
  );
};

const StyledContainer = styled.div`
  text-align: center;
  padding: 20px;

  .images-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    justify-content: center;
  }

  img {
    width: 150px;
    height: auto;
    cursor: pointer;
    border: 2px solid #fff;
    transition: transform 0.2s;

    &:hover {
      transform: scale(1.1);
    }
  }
`;

export default PdfProcessing;


// import { useLocation, useNavigate } from 'react-router-dom';
// import styled from 'styled-components';

// const PdfProcessing = () => {
//   const location = useLocation();
//   const navigate = useNavigate();
//   const { images } = location.state || { images: [] };

//   const handleImageSelection = (imageSrc) => {
//     navigate('/video', { state: { text: imageSrc, type: 'notDemo' } });
//   };

//   return (
//     <StyledContainer>
//       <h2>Select an Image from PDF</h2>
//       <div className="images-container">
//         {images.length > 0 ? (
//           images.map((imageSrc, index) => (
//             <img
//               key={index}
//               src={imageSrc}
//               alt={`PDF Page ${index + 1}`}
//               onClick={() => handleImageSelection(imageSrc)}
//             />
//           ))
//         ) : (
//           <p>No images found in PDF</p>
//         )}
//       </div>
//     </StyledContainer>
//   );
// };

// const StyledContainer = styled.div`
//   text-align: center;
//   padding: 20px;

//   .images-container {
//     display: flex;
//     flex-wrap: wrap;
//     gap: 10px;
//     justify-content: center;
//   }

//   img {
//     width: 150px;
//     height: auto;
//     cursor: pointer;
//     border: 2px solid #fff;
//     transition: transform 0.2s;

//     &:hover {
//       transform: scale(1.1);
//     }
//   }
// `;

// export default PdfProcessing;
