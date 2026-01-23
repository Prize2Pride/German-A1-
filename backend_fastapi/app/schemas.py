"""
Pydantic schemas for API request/response validation
"""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# ============================================================================
# USER SCHEMAS
# ============================================================================

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    native_language: str = "ar"
    proficiency_level: str = "A1"

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None
    timezone: Optional[str] = None
    proficiency_level: Optional[str] = None

class UserResponse(UserBase):
    id: int
    avatar_url: Optional[str]
    is_active: bool
    is_premium: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# LESSON SCHEMAS
# ============================================================================

class LessonBase(BaseModel):
    title: str
    title_ar: str
    slug: str
    level: str
    category: str
    icon: Optional[str] = None

class LessonCreate(LessonBase):
    description: Optional[str] = None
    description_ar: Optional[str] = None
    content: str
    vocabulary: List[Dict[str, Any]] = []
    grammar: Dict[str, Any] = {}

class LessonResponse(LessonBase):
    id: int
    description: Optional[str]
    description_ar: Optional[str]
    vocabulary: List[Dict[str, Any]]
    grammar: Dict[str, Any]
    is_published: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# FLASHCARD SCHEMAS
# ============================================================================

class FlashcardBase(BaseModel):
    front_text: str
    front_text_ar: Optional[str] = None
    back_text: str
    back_text_ar: Optional[str] = None
    pronunciation: Optional[str] = None

class FlashcardCreate(FlashcardBase):
    lesson_id: int
    example_sentence: Optional[str] = None
    example_sentence_ar: Optional[str] = None
    difficulty_level: int = 1

class FlashcardResponse(FlashcardBase):
    id: int
    lesson_id: int
    difficulty_level: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# USER PROGRESS SCHEMAS
# ============================================================================

class UserProgressBase(BaseModel):
    user_id: int
    lesson_id: int
    flashcard_id: Optional[int] = None

class UserProgressResponse(UserProgressBase):
    id: int
    interval: int
    ease_factor: float
    repetitions: int
    next_review_at: datetime
    accuracy_percentage: float
    status: str
    
    class Config:
        from_attributes = True

# ============================================================================
# EXERCISE SCHEMAS
# ============================================================================

class ExerciseBase(BaseModel):
    lesson_id: int
    exercise_type: str  # reading, writing, listening, speaking
    title: str
    title_ar: Optional[str] = None
    question: str
    question_ar: Optional[str] = None
    exercise_format: str  # true_false, fill_blank, multiple_choice, essay

class ExerciseCreate(ExerciseBase):
    description: Optional[str] = None
    content: Dict[str, Any] = {}
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    explanation_ar: Optional[str] = None
    difficulty_level: int = 1
    points: int = 10

class ExerciseResponse(ExerciseBase):
    id: int
    difficulty_level: int
    points: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# EXERCISE SUBMISSION SCHEMAS
# ============================================================================

class ExerciseSubmissionCreate(BaseModel):
    exercise_id: int
    user_answer: str
    time_spent_seconds: int = 0

class ExerciseSubmissionResponse(BaseModel):
    id: int
    exercise_id: int
    user_answer: str
    is_correct: bool
    score: int
    ai_feedback: Optional[str] = None
    ai_feedback_ar: Optional[str] = None
    submitted_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# FLASHCARD REVIEW SCHEMAS
# ============================================================================

class FlashcardReviewCreate(BaseModel):
    flashcard_id: int
    quality: int = Field(..., ge=0, le=5)  # 0-5 quality scale
    time_spent_seconds: int = 0

class FlashcardReviewResponse(BaseModel):
    id: int
    flashcard_id: int
    interval: int
    ease_factor: float
    repetitions: int
    next_review_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# STATISTICS SCHEMAS
# ============================================================================

class UserStatistics(BaseModel):
    total_lessons: int
    completed_lessons: int
    total_flashcards: int
    mastered_flashcards: int
    average_accuracy: float
    total_study_time_hours: float
    current_streak: int
    longest_streak: int

class LessonStatistics(BaseModel):
    lesson_id: int
    title: str
    completion_rate: float
    average_accuracy: float
    total_attempts: int
    average_time_minutes: float

# ============================================================================
# AUTHENTICATION SCHEMAS
# ============================================================================

class TokenData(BaseModel):
    user_id: int
    email: str
    username: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class LoginRequest(BaseModel):
    email: str
    password: str

# ============================================================================
# FEEDBACK SCHEMAS
# ============================================================================

class FeedbackCreate(BaseModel):
    feedback_type: str  # bug, suggestion, content_error
    message: str
    lesson_id: Optional[int] = None
    exercise_id: Optional[int] = None
    rating: Optional[int] = Field(None, ge=1, le=5)

class FeedbackResponse(FeedbackCreate):
    id: int
    user_id: int
    is_resolved: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
# BATCH INGESTION SCHEMAS
# ============================================================================

class IngestionRequest(BaseModel):
    lessons_directory: str

class IngestionResponse(BaseModel):
    status: str
    total_files: int
    successful: int
    failed: int
    total_flashcards: int
    total_exercises: int
    errors: List[Dict[str, str]] = []
