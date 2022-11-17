import './App.css';
import axios from 'axios';
import Movies from './Movies'
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import Stack from "@mui/material/Stack";

import React, { useState, useEffect } from "react";


function App() {
  // data to fetch from backend and input from user for the search
  const [moviesNames, setMoviesNames] = useState([]);
  const [data, setData] = useState([""]);
  const [filteredData, setFilteredData] = useState([]);
  const [newSearchText, setNewSearchText] = useState("");

  // I used help from this link for the searching feature : https://dev.to/salehmubashar/search-bar-in-react-js-545l
  // Function to search Movies
  function filterMovies(e) {
    e.preventDefault()
    setNewSearchText(e.target.searchText.value)
    setFilteredData(
      data.filter((original_data) => {
        // If input is empty, return full data
        if (newSearchText === '') {
            return original_data;
        }
        // If input is not empty, return filtered data
        else {
            return original_data[1].toLowerCase().includes(newSearchText);
        }
      })
    );
  }

  // Get the data from the backend and save it
  useEffect(() => {
    const fetchData = async () => {
      const movies_names = await axios(
        'http://127.0.0.1:5000/sample-names',
      );
      setMoviesNames(movies_names.data);
      const movies_table = await axios(
        'http://127.0.0.1:5000/sample-table',
      );
      setData(movies_table.data);
    };
    
    fetchData();
  }, []);
  
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <h1>Movie Search</h1>
          {/* Searchbar, updating the input data when a character is typed in */}
          <form onSubmit={filterMovies}>
            <Stack spacing={2} sx={{ width: 300 }}>
              <Autocomplete
                id="free-solo-demo"
                freeSolo
                options={moviesNames}
                renderInput={(params) => <TextField {...params} name="searchText" value="newSearchText" label="Search a movie name" />}
                />
            </Stack>
            <input type="submit" value="Submit" />
          </form>
          <div style={{ marginTop: "3rem" }}>
            {/* Movies list */}
            <Movies filteredData={filteredData}/>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
