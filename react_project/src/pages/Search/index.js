import { withMsal } from '@azure/msal-react';
import AddRoundedIcon from '@mui/icons-material/AddRounded';
import {
  CategoryScale,
  Chart as ChartJS,
  Filler,
  Legend,
  LineElement,
  LinearScale,
  PointElement,
  Tooltip,
} from 'chart.js';
import ZoomPlugin from 'chartjs-plugin-zoom';
import cx from 'classnames';
import moment from 'moment';
import { useEffect, useMemo, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { useNavigate, useParams } from 'react-router-dom';
import { addToPortfolio, fetchTickerData, fetchTickers, removeFromPortfolio } from '../../API_logic/API';
import Layout from '../../components/Layout';
import Loader from '../../sharedComponents/Loader';
import abbreviateNumber from '../../utils/abbreviateNumber';
import Card from './../../components/Card';
import './styles.scss';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Filler, Legend, ZoomPlugin);

const options = {
  responsive: true,
  animation: {
    duration: 0,
  },
  scales: {
    y: {
      position: 'right',
      ticks: {
        color: 'white', // Set x-axis text color to white
      },
      grid: {
        color: '#707371', // Set x-axis grid line color to white
      },
    },
    x: {
      ticks: {
        color: 'white', // Set x-axis text color to white
      },
      grid: {
        color: '#707371', // Set x-axis grid line color to white
      },
    },
  },
  plugins: {
    legend: {
      display: false,
    },
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
  },
};

const SearchPage = ({ msalContext }) => {
  const navigate = useNavigate();

  const chartRef = useRef(null);

  const { name } = useParams();
  const [isLoading, setIsLoading] = useState(false);
  const [isInPortFolio, setIsInPortfolio] = useState(null);
  const [data, setData] = useState({});

  const { accounts } = msalContext;
  const username = useMemo(() => accounts[0]?.username || {}, [accounts]);

  useEffect(() => {
    setIsLoading(true);
    fetchTickerData(name)
      .then((resp) => {
        setData(resp.data);
        fetchTickers(username).then((res) => {
          setIsInPortfolio(res.data.includes(resp.data.ticker));
        });
      })
      .catch(() => {
        navigate('/');
      })
      .finally(() => {
        setIsLoading(false);
      });
  }, [name, navigate, username]);

  const addOrRemoveToPortfolio = () => {
    setIsInPortfolio(null);
    if (isInPortFolio) {
      removeFromPortfolio(data.ticker, username).then(() => {
        setIsInPortfolio(false);
      });
    } else {
      addToPortfolio(data.ticker, username).then(() => {
        setIsInPortfolio(true);
      });
    }
  };

  const dataChart = useMemo(
    () => ({
      labels: data?.graph_info?.hourly_prices?.map(({ hour }) =>
        moment().hours(hour.split(':')[0]).minutes(hour.split(':')[1]).utc(true).local().format('HH:mm'),
      ),
      datasets: [
        {
          fill: true,
          data: data?.graph_info?.hourly_prices?.map(({ price }) => price),
          borderColor: '#BE1213',
          backgroundColor: '#BE1213',
        },
      ],
    }),
    [data],
  );

  const chatMeta = chartRef?.current?._sortedMetamers?.[0].data[0];

  const highlighterPosition = useMemo(() => {
    if (!chartRef.current || isLoading) {
      return {
        enabled: false,
      };
    }
    const x = chatMeta?.data[data?.graph_info?.hourly_prices?.length - 1].x || 0;
    const y = chatMeta?.data[data?.graph_info?.hourly_prices?.length - 1].y || 0;
    return {
      enabled: x || y,
      x,
      y: y,
    };
  }, [chatMeta, data?.graph_info?.hourly_prices?.length, isLoading]);

  const lastPriceDetails = useMemo(() => {
    const hourlyPrice = data?.graph_info?.hourly_prices || [];
    const lastPrice = hourlyPrice[hourlyPrice.length - 1]?.price;
    const previousPrice = hourlyPrice?.[hourlyPrice.length - 2]?.price || 0;
    let state = '';
    if (previousPrice > lastPrice) {
      state = 'down';
    } else if (previousPrice < lastPrice) {
      state = 'up';
    } else {
      state = 'hold';
    }
    return {
      lastPrice,
      state,
    };
  }, [data?.graph_info?.hourly_prices]);

  return (
    <Layout title='Ticker Search'>
      {isLoading ? (
        <Loader />
      ) : (
        <div className='searchWrapper'>
          <div className='chartWrapper'>
            <div className='tickerInfoWrapper'>
              <div className='tickerInfo'>
                <p>{data.ticker || '-'}</p>
                <p>
                  {data.info?.primary_exchange || '-'}: {data.ticker || '-'}
                </p>
              </div>
              <div
                className={cx('addToPortfolio', {
                  disabled: isInPortFolio === null,
                })}
                onClick={addOrRemoveToPortfolio}
              >
                <span>{isInPortFolio ? 'Remove from' : 'Add to'} Portfolio</span>
                <AddRoundedIcon sx={{ color: '#266F8C' }} />
              </div>
            </div>
            <div className='chart'>
              <Line ref={chartRef} options={options} data={dataChart} />
              {highlighterPosition?.enabled && (
                <div
                  className={`tag ${lastPriceDetails.state}`}
                  style={{ position: 'absolute', left: highlighterPosition?.x, top: highlighterPosition?.y - 10 }}
                >
                  {lastPriceDetails.lastPrice?.toFixed(2)}
                </div>
              )}
            </div>
          </div>
          <div className='cardInfoWrapper'>
            <Card showBorder>
              <div className='cardInfo'>
                <div className='cardColOne'>
                  <p>
                    Previous Close: &nbsp;
                    <span className='fieldValue'>{abbreviateNumber(data?.info?.previous_close, 2) || '-'}</span>
                  </p>
                  <p>
                    Day Range:&nbsp;
                    <span className='fieldValue'>
                      {abbreviateNumber(data?.info?.day_range.low, 2) || '-'} -
                      {abbreviateNumber(data?.info?.day_range.high, 2) || '-'}
                    </span>
                  </p>
                  <p>
                    Year Range:&nbsp;
                    <span className='fieldValue'>
                      {abbreviateNumber(data?.info?.year_range.low) || '-'} -&nbsp;
                      {abbreviateNumber(data?.info?.year_range.high) || '-'}
                    </span>
                  </p>
                  <p>
                    Market Cap:&nbsp;
                    <span className='fieldValue'>{abbreviateNumber(data?.info?.market_cap, 2) || '-'}</span>
                  </p>
                </div>
                <div className='cardColTwo'>
                  <p>
                    P/E Ratio: <span className='fieldValue'>{data?.info?.pe_ratio || '-'}</span>
                  </p>
                  <p>
                    Dividend Yield: <span className='fieldValue'>{data?.info?.dividend_yield || '-'}%</span>
                  </p>
                  <p>
                    Primary Exchange: <span className='fieldValue'>{data?.info?.primary_exchange || '-'}</span>
                  </p>
                  <p>
                    Average Volume:&nbsp;
                    <span className='fieldValue'>{abbreviateNumber(data?.info?.average_volume, 1) || '-'}</span>
                  </p>
                </div>
              </div>
            </Card>
            <Card showBorder>
              <div className='about'>
                <div>About:</div>
                <p>{data.description || 'N/A'}</p>
              </div>
            </Card>
          </div>
        </div>
      )}
    </Layout>
  );
};

export default withMsal(SearchPage);
