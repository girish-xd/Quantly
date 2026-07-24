import { motion } from "framer-motion";
import { ChatInput } from "./ChatInput";

interface EmptyStateProps {
  onSend: (text: string) => void;
  isLoading: boolean;
  onUpload: (file: File) => void;
}

const SUGGESTIONS = [
  "What is the price of RELIANCE today?",
  "Give me a market summary",
  "Latest news on HDFC",
  "Help me plan a budget",
];

export const EmptyState = ({
  onSend,
  isLoading,
  onUpload,
}: EmptyStateProps) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="min-h-screen flex flex-col items-center justify-center px-4 w-full bg-[#0D0F14]"
    >
      {/* Titles */}
      <div className="text-center mb-8">
        <h1 className="text-[#4F8EF7] text-5xl md:text-6xl font-bold mb-2 tracking-tight">
          Quantly
        </h1>
        <p className="text-[#5A6478] text-lg font-medium">
          Your personal finance AI
        </p>
      </div>

      {/* Input */}
      <div className="w-full max-w-[600px] mb-8">
        <ChatInput onSend={onSend} isLoading={isLoading} onUpload={onUpload} />
      </div>

      {/* Suggestions */}
      <div className="flex flex-wrap justify-center gap-3 w-full max-w-3xl">
        {SUGGESTIONS.map((suggestion, index) => (
          <button
            key={index}
            onClick={() => onSend(suggestion)}
            className="px-4 py-2 rounded-full bg-[#161A23] border border-[#4F8EF7] text-[#5A6478] hover:text-[#E8ECF4] hover:bg-[#1F2535] transition-colors text-sm font-medium"
          >
            {suggestion}
          </button>
        ))}
      </div>
    </motion.div>
  );
};
