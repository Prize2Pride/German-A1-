'use client';

import React, { useState } from 'react';
import { motion } from 'framer-motion';
import Link from 'next/link';
import { Menu, X, Home, BookOpen, Zap, Trophy, User, LogOut, Settings } from 'lucide-react';
import { ProfessorRoued, ProfessorRouedMessages } from './ProfessorRoued';

interface LayoutProps {
  children: React.ReactNode;
  showProfessor?: boolean;
}

export const Layout: React.FC<LayoutProps> = ({ children, showProfessor = true }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [professorVisible, setProfessorVisible] = useState(showProfessor);

  const navigationItems = [
    { icon: Home, label: 'Dashboard', href: '/dashboard' },
    { icon: BookOpen, label: 'Lessons', href: '/lessons' },
    { icon: Zap, label: 'Flashcards', href: '/flashcards' },
    { icon: Trophy, label: 'Leaderboard', href: '/leaderboard' },
    { icon: User, label: 'Profile', href: '/profile' },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-white to-neutral-50 dark:from-neutral-900 dark:to-neutral-800">
      {/* Header */}
      <motion.header
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        className="sticky top-0 z-40 bg-white/80 dark:bg-neutral-900/80 backdrop-blur-md border-b border-neutral-200 dark:border-neutral-700"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <Link href="/" className="flex items-center gap-2 group">
              <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center text-white font-bold text-lg group-hover:shadow-lg transition-shadow">
                P2P
              </div>
              <span className="font-bold text-lg hidden sm:inline text-neutral-900 dark:text-white">
                Prize2Pride
              </span>
            </Link>

            {/* Desktop Navigation */}
            <nav className="hidden md:flex items-center gap-1">
              {navigationItems.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg text-neutral-600 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
                >
                  <item.icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{item.label}</span>
                </Link>
              ))}
            </nav>

            {/* Right Actions */}
            <div className="flex items-center gap-4">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setProfessorVisible(!professorVisible)}
                className="hidden sm:flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white hover:bg-primary-dark transition-colors text-sm font-medium"
              >
                🎓 Professor Roued
              </motion.button>

              {/* Mobile Menu Button */}
              <button
                onClick={() => setSidebarOpen(!sidebarOpen)}
                className="md:hidden p-2 rounded-lg hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
              >
                {sidebarOpen ? (
                  <X className="w-6 h-6" />
                ) : (
                  <Menu className="w-6 h-6" />
                )}
              </button>
            </div>
          </div>
        </div>
      </motion.header>

      {/* Mobile Sidebar */}
      {sidebarOpen && (
        <motion.div
          initial={{ opacity: 0, x: -300 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -300 }}
          className="fixed inset-0 z-30 md:hidden bg-black/50"
          onClick={() => setSidebarOpen(false)}
        >
          <motion.nav
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            className="absolute left-0 top-0 h-full w-64 bg-white dark:bg-neutral-900 shadow-lg p-6 space-y-4"
            onClick={(e) => e.stopPropagation()}
          >
            {navigationItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setSidebarOpen(false)}
                className="flex items-center gap-3 px-4 py-3 rounded-lg text-neutral-700 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors"
              >
                <item.icon className="w-5 h-5" />
                <span className="font-medium">{item.label}</span>
              </Link>
            ))}
          </motion.nav>
        </motion.div>
      )}

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          {children}
        </motion.div>
      </main>

      {/* Footer */}
      <motion.footer
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        className="mt-16 border-t border-neutral-200 dark:border-neutral-700 bg-neutral-50 dark:bg-neutral-900"
      >
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
            <div>
              <h3 className="font-bold text-neutral-900 dark:text-white mb-4">Prize2Pride</h3>
              <p className="text-sm text-neutral-600 dark:text-neutral-400">
                Learn German with Professor Roued. Lerne Deutsch, bevor das Bier warm wird!
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-neutral-900 dark:text-white mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li><Link href="/lessons" className="hover:text-primary transition-colors">Lessons</Link></li>
                <li><Link href="/flashcards" className="hover:text-primary transition-colors">Flashcards</Link></li>
                <li><Link href="/exercises" className="hover:text-primary transition-colors">Exercises</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-neutral-900 dark:text-white mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li><Link href="/about" className="hover:text-primary transition-colors">About</Link></li>
                <li><Link href="/contact" className="hover:text-primary transition-colors">Contact</Link></li>
                <li><Link href="/blog" className="hover:text-primary transition-colors">Blog</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold text-neutral-900 dark:text-white mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-neutral-600 dark:text-neutral-400">
                <li><Link href="/privacy" className="hover:text-primary transition-colors">Privacy</Link></li>
                <li><Link href="/terms" className="hover:text-primary transition-colors">Terms</Link></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-neutral-200 dark:border-neutral-700 pt-8">
            <p className="text-center text-sm text-neutral-600 dark:text-neutral-400">
              © 2026 Prize2Pride German Platform. All rights reserved. | Protocol: OMEGA 777
            </p>
          </div>
        </div>
      </motion.footer>

      {/* Professor Roued Assistant */}
      {professorVisible && (
        <ProfessorRoued
          message={ProfessorRouedMessages.welcome.text}
          mood={ProfessorRouedMessages.welcome.mood}
          onClose={() => setProfessorVisible(false)}
        />
      )}
    </div>
  );
};

export default Layout;
