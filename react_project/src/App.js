import { AuthenticatedTemplate, UnauthenticatedTemplate } from '@azure/msal-react';
import { Spin } from 'antd';
import React, { Suspense, lazy } from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import Login from './components/Login';
const History = lazy(() => import('./pages/History'));
const Search = lazy(() => import('./pages/Search'));
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Disclaimer = lazy(() => import('./pages/Disclaimer'));

const App = () => {
  return (
    <>
      <AuthenticatedTemplate>
        <BrowserRouter>
          <Suspense
            fallback={
              <Layout>
                <Spin fullscreen size='large' />
              </Layout>
            }
          >
            <Routes>
              <Route path='' element={<Dashboard />} />
              <Route exact path='search/:name' element={<Search />} />
              <Route exact path='history' element={<History />} />
              <Route exact path='disclaimer' element={<Disclaimer />} />
            </Routes>
          </Suspense>
        </BrowserRouter>
      </AuthenticatedTemplate>
      <UnauthenticatedTemplate>
        <Login />
      </UnauthenticatedTemplate>
    </>
  );
};

export default App;
