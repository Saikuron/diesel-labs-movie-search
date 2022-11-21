import axios from 'axios';
import Movies from './Movies'
import TextField from "@mui/material/TextField";
import Autocomplete from "@mui/material/Autocomplete";
import Stack from "@mui/material/Stack";
import Button from "@mui/material/Button";
import Container from '@mui/material/Container';

import React, { useState, useEffect } from "react";
import Typography from '@mui/material/Typography';

function App() {
  // data to fetch from backend and input from user for the search
  const [moviesNames, setMoviesNames] = useState([]);
  const [data, setData] = useState([""]);
  const [filteredData, setFilteredData] = useState([]);

  // I used help from this link for the searching feature : https://dev.to/salehmubashar/search-bar-in-react-js-545l
  // Function to search Movies
  function filterMovies(e) {
    e.preventDefault()
    const newSearchText = e.target.searchText.value
    setFilteredData(
      data.filter((original_data) => {
        // If input is empty, return full data
        if (newSearchText === '') {
          return original_data;
        }
        // If input is not empty, return filtered data
        else {
          return original_data[1].toLowerCase().includes(newSearchText.toLowerCase());
        }
      })
    );
  }

  // Get the data from the backend and save it
  useEffect(() => {
    const fetchData = async () => {
      const movies_names = await axios(
        'http://127.0.0.1:5000/whole-names',
      );
      setMoviesNames(movies_names.data);
      const movies_table = await axios(
        'http://127.0.0.1:5000/whole-table',
      );
      setData(movies_table.data);
    };
    
    fetchData();
  }, []);
  
  return (
    <Container maxWidth="sm">
      <div className="App">
        <header className="App-header">
          <div>
            <Typography align="center" sx={{margin: "10%"}} variant="h4">Movie Search</Typography>
            {/* <h1>Movie Search</h1> */}
            {/* Searchbar, updating the input data when a character is typed in */}
            <form onSubmit={filterMovies}>
              <Stack spacing={2} direction="row" >
                <Autocomplete
                  sx={{minWidth: 400}}
                  id="free-solo-demo"
                  freeSolo
                  options={moviesNames}
                  renderInput={(params) => <TextField {...params} 
                    name="searchText" value="newSearchText" label="Type a movie name" />}
                  />
                <Button variant="contained" type="submit">
                  Search
                </Button>
              </Stack>
            </form>
            <div style={{ marginTop: "3rem" }}>
              {/* Movies list */}
              <Movies filteredData={filteredData}/>
            </div>
          </div>
        </header>
      </div>
    </Container>
  );
}

export default App;
