import React from 'react';
import './CommunityPage.css';
import '../App.css'
import { Telegram } from "@twa-dev/types";
import { Box, List, ListItem, ListItemText, Container, TextField } from '@mui/material';
import { useNavigate } from 'react-router-dom';

declare global {
  interface Window {
    Telegram: Telegram;
  }
}

function PostingPage() {
  const [communityNames, setCommunityNames] = React.useState<Array<string>>([]);
  const [community, setCommunity] = React.useState<string>('');
  const navigate = useNavigate();

  const SearchCommunity = React.useCallback(async (): Promise<void> => {
    const headers = {
        "accept": "application/json",
        "authorization": "Bearer my-secret",
        "Content-Type": "application/json"
    };

    const post = {
      community: community
    };

    try {
        const response = await fetch(`/community`, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(post)
        });

        if (!response.ok) {
            throw new Error('Errore durante l\'invio del messaggio');
        }
        const data = await response.json(); 
        // const parsedCommunities = data.data.map((item: string) => {
        //   const [id, name] = item.split(',');
        //   console.log(id)
        //   return data.data;
        // });
        setCommunityNames(data.data);
    } catch (error) {
        window.Telegram.WebApp.showPopup({
            title: "Errore",
            message: "Si è verificato un errore durante l'invio del messaggio.",
            buttons: [{ type: 'ok' }]
        });
        console.error('Errore durante l\'invio del messaggio:', error);
    }
  }, [community]);

  React.useEffect(() => {
    window.Telegram.WebApp.BackButton.show();

    window.Telegram.WebApp.BackButton.onClick(() => {
      window.Telegram.WebApp.BackButton.hide();
      navigate('/post');
    });

    SearchCommunity();
    scrollList();
  }, [navigate, SearchCommunity]);

  const scrollList = () => {
    const listElement = document.getElementById('list');
    if (listElement) {
      listElement.scrollBy(0, 100); // Scorre di 100px
    }
  };

  const handleCommunityChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setCommunity(event.target.value);
  };

  // const handleCommunitySelect = (selectedName: string) => {
  //   setCommunity(selectedName);
  // };

  const handleCommunitySelect = (selectedName: string, selectedId: string) => {
    setCommunity(selectedName);
    localStorage.setItem('selectedCommunityId', selectedId);
    localStorage.setItem('selectedCommunityName', selectedName);
    window.Telegram.WebApp.BackButton.hide();
    navigate('/post');
  };

  return (
    <div className="container-community">
    <Container>
      <Box className="container-community" sx={{ padding: 2 }}>
        <TextField
          id = 'community-input' 
          label="Search Community"
          value={community}
          onChange={handleCommunityChange}
          fullWidth
          variant="outlined"
          className="community-search"
        />
        <Box id="list" sx={{ height: '400px', overflowY: 'scroll', marginTop: 2 }}>
          <List>
          {communityNames.map((item, index) => {
          const [id, name] = item.split(',');
          return (
            <ListItem button key={index} onClick={() => handleCommunitySelect(name, id)}>
              <ListItemText primary={name} />
            </ListItem>
            );
          })}
          </List>
        </Box>
      </Box>
    </Container>
    </div>
  );
}

export default PostingPage;
