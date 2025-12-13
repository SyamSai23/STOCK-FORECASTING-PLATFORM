import cx from 'classnames';
import React from 'react';
import './styles.scss';

// Card component used on Dashboard, Search, History)
const Card = ({ showBorder, children, classname }) => {
  return (
    <div
      className={cx('card', classname, {
        showBorder: showBorder,
      })}
    >
      {children}
    </div>
  );
};

export default Card;
