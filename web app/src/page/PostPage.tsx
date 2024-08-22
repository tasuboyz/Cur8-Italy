import React, { ChangeEvent } from 'react';
import './PostPage.css';
import { usePost } from './hooks/usePost';
import { TitleInput } from '../components/Form/TitleInput';
//import { CommunityInput } from '../components/Form/CommunityInput';
import { DescriptionInput } from '../components/Form/DescriptionInput';
import { TagInput } from '../components/Form/TagInput';
import { DateTimePicker } from '../components/Form/DateTimePicker';
import { SubmitButton } from '../components/Form/SubmitButton';
import useUser from './contexts/useUser';
import { postAPI } from './api/postAPI';
import { useNavigate } from 'react-router-dom';

function PostingPage() {
  
  const [titolo, setTitolo] = React.useState('');
  const [description, setDescription] = React.useState('');
  const [tag, setTag] = React.useState('steemit steemexclusive');
  const [dateTime, setDateTime] = React.useState('');
  const { user } = useUser();
  const [communityId, setCommunityId] = React.useState<string | null>(null);

  React.useEffect(() => {
    // Recuperiamo l'ID della community dal localStorage
    const savedCommunityId = localStorage.getItem('selectedCommunityId');
    if (savedCommunityId) {
      setCommunityId(savedCommunityId);
    }
  }, []);
  // const [community, setCommunity] = React.useState('');
  // const [listItems, setListItems] = React.useState<string[]>([]);
  // const [selectedItem, setSelectedItem] = React.useState<string | null>(null);
  const { sendMessage, loading } = usePost();
  const navigate = useNavigate();

  const handleTitleChange = (event: ChangeEvent<HTMLInputElement>) => {
    setTitolo(event.target.value);
  };

  const handleDescriptionChange = (event: ChangeEvent<HTMLTextAreaElement>) => {
    setDescription(event.target.value);
  };

  const handleTagChange = (event: ChangeEvent<HTMLInputElement>) => {
    setTag(event.target.value);
  };

  const handleDateTimeChange = (event: ChangeEvent<HTMLInputElement>) => {
    setDateTime(event.target.value);
  };

  // const handleCommunityChange = (event: ChangeEvent<HTMLInputElement>) => {
  //   setCommunity(event.target.value);
  // };

  // const handleButtonClick = async () => {
  //   try {
  //     const response = await postAPI.searchCommunity(community);
  //     const data = await response.data;
  //     setListItems(data.map(item => item.name));
  //   } catch (error) {
  //     console.error('Error fetching list:', error);
  //   }
  // };

  const handleButtonClick = async () => {
    try {
      navigate('/community-page');
      return
    } catch (error) {
      console.error('Error fetching list:', error);
    }
  };

  const inviaMessaggio = async (): Promise<void> => {
    const post = {
      title: titolo,
      description: description,
      tag: tag,
      dateTime: dateTime,
      userId: user.userId,
      communityId: communityId
    };
  
    await sendMessage(post);
  
    localStorage.removeItem('title');
    localStorage.removeItem('description');

    window.Telegram.WebApp.close();
  };
  

  const handleImageChange = (event: ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];

    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const imageBase64 = reader.result as string;
        handleSubmit(imageBase64);
      };
      reader.readAsDataURL(file);
    }
  };

  React.useEffect(() => {
    const savedTags = localStorage.getItem('tags');
    if (savedTags) {
      setTag(savedTags);
    }
    const savedTitle = localStorage.getItem('title');
    if (savedTitle) {
      setTitolo(savedTitle);
    }
    const savedDescription = localStorage.getItem('description');
    if (savedDescription) {
      setDescription(savedDescription);
    }
    const savedDateTime = localStorage.getItem('dateTime');
    if (savedDateTime) {
      setDateTime(savedDateTime);
    }
  }, []);

  React.useEffect(() => {
    localStorage.setItem('title', titolo);
  }, [titolo]);

  React.useEffect(() => {
    localStorage.setItem('description', description);
  }, [description]);

  React.useEffect(() => {
    localStorage.setItem('tags', tag);
  }, [tag]);

  interface Upload {
    userId: number | null;
    imageBase64: string;
  }

  const handleSubmit = async (imageBase64: string) => {
    const upload: Upload = {
      userId: user.userId,
      imageBase64: imageBase64
    };

    try {
      const response = await postAPI.uploadImage(upload);

      if (response.error) {
        throw new Error(response.error);
      }

      const data = response.data;
      const jsonString = JSON.stringify(data);
      const stringWithoutQuotes = jsonString.replace(/"/g, '');
      setDescription(prevDescription => prevDescription + '\n' + stringWithoutQuotes);
    } catch (error) {
      console.error('Errore durante l\'invio dell\'immagine:', error);
    }
  };

  // const handleItemClick = (item: string) => {
  //   setSelectedItem(item);
  // };

  return (
    <div className="container">
      <div>
      <button onClick={handleButtonClick}>Search Community</button>
        <TitleInput value={titolo} onChange={handleTitleChange} />
        <DescriptionInput value={description} onChange={handleDescriptionChange} />
        <TagInput value={tag} onChange={handleTagChange} />
        <DateTimePicker value={dateTime} onChange={handleDateTimeChange} />
        <input type="file" onChange={handleImageChange} />
        <SubmitButton onClick={inviaMessaggio} loading={loading} />
        {/* <CommunityInput
          value={community}
          onChange={handleCommunityChange}
          communities={[]} // Passa qui la tua lista di comunità
          onSelect={(community) => console.log('Community selected:', community)}
        /> */}   
      </div>
    </div>
  );
}

export default PostingPage;
