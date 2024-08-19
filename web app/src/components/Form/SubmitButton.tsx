import React from 'react';
import './Form css/SubmitButton.css'

interface SubmitButtonProps {
  onClick: () => void;
  loading: boolean;
}

export const SubmitButton: React.FC<SubmitButtonProps> = ({ onClick, loading }) => {
  return (
    <div className="submit-button-container">
      <button onClick={onClick} className="submit-button" disabled={loading}>
        {loading ? 'Invio...' : 'Invia Messaggio'}
      </button>
    </div>
  );
};

export default SubmitButton;