import { useState, useEffect, ChangeEvent } from 'react';

interface FormState {
  title: string;
  description: string;
  tag: string;
  dateTime: string;
}

export const useFormState = (): [FormState, (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void, (newDescription: string) => void] => {
  const [formState, setFormState] = useState<FormState>({
    title: '',
    description: '',
    tag: 'steemit steemexclusive',
    dateTime: '',
  });

  useEffect(() => {
    const savedTitle = localStorage.getItem('title');
    const savedDescription = localStorage.getItem('description');
    const savedTags = localStorage.getItem('tags');
    const savedDateTime = localStorage.getItem('dateTime');

    setFormState(prevState => ({
      ...prevState,
      title: savedTitle || prevState.title,
      description: savedDescription || prevState.description,
      tag: savedTags || prevState.tag,
      dateTime: savedDateTime || prevState.dateTime,
    }));
  }, []);

  useEffect(() => {
    localStorage.setItem('title', formState.title);
    localStorage.setItem('description', formState.description);
    localStorage.setItem('tags', formState.tag);
    localStorage.setItem('dateTime', formState.dateTime);
  }, [formState]);

  const handleChange = (event: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setFormState(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  const updateDescription = (newDescription: string) => {
    setFormState(prevState => ({
      ...prevState,
      description: prevState.description ? `${prevState.description}\n${newDescription}` : newDescription,
    }));
  };

  return [formState, handleChange, updateDescription];
};
