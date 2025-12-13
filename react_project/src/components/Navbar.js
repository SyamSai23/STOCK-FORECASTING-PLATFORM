import React from 'react';
import { Link } from 'react-router-dom';
import Home from './icons/home.js';
const Navbar = () => {
  const currentPath = window.location.pathname;

  return (
    <nav className='navbar'>
      <logo>Product</logo>
      <logo>Name</logo>
      <ul>
        <li className='navbar-link'>
          <Home isActive={currentPath === '/' ? 'active' : ''} />
          <Link to='/' className={currentPath === '/' ? 'active' : ''}>
            <span className='navbar-links-text'>Dashboard</span>
          </Link>
        </li>
        <li>
          <Link to='/portfolio' className={currentPath === '/portfolio' ? 'active' : ''}>
            Portfolio
          </Link>
        </li>
        <li>
          <Link to='/search' className={currentPath === '/search' ? 'active' : ''}>
            Search
          </Link>
        </li>
        <li>
          <Link to='/' className={currentPath === '/Account' ? 'active' : ''}>
            Account
          </Link>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
