'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, BookOpen, Clock, Users, Star } from 'lucide-react';
import Layout from '@/components/Layout';

interface Lesson {
  id: number;
  title: string;
  level: 'A1' | 'A2';
  category: string;
  duration: number;
  difficulty: number;
  students: number;
  rating: number;
  image: string;
  description: string;
  completed: boolean;
}

const Lessons = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedLevel, setSelectedLevel] = useState<'all' | 'A1' | 'A2'>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  const lessons: Lesson[] = [
    {
      id: 1,
      title: 'Saying Hello - Formal',
      level: 'A1',
      category: 'Greetings',
      duration: 15,
      difficulty: 1,
      students: 2450,
      rating: 4.8,
      image: '👋',
      description: 'Learn formal greetings in German',
      completed: true,
    },
    {
      id: 2,
      title: 'Introducing Yourself',
      level: 'A1',
      category: 'Introduction',
      duration: 20,
      difficulty: 1,
      students: 2100,
      rating: 4.7,
      image: '🎤',
      description: 'Master the art of self-introduction',
      completed: true,
    },
    {
      id: 3,
      title: 'Das Perfekt - Perfect Tense',
      level: 'A2',
      category: 'Grammar',
      duration: 45,
      difficulty: 3,
      students: 1850,
      rating: 4.9,
      image: '⏰',
      description: 'Master the German perfect tense',
      completed: false,
    },
    {
      id: 4,
      title: 'Food & Dining',
      level: 'A1',
      category: 'Vocabulary',
      duration: 30,
      difficulty: 2,
      students: 1650,
      rating: 4.6,
      image: '🍽️',
      description: 'Learn food and dining vocabulary',
      completed: false,
    },
    {
      id: 5,
      title: 'Weather & Seasons',
      level: 'A1',
      category: 'Vocabulary',
      duration: 25,
      difficulty: 1,
      students: 1920,
      rating: 4.7,
      image: '🌤️',
      description: 'Discuss weather and seasons',
      completed: true,
    },
    {
      id: 6,
      title: 'Asking for Directions',
      level: 'A2',
      category: 'Conversation',
      duration: 35,
      difficulty: 2,
      students: 1450,
      rating: 4.8,
      image: '🗺️',
      description: 'Navigate and ask for directions',
      completed: false,
    },
  ];

  const categories = ['all', 'Greetings', 'Introduction', 'Grammar', 'Vocabulary', 'Conversation'];

  const filteredLessons = lessons.filter((lesson) => {
    const matchesSearch = lesson.title.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesLevel = selectedLevel === 'all' || lesson.level === selectedLevel;
    const matchesCategory = selectedCategory === 'all' || lesson.category === selectedCategory;
    return matchesSearch && matchesLevel && matchesCategory;
  });

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.4 },
    },
  };

  const LessonCard = ({ lesson }: { lesson: Lesson }) => (
    <motion.div
      variants={itemVariants}
      whileHover={{ y: -5 }}
      className="bg-white dark:bg-neutral-800 rounded-xl overflow-hidden shadow-md hover:shadow-xl transition-shadow border border-neutral-200 dark:border-neutral-700 cursor-pointer group"
    >
      {/* Image */}
      <div className="h-40 bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center text-6xl group-hover:scale-110 transition-transform">
        {lesson.image}
      </div>

      {/* Content */}
      <div className="p-6">
        <div className="flex items-start justify-between mb-3">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold px-2 py-1 rounded-full bg-primary/20 text-primary">
                {lesson.level}
              </span>
              {lesson.completed && (
                <span className="text-xs font-bold px-2 py-1 rounded-full bg-green-100 text-green-700">
                  ✓ Completed
                </span>
              )}
            </div>
            <h3 className="text-lg font-bold text-neutral-900 dark:text-white">
              {lesson.title}
            </h3>
          </div>
        </div>

        <p className="text-sm text-neutral-600 dark:text-neutral-400 mb-4">
          {lesson.description}
        </p>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-3 mb-4 py-3 border-y border-neutral-200 dark:border-neutral-700">
          <div className="text-center">
            <Clock className="w-4 h-4 mx-auto text-primary mb-1" />
            <p className="text-xs font-semibold text-neutral-900 dark:text-white">
              {lesson.duration}m
            </p>
          </div>
          <div className="text-center">
            <Users className="w-4 h-4 mx-auto text-accent mb-1" />
            <p className="text-xs font-semibold text-neutral-900 dark:text-white">
              {lesson.students.toLocaleString()}
            </p>
          </div>
          <div className="text-center">
            <Star className="w-4 h-4 mx-auto text-gold mb-1" />
            <p className="text-xs font-semibold text-neutral-900 dark:text-white">
              {lesson.rating}
            </p>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2 mb-4">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: lesson.completed ? '100%' : '65%' }}
            transition={{ duration: 0.8 }}
            className="h-full rounded-full bg-gradient-to-r from-primary to-accent"
          />
        </div>

        {/* Button */}
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          className="w-full bg-primary text-white rounded-lg py-2 font-semibold hover:bg-primary-dark transition-colors"
        >
          {lesson.completed ? 'Review' : 'Start Lesson'}
        </motion.button>
      </div>
    </motion.div>
  );

  return (
    <Layout>
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="space-y-8"
      >
        {/* Header */}
        <motion.div variants={itemVariants}>
          <h1 className="text-4xl font-bold text-neutral-900 dark:text-white mb-2">
            📚 German Lessons
          </h1>
          <p className="text-neutral-600 dark:text-neutral-400">
            Choose from {lessons.length} carefully crafted lessons to master German
          </p>
        </motion.div>

        {/* Search & Filters */}
        <motion.div variants={itemVariants} className="space-y-4">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 w-5 h-5 text-neutral-400" />
            <input
              type="text"
              placeholder="Search lessons..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-12 pr-4 py-3 rounded-lg border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white placeholder-neutral-400 focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            />
          </div>

          {/* Filters */}
          <div className="flex flex-wrap gap-3">
            {/* Level Filter */}
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-neutral-600 dark:text-neutral-400" />
              <select
                value={selectedLevel}
                onChange={(e) => setSelectedLevel(e.target.value as any)}
                className="px-4 py-2 rounded-lg border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white text-sm font-medium focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
              >
                <option value="all">All Levels</option>
                <option value="A1">A1 (Beginner)</option>
                <option value="A2">A2 (Elementary)</option>
              </select>
            </div>

            {/* Category Filter */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-4 py-2 rounded-lg border border-neutral-200 dark:border-neutral-700 bg-white dark:bg-neutral-800 text-neutral-900 dark:text-white text-sm font-medium focus:ring-2 focus:ring-primary focus:border-transparent transition-all"
            >
              {categories.map((cat) => (
                <option key={cat} value={cat}>
                  {cat === 'all' ? 'All Categories' : cat}
                </option>
              ))}
            </select>
          </div>
        </motion.div>

        {/* Lessons Grid */}
        <motion.div
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          {filteredLessons.map((lesson) => (
            <LessonCard key={lesson.id} lesson={lesson} />
          ))}
        </motion.div>

        {/* Empty State */}
        {filteredLessons.length === 0 && (
          <motion.div
            variants={itemVariants}
            className="text-center py-12"
          >
            <BookOpen className="w-16 h-16 mx-auto text-neutral-400 mb-4" />
            <h3 className="text-xl font-bold text-neutral-900 dark:text-white mb-2">
              No lessons found
            </h3>
            <p className="text-neutral-600 dark:text-neutral-400">
              Try adjusting your filters or search query
            </p>
          </motion.div>
        )}
      </motion.div>
    </Layout>
  );
};

export default Lessons;
