"""
API Routes for Prize2Pride German Platform
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Lesson, Flashcard, Exercise, UserProgress
from app import schemas
from app.srs_algorithm import (
    submit_flashcard_review,
    get_next_review_items,
    get_daily_recommendation,
    calculate_user_statistics,
    calculate_lesson_statistics
)
import logging

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["api"])

# ============================================================================
# LESSON ENDPOINTS
# ============================================================================

@router.get("/lessons", response_model=List[schemas.LessonResponse])
async def get_lessons(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    level: str = Query(None),
    category: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get list of lessons with optional filtering
    """
    try:
        query = db.query(Lesson).filter(Lesson.is_published == True)
        
        if level:
            query = query.filter(Lesson.level == level)
        
        if category:
            query = query.filter(Lesson.category == category)
        
        lessons = query.offset(skip).limit(limit).all()
        return lessons
    
    except Exception as e:
        logger.error(f"Error fetching lessons: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching lessons")

@router.get("/lessons/{lesson_id}", response_model=schemas.LessonResponse)
async def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    """
    Get specific lesson by ID
    """
    try:
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
        
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")
        
        return lesson
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching lesson {lesson_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching lesson")

@router.get("/lessons/{lesson_id}/flashcards", response_model=List[schemas.FlashcardResponse])
async def get_lesson_flashcards(
    lesson_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all flashcards for a lesson
    """
    try:
        flashcards = db.query(Flashcard).filter(
            Flashcard.lesson_id == lesson_id
        ).offset(skip).limit(limit).all()
        
        return flashcards
    
    except Exception as e:
        logger.error(f"Error fetching flashcards for lesson {lesson_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching flashcards")

# ============================================================================
# FLASHCARD ENDPOINTS
# ============================================================================

@router.get("/flashcards", response_model=List[schemas.FlashcardResponse])
async def get_flashcards(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get list of flashcards
    """
    try:
        flashcards = db.query(Flashcard).offset(skip).limit(limit).all()
        return flashcards
    
    except Exception as e:
        logger.error(f"Error fetching flashcards: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching flashcards")

@router.get("/flashcards/{flashcard_id}", response_model=schemas.FlashcardResponse)
async def get_flashcard(flashcard_id: int, db: Session = Depends(get_db)):
    """
    Get specific flashcard by ID
    """
    try:
        flashcard = db.query(Flashcard).filter(Flashcard.id == flashcard_id).first()
        
        if not flashcard:
            raise HTTPException(status_code=404, detail="Flashcard not found")
        
        return flashcard
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching flashcard {flashcard_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching flashcard")

# ============================================================================
# SRS REVIEW ENDPOINTS
# ============================================================================

@router.get("/user/{user_id}/review-queue", response_model=List[schemas.UserProgressResponse])
async def get_review_queue(
    user_id: int,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get flashcards due for review for a user
    """
    try:
        due_cards = get_next_review_items(db, user_id, limit)
        return due_cards
    
    except Exception as e:
        logger.error(f"Error fetching review queue for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching review queue")

@router.post("/user/{user_id}/flashcard-review")
async def submit_review(
    user_id: int,
    review: schemas.FlashcardReviewCreate,
    db: Session = Depends(get_db)
):
    """
    Submit a flashcard review
    """
    try:
        result = submit_flashcard_review(
            db,
            user_id,
            review.flashcard_id,
            review.quality,
            review.time_spent_seconds
        )
        
        if result['status'] == 'error':
            raise HTTPException(status_code=400, detail=result['error'])
        
        return result
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting review: {str(e)}")
        raise HTTPException(status_code=500, detail="Error submitting review")

@router.get("/user/{user_id}/daily-recommendation")
async def get_recommendation(user_id: int, db: Session = Depends(get_db)):
    """
    Get daily review recommendation for user
    """
    try:
        recommendation = get_daily_recommendation(db, user_id)
        return recommendation
    
    except Exception as e:
        logger.error(f"Error getting recommendation for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error getting recommendation")

# ============================================================================
# STATISTICS ENDPOINTS
# ============================================================================

@router.get("/user/{user_id}/statistics")
async def get_user_stats(user_id: int, db: Session = Depends(get_db)):
    """
    Get comprehensive statistics for a user
    """
    try:
        stats = calculate_user_statistics(db, user_id)
        return stats
    
    except Exception as e:
        logger.error(f"Error calculating statistics for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating statistics")

@router.get("/user/{user_id}/lesson/{lesson_id}/statistics")
async def get_lesson_stats(
    user_id: int,
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """
    Get statistics for a specific lesson
    """
    try:
        stats = calculate_lesson_statistics(db, user_id, lesson_id)
        return stats
    
    except Exception as e:
        logger.error(f"Error calculating statistics: {str(e)}")
        raise HTTPException(status_code=500, detail="Error calculating statistics")

# ============================================================================
# EXERCISE ENDPOINTS
# ============================================================================

@router.get("/exercises", response_model=List[schemas.ExerciseResponse])
async def get_exercises(
    exercise_type: str = Query(None),
    lesson_id: int = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get exercises with optional filtering
    """
    try:
        query = db.query(Exercise)
        
        if exercise_type:
            query = query.filter(Exercise.exercise_type == exercise_type)
        
        if lesson_id:
            query = query.filter(Exercise.lesson_id == lesson_id)
        
        exercises = query.offset(skip).limit(limit).all()
        return exercises
    
    except Exception as e:
        logger.error(f"Error fetching exercises: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching exercises")

@router.get("/exercises/{exercise_id}", response_model=schemas.ExerciseResponse)
async def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    """
    Get specific exercise by ID
    """
    try:
        exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
        
        if not exercise:
            raise HTTPException(status_code=404, detail="Exercise not found")
        
        return exercise
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching exercise {exercise_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching exercise")

# ============================================================================
# USER PROGRESS ENDPOINTS
# ============================================================================

@router.get("/user/{user_id}/progress", response_model=List[schemas.UserProgressResponse])
async def get_user_progress(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get user progress on lessons
    """
    try:
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).offset(skip).limit(limit).all()
        
        return progress
    
    except Exception as e:
        logger.error(f"Error fetching progress for user {user_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching progress")

@router.get("/user/{user_id}/progress/{lesson_id}", response_model=schemas.UserProgressResponse)
async def get_lesson_progress(
    user_id: int,
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user progress on a specific lesson
    """
    try:
        progress = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id == lesson_id
        ).first()
        
        if not progress:
            raise HTTPException(status_code=404, detail="Progress not found")
        
        return progress
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching progress")

# ============================================================================
# HEALTH AND STATUS ENDPOINTS
# ============================================================================

@router.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint with database verification
    """
    try:
        # Test database connection
        db.execute("SELECT 1")
        
        # Get some statistics
        lesson_count = db.query(Lesson).count()
        flashcard_count = db.query(Flashcard).count()
        exercise_count = db.query(Exercise).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "statistics": {
                "lessons": lesson_count,
                "flashcards": flashcard_count,
                "exercises": exercise_count
            }
        }
    
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")

# Include router in main app
def include_routes(app):
    """
    Include routes in FastAPI app
    """
    app.include_router(router)
