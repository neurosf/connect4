import React, { useState } from "react";
import { useEffect } from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./fonts/fonts.css";
import "./App.css";
import Home from "./components/Home";
import Game from "./components/Game";
import Loading from "./components/Loading";
import io from "socket.io-client";

function App() {
  const [socketInstance, setSocketInstance] = useState("");
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const socket = io("http://localhost:5000");
    setLoaded(true);
    setSocketInstance(socket);

    return () => {
      // Disconnect socket when component unmounts
      socket.disconnect();
    };
  }, []);

  return (
    <div className="App">
      {loaded ? (
        <>
          <Router>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route
                path="/humanfirst"
                element={<Game mode={1} socket={socketInstance} player={1} />}
              />
              <Route
                path="/botfirst"
                element={<Game mode={1} socket={socketInstance} player={-1} />}
              />
              <Route
                path="/bots"
                element={<Game mode={2} socket={socketInstance} player={1} />}
              />
            </Routes>
          </Router>
        </>
      ) : (
        <Loading />
      )}
    </div>
  );
}

export default App;
