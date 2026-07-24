import { useState } from "react";
import axios from "axios";
import { ChatWindow } from "./components/ChatWindow";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

// const SESSION_ID = "session_123";

export default function App() {
  const [sessionId] = useState(() => crypto.randomUUID());

  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const sendMessage = async (text: string) => {
    // Is the assistant is responding, user cannot send the messages
    if (isLoading) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: text, timestamp: new Date() },
    ]); //Append the user message to message list
    setIsLoading(true); //assistant will be responding when the user sends a message

    try {
      const response = await axios.post("http://localhost:8000/chat", {
        message: text,
        session_id: sessionId,
      });

      // Append the assistant's response to the message list
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.data.response,
          timestamp: new Date(),
        },
      ]);
    } catch (error) {
      console.error("Chat API Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Something went wrong. Please try again.",
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleUpload = async (file: File) => {
    if (isLoading) return;

    // 1. Instantly inject user placeholder message for the upload action
    setMessages((prev) => [
      ...prev,
      { role: "user", content: `${file.name} uploaded`, timestamp: new Date() },
    ]);
    setIsLoading(true);

    // 2. Build the multipart/form-data payload
    const formData = new FormData();
    formData.append("file", file);
    formData.append("session_id", sessionId);

    try {
      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        },
      );

      // 3. Inject the successful assistant response matching the /chat format
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: response.data.response,
          timestamp: new Date(),
        },
      ]);
    } catch (error) {
      console.error("Upload API Error:", error);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `Failed to upload ${file.name}. Please try again.`,
          timestamp: new Date(),
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <ChatWindow
      messages={messages}
      isLoading={isLoading}
      onSend={sendMessage}
      onUpload={handleUpload}
    />
  );
}

// import { useState } from "react";
// import { ChatWindow } from "./components/ChatWindow";

// function App() {
//   const [messages] = useState<
//     { role: "user" | "assistant"; content: string }[]
//   >([
//     { role: "user", content: "What's the current price of RELIANCE?" },
//     {
//       role: "assistant",
//       content:
//         "Reliance Industries is currently trading at ₹2,847.50, up 1.2% today.",
//     },
//     { role: "user", content: "Give me a market summary." },
//   ]);

//   return (
//     <ChatWindow
//       messages={messages}
//       isLoading={false}
//       onSend={(text) => console.log(text)}
//     />
//   );
// }

// export default App;
