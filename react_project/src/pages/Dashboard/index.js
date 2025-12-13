import { QuestionCircleOutlined } from '@ant-design/icons';
import { withMsal } from '@azure/msal-react';
import ChevronRightIcon from '@mui/icons-material/ChevronRight';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import { Empty, Popconfirm } from 'antd';
import {
  CategoryScale,
  Chart as ChartJS,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Title,
  Tooltip,
} from 'chart.js';
import ZoomPlugin from 'chartjs-plugin-zoom';
import cx from 'classnames';
import { isEmpty, union } from 'lodash';
import moment from 'moment';
import React, { useCallback, useEffect, useMemo, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { fetchDashboardData, fetchTickers, removeFromPortfolio } from '../../API_logic/API';
import Card from '../../components/Card';
import Layout from '../../components/Layout';
import Loader from '../../sharedComponents/Loader';
import getRandomColor from '../../utils/getRandomColor';
import './styles.scss';

const options = {
  responsive: true,
  plugins: {
    zoom: {
      zoom: {
        wheel: {
          enabled: true,
        },
        mode: 'x',
      },
      pan: {
        enabled: true,
        mode: 'x',
      },
    },
    legend: {
      labels: {
        color: 'white', // Set legend text color to white
      },
    },
  },
  elements: {
    point: {
      radius: 1, // Set point radius
    },
    line: {
      borderWidth: 2, // Set line width
    },
  },
  scales: {
    x: {
      ticks: {
        color: 'white', // Set x-axis text color to white
      },
      grid: {
        color: '#707371', // Set x-axis grid line color to white
      },
    },
    y: {
      ticks: {
        color: 'white', // Set y-axis text color to white
      },
      grid: {
        color: '#707371', // Set y-axis grid line color to white
      },
    },
  },
};


ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, ZoomPlugin);

const Dashboard = ({ msalContext }) => {
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [selectedTicker, setSelectedTicker] = useState('');
  const [loading, setLoading] = useState(true);

  const { accounts } = msalContext;
  const { username = '' } = accounts?.[0] || {};

  const init = useCallback(async () => {
    if (!username) {
      return;
    }
    setLoading(true);
    const portfolio = await fetchTickers(username);
    fetchDashboardData(portfolio.data)
      .then((resp) => {
        console.log(resp.data)
        resp.data = resp.data.map((d) => ({ ...d, color: getRandomColor() }));
        setData(resp.data);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [username]);

  useEffect(() => {
    init();
  }, [init]);

  useEffect(() => {
    if (selectedTicker) {
      const selectedTickerData = data.find((d) => d.ticker === selectedTicker);
      setFilteredData(selectedTickerData ? [selectedTickerData] : data);
    } else {
      setFilteredData(data);
    }
  }, [data, selectedTicker]);

  const lineChartData = useMemo(() => {
    if (isEmpty(filteredData)) {
      return null; // Return null if no data is available
    }
  
    // Initialize an object to store prices for each date
    const pricesByDate = {};
  
    // Iterate over filtered data to collect prices by date
    filteredData.forEach((f) => {
      const prices = JSON.parse(f?.quantitative_output?.[1])?.c;
      Object.entries(prices).forEach(([timestamp, price]) => {
        const date = moment.unix(parseFloat(timestamp)).startOf('day').format('MMM DD, YYYY');
        if (!pricesByDate[date]) {
          pricesByDate[date] = {};
        }
        if (!pricesByDate[date][f.ticker]) {
          pricesByDate[date][f.ticker] = [];
        }
        pricesByDate[date][f.ticker].push(price);
      });
    });
  
    // Extract unique dates and sort them
    const dates = Object.keys(pricesByDate).sort((a, b) => moment(a, 'MMM DD, YYYY').valueOf() - moment(b, 'MMM DD, YYYY').valueOf());
  
    // Construct datasets based on pricesByDate
    const datasets = filteredData.map((f) => {
      const ticker = f.ticker;
      const color = f.color;
      const data = dates.map((date) => {
        const prices = pricesByDate[date][ticker];
        return prices ? prices.reduce((acc, curr) => acc + curr, 0) / prices.length : null; // Average price for the day
      });
      return {
        label: ticker,
        data: data,
        borderColor: color,
        backgroundColor: color + '80',
      };
    });
  
    // Adding the "Predicted Closing Price" dataset
    datasets.push({
      label: 'Predicted Closing Price',
      borderColor: '#ff1837',
      backgroundColor: '#ff1837',
      data: Array(dates.length).fill(null), // Fill with nulls to match date length
    });
  
    return {
      labels: dates,
      datasets,
    };
  }, [filteredData]);
  
  
  

  const removeTickerFomPortfolio = (ticker) => {
    setLoading(true);
    removeFromPortfolio(ticker, username).finally(() => {
      init();
    });
  };

  return (
    <Layout title='Dashboard'>
      {loading ? (
        <Loader />
      ) : data.length === 0 ? (
        <Empty description='No Data Found' />
      ) : (
        <div className='dashboardContainer'>
          <div className='analysisWrapper'>
            <Card classname='myPortfolio'>
              <div className='dflex'>
                <span>My Portfolio</span>
                {selectedTicker && (
                  <span className='cursor-pointer' onClick={() => setSelectedTicker('')}>
                    Show All
                  </span>
                )}
              </div>
              <div className='tickerAnalysis'>
                <div className='dflex'>
                  <span>Ticker</span>
                  <span>Date Added</span>
                </div>
                {data.map((d) => (
                  <div className='dflex' key={d._id}>
                    <span
                      className={cx('cursor-pointer', {
                        bold: d.ticker === selectedTicker,
                      })}
                    >
                      <span onClick={() => setSelectedTicker((s) => (s === d.ticker ? '' : d.ticker))}>
                        <ChevronRightIcon />
                        {d.ticker}
                      </span>
                      &nbsp;&nbsp;&nbsp;&nbsp;
                      <Popconfirm
                        title={`Are you sure to remove ${d.ticker} from your portfolio ?`}
                        onConfirm={() => removeTickerFomPortfolio(d.ticker)}
                        okText='Yes'
                        cancelText='No'
                        icon={<QuestionCircleOutlined style={{ color: 'red' }} />}
                      >
                        <DeleteOutlineIcon />
                      </Popconfirm>
                    </span>
                    <span>{moment(d.date).utc(true).local().format('MMM DD, YY')}</span>
                  </div>
                ))}
              </div>
            </Card>
            <Card>
              <div>
                Quantitative Trend Analysis
                {lineChartData?.labels && <Line options={options} data={lineChartData} />}
              </div>
            </Card>
          </div>
          <Card classname='dashboardCard'>
            {filteredData.map((d) => (
              <div key={d._id}>
                <h3>{d.ticker}</h3>
                <p>{d.integrated_output.detailed_prediction}</p>
              </div>
            ))}
          </Card>
        </div>
      )}
    </Layout>
  );
};

export default withMsal(Dashboard);