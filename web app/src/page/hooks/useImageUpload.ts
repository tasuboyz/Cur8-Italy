// import { uploadImage } from '../api/postAPI';
// import React from 'react';
// import { userId } from '../contexts/UserContext'

// export const useImageUpload = (uploadUrl: string) => {
//   const [selectedFile, setSelectedFile] = React.useState<File | null>(null);
//   const [imagePreview, setImagePreview] = React.useState<string | null>(null);
//   const [loading, setLoading] = React.useState(false);
//   const [error, setError] = React.useState<string | null>(null);

//   const handleImageChange = (event: React.ChangeEvent<HTMLInputElement>) => {
//     const file = event.target.files?.[0] || null;
//     setSelectedFile(file);
//     if (file) {
//       const reader = new FileReader();
//       reader.onloadend = () => {
//         setImagePreview(reader.result as string);
//       };
//       reader.readAsDataURL(file);
//     }
//   };

//   const uploadImage = async (): Promise<void> => {
//     if (!selectedFile) {
//       setError('Nessun file selezionato');
//       return;
//     }

//     setLoading(true);
//     setError(null);

//     try {
//       const { data, error } = await uploadImage(userId, selectedFile);
//       if (error) throw new Error(error);
//     } catch (err) {
//       setError(err);
//     } finally {
//       setLoading(false);
//     }
//   };

//   return { handleImageChange, uploadImage, imagePreview, loading, error };
// };
