"use client";
import React from 'react'
import dynamic from 'next/dynamic';


// Load AudioRecorder một cách bất đồng bộ và tắt Server-Side Rendering (SSR)
const AudioRecorder = dynamic(() => import('./AudioRecorder'), {
  ssr: false,
});

const MainUI = () => {
  const [userMsg, setUserMsg] = React.useState("");
  const [status, setStatus] = React.useState(""); // Sending, Success, Error

  const statusColors = {
    Sending: "text-gray-500",
    Success: "text-green-600",
    Error: "text-red-600"
  };


  const handleAddClockify = async () => {
    setStatus("Sending");

    console.log("Clicked Add Clockify button with message:", userMsg);

    const url = 'http://localhost:8000/add-time-entry';
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMsg }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const result = await response.json();
      console.log('Success:', result);
      setStatus("Success");

    } catch (error) {
      console.error('Error adding time entry:', error);
      setStatus("Error: ", error)
    }
  }

  return (
    <div className="w-200 mx-auto">
      <textarea placeholder="What you have done today..." className="border p-2 rounded mb-4 w-full h-50" value={userMsg} onInput={(e) => {
        setUserMsg(e.target.value);
        setStatus("");
        }} />
      <div className={`mb-4 ${statusColors.hasOwnProperty(status) ? statusColors[status] : "text-red-600"}`}>{status}</div>
      <div className='flex flex-row gap-4 h-20'>
        <AudioRecorder/>
        <button className="bg-blue-500 text-white px-4 py-2 rounded w-1/2 cursor-pointer disabled:bg-gray-400 disabled:cursor-auto" onClick={handleAddClockify} disabled={!userMsg.trim() || status == "Sending"}>
          Add Clockify
        </button>
      </div>

    </div>
  )
}

export default MainUI