"""
Spaced Repetition System (SRS) Algorithm Implementation
Based on SM-2 (SuperMemo 2) with language learning enhancements
"""

from datetime import datetime, timedelta
from typing import Dict, Tuple
from sqlalchemy.orm import Session
from app.models import UserProgress, VocabularyHistory, Flashcard
import logging

logger = logging.getLogger(__name__)

# ============================================================================
# SRS CONSTANTS
# ============================================================================

INITIAL_INTERVAL = 1  # First review after 1 day
INITIAL_EASE_FACTOR = 2.5  # Difficulty multiplier
INITIAL_REPETITIONS = 0
MIN_EASE_FACTOR = 1.3
MAX_INTERVAL_DAYS = 365

# Quality scale (0-5)
# 0 = Complete blackout, complete failure to recall
# 1 = Incorrect response, but upon seeing the correct answer it felt familiar
# 2 = Incorrect response, but upon seeing the correct answer it seemed easy to remember
# 3 = Correct response after a hesitation
# 4 = Correct response after a moment of hesitation
# 5 = Perfect response without hesitation

# ============================================================================
# CORE SRS FUNCTIONS
# ============================================================================

class SRSCard:
    """
    Represents an SRS card with SM-2 algorithm
    """
    
    def __init__(self, interval: int = 1, ease_factor: float = 2.5, repetitions: int = 0):
        self.interval = interval
        self.ease_factor = ease_factor
        self.repetitions = repetitions
        self.next_review_at = datetime.utcnow() + timedelta(days=interval)
    
    def calculate_ease_factor(self, quality: int) -> float:
        """
        Calculate new ease factor based on user response quality
        
        Formula: EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        
        Args:
            quality: User response quality (0-5)
        
        Returns:
            new_ease_factor: Updated ease factor (minimum 1.3)
        """
        new_ease_factor = self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        return max(MIN_EASE_FACTOR, new_ease_factor)
    
    def calculate_next_interval(self, quality: int) -> int:
        """
        Calculate days until next review
        
        Args:
            quality: User response quality (0-5)
        
        Returns:
            interval: Days until next review
        """
        if quality < 3:  # Incorrect or hesitant
            return 1  # Review again tomorrow
        
        if self.repetitions == 0:
            return 1  # First review after 1 day
        elif self.repetitions == 1:
            return 3  # Second review after 3 days
        else:
            # Subsequent reviews: interval * ease_factor
            return int(self.interval * self.ease_factor)
    
    def review(self, quality: int) -> Dict:
        """
        Process a card review and update SRS parameters
        
        Args:
            quality: User response quality (0-5)
        
        Returns:
            Updated card state
        """
        if quality < 3:
            # Incorrect response - reset repetitions
            self.repetitions = 0
            self.interval = 1
        else:
            # Correct response
            self.interval = self.calculate_next_interval(quality)
            self.repetitions += 1
        
        # Update ease factor
        self.ease_factor = self.calculate_ease_factor(quality)
        
        # Schedule next review
        self.next_review_at = datetime.utcnow() + timedelta(days=self.interval)
        
        return {
            'interval': self.interval,
            'ease_factor': self.ease_factor,
            'repetitions': self.repetitions,
            'next_review_at': self.next_review_at
        }

# ============================================================================
# DATABASE OPERATIONS
# ============================================================================

def get_user_progress(
    db: Session,
    user_id: int,
    flashcard_id: int
) -> UserProgress:
    """
    Get or create user progress record for a flashcard
    """
    progress = db.query(UserProgress).filter(
        UserProgress.user_id == user_id,
        UserProgress.flashcard_id == flashcard_id
    ).first()
    
    if not progress:
        # Create new progress record
        flashcard = db.query(Flashcard).get(flashcard_id)
        progress = UserProgress(
            user_id=user_id,
            lesson_id=flashcard.lesson_id,
            flashcard_id=flashcard_id,
            interval=INITIAL_INTERVAL,
            ease_factor=INITIAL_EASE_FACTOR,
            repetitions=INITIAL_REPETITIONS,
            status='new'
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
    
    return progress

def submit_flashcard_review(
    db: Session,
    user_id: int,
    flashcard_id: int,
    quality: int,
    time_spent_seconds: int = 0
) -> Dict:
    """
    Submit a flashcard review and update SRS parameters
    
    Args:
        db: Database session
        user_id: User ID
        flashcard_id: Flashcard ID
        quality: Review quality (0-5)
        time_spent_seconds: Time spent on review
    
    Returns:
        Updated progress information
    """
    try:
        # Get or create progress
        progress = get_user_progress(db, user_id, flashcard_id)
        
        # Create SRS card from current progress
        card = SRSCard(
            interval=progress.interval,
            ease_factor=float(progress.ease_factor),
            repetitions=progress.repetitions
        )
        
        # Save old values for history
        interval_before = progress.interval
        ease_factor_before = float(progress.ease_factor)
        
        # Review the card
        result = card.review(quality)
        
        # Update progress
        progress.interval = result['interval']
        progress.ease_factor = result['ease_factor']
        progress.repetitions = result['repetitions']
        progress.next_review_at = result['next_review_at']
        progress.last_reviewed_at = datetime.utcnow()
        progress.time_spent_seconds += time_spent_seconds
        
        # Update accuracy
        if quality >= 3:
            progress.correct_count += 1
        else:
            progress.incorrect_count += 1
        
        total_reviews = progress.correct_count + progress.incorrect_count
        progress.accuracy_percentage = (progress.correct_count / total_reviews * 100) if total_reviews > 0 else 0
        
        # Update status
        if progress.repetitions >= 5 and progress.ease_factor >= 2.5 and progress.accuracy_percentage >= 90:
            progress.status = 'mastered'
        elif progress.repetitions >= 2:
            progress.status = 'learning'
        else:
            progress.status = 'new'
        
        # Save progress
        db.commit()
        
        # Save to vocabulary history
        history = VocabularyHistory(
            user_id=user_id,
            flashcard_id=flashcard_id,
            review_quality=quality,
            review_time_seconds=time_spent_seconds,
            interval_before=interval_before,
            interval_after=result['interval'],
            ease_factor_before=ease_factor_before,
            ease_factor_after=result['ease_factor']
        )
        db.add(history)
        db.commit()
        
        logger.info(f"✅ Flashcard {flashcard_id} reviewed for user {user_id}")
        
        return {
            'status': 'success',
            'flashcard_id': flashcard_id,
            'quality': quality,
            'interval': result['interval'],
            'ease_factor': result['ease_factor'],
            'repetitions': result['repetitions'],
            'next_review_at': result['next_review_at'].isoformat(),
            'accuracy_percentage': float(progress.accuracy_percentage),
            'status': progress.status
        }
    
    except Exception as e:
        logger.error(f"Error submitting flashcard review: {str(e)}")
        db.rollback()
        return {
            'status': 'error',
            'error': str(e)
        }

# ============================================================================
# REVIEW QUEUE MANAGEMENT
# ============================================================================

def get_next_review_items(
    db: Session,
    user_id: int,
    limit: int = 20
) -> list:
    """
    Get cards due for review, prioritized by:
    1. Overdue cards (highest priority)
    2. New cards
    3. Cards with low ease factor (need reinforcement)
    """
    try:
        now = datetime.utcnow()
        
        # Query for due cards
        due_cards = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.next_review_at <= now
        ).order_by(
            # Prioritize overdue cards
            (UserProgress.next_review_at < now - timedelta(days=1)).desc(),
            # Then new cards
            UserProgress.repetitions.asc(),
            # Then low ease factor
            UserProgress.ease_factor.asc(),
            # Then oldest reviews
            UserProgress.next_review_at.asc()
        ).limit(limit).all()
        
        return due_cards
    
    except Exception as e:
        logger.error(f"Error getting next review items: {str(e)}")
        return []

def get_daily_recommendation(db: Session, user_id: int) -> Dict:
    """
    Calculate recommended daily review load
    """
    try:
        now = datetime.utcnow()
        
        # Get statistics
        total_cards = db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).count()
        
        due_cards = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.next_review_at <= now
        ).count()
        
        avg_ease = db.query(UserProgress).filter(
            UserProgress.user_id == user_id
        ).with_entities(
            db.func.avg(UserProgress.ease_factor)
        ).scalar() or 2.5
        
        # Recommend 20-30 reviews per day for optimal learning
        recommended_daily = 25
        estimated_time_minutes = due_cards * 0.5  # ~30 seconds per card
        
        return {
            'total_cards': total_cards,
            'due_cards': due_cards,
            'recommended_daily': recommended_daily,
            'estimated_time_minutes': estimated_time_minutes,
            'average_ease_factor': float(avg_ease)
        }
    
    except Exception as e:
        logger.error(f"Error calculating daily recommendation: {str(e)}")
        return {}

# ============================================================================
# STATISTICS CALCULATION
# ============================================================================

def calculate_user_statistics(db: Session, user_id: int) -> Dict:
    """
    Calculate comprehensive learning statistics
    """
    try:
        # Get progress statistics
        progress_stats = db.query(
            db.func.count(UserProgress.id).label('total_cards'),
            db.func.sum(db.case(
                (UserProgress.status == 'mastered', 1),
                else_=0
            )).label('mastered_cards'),
            db.func.sum(db.case(
                (UserProgress.status == 'learning', 1),
                else_=0
            )).label('learning_cards'),
            db.func.sum(db.case(
                (UserProgress.status == 'new', 1),
                else_=0
            )).label('new_cards'),
            db.func.avg(UserProgress.accuracy_percentage).label('avg_accuracy'),
            db.func.avg(UserProgress.ease_factor).label('avg_ease_factor'),
            db.func.sum(UserProgress.time_spent_seconds).label('total_time_seconds')
        ).filter(
            UserProgress.user_id == user_id
        ).first()
        
        total_cards = progress_stats.total_cards or 0
        mastered_cards = progress_stats.mastered_cards or 0
        
        return {
            'total_cards': total_cards,
            'mastered_cards': mastered_cards,
            'mastery_percentage': (mastered_cards / total_cards * 100) if total_cards > 0 else 0,
            'learning_cards': progress_stats.learning_cards or 0,
            'new_cards': progress_stats.new_cards or 0,
            'average_accuracy': float(progress_stats.avg_accuracy or 0),
            'average_ease_factor': float(progress_stats.avg_ease_factor or 2.5),
            'total_study_time_hours': (progress_stats.total_time_seconds or 0) / 3600
        }
    
    except Exception as e:
        logger.error(f"Error calculating user statistics: {str(e)}")
        return {}

def calculate_lesson_statistics(db: Session, user_id: int, lesson_id: int) -> Dict:
    """
    Calculate statistics for a specific lesson
    """
    try:
        stats = db.query(
            db.func.count(UserProgress.id).label('total_cards'),
            db.func.sum(db.case(
                (UserProgress.status == 'mastered', 1),
                else_=0
            )).label('mastered_cards'),
            db.func.avg(UserProgress.accuracy_percentage).label('avg_accuracy'),
            db.func.sum(UserProgress.time_spent_seconds).label('total_time_seconds')
        ).filter(
            UserProgress.user_id == user_id,
            UserProgress.lesson_id == lesson_id
        ).first()
        
        total_cards = stats.total_cards or 0
        mastered_cards = stats.mastered_cards or 0
        
        return {
            'lesson_id': lesson_id,
            'total_cards': total_cards,
            'mastered_cards': mastered_cards,
            'mastery_percentage': (mastered_cards / total_cards * 100) if total_cards > 0 else 0,
            'average_accuracy': float(stats.avg_accuracy or 0),
            'total_study_time_minutes': (stats.total_time_seconds or 0) / 60
        }
    
    except Exception as e:
        logger.error(f"Error calculating lesson statistics: {str(e)}")
        return {}

# ============================================================================
# MASTERY CHECKING
# ============================================================================

def check_mastery(progress: UserProgress) -> bool:
    """
    Check if card meets mastery criteria
    """
    return (
        progress.repetitions >= 5 and
        progress.ease_factor >= 2.5 and
        progress.accuracy_percentage >= 90 and
        progress.status == 'mastered'
    )

def get_mastered_cards(db: Session, user_id: int) -> int:
    """
    Get count of mastered cards for user
    """
    try:
        count = db.query(UserProgress).filter(
            UserProgress.user_id == user_id,
            UserProgress.status == 'mastered'
        ).count()
        return count
    except Exception as e:
        logger.error(f"Error getting mastered cards: {str(e)}")
        return 0

# ============================================================================
# ADAPTIVE INTERVALS
# ============================================================================

def calculate_adaptive_interval(
    base_interval: int,
    ease_factor: float,
    user_accuracy: float,
    card_difficulty: int
) -> int:
    """
    Calculate adaptive interval based on multiple factors
    
    Args:
        base_interval: Base interval from SM-2
        ease_factor: Ease factor from SM-2
        user_accuracy: User's overall accuracy (0-1)
        card_difficulty: Card difficulty (1-5)
    
    Returns:
        Adjusted interval in days
    """
    # Apply difficulty adjustment
    difficulty_factor = 1.0 + (card_difficulty - 3) * 0.1
    
    # Apply accuracy adjustment
    accuracy_factor = 1.0 + (user_accuracy - 0.7) * 0.5
    
    # Calculate final interval
    adjusted_interval = int(base_interval * ease_factor * difficulty_factor * accuracy_factor)
    
    # Bounds checking
    return max(1, min(adjusted_interval, MAX_INTERVAL_DAYS))
