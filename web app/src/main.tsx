import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'
import { UserProvider } from './page/contexts/UserContext.tsx';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <UserProvider>
    <App />
  </UserProvider>,
  </React.StrictMode>,
)
