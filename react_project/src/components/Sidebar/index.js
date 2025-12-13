import { useMsal } from '@azure/msal-react';
import {
  ChevronLeft,
  HistoryRounded,
  HomeRounded,
  LogoutRounded,
  MenuOpenRounded,
  WarningAmberRounded,
} from '@mui/icons-material';
import wwLogo from './Logo.png';
import Backdrop from '@mui/material/Backdrop';
import { Modal } from 'antd';
import cx from 'classnames';
import React, { memo, useCallback, useEffect, useMemo, useState } from 'react';
import { isMobile } from 'react-device-detect';
import { useLocation, useNavigate } from 'react-router-dom';

import './styles.scss';

// Left navbar component
const Sidebar = ({ isCollapsed, setIsCollapsed }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { instance } = useMsal();

  const [activeItem, setActiveItem] = useState(null);
  const { confirm } = Modal;

  // Handle logout
  const onLogoutClick = useCallback(() => {
    setIsCollapsed(isMobile);
    confirm({
      title: 'Are you sure, you want to Logout?',
      okText: 'Yes, Logout',
      cancelText: 'No',
      onOk: () => instance.logout(),
      icon: <LogoutRounded fontSize='medium' />,
      width: isMobile ? 300 : 400,
    });
  }, [instance, confirm, setIsCollapsed]);

  const redirect = (path) => {
    if (location === path) {
      return;
    } else {
      navigate(path);
    }
  };

  // // For mobile devices, collapse the sidebar
  useEffect(() => {
    document.body.style.overflow = isCollapsed ? 'unset' : 'hidden';
  }, [isCollapsed]);

  const sidebarArray = useMemo(
    () => [
      {
        name: 'Dashboard',
        svg: <HomeRounded fontSize='medium' />,
        url: '/',
        order: 0,
      },
      {
        name: 'History',
        svg: <HistoryRounded fontSize='medium' />,
        url: '/history',
        order: 1,
      },
      {
        name: 'Disclaimer',
        svg: <WarningAmberRounded fontSize='medium' />,
        url: '/disclaimer',
        order: 2,
      },
      {
        name: 'Log Out',
        svg: <LogoutRounded fontSize='medium' />,
        handleClick: onLogoutClick,
        order: 3,
      },
    ],
    [onLogoutClick],
  );

  const onItemClick = (item) => {
    if (item.handleClick) {
      item.handleClick();
    } else {
      redirect(item.url || '/');
    }
  };

  useEffect(() => {
    const findCurrent = sidebarArray.find((a) => location.pathname === a.url);
    setActiveItem(findCurrent?.order);
  }, [location, sidebarArray]);

  return (
    <>
      {/* <Backdrop open={!isCollapsed && isMobile} sx={{ zIndex: 1000 }} onClick={() => setIsCollapsed(true)} /> */}
      <aside
        className='sidebar'
        style={isCollapsed ? { width: isMobile ? 0 : 85, padding: isMobile ? 0 : '' } : { width: 180 }}
      >
        {isMobile && <MenuOpenRounded className='hamburgerIcon' onClick={() => setIsCollapsed(true)} />}
        <div className='productWrapper' style={isCollapsed ? { marginLeft: isMobile ? 0 : 20 } : {}}>
          <img
            src={wwLogo}
            alt="Product Name Logo" 
            className={cx({
              visibilityHidden: isCollapsed,
              smallerImage: true // Add class to make image smaller
            })}
            style={{ width: '55px', height: 'auto' }}
          />
          <span
            className={cx({
              visibilityHidden: isCollapsed,
            })}
          >
            Wealth Wingman
          </span>
        </div>
        <div
          className={cx('itemWrapper', {
            collapsed: isCollapsed,
          })}
        >
          {!!sidebarArray.length &&
            sidebarArray.map((item, index) => {
              return (
                <div
                  key={index}
                  className={cx('item', {
                    active: index === activeItem,
                  })}
                  onClick={() => onItemClick(item)}
                >
                  {item.svg}
                  <span
                    className={cx('itemName', {
                      visibilityHidden: isCollapsed,
                    })}
                  >
                    {item.name}
                  </span>
                </div>
              );
            })}
        </div>
        <div className='collapsableChevron' onClick={() => setIsCollapsed(!isCollapsed)}>
          <ChevronLeft
            sx={{
              color: 'white',
              rotate: isCollapsed ? '180deg' : '',
              transition: '0.5s cubic-bezier(0.36, -0.01, 0, 0.77)',
            }}
          />
        </div>
      </aside>
    </>
  );
};

export default memo(Sidebar);
