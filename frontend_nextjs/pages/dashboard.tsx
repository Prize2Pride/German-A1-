'use client';

import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Zap, BookOpen, Trophy, Flame, Target, Award } from 'lucide-react';
import Layout from '@/components/Layout';

interface DashboardStats {
  dailyXP: number;
  totalXP: number;
  streak: number;
  lessonsCompleted: number;
  cardsReviewed: number;
  masteredCards: number;
  accuracy: number;
}

interface ChartData {
  date: string;
  xp: number;
  lessons: number;
  cards: number;
}

const Dashboard = () => {
  const [stats, setStats] = useState<DashboardStats>({
    dailyXP: 150,
    totalXP: 4250,
    streak: 12,
    lessonsCompleted: 24,
    cardsReviewed: 342,
    masteredCards: 156,
    accuracy: 87,
  });

  const [chartData] = useState<ChartData[]>([
    { date: 'Mon', xp: 120, lessons: 2, cards: 45 },
    { date: 'Tue', xp: 150, lessons: 3, cards: 52 },
    { date: 'Wed', xp: 100, lessons: 1, cards: 38 },
    { date: 'Thu', xp: 180, lessons: 4, cards: 68 },
    { date: 'Fri', xp: 160, lessons: 3, cards: 55 },
    { date: 'Sat', xp: 200, lessons: 5, cards: 72 },
    { date: 'Sun', xp: 140, lessons: 2, cards: 42 },
  ]);

  const skillData = [
    { name: 'Reading', value: 92, color: '#22c55e' },
    { name: 'Writing', value: 78, color: '#f59e0b' },
    { name: 'Listening', value: 85, color: '#3b82f6' },
    { name: 'Speaking', value: 72, color: '#8b5cf6' },
  ];

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

  const StatCard = ({ icon: Icon, label, value, unit, color }: any) => (
    <motion.div
      variants={itemVariants}
      className="bg-white dark:bg-neutral-800 rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow border border-neutral-200 dark:border-neutral-700"
    >
      <div className="flex items-start justify-between">
        <div>
          <p className="text-neutral-600 dark:text-neutral-400 text-sm font-medium mb-2">{label}</p>
          <p className="text-3xl font-bold text-neutral-900 dark:text-white">
            {value}
            <span className="text-lg text-neutral-500 ml-1">{unit}</span>
          </p>
        </div>
        <div className={`p-3 rounded-lg bg-gradient-to-br ${color}`}>
          <Icon className="w-6 h-6 text-white" />
        </div>
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
            Welcome back, Learner! 👋
          </h1>
          <p className="text-neutral-600 dark:text-neutral-400">
            You're on a {stats.streak}-day streak. Keep it up!
          </p>
        </motion.div>

        {/* Stats Grid */}
        <motion.div
          variants={containerVariants}
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        >
          <StatCard
            icon={Zap}
            label="Daily XP"
            value={stats.dailyXP}
            unit="XP"
            color="from-primary to-green-500"
          />
          <StatCard
            icon={Trophy}
            label="Total XP"
            value={stats.totalXP}
            unit="XP"
            color="from-accent to-orange-500"
          />
          <StatCard
            icon={Flame}
            label="Current Streak"
            value={stats.streak}
            unit="days"
            color="from-red-400 to-pink-500"
          />
          <StatCard
            icon={BookOpen}
            label="Lessons Completed"
            value={stats.lessonsCompleted}
            unit=""
            color="from-blue-400 to-cyan-500"
          />
          <StatCard
            icon={Target}
            label="Cards Reviewed"
            value={stats.cardsReviewed}
            unit=""
            color="from-purple-400 to-pink-500"
          />
          <StatCard
            icon={Award}
            label="Mastered Cards"
            value={stats.masteredCards}
            unit=""
            color="from-gold to-yellow-500"
          />
        </motion.div>

        {/* Charts */}
        <motion.div variants={itemVariants} className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Weekly Activity */}
          <div className="bg-white dark:bg-neutral-800 rounded-xl p-6 shadow-md border border-neutral-200 dark:border-neutral-700">
            <h2 className="text-xl font-bold text-neutral-900 dark:text-white mb-4">
              Weekly Activity
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="date" stroke="#9ca3af" />
                <YAxis stroke="#9ca3af" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#1f2937',
                    border: 'none',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Legend />
                <Bar dataKey="xp" fill="#22c55e" name="XP Earned" />
                <Bar dataKey="cards" fill="#f59e0b" name="Cards Reviewed" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Skill Distribution */}
          <div className="bg-white dark:bg-neutral-800 rounded-xl p-6 shadow-md border border-neutral-200 dark:border-neutral-700">
            <h2 className="text-xl font-bold text-neutral-900 dark:text-white mb-4">
              Skill Levels
            </h2>
            <div className="space-y-4">
              {skillData.map((skill) => (
                <div key={skill.name}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-neutral-700 dark:text-neutral-300">
                      {skill.name}
                    </span>
                    <span className="text-sm font-bold text-neutral-900 dark:text-white">
                      {skill.value}%
                    </span>
                  </div>
                  <div className="w-full bg-neutral-200 dark:bg-neutral-700 rounded-full h-2">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${skill.value}%` }}
                      transition={{ duration: 1, delay: 0.2 }}
                      className="h-full rounded-full"
                      style={{ backgroundColor: skill.color }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Progress Chart */}
        <motion.div
          variants={itemVariants}
          className="bg-white dark:bg-neutral-800 rounded-xl p-6 shadow-md border border-neutral-200 dark:border-neutral-700"
        >
          <h2 className="text-xl font-bold text-neutral-900 dark:text-white mb-4">
            Learning Progress
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="date" stroke="#9ca3af" />
              <YAxis stroke="#9ca3af" />
              <Tooltip
                contentStyle={{
                  backgroundColor: '#1f2937',
                  border: 'none',
                  borderRadius: '8px',
                  color: '#fff',
                }}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="xp"
                stroke="#22c55e"
                name="XP Earned"
                strokeWidth={2}
                dot={{ fill: '#22c55e', r: 4 }}
              />
              <Line
                type="monotone"
                dataKey="lessons"
                stroke="#f59e0b"
                name="Lessons"
                strokeWidth={2}
                dot={{ fill: '#f59e0b', r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </motion.div>

        {/* Quick Actions */}
        <motion.div
          variants={itemVariants}
          className="grid grid-cols-1 md:grid-cols-3 gap-4"
        >
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-gradient-to-r from-primary to-green-500 text-white rounded-lg p-6 font-semibold hover:shadow-lg transition-shadow"
          >
            📚 Start Lesson
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-gradient-to-r from-accent to-orange-500 text-white rounded-lg p-6 font-semibold hover:shadow-lg transition-shadow"
          >
            🎯 Review Flashcards
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-gradient-to-r from-purple-400 to-pink-500 text-white rounded-lg p-6 font-semibold hover:shadow-lg transition-shadow"
          >
            🏆 View Leaderboard
          </motion.button>
        </motion.div>
      </motion.div>
    </Layout>
  );
};

export default Dashboard;
