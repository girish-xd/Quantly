import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { ChatWindow } from "./components/ChatWindow";

interface Message {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function App() {
  const [sessionId, setSessionId] = useState<string>("");
  const [sessionToken, setSessionToken] = useState<string>("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Ref to hold pending initialization promise to prevent duplicate requests
  const initPromiseRef = useRef<Promise<{ id: string; token: string }> | null>(null);

  const getOrInitSession = async (): Promise<{ id: string; token: string }> => {
    if (sessionId && sessionToken) {
      return { id: sessionId, token: sessionToken };
    }

    if (initPromiseRef.current) {
      return initPromiseRef.current;
    }

    initPromiseRef.current = (async () => {
      try {
        const response = await axios.post("http://localhost:8000/session");
        const newId = response.data.session_id;
        const newToken = response.data.session_token;
        setSessionId(newId);
        setSessionToken(newToken);
        return { id: newId, token: newToken };
      } catch (err) {
        console.error("Failed to acquire server session:", err);
        throw err;
      } finally {
        initPromiseRef.current = null;
      }
    })();

    return initPromiseRef.current;
  };

  useEffect(() => {
    getOrInitSession().catch(() => {
      // Handled lazily if server is temporarily unreachable on startup
    });
  }, []);

  const sendMessage = async (text: string) => {
    if (isLoading) return;

    setMessages((prev) => [
      ...prev,
      { role: "user", content: text, timestamp: new Date() },
    ]);
    setIsLoading(true);

    try {
      const { id, token } = await getOrInitSession();
      const response = await axios.post(
        "http://localhost:8000/chat",
        {
          message: text,
          session_id: id,
          session_token: token,
        },
        {
          headers: {
            "X-Session-Token": token,
          },
        }
      );

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

    setMessages((prev) => [
      ...prev,
      { role: "user", content: `${file.name} uploaded`, timestamp: new Date() },
    ]);
    setIsLoading(true);

    try {
      const { id, token } = await getOrInitSession();
      const formData = new FormData();
      formData.append("file", file);
      formData.append("session_id", id);
      formData.append("session_token", token);

      const response = await axios.post(
        "http://localhost:8000/upload",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
            "X-Session-Token": token,
          },
        }
      );

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
