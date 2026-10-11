import { motion } from "framer-motion";


export const Header = () => {
  return (
    <motion.header
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="fixed top-0 inset-x-0 h-16 flex items-center justify-between px-6 bg-[#0D0F14]/80 backdrop-blur-md border-b border-[#1F2535] z-20"
    >
      <div className="text-[#4F8EF7] font-bold text-xl tracking-wide">
        Quantly
      </div>
      <div className="text-[#5A6478] text-sm font-medium">
        Personal Finance AI
      </div>
    </motion.header>
  );
};
