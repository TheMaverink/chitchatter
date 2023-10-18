import React, { useState } from "react";
import RecordMessage from "./RecordMessage";

import Title from "./Title";

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  

  const createBlobUrl = (data: any) => {
    const blob = new Blob([data],{type:"audio/mpeg"})
    const url = window.URL.createObjectURL(blob)
    return url
  };

  const handleStop = async (blobUrl:string) => {
    console.log(blobUrl)

    try{

      setIsLoading(true)

      const myMessage = {sender:"me",blobUrl}
  
      const messagesArr = [...messages,myMessage]
  
      setIsLoading(false)

     const response =  await fetch(blobUrl)
     const blob = await response.blob()

     const formData = new FormData();
     formData.append("file", blob, "myFile.wav");

    }catch(error){

    }



  };

  return (
    <div className="h-screen overflow-y-hidden">
      <Title setMessages={setMessages}></Title>
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
        
        <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <div>
              <RecordMessage handleStop={handleStop} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Controller;
