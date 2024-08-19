import React from 'react';
import './Form css/TagInput.css'

interface TagInputProps {
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export const TagInput: React.FC<TagInputProps> = ({ value, onChange }) => {
  return (
    <div className="form-group">
      <input
        type="text"
        id="tag"
        value={value}
        onChange={onChange}
        className="form-control"
        placeholder="Inserisci i tag separati da spazi"
      />
    </div>
  );
};

export default TagInput;
