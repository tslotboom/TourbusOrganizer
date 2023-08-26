import { useState } from 'react';

import './App.css';

function App() {
  const [touristAdder, setTouristAdder] = useState((<><input type="text"></input><br></br></>));

  function addTourist() {
    setTouristAdder(( <>{touristAdder}<input type="text"></input><br></br></>))
  }

  return (


    <>
      <title>Tourbus Organizer</title>
      <h1>Tourbus Organizer</h1>
      {/* <form> */}
          {/* <fieldset> */}
              <legend>Enter information about tour: </legend>
              <label>Length of tour in days:</label>
              <input type="text"></input><br></br>
              <label>Names of tourists:</label><br />
              {touristAdder}
              <AddTouristButton onClick={addTourist}/>
              <a href="link/to/your/download/file" download onClick={() => {getSeatingPlan()}}>Download Seating Plan</a>
          {/* </fieldset> */}
      {/* </form> */}
    </>
  );
}

function AddTouristButton({onClick}){
  return (
    <><button onClick={onClick}>Add another tourist</button><br></br></>
  )
}

function getSeatingPlan(){
  const data = {"data": "data"}
  fetch("http://127.0.0.1:5000/getExcelFile", {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  }).then(res => res.json()).then(data => {
    console.log(data)
  })
}
export default App;
