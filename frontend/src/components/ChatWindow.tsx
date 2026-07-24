import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChatMessage } from "./ChatMessage";
import { ChatInput } from "./ChatInput";
import { ThinkingIndicator } from "./ThinkingIndicator";
import { Header } from "./header";
import { EmptyState } from "./EmptyState";

interface ChatWindowProps {
  messages: { role: "user" | "assistant"; content: string; timestamp: Date }[];
  isLoading: boolean;
  onSend: (text: string) => void;
  onUpload: (file: File) => void;
}

export const ChatWindow = ({
  messages,
  isLoading,
  onSend,
  onUpload,
}: ChatWindowProps) => {
  const messagesEndRef = useRef(null);

  // Auto-scroll when a new message appears
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const isEmpty = messages.length === 0 && !isLoading;

  return (
    <div className="w-full h-[100dvh] bg-[#0D0F14] overflow-hidden relative text-[#E8ECF4]">
      <AnimatePresence mode="wait">
        {isEmpty ? (
          <EmptyState onSend={onSend} isLoading={isLoading} />
        ) : (
          <motion.div
            key="chat-interface"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="flex flex-col h-full w-full"
          >
            <Header />

            <main className="flex-1 overflow-y-auto pt-24 pb-6 px-4 sm:px-6 w-full flex justify-center">
              <div className="w-full max-w-xl flex flex-col gap-4 relative">
                <AnimatePresence mode="popLayout">
                  {messages.map((msg, index) => (
                    <motion.div
                      key={`msg-${index}`}
                      layout
                      initial={{ opacity: 0, y: 10, scale: 0.95 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                      transition={{ duration: 0.2 }}
                    >
                      <ChatMessage
                        role={msg.role}
                        content={msg.content}
                        timestamp={msg.timestamp}
                      />
                    </motion.div>
                  ))}

                  {isLoading && (
                    <motion.div
                      key="thinking-indicator"
                      layout
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, scale: 0.95 }}
                    >
                      <ThinkingIndicator />
                    </motion.div>
                  )}
                </AnimatePresence>

                <div
                  ref={messagesEndRef}
                  className="h-4 w-full flex-shrink-0"
                />
              </div>
            </main>

            <div className="w-full bg-[#0D0F14] border-t border-[#1F2535] p-4 flex justify-center flex-shrink-0 z-10">
              <div className="w-full max-w-[600px]">
                <ChatInput
                  onSend={onSend}
                  isLoading={isLoading}
                  onUpload={onUpload}
                />
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
