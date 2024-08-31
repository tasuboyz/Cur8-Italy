import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './components/Form/Form css/CommunityButton.css'
import './components/Form/Form css/DateTimePicker.css'
import './components/Form/Form css/DescriptionInput.css'
import './components/Form/Form css/TagInput.css'
import './components/Form/Form css/TitleInput.css'
import './components/Form/Form css/SubmitButton.css'
//import './page/CommunityPage.css'

import { UserProvider } from './page/contexts/UserContext.tsx';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <UserProvider>
    <App />
  </UserProvider>,
  </React.StrictMode>,
)
