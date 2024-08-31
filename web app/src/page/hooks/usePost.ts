import React from 'react';
import { postAPI } from '../api/postAPI';
import useUser from '../contexts/useUser';

export const usePost = () => {
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);
  const { user } = useUser(); 

  const sendMessage = async (post: { title: string; description: string; tag: string; dateTime: string; }) => {
    setLoading(true);
    setError(null);
    try {
      const response = await postAPI.submit({ ...post, userId: user.userId });
      if (response.error) {
        setError(response.error);
      }
    } catch (err) {
      window.Telegram.WebApp.showPopup({
      title: "Errore",
      message: `${error}`,
      buttons: [{ type: 'ok' }]});
      setError('Errore durante l\'invio del messaggio');
    } finally {
      setLoading(false);
    }
  };

  return { sendMessage, loading, error };
};
