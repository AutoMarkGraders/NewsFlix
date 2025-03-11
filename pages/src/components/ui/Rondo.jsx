import { useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { api } from '@/api';
import styled from "styled-components";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const Rondo = () => {
  const navigate = useNavigate();
  const imageInputRef = useRef(null);

  const handleFileInput = async (event) => {
    try {
      const file = event.target.files[0];

      if (!file) {
        throw new Error('Please select a file');
      }
      if (file.type.startsWith('image/')) {
        // Image Upload Handling
        toast.info('Processing image. Please wait...', { autoClose: 15000 });
        const formData = new FormData();
        formData.append('image', file);
        const response = await api.post('/news/image', formData, { headers: {'Content-Type': 'multipart/form-data',}, });
        const ocrText = response.data.text; // contains the text in a field named 'text'
        navigate('/video', { state: { text: ocrText, type: 'notDemo' } });
      } 
      else if (file.type === 'application/pdf') {
        toast.info('Redirecting to PDF processing...', { autoClose: 5000 });

        const reader = new FileReader();
        reader.onload = (e) => {
          const pdfData = e.target.result;
          navigate('/pdf-processing', { state: { pdfData, fileName: file.name } });
        };
        reader.readAsArrayBuffer(file);
      } else {
        throw new Error('Unsupported file type');
      }
    } catch (error) {
      toast.error('ERROR');
      console.error('Error uploading file:', error);
    }
  };

  const handleTextInput = () => {
    navigate('/video', { state: { text: '', type: 'notDemo'} });
  };

  return (
    <StyledWrapper>
      <div className="rondo">

        <p onClick={() => imageInputRef.current.click()}>
          <span>News File 📰</span>
        </p>
        <input
          type="file"
          ref={imageInputRef}
          style={{ display: 'none' }}
          onChange={handleFileInput}
        />

        <p onClick={handleTextInput}>
          <span>Article Text 📝</span>
        </p>

        <p onClick={() => navigate('/history')}>
          <span>Reel History 💾</span>
        </p>
        
      </div>
      <ToastContainer />
    </StyledWrapper>
  );
};

const StyledWrapper = styled.div`
  .rondo {
    width: 320px;
    height: 254px;
    border-radius: 14px;
    background: rgba(33, 33, 33, 0.3); /* Set transparency here */
    display: flex;
    gap: 8px;
    padding: 0.4em;
  }

  .rondo p {
    height: 100%;
    flex: 1;
    overflow: hidden;
    cursor: pointer;
    border-radius: 10px;
    transition: all 0.5s;
    background: rgba(33, 33, 33, 0.01); /* Set transparency here */
    border: 8px solid rgba(255, 255, 255, 0.8); /* Set transparency here */
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .rondo p:hover {
    flex: 4;
  }

  .rondo p span {
    min-width: 14em;
    padding: 0.5em;
    text-align: center;
    transform: rotate(-90deg);
    transition: all 0.5s;
    text-transform: none;
    font-weight: 400;
    font-size: 1.1em;
    color: rgba(255, 255, 255, 0.8); /* Set transparency here */
    letter-spacing: 0.1em;
  }

  .rondo p:hover span {
    transform: rotate(0);
  }
`;

export default Rondo;
// import { useRef } from 'react';
// import { useNavigate } from 'react-router-dom';
// import { api } from '@/api';
// import styled from "styled-components";
// import { ToastContainer, toast } from 'react-toastify';
// import 'react-toastify/dist/ReactToastify.css';
// import * as pdfjsLib from 'pdfjs-dist';
// // Set worker file path explicitly
// // Dynamically set the correct worker path for Vite
// pdfjsLib.GlobalWorkerOptions.workerSrc = new URL(
//   'pdfjs-dist/build/pdf.worker.min.mjs',
//   import.meta.url
// ).toString();

// const Rondo = () => {
//   const navigate = useNavigate();
//   const imageInputRef = useRef(null);

//   const handleImageInput = async (event) => {
//     try {
//       const file = event.target.files[0];

//       if (!file) {
//         throw new Error('Please select a file');
//       }

//       if (file.type.startsWith('image/')) {
//         // Image Upload Handling
//         toast.info('Processing image. Please wait...', { autoClose: 15000 });
//         const formData = new FormData();
//         formData.append('image', file);
//         const response = await api.post('/news/image', formData, {
//           headers: { 'Content-Type': 'multipart/form-data' },
//         });
//         const ocrText = response.data.text;
//         navigate('/video', { state: { text: ocrText, type: 'notDemo' } });
//       } 
//       else if (file.type === 'application/pdf') {
//         // PDF Processing
//         toast.info('Extracting images from PDF. Please wait...', { autoClose: 15000 });

//         const reader = new FileReader();
//         reader.onload = async (e) => {
//           const pdfData = new Uint8Array(e.target.result);
//           const pdfDoc = await pdfjsLib.getDocument({ data: pdfData }).promise;

//           let extractedImages = [];
          
//           for (let pageNum = 1; pageNum <= pdfDoc.numPages; pageNum++) {
//             const page = await pdfDoc.getPage(pageNum);
//             const scale = 2;
//             const viewport = page.getViewport({ scale });

//             const canvas = document.createElement('canvas');
//             const context = canvas.getContext('2d');
//             canvas.width = viewport.width;
//             canvas.height = viewport.height;

//             await page.render({ canvasContext: context, viewport }).promise;
//             extractedImages.push(canvas.toDataURL('image/png'));
//           }

//           if (extractedImages.length > 0) {
//             navigate('/pdf-processing', { state: { images: extractedImages } });
//           } else {
//             throw new Error('No images found in PDF');
//           }
//         };
//         reader.readAsArrayBuffer(file);
//       } else {
//         throw new Error('Unsupported file type');
//       }
//     } catch (error) {
//       toast.error('Error processing file');
//       console.error('Error:', error);
//     }
//   };

//   return (
//     <StyledWrapper>
//       <div className="rondo">
//         <p onClick={() => imageInputRef.current.click()}>
//           <span>News File 📰</span>
//         </p>
//         <input
//           type="file"
//           ref={imageInputRef}
//           style={{ display: 'none' }}
//           accept="image/*,application/pdf"
//           onChange={handleImageInput}
//         />

//         <p onClick={() => navigate('/video', { state: { text: '', type: 'notDemo' } })}>
//           <span>Article Text 📝</span>
//         </p>

//         <p onClick={() => navigate('/history')}>
//           <span>Reel History 💾</span>
//         </p>
//       </div>
//       <ToastContainer />
//     </StyledWrapper>
//   );
// };

// const StyledWrapper = styled.div`
//   .rondo {
//     width: 320px;
//     height: 254px;
//     border-radius: 14px;
//     background: rgba(33, 33, 33, 0.3);
//     display: flex;
//     gap: 8px;
//     padding: 0.4em;
//   }
//   .rondo p {
//     height: 100%;
//     flex: 1;
//     cursor: pointer;
//     border-radius: 10px;
//     transition: all 0.5s;
//     background: rgba(33, 33, 33, 0.01);
//     border: 8px solid rgba(255, 255, 255, 0.8);
//     display: flex;
//     justify-content: center;
//     align-items: center;
//   }
//   .rondo p:hover {
//     flex: 4;
//   }
//   .rondo p span {
//     min-width: 14em;
//     padding: 0.5em;
//     text-align: center;
//     transform: rotate(-90deg);
//     transition: all 0.5s;
//     text-transform: none;
//     font-weight: 400;
//     font-size: 1.1em;
//     color: rgba(255, 255, 255, 0.8);
//     letter-spacing: 0.1em;
//   }
//   .rondo p:hover span {
//     transform: rotate(0);
//   }
// `;

// export default Rondo;



























