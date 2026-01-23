# 🧠 Prize2Pride SRS Algorithm - Spaced Repetition System

**Protocol:** OMEGA 777  
**Version:** 1.0  
**Algorithm:** SM-2 (SuperMemo 2) Enhanced

---

## 📚 OVERVIEW

The Spaced Repetition System (SRS) is the core engine that optimizes vocabulary retention through scientifically-proven spacing intervals. This implementation uses the SM-2 algorithm with enhancements for language learning.

---

## 🎯 CORE ALGORITHM: SM-2 ENHANCED

### Algorithm Parameters

```python
# Initial values
INITIAL_INTERVAL = 1  # First review after 1 day
INITIAL_EASE_FACTOR = 2.5  # Difficulty multiplier
INITIAL_REPETITIONS = 0

# Quality scale (0-5)
# 0 = Complete blackout, complete failure to recall
# 1 = Incorrect response, but upon seeing the correct answer it felt familiar
# 2 = Incorrect response, but upon seeing the correct answer it seemed easy to remember
# 3 = Correct response after a hesitation
# 4 = Correct response after a moment of hesitation
# 5 = Perfect response without hesitation
```

### Ease Factor Calculation

```python
def calculate_ease_factor(old_ease_factor, quality):
    """
    Calculate new ease factor based on user response quality
    
    Args:
        old_ease_factor: Previous ease factor (default 2.5)
        quality: User response quality (0-5)
    
    Returns:
        new_ease_factor: Updated ease factor (minimum 1.3)
    """
    new_ease_factor = old_ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    return max(1.3, new_ease_factor)
```

### Interval Calculation

```python
def calculate_next_interval(repetitions, ease_factor, quality):
    """
    Calculate days until next review
    
    Args:
        repetitions: Number of times card has been reviewed
        ease_factor: Current ease factor
        quality: User response quality (0-5)
    
    Returns:
        interval: Days until next review
    """
    if quality < 3:  # Incorrect or hesitant
        return 1  # Review again tomorrow
    
    if repetitions == 0:
        return 1  # First review after 1 day
    elif repetitions == 1:
        return 3  # Second review after 3 days
    else:
        # Subsequent reviews: interval * ease_factor
        return int(previous_interval * ease_factor)
```

### Complete SM-2 Implementation

```python
class SRSCard:
    def __init__(self):
        self.interval = 1
        self.ease_factor = 2.5
        self.repetitions = 0
        self.next_review_at = datetime.now() + timedelta(days=1)
    
    def review(self, quality: int) -> dict:
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
            if self.repetitions == 0:
                self.interval = 1
            elif self.repetitions == 1:
                self.interval = 3
            else:
                self.interval = int(self.interval * self.ease_factor)
            
            self.repetitions += 1
        
        # Update ease factor
        self.ease_factor = self.calculate_ease_factor(quality)
        self.ease_factor = max(1.3, self.ease_factor)  # Minimum ease factor
        
        # Schedule next review
        self.next_review_at = datetime.now() + timedelta(days=self.interval)
        
        return {
            'interval': self.interval,
            'ease_factor': self.ease_factor,
            'repetitions': self.repetitions,
            'next_review_at': self.next_review_at
        }
    
    def calculate_ease_factor(self, quality: int) -> float:
        """Calculate new ease factor"""
        return self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
```

---

## 📊 REVIEW SCHEDULE EXAMPLES

### Example 1: Perfect Performance (Quality = 5)
```
Review 1: Day 1 (Initial)
  → Interval = 1, Ease = 2.5, Repetitions = 1
  → Next review: Day 2

Review 2: Day 3 (Quality = 5)
  → Interval = 3, Ease = 2.6, Repetitions = 2
  → Next review: Day 6

Review 3: Day 6 (Quality = 5)
  → Interval = 7.8 ≈ 8, Ease = 2.7, Repetitions = 3
  → Next review: Day 14

Review 4: Day 14 (Quality = 5)
  → Interval = 21.6 ≈ 22, Ease = 2.8, Repetitions = 4
  → Next review: Day 36

Review 5: Day 36 (Quality = 5)
  → Interval = 60.64 ≈ 61, Ease = 2.9, Repetitions = 5
  → Next review: Day 97
```

### Example 2: Mixed Performance
```
Review 1: Day 1 (Quality = 5)
  → Interval = 1, Ease = 2.5, Repetitions = 1
  → Next review: Day 2

Review 2: Day 3 (Quality = 3)
  → Interval = 3, Ease = 2.36, Repetitions = 2
  → Next review: Day 6

Review 3: Day 6 (Quality = 2) ❌ INCORRECT
  → Interval = 1, Ease = 2.08, Repetitions = 0 (RESET)
  → Next review: Day 7

Review 4: Day 7 (Quality = 4)
  → Interval = 1, Ease = 2.18, Repetitions = 1
  → Next review: Day 8

Review 5: Day 8 (Quality = 5)
  → Interval = 3, Ease = 2.28, Repetitions = 2
  → Next review: Day 11
```

---

## 🎓 LANGUAGE LEARNING ENHANCEMENTS

### Difficulty Adjustments

For German language learning, we apply contextual difficulty modifiers:

```python
def get_difficulty_multiplier(card_type: str, proficiency_level: str) -> float:
    """
    Apply difficulty multipliers based on card type and user proficiency
    """
    multipliers = {
        'vocabulary': {
            'A1': 1.0,
            'A2': 0.9,  # Easier for advanced learners
            'B1': 0.8
        },
        'grammar': {
            'A1': 1.2,  # Harder for beginners
            'A2': 1.0,
            'B1': 0.9
        },
        'pronunciation': {
            'A1': 1.1,
            'A2': 1.0,
            'B1': 0.9
        }
    }
    
    return multipliers.get(card_type, {}).get(proficiency_level, 1.0)
```

### Adaptive Intervals

```python
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
    return max(1, min(adjusted_interval, 365))  # 1 day to 1 year
```

---

## 🔄 REVIEW QUEUE MANAGEMENT

### Get Next Review Items

```python
def get_next_review_items(user_id: int, limit: int = 20) -> list:
    """
    Get cards due for review, prioritized by:
    1. Overdue cards (highest priority)
    2. New cards
    3. Cards with low ease factor (need reinforcement)
    """
    query = """
    SELECT id, flashcard_id, interval, ease_factor, repetitions
    FROM user_progress
    WHERE user_id = %s
      AND next_review_at <= NOW()
    ORDER BY
      CASE 
        WHEN next_review_at < NOW() - INTERVAL '1 day' THEN 1  -- Overdue
        WHEN repetitions = 0 THEN 2                             -- New
        WHEN ease_factor < 2.0 THEN 3                           -- Low ease
        ELSE 4                                                   -- Regular
      END,
      next_review_at ASC,
      ease_factor ASC
    LIMIT %s
    """
    return execute_query(query, (user_id, limit))
```

### Daily Review Recommendations

```python
def get_daily_recommendation(user_id: int) -> dict:
    """
    Calculate recommended daily review load
    """
    query = """
    SELECT 
      COUNT(*) as total_cards,
      SUM(CASE WHEN next_review_at <= NOW() THEN 1 ELSE 0 END) as due_cards,
      AVG(ease_factor) as avg_ease
    FROM user_progress
    WHERE user_id = %s
    """
    stats = execute_query(query, (user_id,))[0]
    
    # Recommend 20-30 reviews per day for optimal learning
    recommended_daily = 25
    
    return {
        'total_cards': stats['total_cards'],
        'due_cards': stats['due_cards'],
        'recommended_daily': recommended_daily,
        'estimated_time_minutes': stats['due_cards'] * 0.5  # ~30 seconds per card
    }
```

---

## 📈 PERFORMANCE METRICS

### User Progress Tracking

```python
def calculate_user_statistics(user_id: int) -> dict:
    """
    Calculate comprehensive learning statistics
    """
    query = """
    SELECT
      COUNT(*) as total_cards,
      SUM(CASE WHEN status = 'mastered' THEN 1 ELSE 0 END) as mastered_cards,
      SUM(CASE WHEN status = 'learning' THEN 1 ELSE 0 END) as learning_cards,
      SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) as new_cards,
      AVG(accuracy_percentage) as avg_accuracy,
      AVG(ease_factor) as avg_ease_factor,
      SUM(time_spent_seconds) as total_time_seconds
    FROM user_progress
    WHERE user_id = %s
    """
    stats = execute_query(query, (user_id,))[0]
    
    return {
        'total_cards': stats['total_cards'],
        'mastered_cards': stats['mastered_cards'],
        'mastery_percentage': (stats['mastered_cards'] / stats['total_cards']) * 100,
        'learning_cards': stats['learning_cards'],
        'new_cards': stats['new_cards'],
        'average_accuracy': stats['avg_accuracy'],
        'average_ease_factor': stats['avg_ease_factor'],
        'total_study_time_hours': stats['total_time_seconds'] / 3600
    }
```

---

## 🎯 MASTERY CRITERIA

A card is considered "mastered" when:

1. **Repetitions ≥ 5** - Card has been reviewed at least 5 times
2. **Ease Factor ≥ 2.5** - Consistent correct responses
3. **Accuracy ≥ 90%** - High accuracy rate
4. **Last 3 Reviews = Quality 4-5** - Recent perfect performance

```python
def check_mastery(card_progress: dict) -> bool:
    """Check if card meets mastery criteria"""
    return (
        card_progress['repetitions'] >= 5 and
        card_progress['ease_factor'] >= 2.5 and
        card_progress['accuracy_percentage'] >= 90 and
        card_progress['last_three_qualities'] == [4, 4, 4]  # or similar
    )
```

---

## 🚀 IMPLEMENTATION ROADMAP

1. **Phase 1:** Implement basic SM-2 algorithm
2. **Phase 2:** Add database integration
3. **Phase 3:** Implement review queue management
4. **Phase 4:** Add language learning enhancements
5. **Phase 5:** Implement adaptive intervals
6. **Phase 6:** Add analytics and reporting

---

*SRS Algorithm v1.0 | Protocol: OMEGA 777 | Authority: Manus AI*
