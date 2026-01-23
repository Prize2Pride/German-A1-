'use client';

import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Volume2, RotateCcw, ThumbsUp, ThumbsDown, ChevronLeft, ChevronRight } from 'lucide-react';
import Layout from '@/components/Layout';

interface Flashcard {
  id: number;
  front: string;
  back: string;
  pronunciation: string;
  example: string;
  difficulty: 'easy' | 'medium' | 'hard';
  nextReview: Date;
}

const Flashcards = () => {
  const [cards, setCards] = useState<Flashcard[]>([
    {
      id: 1,
      front: 'Guten Morgen',
      back: 'Good morning',
      pronunciation: 'GOO-ten MOR-gen',
      example: 'Guten Morgen! Wie geht es dir?',
      difficulty: 'easy',
      nextReview: new Date(),
    },
    {
      id: 2,
      front: 'Danke schön',
      back: 'Thank you very much',
      pronunciation: 'DAHN-kuh SHÖN',
      example: 'Danke schön für deine Hilfe!',
      difficulty: 'easy',
      nextReview: new Date(),
    },
    {
      id: 3,
      front: 'Das Perfekt',
      back: 'The perfect tense (past)',
      pronunciation: 'dahs PAIR-fekt',
      example: 'Ich habe das Buch gelesen.',
      difficulty: 'hard',
      nextReview: new Date(),
    },
    {
      id: 4,
      front: 'Wunderbar',
      back: 'Wonderful, marvelous',
      pronunciation: 'VOON-der-bar',
      example: 'Das ist wunderbar!',
      difficulty: 'medium',
      nextReview: new Date(),
    },
  ]);

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [reviewedCount, setReviewedCount] = useState(0);
  const [masteredCount, setMasteredCount] = useState(0);

  const currentCard = cards[currentIndex];

  const handleNext = () => {
    if (currentIndex < cards.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setIsFlipped(false);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setIsFlipped(false);
    }
  };

  const handleReview = (quality: 'easy' | 'medium' | 'hard') => {
    setReviewedCount(reviewedCount + 1);
    if (quality === 'easy') {
      setMasteredCount(masteredCount + 1);
    }
    handleNext();
  };

  const cardVariants = {
    hidden: { opacity: 0, scale: 0.8, rotateY: -90 },
    visible: {
      opacity: 1,
      scale: 1,
      rotateY: 0,
      transition: { duration: 0.5 },
    },
    exit: {
      opacity: 0,
      scale: 0.8,
      rotateY: 90,
      transition: { duration: 0.3 },
    },
  };

  const flipVariants = {
    hidden: { rotateY: 0 },
    flipped: { rotateY: 180 },
  };

  return (
    <Layout>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="max-w-2xl mx-auto space-y-8"
      >
        {/* Header */}
        <motion.div
          initial={{ y: -20 }}
          animate={{ y: 0 }}
        >
          <h1 className="text-4xl font-bold text-neutral-900 dark:text-white mb-2">
            🎯 Flashcard Review
          </h1>
          <p className="text-neutral-600 dark:text-neutral-400">
            Master German vocabulary with spaced repetition
          </p>
        </motion.div>

        {/* Progress */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="bg-white dark:bg-neutral-800 rounded-xl p-6 border border-neutral-200 dark:border-neutral-700"
        >
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-semibold text-neutral-900 dark:text-white">
              Progress: {currentIndex + 1} / {cards.length}
            </h3>
            <span className="text-sm text-neutral-600 dark:text-neutral-400">
              Mastered: {masteredCount}
            </span>
          </div>
          <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${((currentIndex + 1) / cards.length) * 100}%` }}
              transition={{ duration: 0.5 }}
              className="h-full rounded-full bg-gradient-to-r from-primary to-accent"
            />
          </div>
        </motion.div>

        {/* Flashcard */}
        <AnimatePresence mode="wait">
          {currentCard && (
            <motion.div
              key={currentCard.id}
              variants={cardVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
              onClick={() => setIsFlipped(!isFlipped)}
              className="h-80 cursor-pointer perspective"
            >
              <motion.div
                variants={flipVariants}
                animate={isFlipped ? 'flipped' : 'hidden'}
                transition={{ duration: 0.6 }}
                className="relative w-full h-full"
                style={{ transformStyle: 'preserve-3d' }}
              >
                {/* Front */}
                <motion.div
                  className="absolute w-full h-full bg-gradient-to-br from-primary/20 to-accent/20 rounded-2xl p-8 flex flex-col items-center justify-center border-2 border-primary/30 shadow-xl"
                  style={{ backfaceVisibility: 'hidden' }}
                >
                  <p className="text-5xl font-bold text-neutral-900 dark:text-white text-center mb-4">
                    {currentCard.front}
                  </p>
                  <p className="text-sm text-neutral-600 dark:text-neutral-400 italic">
                    {currentCard.pronunciation}
                  </p>
                  <p className="text-center text-neutral-600 dark:text-neutral-400 mt-8 text-sm">
                    Click to reveal
                  </p>
                </motion.div>

                {/* Back */}
                <motion.div
                  className="absolute w-full h-full bg-gradient-to-br from-accent/20 to-gold/20 rounded-2xl p-8 flex flex-col items-center justify-center border-2 border-accent/30 shadow-xl"
                  style={{ backfaceVisibility: 'hidden', transform: 'rotateY(180deg)' }}
                >
                  <div className="text-center space-y-6">
                    <div>
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                        Translation
                      </p>
                      <p className="text-3xl font-bold text-neutral-900 dark:text-white">
                        {currentCard.back}
                      </p>
                    </div>

                    <div className="border-t border-neutral-300 dark:border-neutral-600 pt-6">
                      <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-2">
                        Example
                      </p>
                      <p className="text-lg text-neutral-900 dark:text-white italic">
                        {currentCard.example}
                      </p>
                    </div>
                  </div>
                </motion.div>
              </motion.div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Controls */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="space-y-6"
        >
          {/* Audio & Navigation */}
          <div className="flex justify-between items-center">
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-3 rounded-full bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
            >
              <Volume2 className="w-6 h-6 text-primary" />
            </motion.button>

            <div className="flex gap-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handlePrevious}
                disabled={currentIndex === 0}
                className="p-3 rounded-full bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors disabled:opacity-50"
              >
                <ChevronLeft className="w-6 h-6" />
              </motion.button>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handleNext}
                disabled={currentIndex === cards.length - 1}
                className="p-3 rounded-full bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors disabled:opacity-50"
              >
                <ChevronRight className="w-6 h-6" />
              </motion.button>
            </div>

            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              className="p-3 rounded-full bg-white dark:bg-neutral-800 border border-neutral-200 dark:border-neutral-700 hover:bg-neutral-100 dark:hover:bg-neutral-700 transition-colors"
            >
              <RotateCcw className="w-6 h-6 text-neutral-600 dark:text-neutral-400" />
            </motion.button>
          </div>

          {/* Review Buttons */}
          <div className="grid grid-cols-3 gap-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleReview('hard')}
              className="bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-300 rounded-lg py-3 font-semibold hover:bg-red-200 dark:hover:bg-red-900/50 transition-colors flex items-center justify-center gap-2"
            >
              <ThumbsDown className="w-4 h-4" />
              Hard
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleReview('medium')}
              className="bg-yellow-100 dark:bg-yellow-900/30 text-yellow-700 dark:text-yellow-300 rounded-lg py-3 font-semibold hover:bg-yellow-200 dark:hover:bg-yellow-900/50 transition-colors"
            >
              Medium
            </motion.button>

            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => handleReview('easy')}
              className="bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 rounded-lg py-3 font-semibold hover:bg-green-200 dark:hover:bg-green-900/50 transition-colors flex items-center justify-center gap-2"
            >
              <ThumbsUp className="w-4 h-4" />
              Easy
            </motion.button>
          </div>
        </motion.div>

        {/* Completion Message */}
        {currentIndex === cards.length - 1 && reviewedCount === cards.length && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-gradient-to-r from-primary to-accent rounded-xl p-8 text-white text-center"
          >
            <p className="text-3xl font-bold mb-2">🎉 Session Complete!</p>
            <p className="text-lg opacity-90">
              You mastered {masteredCount} out of {cards.length} cards
            </p>
          </motion.div>
        )}
      </motion.div>
    </Layout>
  );
};

export default Flashcards;
