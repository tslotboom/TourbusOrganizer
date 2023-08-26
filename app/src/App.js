import { useState, useEffect } from 'react';

import './App.css';


function App() {
  const [numDays, setNumdays] = useState('')
  const [tourists, setTourists] = useState(['']);
  const [fileGenerated, setFileGenerated] = useState(false);
  const [initialTourists, setInitialTourists] = useState(['']); // Store the initial state of tourists


  function addTourist() {
    setTourists([...tourists, '']);
  }

  function handleTouristChange(index, value) {
    const updatedTourists = [...tourists];
    updatedTourists[index] = value;
    setTourists(updatedTourists);
  }

  function generateFile(numDays, touristsData) {
    // Logic to generate the file
    // After generating the file, setFileGenerated(true);

    const requestData = {
        "numDays": numDays,
        "tourists": [...touristsData]
    }

    setFileGenerated(true);

    console.log(requestData)

  fetch("http://127.0.0.1:5000/getExcelFile", {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(requestData),
  })
    .then((res) => {
      // Check if the response status indicates success
      if (res.status === 200) {
        return res.blob(); // Convert the response to a blob
      } else {
        throw new Error("Failed to generate the file.");
      }
    })
    .then((blob) => {
      // Create a URL for the blob data
      // const url = window.URL.createObjectURL(blob);

      // Create a link element to trigger the download
      const a = document.createElement("a");
      console.log("Current directory:", __dirname);
      a.href = "./tourbus.xlsx";
      a.download = "tourbus.xlsx"; // Set the filename for the download
      document.body.appendChild(a);
      a.click();

      // Clean up by revoking the object URL
      // window.URL.revokeObjectURL(url);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
  }

  function downloadSeatingPlan() {
  // Create an object containing the tourists' data

}


  // Use useEffect to track changes in the tourists array
  useEffect(() => {
    if (!arraysAreEqual(tourists, initialTourists)) {
      setFileGenerated(false); // Reset fileGenerated if changes are detected
    }
  }, [tourists, initialTourists]);

  // Helper function to check if two arrays are equal
  const arraysAreEqual = (array1, array2) => {
    if (array1.length !== array2.length) return false;
    for (let i = 0; i < array1.length; i++) {
      if (array1[i] !== array2[i]) return false;
    }
    return true;
  };

  // Initialize initialTourists when the component mounts
  useEffect(() => {
    setInitialTourists([...tourists]);
  }, []);

  return (
    <>
      <title>Tourbus Organizer</title>
      <h1>Tourbus Organizer</h1>
      <legend>Enter information about the tour: </legend>
      <label>Length of tour in days:  </label>
      <input type="text" value={numDays} onChange={(e) => setNumdays(e.target.value)}/>
      <br></br>
      <label>Names of tourists: </label>
      {tourists.map((tourist, index) => (
        <div key={index}>
          <input
            type="text"
            value={tourist}
            onChange={(e) => handleTouristChange(index, e.target.value)}
          />
        </div>
      ))}
      <button onClick={addTourist}>Add another tourist</button>
      <button onClick={() => generateFile(numDays, tourists)}>Generate File</button>

    </>
   );
}

/**
      {!fileGenerated ? (
        <button onClick={() => generateFile(numDays, tourists)}>Generate File</button>
      ) : (
        <>
          <button onClick={downloadSeatingPlan}>Download Seating Plan</button>
          <p>Seating plan has been generated and is ready for download.</p>
        </>
      )}
      */


export default App;
