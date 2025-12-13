import React, { useState } from 'react';
import { isMobile } from 'react-device-detect';
import Header from '../Header';
import Sidebar from '../Sidebar';
import './styles.scss';

const Layout = ({ title = '', showSearch = true, children }) => {
  const [isCollapsed, setIsCollapsed] = useState(isMobile);

  return (
    <main className='layoutWrapper'>
      {showSearch && <Sidebar isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />}
      <div className='contentWrapper'>
        <Header title={title} openSideBar={() => setIsCollapsed(false)} />
        {children || null}
      </div>
    </main>
  );
};

export default Layout;
