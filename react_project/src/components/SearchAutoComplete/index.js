import SearchRoundedIcon from '@mui/icons-material/SearchRounded';
import { TextField } from '@mui/material';
import { notification } from 'antd';
import React, { useState } from 'react';
import { isMobile } from 'react-device-detect';
import { useNavigate } from 'react-router-dom';
import { fetchTickerData } from '../../API_logic/API';
import Loader from './../../sharedComponents/Loader';
import './styles.scss';

const SearchAutoComplete = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();
  
  // Handle input to Search Bar
  const handleKeyPress = (e, clicked = false) => {
    if (e?.keyCode === 13 || clicked) {
      if (!searchQuery) {
        return notification.open({
          type: 'error',
          description: 'Please Enter Ticker Name',
          placement: isMobile ? 'bottomRight' : 'topRight',
        });
      }
      setIsLoading(true);
      fetchTickerData(searchQuery)
        .then((resp) => {
          navigate(`/search/${resp.data.ticker}`);
        })
        .catch(() => {
          if (e?.target) {
            e.target.value = '';
          }
        })
        .finally(() => {
          setIsLoading(false);
        });
    }
  };

  return (
    <>
      <TextField
        fullWidth
        sx={isMobile ? {} : { width: '25vw' }}
        className='autoCompleteWrapper'
        onKeyDown={handleKeyPress}
        onChange={(e) => setSearchQuery(e.target?.value || '')}
        hiddenLabel
        id='filled-hidden-label-normal'
        placeholder='Ticker Search'
        InputProps={{
          autoComplete: 'off',
          endAdornment: <SearchRoundedIcon onClick={() => handleKeyPress(null, true)} className='searchRoundedIcon' />,
        }}
      />
      {isLoading && <Loader />}
    </>
  );
};

export default SearchAutoComplete;
