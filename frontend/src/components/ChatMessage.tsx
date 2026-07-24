import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";

interface ChatMessageProps {
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export const ChatMessage = ({ role, content, timestamp }: ChatMessageProps) => {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
      className={`flex w-full ${isUser ? "justify-end" : "justify-start"} mb-2`}
    >
      <div
        className={`flex flex-col ${isUser ? "items-end" : "items-start"} max-w-[85%] sm:max-w-[75%]`}
      >
        {/* The Message Bubble */}
        <div
          style={{ fontFamily: '"Inter", sans-serif' }}
          className={`
            rounded-2xl
            ${
              isUser
                ? "bg-gradient-to-br from-[#4F8EF7] to-[#1E5DE3] shadow-[0_2px_10px_rgba(30,93,227,0.2),inset_0_1px_0_rgba(255,255,255,0.15)] text-white px-4 py-2 rounded-br-sm"
                : "bg-gradient-to-br from-[#1C212D] to-[#161A23] border border-[#1F2535] shadow-sm text-[#E8ECF4] px-6 py-3 rounded-bl-sm"
            }
          `}
        >
          {isUser ? (
            <p className="leading-snug">{content}</p>
          ) : (
            <div className="leading-relaxed prose prose-invert prose-sm max-w-none prose-p:last:mb-0">
              <ReactMarkdown>{content}</ReactMarkdown>
            </div>
          )}
        </div>
        {/*Timestamp*/}
        <span
          className={`text-[11px] mt-1.5 ${isUser ? "mr-1" : "ml-1"}`}
          style={{ color: "#5A6478" }}
        >
          {timestamp.toLocaleTimeString([], {
            hour: "2-digit",
            minute: "2-digit",
          })}
        </span>
      </div>
    </motion.div>
  );
};

// import { motion } from "framer-motion";
// import ReactMarkdown from "react-markdown";

// interface ChatMessageProps {
//   role: "user" | "assistant";
//   content: string;
//   timestamp: Date;
// }

// export const ChatMessage = ({ role, content, timestamp }: ChatMessageProps) => {
//   const isUser = role === "user";

//   return (
//     <motion.div
//       initial={{ opacity: 0, y: 12 }}
//       animate={{ opacity: 1, y: 0 }}
//       transition={{ duration: 0.3, ease: "easeOut" }}
//       className={`flex w-full ${isUser ? "justify-end" : "justify-start"} mb-6`}
//     >
//       <div
//         style={{ fontFamily: '"Inter", sans-serif' }}
//         className={`
//           max-w-[85%] sm:max-w-[75%] rounded-2xl
//           ${
//             isUser
//               ? "bg-gradient-to-br from-[#4F8EF7] to-[#1E5DE3] shadow-[0_2px_10px_rgba(30,93,227,0.2),inset_0_1px_0_rgba(255,255,255,0.15)] text-white px-4 py-2.5 rounded-br-sm"
//               : "bg-gradient-to-br from-[#1C212D] to-[#161A23] border border-[#1F2535] shadow-sm text-[#E8ECF4] px-6 py-4 rounded-bl-sm"
//           }
//         `}
//       >
//         {isUser ? (
//           <p className="leading-snug">{content}</p>
//         ) : (
//           <div className="leading-relaxed prose prose-invert prose-sm max-w-none prose-p:last:mb-0">
//             <ReactMarkdown>{content}</ReactMarkdown>
//           </div>
//         )}
//       </div>
//       <span
//         className="bottom-1 right-2 text-[11px]"
//         style={{ color: "#5A6478" }}
//       >
//         {timestamp.toLocaleTimeString([], {
//           hour: "2-digit",
//           minute: "2-digit",
//         })}
//       </span>
//     </motion.div>
//   );
// };
