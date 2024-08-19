import React, { createContext, useState, useEffect } from 'react';

export interface User {
  userId: number | null;
  first_name?: string;
  last_name?: string;
  username?: string;
  language_code?: string;
}

export interface UserContextType {
  user: User;
}

export const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User>({
    userId: null,
    first_name: undefined,
    last_name: undefined,
    username: undefined,
    language_code: undefined,
  });

  useEffect(() => {
    const telegramUser = window.Telegram.WebApp.initDataUnsafe?.user;
    
    if (telegramUser) {
      setUser({
        userId: telegramUser.id,
        first_name: telegramUser.first_name,
        last_name: telegramUser.last_name,
        username: telegramUser.username,
        language_code: telegramUser.language_code,
      });
    }
  }, []);

  return (
    <UserContext.Provider value={{ user }}>
      {children}
    </UserContext.Provider>
  );
};
