import './App.css';

import React, { useState } from "react";
import Papa from "papaparse";

// Allowed extensions for input file
const allowedExtensions = ["csv"];

function App() {
  const [data, setData] = useState({});
  // const [parsedData, setParsedData] = useState({});
  const [error, setError] = useState("");
  const [file, setFile] = useState("");

  const handleFileChange = (e) => {
    setError("");
     
    // Check if user has entered the file
    if (e.target.files.length) {
        const inputFile = e.target.files[0];
         
        // Check the file extensions, if it not
        // included in the allowed extensions
        // we show the error
        // const fileExtension = inputFile?.type.split("/")[1];
        const fileExtension = inputFile?.name.split(".")[1];
        if (!allowedExtensions.includes(fileExtension)) {
            setError("Please input a csv file");
            return;
        }

        // If input type is correct set the state
        setFile(inputFile);
      }
  };

  const handleParse = () => {

    // If user clicks the parse button without
    // a file we show a error
    if (!file) return setError("Enter a valid file");

    // Initialize a reader which allows user
    // to read any file or blob.
    const reader = new FileReader();

    // Event listener on reader when the file
    // loads, we parse it and set the data.
    reader.onload = async ({ target }) => {
        const csv = Papa.parse(target.result, { header: true });
        const parsedData = csv?.data;
        console.log(parsedData)
        setData(parsedData);
        const columns = Object.keys(parsedData[0]);
        console.log(columns)
        // setData(columns);
        // console.log(columns.map((col, idx) => col + idx));
    };
    reader.readAsText(file);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div>
            <label htmlFor="csvInput" style={{ display: "block" }}>
                Enter CSV File
            </label>
            <input
                onChange={handleFileChange}
                id="csvInput"
                name="file"
                type="File"
            />
            <div>
                <button onClick={handleParse}>Parse</button>
            </div>
            <div style={{ marginTop: "3rem" }}>
                {/* {error ? error : data.map((col,
                  idx) => <div key={idx}>{col}</div>)} */}
                {/* {error ? error : data.map((elem, idx) => <div key={idx}> {'' + elem["movieId"] + ' - ' + elem["imdbId"]} </div>)} */}
                {/* {error ? error : parsedData.map((elem, idx) => <div key={idx}> {'' + elem["movieId"] + ' - ' + elem["imdbId"]} </div>)} */}
            </div>
        </div>
      </header>
    </div>
  );
}

export default App;
