import React from "react";
import { useReactMediaRecorder } from "react-media-recorder-2";


const AudioRecorder = ({ onSpeechToTextCompleted }) => {
  const { status, startRecording, stopRecording, mediaBlobUrl } =
    useReactMediaRecorder({ audio: true });

    const [currentBlobUrl, setCurrentBlobUrl] = React.useState(null);
    const [inProgressSTT, setInProgressSTT] = React.useState(false);

    React.useEffect(() => {
      if (status === "recording") {
        setCurrentBlobUrl(null)
      }
    }, [status])

    React.useEffect(() => {
      if (mediaBlobUrl) {
        setCurrentBlobUrl(mediaBlobUrl)
      }
    }, [mediaBlobUrl])

  const handleSendToBackend = async () => {
    if (!mediaBlobUrl) return;

    setInProgressSTT(true);

    // Chuyển đổi blob url thành file thực tế
    const audioBlob = await fetch(mediaBlobUrl).then((r) => r.blob());
    const formData = new FormData();
    formData.append("file", audioBlob, "speech.wav");

    // Gửi đến FastAPI
    const response = await fetch("http://localhost:8000/stt", {
      method: "POST",
      body: formData,
    });
    const result = await response.json();
    console.log("Server response:", result.transcript);
    onSpeechToTextCompleted(result.transcript)

    setInProgressSTT(false);
  };

  return (
    <div className="w-full flex flex-row gap-4">
      {status === "idle" || status === "stopped" ? 
        (<button className="bg-green-600 text-white px-4 py-2 cursor-pointer rounded min-w-[200]" onClick={startRecording}>Start Speaking</button>) :
        (<button className="bg-rose-400 text-white px-4 py-2 cursor-pointer rounded min-w-[200]" onClick={stopRecording}>Stop</button>)
      }
      
      {currentBlobUrl && (
        <button className="bg-blue-500 text-white px-4 py-2 cursor-pointer rounded min-w-[200] disabled:bg-gray-400 disabled:cursor-auto" onClick={handleSendToBackend} disabled={inProgressSTT}>Speech To Text</button>
      )}
    </div>
  );
};

export default AudioRecorder