import React from 'react'; 
import { UpdateTicker } from '../API_logic/API';

 // For handling click to Add Ticker button on Search
const TickerADD = ({ticker, update_data, set_update_data, data, check}) => {

    const handleClick = () => {
        const action = "update";
        const collection = "mark";
        const query = {"user": "mark"};
            
        UpdateTicker(action, collection, query, ticker, data)
            .then(response => {
                if (response.success) {
                    set_update_data(!update_data);
                } else {
                    // Handle the error by setting the error message
                    console.log("error")
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        // You can place any action you want to perform on click here.
    };
    if (check==null){
        return (
            <div>
    
            </div>
        )
    }
    if (ticker!= null) {
        return (
            <div className='Add_To_Portfolio'>
                <button onClick={handleClick}>
                    Add To Portfolio
                </button>
            </div>
            )
    };
    return (
        <div>

        </div>
    )
    
}

export default TickerADD;