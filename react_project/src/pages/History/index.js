import { withMsal } from '@azure/msal-react';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import Accordion from '@mui/material/Accordion';
import AccordionDetails from '@mui/material/AccordionDetails';
import AccordionSummary from '@mui/material/AccordionSummary';
import { DatePicker, Empty } from 'antd';
import dayjs from 'dayjs';
import { groupBy } from 'lodash';
import moment from 'moment';
import React, { useCallback, useEffect, useState } from 'react';
import { isMobile } from 'react-device-detect';
import { fetchHistoryData, fetchTickers } from '../../API_logic/API';
import Card from '../../components/Card';
import Layout from '../../components/Layout';
import Loader from '../../sharedComponents/Loader';
import trendUp from './../../assets/trend-upward.svg';
import trendDown from './../../assets/trending-down.svg';
import getAccuracy from '../../utils/getAccuracy';
import getActualResult from '../../utils/getActualResult';
import './styles.scss';

const { RangePicker } = DatePicker;
const whiteText = {
  color: 'white'
};
const History = ({ msalContext }) => {
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = React.useState(null);
  const [data, setData] = useState({});
  const [accuracy, setAccuracy] = useState({});
  const [tableData, setTableData] = useState([]);
  const [dateRange, setDateRange] = useState({
    startDate:moment().subtract(1, 'month'),
    endDate:moment().subtract(5, 'days')
  });
  const { accounts } = msalContext;
  const handleChange = (panel) => (event, isExpanded) => {
    setExpanded(isExpanded ? panel : false);
  };
  const init = useCallback(async () => {
    setLoading(true);
    const portfolio = await fetchTickers(accounts[0]?.username);
    fetchHistoryData(portfolio.data, dateRange)
      .then((resp) => {
        setData(resp.data);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [dateRange, accounts]);
  useEffect(() => {
    init();
  }, [dateRange, init]);
  useEffect(() => {
    const calculateAccuracy = async () => {
        const accuracies = await getAccuracy(data);
        setAccuracy(accuracies); // You can use the accuracy object here
      };
    
    const fetchRealResults = async () => {
        const promises = data.results?.map(async (result) => {
            const realResult = await getActualResult(result.ticker, result.date, result.integrated_output.general_prediction, result.closing_price);
            return {
                ...result,
                real_result: realResult
            };
        });
        const updatedResults = await Promise.all(promises);
        let tData = updatedResults?.map((td) => ({
            ...td,
            dateTime: moment(td.date).hours(td.time.split(':')[0]).minutes(td.time.split(':')[1]).utc(true).local(),
        }));
        tData = groupBy(
            tData?.sort((a, b) => moment(b.dateTime).diff(a.dateTime)),
            'ticker',
        );
        setTableData({ ...tData });
    };

    calculateAccuracy();
    if (data.results) {
      fetchRealResults();
  }
}, [data]);


  const onRangeChange = (e) => {
    if (!e) {
      return;
    }
    setDateRange({
      startDate: moment(new Date(e[0])),
      endDate: moment(new Date(e[1])),
    });
  };
  const rangePresets = [
    { label: 'Last 7 Days', value: [dayjs().add(-7, 'd'), dayjs()] },
    { label: 'Last 14 Days', value: [dayjs().add(-14, 'd'), dayjs()] },
    { label: 'Last 30 Days', value: [dayjs().add(-30, 'd'), dayjs()] },
    { label: 'Last 90 Days', value: [dayjs().add(-90, 'd'), dayjs()] },
  ];
  
  return (
    <Layout title='History'>
      {loading ? (
        <Loader />
      ) : (
        <>
          <div className='topWrapper'>
            <Card classname='contentHistoryCard'>
              <div className='contentHistory'>
                <div>Performance Summary</div>
                <div className='analysisParams'>
                  <div>
                  <p>Correct Predictions:</p> <p>{accuracy.total_accuracy}</p>                  
                  </div>
                  <div>
                    <p>Correct Up/Total Up:</p>
                    <p className='correctUp letterSpacing3'>
                      {accuracy.bullish_accuracy.split('/')?.[0]} 
                      <span className='slashColor'>/</span>
                      {accuracy.bullish_accuracy.split('/')?.[1]}
                    </p>
                  </div>
                  <div>
                    <p>Correct Down/Total Down:</p>
                    <p className='correctDown letterSpacing3'>
                      {accuracy.bearish_accuracy.split('/')?.[0]}
                      <span className='slashColor'>/</span>
                      {accuracy.bearish_accuracy.split('/')?.[1]}
                    </p>
                  </div>
                </div>
              </div>
            </Card>
            <div className='dateRangeWrapper'>
              <h3>Select Date Range:</h3>
              <RangePicker
                defaultValue={[dayjs(new Date(dateRange.startDate)), dayjs(new Date(dateRange.endDate))]}
                presets={isMobile ? [] : rangePresets}
                onChange={onRangeChange}
                style={{backgroundColor: 'f0f0f0' , borderColor: '#6f6f6f'}}
                format={'MMM DD, YY'}
              />
            </div>
          </div>
          <div style={{ overflowX: 'scroll', marginBottom: isMobile ? 0 : 16 }}>
            {data.results?.length > 0 ? (
              <table className='table'>
                <thead>
                  <tr style={{ width: '120%'}}>
                    <th>Date</th>
                    <th>Ticker</th>
                    <th>{isMobile ? 'Predic.' : 'Predicted'}</th>
                    <th>Result</th>
                    <th>Price</th>
                    {!isMobile && <th>More Info</th>}
                  </tr>
                </thead>
                <tbody>
                  {Object.keys(tableData).map((td, index) => (
                    <tr key={index}>
                      <Accordion
                        expanded={expanded === tableData[td][0].ticker}
                        onChange={handleChange(tableData[td][0].ticker)}
                        sx={{ boxShadow: 'unset' }}
                      >
                        <AccordionSummary sx={{ background: '#f2f2f2' }} expandIcon={<ExpandMoreIcon />}>
                          <td>{moment(tableData[td][0].dateTime).format('MMM DD, YY')}</td>
                          <td>{tableData[td][0].ticker}</td>
                          <td
                            className={
                              tableData[td]?.[0].integrated_output?.general_prediction === 'Bullish'
                                ? 'correctUp'
                                : 'correctDown'
                            }
                          >
                            {isMobile ? (
                              <img
                                height={31}
                                src={
                                  tableData[td]?.[0].integrated_output?.general_prediction === 'Bullish'
                                    ? trendUp
                                    : trendDown
                                }
                                alt={tableData[td]?.[0].integrated_output?.general_prediction}
                              />
                            ) : (
                              tableData[td]?.[0].integrated_output?.general_prediction
                            )}
                          </td>
                          <td className={tableData[td]?.[0].real_result === 'Bullish' ? 'correctUp' : 'correctDown'}>
                            {isMobile ? (
                              <img
                                height={31}
                                src={tableData[td]?.[0].real_result === 'Bullish' ? trendUp : trendDown}
                                alt={tableData[td]?.[0].real_result}
                              />
                            ) : (
                              tableData[td]?.[0].real_result
                            )}
                          </td>
                          <td>{tableData[td]?.[0].closing_price}</td>
                        </AccordionSummary>
                        <AccordionDetails>
                          {index % 2 === 0 && <tr />}
                          {tableData[td]?.map((t, index) => (
                            <tr key={index} className='accordionData'>
                              <td>
                                {t.dateTime.format('MMM DD, YY')}
                                {isMobile ? <br /> : <>&nbsp;</>}
                                {t.dateTime.format('hh:mm')}
                              </td>
                              <td></td>
                              <td
                                className={
                                  t?.integrated_output?.general_prediction === 'Bullish' ? 'correctUp' : 'correctDown'
                                }
                              >
                                {isMobile ? (
                                  <img
                                    height={31}
                                    src={t?.integrated_output?.general_prediction === 'Bullish' ? trendUp : trendDown}
                                    alt={t?.integrated_output?.general_prediction}
                                  />
                                ) : (
                                  t?.integrated_output?.general_prediction
                                )}
                              </td>
                              <td className={t.real_result === 'Bullish' ? 'correctUp' : 'correctDown'}>
                                {isMobile ? (
                                  <img
                                    height={31}
                                    src={t?.real_result === 'Bullish' ? trendUp : trendDown}
                                    alt={t?.real_result}
                                  />
                                ) : (
                                  t?.real_result
                                )}
                              </td>
                              <td>{t.closing_price}</td>
                              {!isMobile && <td />}
                            </tr>
                          ))}
                        </AccordionDetails>
                      </Accordion>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <Empty description={<span style={whiteText}>No Data Found</span>} />

            )}
          </div>
        </>
      )}
    </Layout>
  );
};
export default withMsal(History);