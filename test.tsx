import React, { useState } from 'react';

function Preview({ title, description, imageUrl }) {
  return (
    <div className="preview">
      <h2>{title}</h2>
      <p>{description}</p>
      {imageUrl && <img src={imageUrl} alt="Preview" />}
    </div>
  );
}

function PostingPage() {
  const [titolo, setTitolo] = useState('');
  const [description, setDescription] = useState('');
  const [imageUrl, setImageUrl] = useState('');

  const handleTitleChange = (event) => {
    setTitolo(event.target.value);
  };

  const handleDescriptionChange = (event) => {
    setDescription(event.target.value);
    const urlMatch = event.target.value.match(/(https?:\/\/.*\.(?:png|jpg|jpeg|gif))/i);
    if (urlMatch) {
      setImageUrl(urlMatch[0]);
    } else {
      setImageUrl('');
    }
  };

  return (
    <div className="container">
      <TitleInput value={titolo} onChange={handleTitleChange} />
      <DescriptionInput value={description} onChange={handleDescriptionChange} />
      <Preview title={titolo} description={description} imageUrl={imageUrl} />
      <SubmitButton onClick={inviaMessaggio} loading={loading} />
    </div>
  );
}

export default PostingPage;
