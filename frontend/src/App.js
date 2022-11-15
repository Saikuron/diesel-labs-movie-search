import './App.css';
import axios from 'axios';
import Movies from './Movies'
import TextField from "@mui/material/TextField";

import React, { useState, useEffect } from "react";


function App() {
  // data to fetch from backend and input from user for the search
  const [data, setData] = useState([]);
  const [inputText, setInputText] = useState("");

  // function to get the input from the user
  function inputHandler(e) {
    const lowerCase = e.target.value.toLowerCase();
    setInputText(lowerCase);
  };

  // Get the data from the backend and save it
  useEffect(() => {
    const fetchData = async () => {
      const result = await axios(
        'http://127.0.0.1:5000/whole',
      );
      setData(result.data);
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <div>
            <h1>Movie Search</h1>
            {/* Searchbar, updating the input data when a character is typed in */}
            <div className="SearchBar">
              <TextField
                id="outlined-basic"
                onChange={inputHandler}
                variant="outlined"
                fullWidth
                label="Search"
              />
            </div>
            <div style={{ marginTop: "3rem" }}>
              {/* Movies list, including the input text */}
              <Movies input={inputText} data={data}/>
            </div>
        </div>
      </header>
    </div>
  );
}

export default App;
