import React, { useState, useEffect, useCallback } from "react";
import ChatBox from "./Chat";
import axios from 'axios';

function App() {
  const [currMsg, setCurrMsg] = useState('');
  const [history, setHistory] = useState([]);
  const [conn, setConn] = useState(null);
  // const [render, setRender] = useState(false);

  const handleInputChnage = event => {
    setCurrMsg(event.target.value);
  }

  const handleSubmit = event => {
    conn.send(currMsg);
    setCurrMsg('');
  }

  const establishConnection = () => {
    axios.post('http://127.0.0.1:8000/api/token/refresh/', {
      refresh: "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1MjMyMzUyOCwiaWF0IjoxNjUyMjM3MTI4LCJqdGkiOiJmNDMyOWRkNTUyOGU0YTc2OTQwYTg5OTBlZjcyOGM5NSIsInVzZXJfaWQiOjF9.d3ZSZNzo7KhOw3rukrIr9pUjm7dtCr-9czVWFSSr4yU"
    })
      .then(response => {
        const access_token = response.data.access;
        const ws = new WebSocket('ws://127.0.0.1:8000/ws/?token=' + access_token);
        ws.onopen = (event) => {
          console.log('Connection Open');
          ws.send("Hello World. How are you?");
          setConn(ws);
        }
        ws.onmessage = (event => {
          console.log(event.data);
          setHistory(prev => [...prev, event.data]);
        })
        ws.onclose = event => console.log("Connection Closed.");
      })
      .catch(err => console.error("Error: ", err.message))
  }

  useEffect(() => {
    if (!conn) {
      console.log("UseEffect Executing..");
      establishConnection();
    }
    return () => {
      if (conn)
        conn.close();
    }
  }, []);


  return (
    <div className="App">
      <ChatBox msgList={history} />
      <label htmlFor="message">Enter Message:  </label>
      <input type="text" name="message" id="message" placeholder="Enter your Message" value={currMsg} onChange={handleInputChnage} />
      <button onClick={handleSubmit}>Send</button>
    </div>
  );
}

export default App;
