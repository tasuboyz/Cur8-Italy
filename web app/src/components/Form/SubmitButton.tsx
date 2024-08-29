import React from 'react';
//import '../../App.css'

interface SubmitButtonProps {
  onClick: () => void;
  loading: boolean;
}

export const SubmitButton: React.FC<SubmitButtonProps> = ({ onClick, loading }) => {
  return (
    <div>
      <button onClick={onClick} className="submit-button" disabled={loading}>
        {loading ? 'Invio...' : 'Invia Messaggio'}
      </button>
    </div>
  );
};

export default SubmitButton;