import { withMsal } from '@azure/msal-react';
import MenuRoundedIcon from '@mui/icons-material/MenuRounded';
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';
import { Box, Popover } from '@mui/material';
import React, { useState } from 'react';
import { isMobile } from 'react-device-detect';
import SearchAutoComplete from '../SearchAutoComplete';
import './styles.scss';


const Header = ({ title, openSideBar, msalContext }) => {
  const [userPopperOpen, setPopperOpen] = useState(false);
  const { accounts } = msalContext;

  const UserInfo = () => {
    return (
      <div className='accountUserName'>
        <p>{accounts[0]?.username}</p>
        <p>Subscription</p>
      </div>
    );
  };

  const handleUserClick = () => {
    setPopperOpen(!userPopperOpen);
  };

  return (
    <div className='header'>
      {isMobile && <MenuRoundedIcon className='hamburgerIcon' style = {{color: 'white' }} onClick={openSideBar} />}
      {!isMobile && <div className='title'>{title}</div>}
      <div className='searchBarWrapper'>
        <SearchAutoComplete />
      </div>
      <div className='AccountInfoWrapper'>
        {!isMobile && (
          <>
            <UserInfo />
          </>
        )}
        <Box position='relative'>
          <PersonRoundedIcon fontSize='large' sx={{ cursor: 'pointer' }} onClick={handleUserClick} />
          {isMobile && (
            <Popover
              disablePortal
              onClose={handleUserClick}
              placement='bottom-end'
              transition
              open={userPopperOpen}
              anchorOrigin={{
                vertical: 60,
                horizontal: 'right',
              }}
            >
              <UserInfo />
            </Popover>
          )}
        </Box>
      </div>
    </div>
  );
};

export default withMsal(Header);
