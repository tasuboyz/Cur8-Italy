import React, { useState, useEffect, ChangeEvent } from 'react';
import { Telegram } from "@twa-dev/types";
import { useNavigate } from 'react-router-dom';
import { CommunityInput } from '../components/Form/CommunityInput';
import { postAPI } from './api/postAPI';

declare global {
  interface Window {
    Telegram: Telegram;
  }
}

interface Community {
  id: string;
  name: string;
}

const CommunityPage: React.FC = () => {
  const [communities, setCommunities] = useState<Community[]>([]);
  const [selectedCommunity, setSelectedCommunity] = useState<Community | null>(null);
  const [showList, setShowList] = useState(false);
  const navigate = useNavigate();
  const [community, setCommunity] = useState('');

  useEffect(() => {
    window.Telegram.WebApp.BackButton.show();

    window.Telegram.WebApp.BackButton.onClick(() => {
      window.Telegram.WebApp.BackButton.hide();
      navigate('/post');
    });    
   
  }, [navigate]);

  const fetchCommunities = async () => {
    try {
      const response = await postAPI.searchCommunity('');

      if (response.error) {
        throw new Error(response.error);
      }

      const data = response.data;
      const firstFiveItems = data.slice(0, 5).map(item => item.name).join(', ');
      window.Telegram.WebApp.showPopup({
        title: "Comunità selezionata",
        message: `Hai selezionato: ${firstFiveItems}`,
        buttons: [{ type: 'ok' }]
      });
      setCommunities(data);
    } catch (error) {
      console.error('Errore durante il fetch delle comunità:', error);
    }
  };

  const handleCommunityChange = (event: ChangeEvent<HTMLInputElement>) => {
    setCommunity(event.target.value);
  };

  const handleCommunitySelect = (community: Community) => {
    setSelectedCommunity(community);
    window.Telegram.WebApp.showPopup({
      title: "Comunità selezionata",
      message: `Hai selezionato: ${community.name}`,
      buttons: [{ type: 'ok' }]
    });
  };

  const handleShowList = () => {
    fetchCommunities();
    setShowList(true);
  };

  return (
    <div>
      <h1>Seleziona una Comunità</h1>
      <CommunityInput
        value={community}
        onChange={handleCommunityChange}
        communities={[]} // Passa qui la tua lista di comunità
        onSelect={(community) => console.log('Community selected:', community)}
      />
      <button onClick={handleShowList}>Mostra Elenco</button>
      {showList && (
        <div className="scrollable-list">
          <ul>
            {communities.map((community) => (
              <li
                key={community.id}
                className={selectedCommunity?.id === community.id ? 'selected' : ''}
                onClick={() => handleCommunitySelect(community)}
              >
                {community.name}
              </li>
            ))}
          </ul>
        </div>
      )}
      {selectedCommunity && (
        <div>
          <h2>Comunità selezionata: {selectedCommunity.name}</h2>
        </div>
      )}
    </div>
  );
};

export default CommunityPage;
