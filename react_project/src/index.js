import { PublicClientApplication } from '@azure/msal-browser';
import { MsalProvider } from '@azure/msal-react';
import React, { StrictMode } from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import { msalConfig } from './auth/config';
import './index.scss';
import ErrorBoundary from './sharedComponents/ErrorBoundary';

const pca = new PublicClientApplication(msalConfig);

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <MsalProvider instance={pca}>
    <StrictMode>
      <ErrorBoundary>
        <App />
      </ErrorBoundary>
    </StrictMode>
  </MsalProvider>,
);
