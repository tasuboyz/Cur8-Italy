// src/contexts/useUser.ts
import { useContext } from 'react';
import { UserContext, UserContextType } from './UserContext';

const useUser = (): UserContextType => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

export default useUser;
