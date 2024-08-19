import React from 'react';
import './Form css/DescriptionInput.css'

interface DescriptionInputProps {
  value: string;
  onChange: (event: React.ChangeEvent<HTMLTextAreaElement>) => void;
  maxLength?: number;
}

export const DescriptionInput: React.FC<DescriptionInputProps> = ({ value, onChange, maxLength = 15000 }) => {
  return (
    <div className="form-group">
      <textarea
        id="description"
        value={value}
        onChange={onChange}
        className="input-description"
        placeholder="Inserisci la descrizione del post"
        maxLength={maxLength}
      />
      <div className="character-count">
        {value.length}/{maxLength}
      </div>
    </div>
  );
};

export default DescriptionInput;