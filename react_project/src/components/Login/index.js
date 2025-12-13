import { useMsal } from '@azure/msal-react';
import React from 'react';
import microsoftLogo from './../../assets/Microsoft_logo.svg';
import './styles.scss';

export default function Login() {
  const { instance } = useMsal();

  const initializeSignIn = () => {
    instance.loginRedirect();
  };

  return (
    <div className='loginContainer' onClick={initializeSignIn}>
      <img height={30} src={microsoftLogo} alt='microsoft_logo' />
      <span>Sign in with Microsoft</span>
    </div>
  );
}
