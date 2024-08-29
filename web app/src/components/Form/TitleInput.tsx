import React from 'react';
//import '../../App.css'

interface TitleInputProps {
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  maxLength?: number;
}

export const TitleInput: React.FC<TitleInputProps> = ({ value, onChange, maxLength = 100 }) => {
  return (
    <div>
      <input
        type="text"
        id="title"
        value={value}
        onChange={onChange}
        className="title-input"
        placeholder="Inserisci il titolo"
        maxLength={maxLength}
      />
      <div className="character-count">
        {value.length}/{maxLength}
      </div>
    </div>
  );
};

export default TitleInput;