'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, MessageCircle, Volume2 } from 'lucide-react';

interface ProfessorRouedProps {
  message?: string;
  isVisible?: boolean;
  onClose?: () => void;
  mood?: 'happy' | 'encouraging' | 'proud' | 'thinking';
}

/**
 * Professor Roued - AI Tutor Component
 * 
 * Personality:
 * - Humorous and authoritative
 * - Arabic/Tunisian cultural context
 * - Encouraging and motivational
 * - Expert in German language
 * 
 * Brand Voice: "Lerne Deutsch, bevor das Bier warm wird!"
 */
export const ProfessorRoued: React.FC<ProfessorRouedProps> = ({
  message = "Lerne Deutsch, bevor das Bier warm wird!",
  isVisible = true,
  onClose,
  mood = 'happy',
}) => {
  const [displayedText, setDisplayedText] = useState('');
  const [isTyping, setIsTyping] = useState(true);

  // Typewriter effect
  useEffect(() => {
    if (!isTyping || !message) return;

    let index = 0;
    const interval = setInterval(() => {
      if (index < message.length) {
        setDisplayedText(message.substring(0, index + 1));
        index++;
      } else {
        setIsTyping(false);
      }
    }, 30);

    return () => clearInterval(interval);
  }, [message, isTyping]);

  // Mood-based expressions
  const moodExpressions = {
    happy: '😄',
    encouraging: '💪',
    proud: '🎓',
    thinking: '🤔',
  };

  // Mood-based colors
  const moodColors = {
    happy: 'from-green-400 to-emerald-500',
    encouraging: 'from-orange-400 to-amber-500',
    proud: 'from-blue-400 to-indigo-500',
    thinking: 'from-purple-400 to-pink-500',
  };

  const containerVariants = {
    hidden: { opacity: 0, scale: 0.8, y: 20 },
    visible: {
      opacity: 1,
      scale: 1,
      y: 0,
      transition: { duration: 0.4, ease: 'easeOut' },
    },
    exit: {
      opacity: 0,
      scale: 0.8,
      y: 20,
      transition: { duration: 0.3 },
    },
  };

  const messageVariants = {
    hidden: { opacity: 0, y: 10 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { delay: 0.2, duration: 0.3 },
    },
  };

  const pulseVariants = {
    animate: {
      scale: [1, 1.05, 1],
      transition: { duration: 2, repeat: Infinity },
    },
  };

  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
          className="fixed bottom-8 right-8 z-50 max-w-sm"
        >
          {/* Professor Avatar */}
          <motion.div
            variants={pulseVariants}
            animate="animate"
            className={`mb-4 w-20 h-20 rounded-full bg-gradient-to-br ${moodColors[mood]} shadow-lg flex items-center justify-center text-4xl cursor-pointer hover:shadow-xl transition-shadow`}
            onClick={onClose}
          >
            <span>{moodExpressions[mood]}</span>
          </motion.div>

          {/* Message Bubble */}
          <motion.div
            variants={messageVariants}
            className="glass rounded-2xl p-6 shadow-xl border border-white/20"
          >
            {/* Header */}
            <div className="flex items-center gap-2 mb-3">
              <Sparkles className="w-5 h-5 text-primary" />
              <h3 className="font-bold text-lg text-primary">Professor Roued</h3>
            </div>

            {/* Message */}
            <p className="text-neutral-700 dark:text-neutral-200 text-sm leading-relaxed mb-4">
              {displayedText}
              {isTyping && <span className="animate-pulse">▌</span>}
            </p>

            {/* Action Buttons */}
            <div className="flex gap-2">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="flex-1 flex items-center justify-center gap-2 bg-primary text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-primary-dark transition-colors"
              >
                <Volume2 className="w-4 h-4" />
                Listen
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onClose}
                className="flex-1 flex items-center justify-center gap-2 bg-neutral-200 dark:bg-neutral-700 text-neutral-900 dark:text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-neutral-300 dark:hover:bg-neutral-600 transition-colors"
              >
                <MessageCircle className="w-4 h-4" />
                Close
              </motion.button>
            </div>
          </motion.div>

          {/* Floating particles */}
          {[...Array(3)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-primary rounded-full"
              animate={{
                x: [0, Math.random() * 100 - 50],
                y: [0, Math.random() * 100 - 50],
                opacity: [1, 0],
              }}
              transition={{
                duration: 2,
                delay: i * 0.2,
                repeat: Infinity,
              }}
              style={{
                left: '50%',
                top: '50%',
              }}
            />
          ))}
        </motion.div>
      )}
    </AnimatePresence>
  );
};

/**
 * Professor Roued Messages Library
 * Contextual messages for different scenarios
 */
export const ProfessorRouedMessages = {
  welcome: {
    text: "Willkommen! Ich bin Professor Roued. Lerne Deutsch, bevor das Bier warm wird!",
    mood: 'happy' as const,
  },
  encouragement: {
    text: "Du machst großartige Fortschritte! Weiter so! 💪",
    mood: 'encouraging' as const,
  },
  correct: {
    text: "Perfekt! Das ist richtig. Du wirst ein Deutsch-Meister!",
    mood: 'proud' as const,
  },
  incorrect: {
    text: "Nicht ganz. Versuch es nochmal. Jeder Fehler ist eine Lektion!",
    mood: 'thinking' as const,
  },
  milestone: {
    text: "Glückwunsch! Du hast einen Meilenstein erreicht! 🎉",
    mood: 'proud' as const,
  },
  daily_reminder: {
    text: "Zeit zum Lernen! Dein Gehirn wartet auf neue Wörter!",
    mood: 'encouraging' as const,
  },
  streak: {
    text: "Wow! Du hast eine großartige Lernsträhne! Halte sie am Laufen!",
    mood: 'happy' as const,
  },
};

export default ProfessorRoued;
