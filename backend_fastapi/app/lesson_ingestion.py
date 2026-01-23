"""
Autonomous Lesson Ingestion Engine
Parses Markdown lessons and populates database
"""

import os
import re
import glob
import json
import logging
from typing import List, Dict, Tuple
from pathlib import Path
from datetime import datetime
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

# ============================================================================
# PARSING FUNCTIONS
# ============================================================================

def extract_metadata(filename: str, content: str) -> Dict:
    """
    Extract lesson metadata from filename and header
    """
    try:
        # Parse filename: 001-saying-hello---formal.md
        parts = filename.replace('.md', '').split('-')
        lesson_id = int(parts[0])
        
        # Extract title from first line
        lines = content.split('\n')
        title = lines[0].replace('# ', '').strip()
        
        # Extract level (A1, A2, B1, etc.)
        level_match = re.search(r'(A1|A2|B1|B2|C1|C2)', content)
        level = level_match.group(1) if level_match else 'A1'
        
        # Create slug from filename
        slug = filename.replace('.md', '')
        
        # Extract category from title
        category = extract_category(title)
        
        # Extract icon
        icon = extract_icon(content)
        
        return {
            'lesson_id': lesson_id,
            'title': title,
            'slug': slug,
            'level': level,
            'category': category,
            'icon': icon,
            'description': f'Learn {category} in German at {level} level'
        }
    except Exception as e:
        logger.error(f"Error extracting metadata from {filename}: {str(e)}")
        return None

def extract_category(title: str) -> str:
    """
    Extract category from title
    """
    # Remove lesson number and extract main topic
    title_clean = re.sub(r'^\d+\s*[-:]\s*', '', title)
    # Extract first meaningful part
    parts = title_clean.split('-')
    return parts[0].strip() if parts else 'General'

def extract_icon(content: str) -> str:
    """
    Extract icon emoji from content
    """
    # Look for emoji patterns
    emoji_pattern = r'[🀀-🿿]'
    match = re.search(emoji_pattern, content)
    return match.group(0) if match else '📚'

def extract_vocabulary(content: str) -> List[Dict]:
    """
    Extract vocabulary table from VOKABULAR section
    """
    try:
        vocab_section = re.search(
            r'## 1\. VOKABULAR.*?\n\n(.*?)\n\n---',
            content,
            re.DOTALL
        )
        
        if not vocab_section:
            return []
        
        table_content = vocab_section.group(1)
        rows = table_content.split('\n')[2:]  # Skip header and separator
        
        vocabulary = []
        for row in rows:
            if row.strip() and '|' in row:
                cells = [cell.strip() for cell in row.split('|')[1:-1]]
                if len(cells) >= 2:
                    vocab_item = {
                        'german': cells[0],
                        'arabic': cells[1] if len(cells) > 1 else '',
                        'pronunciation': cells[2] if len(cells) > 2 else '',
                        'formal': 'formal' in cells[0].lower()
                    }
                    vocabulary.append(vocab_item)
        
        return vocabulary
    except Exception as e:
        logger.error(f"Error extracting vocabulary: {str(e)}")
        return []

def extract_flashcards(content: str) -> List[Dict]:
    """
    Extract flashcards from FLASHCARDS section
    """
    try:
        flashcard_section = re.search(
            r'## 2\. FLASHCARDS.*?\n\n(.*?)\n\n---',
            content,
            re.DOTALL
        )
        
        if not flashcard_section:
            return []
        
        flashcards = []
        pattern = r'\d+\.\s+\*\*(.+?)\*\*\s+→\s+(.+?)\n\s+\*Beispiel:\*\s+(.+?)(?=\n\d+\.|$)'
        
        matches = re.findall(pattern, flashcard_section.group(1), re.DOTALL)
        
        for german, arabic, example in matches:
            flashcard = {
                'front_text': german.strip(),
                'front_text_ar': arabic.strip(),
                'back_text': example.strip(),
                'example_sentence': example.strip(),
                'difficulty_level': 1,
                'category': 'Vocabulary'
            }
            flashcards.append(flashcard)
        
        return flashcards
    except Exception as e:
        logger.error(f"Error extracting flashcards: {str(e)}")
        return []

def extract_grammar(content: str) -> Dict:
    """
    Extract grammar explanation from GRAMMATIK section
    """
    try:
        grammar_section = re.search(
            r'## 5\. GRAMMATIK.*?\n\n(.*?)\n\n---',
            content,
            re.DOTALL
        )
        
        if not grammar_section:
            return {}
        
        section_text = grammar_section.group(1)
        
        # Extract tip
        tip_match = re.search(r'\*\*Tipp:\*\*\s+(.+?)(?=\n\n|\*\*)', section_text, re.DOTALL)
        tip = tip_match.group(1).strip() if tip_match else ''
        
        # Extract examples
        examples = re.findall(r'^\d+\.\s+(.+?)$', section_text, re.MULTILINE)
        
        return {
            'topic': 'Grammar',
            'explanation': tip,
            'examples': examples[:5]  # Limit to 5 examples
        }
    except Exception as e:
        logger.error(f"Error extracting grammar: {str(e)}")
        return {}

def extract_exercises(content: str) -> List[Dict]:
    """
    Extract exercises from ÜBUNGEN section
    """
    try:
        exercises_section = re.search(
            r'## 6\. ÜBUNGEN.*?\n\n(.*?)\n\n---',
            content,
            re.DOTALL
        )
        
        if not exercises_section:
            return []
        
        exercises = []
        section_text = exercises_section.group(1)
        
        # Extract True/False exercises
        tf_section = re.search(
            r'\*\*A\) Richtig oder Falsch\?\*\*(.*?)(?=\*\*B\)|$)',
            section_text,
            re.DOTALL
        )
        if tf_section:
            tf_items = re.findall(
                r'^\d+\.\s+"(.+?)"\s+\((.+?)\)',
                tf_section.group(1),
                re.MULTILINE
            )
            for question, answer in tf_items[:5]:  # Limit to 5
                exercises.append({
                    'exercise_type': 'listening',
                    'exercise_format': 'true_false',
                    'question': question,
                    'correct_answer': answer.strip(),
                    'difficulty_level': 1
                })
        
        # Extract Fill-in-the-blanks exercises
        blank_section = re.search(
            r'\*\*B\) Lückentext:\*\*(.*?)(?=\*\*|---)',
            section_text,
            re.DOTALL
        )
        if blank_section:
            blank_items = re.findall(
                r'(.+?___.+?)(?=\n\(|\n\d+\.|\n\n)',
                blank_section.group(1),
                re.DOTALL
            )
            for item in blank_items[:5]:  # Limit to 5
                exercises.append({
                    'exercise_type': 'writing',
                    'exercise_format': 'fill_blank',
                    'question': item.strip(),
                    'difficulty_level': 2
                })
        
        return exercises
    except Exception as e:
        logger.error(f"Error extracting exercises: {str(e)}")
        return []

# ============================================================================
# DATABASE INSERTION FUNCTIONS
# ============================================================================

def insert_lesson(db: Session, lesson_data: Dict) -> int:
    """
    Insert lesson into database
    """
    from app.models import Lesson
    
    try:
        lesson = Lesson(
            title=lesson_data['title'],
            title_ar=lesson_data.get('title_ar', lesson_data['title']),
            slug=lesson_data['slug'],
            level=lesson_data['level'],
            category=lesson_data['category'],
            icon=lesson_data.get('icon', '📚'),
            description=lesson_data.get('description', ''),
            content=lesson_data.get('content', ''),
            vocabulary=lesson_data.get('vocabulary', []),
            grammar=lesson_data.get('grammar', {}),
            is_published=True
        )
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson.id
    except Exception as e:
        logger.error(f"Error inserting lesson: {str(e)}")
        db.rollback()
        return None

def insert_flashcard(db: Session, flashcard_data: Dict) -> int:
    """
    Insert flashcard into database
    """
    from app.models import Flashcard
    
    try:
        flashcard = Flashcard(
            lesson_id=flashcard_data['lesson_id'],
            front_text=flashcard_data['front_text'],
            front_text_ar=flashcard_data.get('front_text_ar', ''),
            back_text=flashcard_data['back_text'],
            example_sentence=flashcard_data.get('example_sentence', ''),
            difficulty_level=flashcard_data.get('difficulty_level', 1),
            category=flashcard_data.get('category', 'Vocabulary')
        )
        db.add(flashcard)
        db.commit()
        db.refresh(flashcard)
        return flashcard.id
    except Exception as e:
        logger.error(f"Error inserting flashcard: {str(e)}")
        db.rollback()
        return None

def insert_exercise(db: Session, exercise_data: Dict) -> int:
    """
    Insert exercise into database
    """
    from app.models import Exercise
    
    try:
        exercise = Exercise(
            lesson_id=exercise_data['lesson_id'],
            exercise_type=exercise_data['exercise_type'],
            title=exercise_data.get('title', exercise_data['question'][:50]),
            question=exercise_data['question'],
            exercise_format=exercise_data['exercise_format'],
            correct_answer=exercise_data.get('correct_answer', ''),
            difficulty_level=exercise_data.get('difficulty_level', 1),
            points=exercise_data.get('points', 10)
        )
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        return exercise.id
    except Exception as e:
        logger.error(f"Error inserting exercise: {str(e)}")
        db.rollback()
        return None

# ============================================================================
# MAIN INGESTION FUNCTION
# ============================================================================

def ingest_lesson(filename: str, content: str, db: Session) -> Dict:
    """
    Complete lesson ingestion pipeline
    """
    try:
        # Extract all data
        metadata = extract_metadata(filename, content)
        if not metadata:
            return {
                'status': 'error',
                'filename': filename,
                'error': 'Failed to extract metadata'
            }
        
        vocabulary = extract_vocabulary(content)
        flashcards = extract_flashcards(content)
        grammar = extract_grammar(content)
        exercises = extract_exercises(content)
        
        # Prepare lesson data
        lesson_data = {
            'title': metadata['title'],
            'title_ar': metadata['title'],
            'slug': metadata['slug'],
            'level': metadata['level'],
            'category': metadata['category'],
            'icon': metadata['icon'],
            'description': metadata['description'],
            'content': content,
            'vocabulary': vocabulary,
            'grammar': grammar
        }
        
        # Insert lesson
        lesson_id = insert_lesson(db, lesson_data)
        if not lesson_id:
            return {
                'status': 'error',
                'filename': filename,
                'error': 'Failed to insert lesson'
            }
        
        # Insert flashcards
        flashcard_count = 0
        for flashcard in flashcards:
            flashcard['lesson_id'] = lesson_id
            if insert_flashcard(db, flashcard):
                flashcard_count += 1
        
        # Insert exercises
        exercise_count = 0
        for exercise in exercises:
            exercise['lesson_id'] = lesson_id
            if insert_exercise(db, exercise):
                exercise_count += 1
        
        return {
            'status': 'success',
            'filename': filename,
            'lesson_id': lesson_id,
            'flashcards_created': flashcard_count,
            'exercises_created': exercise_count
        }
    
    except Exception as e:
        logger.error(f"Error ingesting lesson {filename}: {str(e)}")
        return {
            'status': 'error',
            'filename': filename,
            'error': str(e)
        }

def ingest_all_lessons(lessons_directory: str, db: Session) -> Dict:
    """
    Ingest all lessons from directory
    """
    results = {
        'total_files': 0,
        'successful': 0,
        'failed': 0,
        'total_flashcards': 0,
        'total_exercises': 0,
        'errors': [],
        'start_time': datetime.now().isoformat()
    }
    
    # Get all markdown files
    lesson_files = sorted(glob.glob(f'{lessons_directory}/*.md'))
    results['total_files'] = len(lesson_files)
    
    logger.info(f"🤖 Starting ingestion of {len(lesson_files)} lessons...")
    
    for i, filepath in enumerate(lesson_files, 1):
        filename = os.path.basename(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = ingest_lesson(filename, content, db)
            
            if result['status'] == 'success':
                results['successful'] += 1
                results['total_flashcards'] += result['flashcards_created']
                results['total_exercises'] += result['exercises_created']
                logger.info(f"✅ [{i}/{len(lesson_files)}] {filename}")
            else:
                results['failed'] += 1
                results['errors'].append(result)
                logger.error(f"❌ [{i}/{len(lesson_files)}] {filename}: {result['error']}")
        
        except Exception as e:
            results['failed'] += 1
            results['errors'].append({
                'filename': filename,
                'error': str(e)
            })
            logger.error(f"❌ [{i}/{len(lesson_files)}] {filename}: {str(e)}")
    
    results['end_time'] = datetime.now().isoformat()
    
    logger.info(f"\n📊 Ingestion Complete!")
    logger.info(f"   ✅ Successful: {results['successful']}/{results['total_files']}")
    logger.info(f"   ❌ Failed: {results['failed']}/{results['total_files']}")
    logger.info(f"   📚 Flashcards created: {results['total_flashcards']}")
    logger.info(f"   ✏️  Exercises created: {results['total_exercises']}")
    
    return results

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def save_ingestion_report(results: Dict, output_file: str = 'ingestion_report.json'):
    """
    Save ingestion results to file
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Ingestion report saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving ingestion report: {str(e)}")

def validate_lesson_data(lesson_data: Dict) -> List[str]:
    """
    Validate extracted lesson data
    """
    errors = []
    
    # Check required fields
    required_fields = ['title', 'level', 'content']
    for field in required_fields:
        if not lesson_data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Check vocabulary
    if not lesson_data.get('vocabulary'):
        errors.append("No vocabulary found")
    
    # Check level is valid
    valid_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']
    if lesson_data.get('level') not in valid_levels:
        errors.append(f"Invalid level: {lesson_data.get('level')}")
    
    # Check content length
    if len(lesson_data.get('content', '')) < 100:
        errors.append("Content too short")
    
    return errors
