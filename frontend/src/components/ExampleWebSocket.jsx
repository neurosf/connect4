import io from 'socket.io-client';
import React, { useEffect } from 'react';

const ENDPOINT = 'http://localhost:5000';

const socket = io(ENDPOINT);

function TestSocket() {
  useEffect(() => {

    socket.on('connect', () => {
      console.log('Connected to server');

      // Emit an event to the server
      socket.emit('play_event', {
        board: [
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0]
        ],
        turn: 1, // 1 or -1
        mode:1,// 1 or 2
        play_col:-1 // -1 if AI turn else humen selection
      });

      // Listen for responses from the server
      socket.on('response', (data) => {
        console.log('Received response:', data);
        // Handle the response data as needed
      });
    });

    // Clean up the socket connection on component unmount
    return () => {
      socket.disconnect();
    };
  }, []);

  return (
    <div className="App">
      {/* Your React components and logic */}
    </div>
  );
}

export default TestSocket;
