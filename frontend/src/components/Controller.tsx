import React, { useState } from "react";

import Title from "./Title"

function Controller() {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState<any[]>([]);

  const createBlobUrl = (data: any) => {};

  const handleStop = async () => {};

  return (
    <div className="h-screen overflow-y-hidden">
        <Title setMessages={setMessages}></Title>
      <div className="flex flex-col justify-between h-full overflow-y-scroll pb-96">
      <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-sky-500 to-green-500">
          <div className="flex justify-center items-center w-full">
            <div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Controller;