import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import arrow from './icons/arrow.svg';

// Portfolio Table for use in Ticker card on Dashboard
const PfTable = ({ data, enlarged }) => {
  const location = useLocation();
  const isPortfolioPage = location.pathname === '/portfolio';
  const cardContainerClass = enlarged ? 'gray-card-container-enlarged' : 'gray-card-container';

  return (
    <div className={cardContainerClass}>
      <div className="portfolio-header">
        <h2>My Portfolio</h2>
        {!isPortfolioPage && (
          <Link to="/portfolio" className="arrow-link">
            <img src={arrow} alt="Arrow" className="arrow" />
          </Link>
        )}
      </div>
      <table className="table-no-lines">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Date Added</th>
          </tr>
        </thead>
        <tbody>
          {data.map((item, index) => (
            <tr key={index}>
              <td>{item?.symbol}</td>
              <td>{item?.date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default PfTable;
