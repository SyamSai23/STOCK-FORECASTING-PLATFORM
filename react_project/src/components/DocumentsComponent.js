import React from 'react';
import PfTable from './PfTable';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom


// Import your SVG file (update the path accordingly)
import userIcon from './icons/user-icon.svg';

function DocumentsComponent({ page, data, loading, table, enlarged }) {
  if (loading) {
    return <p>Loading...</p>;
  }

  if (!data) {
    return <p></p>;
  }

  return (
    <>
      <header className="page-header">
        <h1>{page}</h1>
        <div className="user-info">
          <div className="user-details">
            <h2 className="username">{data.user}</h2>
            <Link to="/account" className="account-link">
              Account Info
            </Link>
          </div>
          <img src={userIcon} alt="User Icon" className="user-icon" />
        </div>
      </header>
      {/* Portfolio Table */}
      {table && <PfTable data={data.ticker} enlarged={enlarged}/>}
    </>
  );
}

export default DocumentsComponent;
