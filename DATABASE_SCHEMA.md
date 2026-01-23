# 📊 Prize2Pride German Platform - Database Schema Design

**Protocol:** OMEGA 777  
**Date:** January 23, 2026

---

## 🏗️ DATABASE ARCHITECTURE

### Core Principles
1. **Normalized Design** - Eliminate redundancy
2. **Performance Optimized** - Indexed for fast queries
3. **Scalable** - Support 10,000+ concurrent users
4. **ACID Compliant** - Data integrity guaranteed
5. **Audit Trail** - Track all user actions

---

## 📋 TABLE SCHEMAS

### 1. USERS TABLE
```sql
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  username VARCHAR(100) UNIQUE NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  native_language VARCHAR(50) DEFAULT 'ar', -- Arabic
  proficiency_level VARCHAR(10) DEFAULT 'A1', -- A1, A2, B1, etc.
  avatar_url VARCHAR(500),
  bio TEXT,
  timezone VARCHAR(50) DEFAULT 'UTC',
  preferences JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_login_at TIMESTAMP,
  is_active BOOLEAN DEFAULT true,
  is_premium BOOLEAN DEFAULT false,
  INDEX idx_email (email),
  INDEX idx_username (username)
);
```

### 2. LESSONS TABLE
```sql
CREATE TABLE lessons (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  title_ar VARCHAR(255) NOT NULL,
  slug VARCHAR(255) UNIQUE NOT NULL,
  description TEXT,
  description_ar TEXT,
  level VARCHAR(10) NOT NULL, -- A1, A2, B1, etc.
  category VARCHAR(100) NOT NULL, -- Greetings, Numbers, etc.
  icon VARCHAR(10),
  content TEXT NOT NULL, -- Markdown content
  content_html TEXT, -- Pre-rendered HTML
  vocabulary JSONB NOT NULL DEFAULT '[]',
  grammar JSONB NOT NULL DEFAULT '{}',
  slang JSONB NOT NULL DEFAULT '[]',
  comedy JSONB NOT NULL DEFAULT '{}',
  audio_files JSONB DEFAULT '[]', -- URLs to audio files
  image_files JSONB DEFAULT '[]', -- URLs to images
  order_index INT,
  is_published BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_level (level),
  INDEX idx_category (category),
  INDEX idx_slug (slug)
);
```

### 3. FLASHCARDS TABLE
```sql
CREATE TABLE flashcards (
  id SERIAL PRIMARY KEY,
  lesson_id INT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  front_text VARCHAR(500) NOT NULL, -- German text
  front_text_ar VARCHAR(500), -- Arabic translation
  back_text TEXT NOT NULL, -- Definition/explanation
  back_text_ar TEXT, -- Arabic explanation
  pronunciation VARCHAR(255),
  example_sentence TEXT,
  example_sentence_ar TEXT,
  difficulty_level INT DEFAULT 1, -- 1-5
  category VARCHAR(100), -- Vocabulary, Grammar, etc.
  tags JSONB DEFAULT '[]',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_lesson_id (lesson_id),
  INDEX idx_difficulty (difficulty_level)
);
```

### 4. USER_PROGRESS TABLE (SRS Tracking)
```sql
CREATE TABLE user_progress (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  lesson_id INT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  flashcard_id INT REFERENCES flashcards(id) ON DELETE SET NULL,
  
  -- SRS Algorithm Fields
  interval INT DEFAULT 1, -- Days until next review
  ease_factor DECIMAL(3,2) DEFAULT 2.5, -- Difficulty multiplier
  repetitions INT DEFAULT 0, -- Number of times reviewed
  next_review_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  last_reviewed_at TIMESTAMP,
  
  -- Performance Metrics
  correct_count INT DEFAULT 0,
  incorrect_count INT DEFAULT 0,
  accuracy_percentage DECIMAL(5,2) DEFAULT 0,
  time_spent_seconds INT DEFAULT 0,
  
  -- Status
  status VARCHAR(50) DEFAULT 'new', -- new, learning, reviewing, mastered
  is_completed BOOLEAN DEFAULT false,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id, lesson_id),
  INDEX idx_user_id (user_id),
  INDEX idx_next_review (next_review_at),
  INDEX idx_status (status)
);
```

### 5. EXERCISES TABLE
```sql
CREATE TABLE exercises (
  id SERIAL PRIMARY KEY,
  lesson_id INT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
  exercise_type VARCHAR(50) NOT NULL, -- reading, writing, listening, speaking
  title VARCHAR(255) NOT NULL,
  title_ar VARCHAR(255),
  description TEXT,
  question TEXT NOT NULL,
  question_ar TEXT,
  exercise_format VARCHAR(50) NOT NULL, -- multiple_choice, fill_blank, true_false, essay
  
  -- Content
  content JSONB NOT NULL DEFAULT '{}', -- Format-specific data
  correct_answer TEXT,
  explanation TEXT,
  explanation_ar TEXT,
  
  difficulty_level INT DEFAULT 1, -- 1-5
  points INT DEFAULT 10,
  
  -- Media
  audio_url VARCHAR(500),
  image_url VARCHAR(500),
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_lesson_id (lesson_id),
  INDEX idx_exercise_type (exercise_type),
  INDEX idx_difficulty (difficulty_level)
);
```

### 6. USER_EXERCISE_SUBMISSIONS TABLE
```sql
CREATE TABLE user_exercise_submissions (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  exercise_id INT NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
  
  -- Submission Data
  user_answer TEXT NOT NULL,
  is_correct BOOLEAN NOT NULL,
  score INT DEFAULT 0,
  max_score INT DEFAULT 10,
  
  -- Feedback
  ai_feedback TEXT, -- AI-generated feedback from Professor Roued
  ai_feedback_ar TEXT,
  
  -- Timing
  time_spent_seconds INT DEFAULT 0,
  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_exercise_id (exercise_id),
  INDEX idx_is_correct (is_correct)
);
```

### 7. VOCABULARY_HISTORY TABLE
```sql
CREATE TABLE vocabulary_history (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  flashcard_id INT NOT NULL REFERENCES flashcards(id) ON DELETE CASCADE,
  
  -- Review Data
  review_quality INT NOT NULL, -- 0-5 (Leitner scale)
  review_time_seconds INT,
  
  -- SRS Calculation
  interval_before INT,
  interval_after INT,
  ease_factor_before DECIMAL(3,2),
  ease_factor_after DECIMAL(3,2),
  
  reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_flashcard_id (flashcard_id),
  INDEX idx_reviewed_at (reviewed_at)
);
```

### 8. ACHIEVEMENTS TABLE
```sql
CREATE TABLE achievements (
  id SERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  title_ar VARCHAR(255),
  description TEXT,
  description_ar TEXT,
  icon VARCHAR(500),
  badge_color VARCHAR(50),
  
  -- Achievement Criteria
  criteria_type VARCHAR(50) NOT NULL, -- lessons_completed, flashcards_mastered, streak, etc.
  criteria_value INT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 9. USER_ACHIEVEMENTS TABLE
```sql
CREATE TABLE user_achievements (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  achievement_id INT NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
  
  unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id, achievement_id),
  INDEX idx_user_id (user_id)
);
```

### 10. LEARNING_STREAKS TABLE
```sql
CREATE TABLE learning_streaks (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  
  current_streak INT DEFAULT 0,
  longest_streak INT DEFAULT 0,
  
  last_activity_date DATE,
  streak_started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id),
  INDEX idx_user_id (user_id)
);
```

### 11. FEEDBACK TABLE
```sql
CREATE TABLE feedback (
  id SERIAL PRIMARY KEY,
  user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  lesson_id INT REFERENCES lessons(id) ON DELETE SET NULL,
  exercise_id INT REFERENCES exercises(id) ON DELETE SET NULL,
  
  feedback_type VARCHAR(50) NOT NULL, -- bug, suggestion, content_error
  message TEXT NOT NULL,
  rating INT, -- 1-5 stars
  
  is_resolved BOOLEAN DEFAULT false,
  admin_response TEXT,
  
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_user_id (user_id),
  INDEX idx_is_resolved (is_resolved)
);
```

---

## 🔑 KEY INDEXES FOR PERFORMANCE

```sql
-- SRS Query Optimization
CREATE INDEX idx_next_review_by_user ON user_progress(user_id, next_review_at);

-- Lesson Discovery
CREATE INDEX idx_lessons_by_level_category ON lessons(level, category);

-- User Activity Tracking
CREATE INDEX idx_submissions_by_user_date ON user_exercise_submissions(user_id, submitted_at);

-- Vocabulary Search
CREATE INDEX idx_flashcards_by_lesson ON flashcards(lesson_id);
```

---

## 🔄 RELATIONSHIPS DIAGRAM

```
users (1) ──────────── (N) user_progress
         ├──────────── (N) user_exercise_submissions
         ├──────────── (N) vocabulary_history
         ├──────────── (N) user_achievements
         ├──────────── (1) learning_streaks
         └──────────── (N) feedback

lessons (1) ──────────── (N) flashcards
         ├──────────── (N) exercises
         ├──────────── (N) user_progress
         └──────────── (N) feedback

exercises (1) ──────────── (N) user_exercise_submissions
            └──────────── (N) feedback

flashcards (1) ──────────── (N) vocabulary_history
            └──────────── (N) user_progress

achievements (1) ──────────── (N) user_achievements
```

---

## 🚀 IMPLEMENTATION STRATEGY

### Step 1: Create Base Tables
- users, lessons, flashcards, exercises

### Step 2: Create Progress Tracking
- user_progress, vocabulary_history, user_exercise_submissions

### Step 3: Create Engagement Features
- achievements, user_achievements, learning_streaks

### Step 4: Create Feedback System
- feedback

### Step 5: Add Indexes
- Performance optimization indexes

### Step 6: Add Constraints
- Foreign keys, unique constraints, check constraints

---

## 📈 PERFORMANCE TARGETS

| Query Type | Target Response Time |
|------------|----------------------|
| Get user dashboard | < 100ms |
| Load lesson with exercises | < 200ms |
| Get next SRS review items | < 50ms |
| Submit exercise answer | < 100ms |
| Get user statistics | < 150ms |
| Bulk lesson ingestion | < 5s per 100 lessons |

---

## 🔐 SECURITY CONSIDERATIONS

1. **Password Hashing:** bcrypt with salt
2. **SQL Injection Prevention:** Parameterized queries
3. **Rate Limiting:** On submission endpoints
4. **Data Privacy:** GDPR compliance
5. **Audit Trail:** Track all modifications
6. **Encryption:** Sensitive data at rest and in transit

---

*Database Schema v1.0 | Protocol: OMEGA 777 | Authority: Manus AI*
