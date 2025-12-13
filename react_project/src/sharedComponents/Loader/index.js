import Backdrop from '@mui/material/Backdrop';
import CircularProgress from '@mui/material/CircularProgress';
import * as React from 'react';
import { createPortal } from 'react-dom';

export default function Loader() {
  return createPortal(
    <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }} open>
      <CircularProgress color='inherit' />
    </Backdrop>,
    document.getElementById('portal-root'),
  );
}
