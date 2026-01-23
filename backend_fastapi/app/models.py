"""
SQLAlchemy models for Prize2Pride German Platform
"""

from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Numeric, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

# ============================================================================
# USERS TABLE
# ============================================================================

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    username = Column(String(100), unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    native_language = Column(String(50), default="ar")
    proficiency_level = Column(String(10), default="A1")
    avatar_url = Column(String(500))
    bio = Column(Text)
    timezone = Column(String(50), default="UTC")
    preferences = Column(JSON, default={})
    is_active = Column(Boolean, default=True)
    is_premium = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login_at = Column(DateTime)
    
    # Relationships
    progress = relationship("UserProgress", back_populates="user")
    submissions = relationship("UserExerciseSubmission", back_populates="user")
    vocabulary_history = relationship("VocabularyHistory", back_populates="user")
    achievements = relationship("UserAchievement", back_populates="user")
    feedback = relationship("Feedback", back_populates="user")

# ============================================================================
# LESSONS TABLE
# ============================================================================

class Lesson(Base):
    __tablename__ = "lessons"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_ar = Column(String(255), nullable=False)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text)
    description_ar = Column(Text)
    level = Column(String(10), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)
    icon = Column(String(10))
    content = Column(Text, nullable=False)
    content_html = Column(Text)
    vocabulary = Column(JSON, default=[])
    grammar = Column(JSON, default={})
    slang = Column(JSON, default=[])
    comedy = Column(JSON, default={})
    audio_files = Column(JSON, default=[])
    image_files = Column(JSON, default=[])
    order_index = Column(Integer)
    is_published = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    flashcards = relationship("Flashcard", back_populates="lesson")
    exercises = relationship("Exercise", back_populates="lesson")
    progress = relationship("UserProgress", back_populates="lesson")
    feedback = relationship("Feedback", back_populates="lesson")

# ============================================================================
# FLASHCARDS TABLE
# ============================================================================

class Flashcard(Base):
    __tablename__ = "flashcards"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    front_text = Column(String(500), nullable=False)
    front_text_ar = Column(String(500))
    back_text = Column(Text, nullable=False)
    back_text_ar = Column(Text)
    pronunciation = Column(String(255))
    example_sentence = Column(Text)
    example_sentence_ar = Column(Text)
    difficulty_level = Column(Integer, default=1)
    category = Column(String(100))
    tags = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lesson = relationship("Lesson", back_populates="flashcards")
    vocabulary_history = relationship("VocabularyHistory", back_populates="flashcard")
    progress = relationship("UserProgress", back_populates="flashcard")

# ============================================================================
# USER PROGRESS TABLE (SRS TRACKING)
# ============================================================================

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id"))
    
    # SRS Algorithm Fields
    interval = Column(Integer, default=1)
    ease_factor = Column(Numeric(3, 2), default=2.5)
    repetitions = Column(Integer, default=0)
    next_review_at = Column(DateTime, default=datetime.utcnow, index=True)
    last_reviewed_at = Column(DateTime)
    
    # Performance Metrics
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    accuracy_percentage = Column(Numeric(5, 2), default=0)
    time_spent_seconds = Column(Integer, default=0)
    
    # Status
    status = Column(String(50), default="new", index=True)
    is_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress")
    lesson = relationship("Lesson", back_populates="progress")
    flashcard = relationship("Flashcard", back_populates="progress")

# ============================================================================
# EXERCISES TABLE
# ============================================================================

class Exercise(Base):
    __tablename__ = "exercises"
    
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    exercise_type = Column(String(50), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    title_ar = Column(String(255))
    description = Column(Text)
    question = Column(Text, nullable=False)
    question_ar = Column(Text)
    exercise_format = Column(String(50), nullable=False)
    content = Column(JSON, default={})
    correct_answer = Column(Text)
    explanation = Column(Text)
    explanation_ar = Column(Text)
    difficulty_level = Column(Integer, default=1, index=True)
    points = Column(Integer, default=10)
    audio_url = Column(String(500))
    image_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    lesson = relationship("Lesson", back_populates="exercises")
    submissions = relationship("UserExerciseSubmission", back_populates="exercise")
    feedback = relationship("Feedback", back_populates="exercise")

# ============================================================================
# USER EXERCISE SUBMISSIONS TABLE
# ============================================================================

class UserExerciseSubmission(Base):
    __tablename__ = "user_exercise_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    
    # Submission Data
    user_answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False, index=True)
    score = Column(Integer, default=0)
    max_score = Column(Integer, default=10)
    
    # Feedback
    ai_feedback = Column(Text)
    ai_feedback_ar = Column(Text)
    
    # Timing
    time_spent_seconds = Column(Integer, default=0)
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="submissions")
    exercise = relationship("Exercise", back_populates="submissions")

# ============================================================================
# VOCABULARY HISTORY TABLE
# ============================================================================

class VocabularyHistory(Base):
    __tablename__ = "vocabulary_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    flashcard_id = Column(Integer, ForeignKey("flashcards.id"), nullable=False, index=True)
    
    # Review Data
    review_quality = Column(Integer, nullable=False)
    review_time_seconds = Column(Integer)
    
    # SRS Calculation
    interval_before = Column(Integer)
    interval_after = Column(Integer)
    ease_factor_before = Column(Numeric(3, 2))
    ease_factor_after = Column(Numeric(3, 2))
    
    reviewed_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="vocabulary_history")
    flashcard = relationship("Flashcard", back_populates="vocabulary_history")

# ============================================================================
# ACHIEVEMENTS TABLE
# ============================================================================

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    title_ar = Column(String(255))
    description = Column(Text)
    description_ar = Column(Text)
    icon = Column(String(500))
    badge_color = Column(String(50))
    criteria_type = Column(String(50), nullable=False)
    criteria_value = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    users = relationship("UserAchievement", back_populates="achievement")

# ============================================================================
# USER ACHIEVEMENTS TABLE
# ============================================================================

class UserAchievement(Base):
    __tablename__ = "user_achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), nullable=False, index=True)
    unlocked_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="users")

# ============================================================================
# LEARNING STREAKS TABLE
# ============================================================================

class LearningStreak(Base):
    __tablename__ = "learning_streaks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(String(10))
    streak_started_at = Column(DateTime, default=datetime.utcnow)

# ============================================================================
# FEEDBACK TABLE
# ============================================================================

class Feedback(Base):
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    exercise_id = Column(Integer, ForeignKey("exercises.id"))
    feedback_type = Column(String(50), nullable=False)
    message = Column(Text, nullable=False)
    rating = Column(Integer)
    is_resolved = Column(Boolean, default=False, index=True)
    admin_response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="feedback")
    lesson = relationship("Lesson", back_populates="feedback")
    exercise = relationship("Exercise", back_populates="feedback")
