import './App.css';
import axios from 'axios';
import Movies from './Movies'
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import Stack from "@mui/material/Stack";

import React, { useState, useEffect } from "react";


function App() {
  // data to fetch from backend and input from user for the search
  const [data, setData] = useState([]);
  const [movies_names, setMoviesNames] = useState([]);
  const [inputText, setInputText] = useState("");

  // function to get the input from the user
  function inputHandler(e) {
    const lowerCase = e.target.value.toLowerCase();
    setInputText(lowerCase);
  };

  // Get the data from the backend and save it
  useEffect(() => {
    const fetchData = async () => {
      const whole_data = await axios(
        'http://127.0.0.1:5000/whole',
      );
      setData(whole_data.data);
      const movies_data = await axios(
        'http://127.0.0.1:5000/movies-names',
      );
      setMoviesNames(movies_data.data);
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <div>
          <h1>Movie Search</h1>
          <Stack spacing={2} sx={{ width: 300 }}>
            <Autocomplete
              id="free-solo-demo"
              freeSolo
              // onChange={() => console.log("test")}
              options={movies_names}
              // options={top100Films.map((option) => option.title)}
              renderInput={(params) => <TextField onChange={inputHandler} {...params} label="Search a movie name" />}
            />
            {/* <Autocomplete
              freeSolo
              id="free-solo-2-demo"
              disableClearable
              options={movies_names}
              // options={top100Films.map((option) => option.title)}
              renderInput={(params) => (
                <TextField
                  {...params}
                  label="Search input"
                  InputProps={{
                    ...params.InputProps,
                    type: 'search',
                  }}
                />
              )}
            /> */}
          </Stack>
          {/* Searchbar, updating the input data when a character is typed in */}
          {/* <div className="SearchBar">
            <TextField
              id="outlined-basic"
              onChange={inputHandler}
              variant="outlined"
              fullWidth
              label="Search"
            />
          </div> */}
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
