import { useState, KeyboardEvent, useRef, useEffect, ChangeEvent } from "react";

interface ChatInputProps {
  onSend: (text: string) => void;
  isLoading: boolean;
  onUpload: (file: File) => void;
}

export const ChatInput = ({ onSend, isLoading, onUpload }: ChatInputProps) => {
  const [value, setValue] = useState<string>("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleSend = () => {
    if (value.trim() === "" || isLoading) return;
    onSend(value.trim());
    setValue("");

    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    onUpload(file);

    // Reset the input value so the same file can be uploaded again if needed
    e.target.value = "";
  };

  const handleAttachmentClick = () => {
    if (isLoading) return;
    fileInputRef.current?.click();
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 200)}px`;
    }
  }, [value]);

  return (
    <div className="fixed bottom-6 left-0 right-0 px-4 sm:px-6 z-50 flex justify-center pointer-events-none">
      <div className="w-full max-w-2xl flex items-end bg-[#161A23] border border-[#1F2535] rounded-3xl p-1.5 shadow-lg pointer-events-auto transition-all duration-200">
        {/* Hidden File Input */}
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".csv"
          className="hidden"
        />

        {/* Paperclip Button */}
        <button
          onClick={handleAttachmentClick}
          disabled={isLoading}
          className="
            flex-shrink-0 h-10 w-10 sm:h-12 sm:w-12 rounded-full
            text-[#5A6478] flex items-center justify-center text-xl
            hover:text-[#E8ECF4] hover:bg-[#1F2535] active:scale-95 transition-all
            disabled:opacity-40 disabled:cursor-not-allowed disabled:hover:bg-transparent
            mb-0.5 ml-0.5
          "
          type="button"
          aria-label="Upload CSV file"
        >
          <span>&#128206;</span>
        </button>
        {/* The Textarea */}
        <textarea
          ref={textareaRef}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={isLoading}
          rows={1}
          placeholder="Ask Quantly anything..."
          className="
            flex-1 bg-transparent text-[#E8ECF4] placeholder:text-[#5A6478] font-['Inter'] 
            px-4 py-2.5 sm:py-3 text-sm sm:text-base outline-none resize-none leading-relaxed
            disabled:opacity-50
            overflow-y-auto
            [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]
          "
          style={{ maxHeight: "200px" }}
        />

        {/* The Send Button */}
        <button
          onClick={handleSend}
          disabled={isLoading || value.trim() === ""}
          className="
            flex-shrink-0 h-10 w-10 sm:h-12 sm:w-12 rounded-full
            bg-[#4F8EF7] text-white flex items-center justify-center text-lg sm:text-xl
            hover:bg-[#3A76D2] active:scale-95 transition-all
            disabled:bg-[#1F2535] disabled:text-[#5A6478] disabled:cursor-not-allowed
            mb-0.5 mr-0.5
          "
          aria-label="Send message"
        >
          {isLoading ? (
            <span className="animate-pulse text-base">...</span>
          ) : (
            <span className="ml-0.5">&#10148;</span>
          )}
        </button>
      </div>
    </div>
  );
};
