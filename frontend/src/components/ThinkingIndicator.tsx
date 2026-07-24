import { useState, useEffect } from "react";
import { motion } from "framer-motion";

const PHRASES = ["Thinking...", "Crunching numbers...", "Fetching data..."];

export const ThinkingIndicator = () => {
  const [phraseIndex, setPhraseIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPhraseIndex((prev) => (prev + 1) % PHRASES.length);
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className="flex w-full justify-start mb-6"
    >
      <div
        className="
          max-w-[85%] sm:max-w-[75%] rounded-2xl font-['Inter'] px-6 py-4 rounded-bl-sm
          flex items-center gap-4
        "
      >
        {/* 1. Pulsing Dots */}
        <div className="flex gap-1.5">
          {[0, 0.15, 0.3].map((delay, i) => (
            <motion.div
              key={i}
              animate={{ scale: [1, 1.4, 1] }}
              transition={{
                duration: 1.2,
                repeat: Infinity,
                ease: "easeInOut",
                delay: delay,
              }}
              className="w-2 h-2 rounded-full bg-[#4F8EF7]"
            />
          ))}
        </div>

        {/* 2. Cycling Sub-text */}
        <span className="text-[#5A6478] text-sm font-medium w-[140px] truncate">
          {PHRASES[phraseIndex]}
        </span>
      </div>
    </motion.div>
  );
};
