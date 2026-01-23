# 🤖 Autonomous Lesson Ingestion Engine

**Protocol:** OMEGA 777  
**Version:** 1.0  
**Purpose:** Parse 500+ Markdown lessons and populate database automatically

---

## 📋 OVERVIEW

The Lesson Ingestion Engine automatically:
1. Scans the `lessons_500/` directory for Markdown files
2. Parses structured lesson content
3. Extracts vocabulary, grammar, examples, and exercises
4. Populates the PostgreSQL database
5. Generates flashcards from vocabulary
6. Creates exercise records
7. Validates data integrity
8. Handles errors gracefully

---

## 🏗️ ARCHITECTURE

```
Input: lessons_500/*.md files
   ↓
Parser: Extract structured data
   ↓
Validator: Check data quality
   ↓
Transformer: Convert to database format
   ↓
Database: Insert into PostgreSQL
   ↓
Output: Indexed, searchable lessons
```

---

## 📝 MARKDOWN LESSON FORMAT

### Expected Structure

```markdown
# Lektion 001: Hallo sagen - Formell (Saying Hello - Formal)

## 🎓 Prize2Pride German | Professor Roued | A1

---

## 1. VOKABULAR 📚

| Deutsch | العربية | Pronunciation |
|---------|---------|---|
| Guten Tag | طاب يومك | GOO-ten TAHK |
| Hallo | مرحبًا | HAH-lo |

---

## 2. FLASHCARDS 🎴

1. **Guten Tag** → طاب يومك
   *Beispiel:* Guten Tag, wie kann ich Ihnen helfen?

---

## 3. TEXT 😂

1. **Guten Tag! Ich heiße Herr Müller.**
   صباح الخير! اسمي السيد مولر.

---

## 4. DIALOG 💬

**A:** Guten Tag! Wie heißen Sie?
**B:** Guten Tag! Ich heiße Herr Weber.

---

## 5. GRAMMATIK 📖

**Tipp:** Im formellen Deutsch benutzt man "Sie" für Höflichkeit.

---

## 6. ÜBUNGEN ✏️

**A) Richtig oder Falsch?**
1. "Hallo" ist eine formelle Begrüßung. (Falsch)

**B) Lückentext:**
Guten ___! Mein Name ist ___.

---

## 7. LÖSUNGEN ✅

**A) Richtig oder Falsch?**
1. Falsch

**B) Lückentext:**
Guten **Tag**! Mein Name ist **Schmidt**.
```

---

## 🔍 PARSING LOGIC

### Step 1: Extract Metadata

```python
def extract_metadata(filename: str, content: str) -> dict:
    """Extract lesson metadata from filename and header"""
    
    # Parse filename: 001-saying-hello---formal.md
    lesson_id = int(filename.split('-')[0])
    title_slug = filename.replace('.md', '')
    
    # Extract from content
    lines = content.split('\n')
    title = lines[0].replace('# ', '').strip()
    
    # Extract level (A1, A2, B1, etc.)
    level_match = re.search(r'(A1|A2|B1|B2|C1|C2)', content)
    level = level_match.group(1) if level_match else 'A1'
    
    return {
        'lesson_id': lesson_id,
        'title': title,
        'slug': title_slug,
        'level': level,
        'category': extract_category(title),
        'icon': extract_icon(content)
    }
```

### Step 2: Extract Vocabulary

```python
def extract_vocabulary(content: str) -> list:
    """Extract vocabulary table from VOKABULAR section"""
    
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
                vocabulary.append({
                    'german': cells[0],
                    'arabic': cells[1],
                    'pronunciation': cells[2] if len(cells) > 2 else '',
                    'formal': 'formal' in cells[0].lower()
                })
    
    return vocabulary
```

### Step 3: Extract Flashcards

```python
def extract_flashcards(content: str) -> list:
    """Extract flashcards from FLASHCARDS section"""
    
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
        flashcards.append({
            'front_text': german.strip(),
            'front_text_ar': arabic.strip(),
            'example_sentence': example.strip(),
            'difficulty_level': 1
        })
    
    return flashcards
```

### Step 4: Extract Grammar

```python
def extract_grammar(content: str) -> dict:
    """Extract grammar explanation from GRAMMATIK section"""
    
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
        'topic': extract_grammar_topic(section_text),
        'explanation': tip,
        'examples': examples
    }
```

### Step 5: Extract Exercises

```python
def extract_exercises(content: str) -> list:
    """Extract exercises from ÜBUNGEN section"""
    
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
    tf_section = re.search(r'\*\*A\) Richtig oder Falsch\?\*\*(.*?)(?=\*\*B\)|$)', section_text, re.DOTALL)
    if tf_section:
        tf_items = re.findall(r'^\d+\.\s+"(.+?)"\s+\((.+?)\)', tf_section.group(1), re.MULTILINE)
        for question, answer in tf_items:
            exercises.append({
                'exercise_type': 'listening',
                'exercise_format': 'true_false',
                'question': question,
                'correct_answer': answer.strip(),
                'difficulty_level': 1
            })
    
    # Extract Fill-in-the-blanks exercises
    blank_section = re.search(r'\*\*B\) Lückentext:\*\*(.*?)(?=\*\*|---)', section_text, re.DOTALL)
    if blank_section:
        blank_items = re.findall(r'(.+?___.+?)(?=\n\(|\n\d+\.|\n\n)', blank_section.group(1), re.DOTALL)
        for item in blank_items:
            exercises.append({
                'exercise_type': 'writing',
                'exercise_format': 'fill_blank',
                'question': item.strip(),
                'difficulty_level': 2
            })
    
    return exercises
```

---

## 💾 DATABASE INSERTION

```python
def ingest_lesson(filename: str, content: str, db_connection) -> dict:
    """
    Complete lesson ingestion pipeline
    """
    
    try:
        # Extract all data
        metadata = extract_metadata(filename, content)
        vocabulary = extract_vocabulary(content)
        flashcards = extract_flashcards(content)
        grammar = extract_grammar(content)
        exercises = extract_exercises(content)
        
        # Insert lesson
        lesson_id = insert_lesson(db_connection, {
            'title': metadata['title'],
            'slug': metadata['slug'],
            'level': metadata['level'],
            'category': metadata['category'],
            'icon': metadata['icon'],
            'content': content,
            'vocabulary': json.dumps(vocabulary),
            'grammar': json.dumps(grammar)
        })
        
        # Insert flashcards
        for flashcard in flashcards:
            flashcard['lesson_id'] = lesson_id
            insert_flashcard(db_connection, flashcard)
        
        # Insert exercises
        for exercise in exercises:
            exercise['lesson_id'] = lesson_id
            insert_exercise(db_connection, exercise)
        
        return {
            'status': 'success',
            'lesson_id': lesson_id,
            'flashcards_created': len(flashcards),
            'exercises_created': len(exercises)
        }
    
    except Exception as e:
        return {
            'status': 'error',
            'filename': filename,
            'error': str(e)
        }
```

---

## 🚀 BATCH INGESTION

```python
def ingest_all_lessons(lessons_directory: str, db_connection) -> dict:
    """
    Ingest all lessons from directory
    """
    
    results = {
        'total_files': 0,
        'successful': 0,
        'failed': 0,
        'total_flashcards': 0,
        'total_exercises': 0,
        'errors': []
    }
    
    # Get all markdown files
    lesson_files = sorted(glob.glob(f'{lessons_directory}/*.md'))
    results['total_files'] = len(lesson_files)
    
    print(f"🤖 Starting ingestion of {len(lesson_files)} lessons...")
    
    for i, filepath in enumerate(lesson_files, 1):
        filename = os.path.basename(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            result = ingest_lesson(filename, content, db_connection)
            
            if result['status'] == 'success':
                results['successful'] += 1
                results['total_flashcards'] += result['flashcards_created']
                results['total_exercises'] += result['exercises_created']
                print(f"✅ [{i}/{len(lesson_files)}] {filename}")
            else:
                results['failed'] += 1
                results['errors'].append(result)
                print(f"❌ [{i}/{len(lesson_files)}] {filename}: {result['error']}")
        
        except Exception as e:
            results['failed'] += 1
            results['errors'].append({
                'filename': filename,
                'error': str(e)
            })
            print(f"❌ [{i}/{len(lesson_files)}] {filename}: {str(e)}")
    
    print(f"\n📊 Ingestion Complete!")
    print(f"   ✅ Successful: {results['successful']}/{results['total_files']}")
    print(f"   ❌ Failed: {results['failed']}/{results['total_files']}")
    print(f"   📚 Flashcards created: {results['total_flashcards']}")
    print(f"   ✏️  Exercises created: {results['total_exercises']}")
    
    return results
```

---

## ✅ DATA VALIDATION

```python
def validate_lesson_data(lesson_data: dict) -> list:
    """Validate extracted lesson data"""
    
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
```

---

## 🔄 ERROR HANDLING

```python
def handle_ingestion_error(error_type: str, filename: str, error: Exception):
    """Handle different types of ingestion errors"""
    
    error_log = {
        'timestamp': datetime.now().isoformat(),
        'filename': filename,
        'error_type': error_type,
        'error_message': str(error),
        'traceback': traceback.format_exc()
    }
    
    # Log to file
    with open('ingestion_errors.log', 'a') as f:
        f.write(json.dumps(error_log) + '\n')
    
    # Notify admin
    if error_type == 'CRITICAL':
        send_admin_notification(error_log)
```

---

## 📊 INGESTION REPORT

After ingestion, generate a comprehensive report:

```json
{
  "ingestion_date": "2026-01-23",
  "total_files_processed": 20,
  "successful_ingestions": 20,
  "failed_ingestions": 0,
  "statistics": {
    "total_lessons": 20,
    "total_flashcards": 450,
    "total_exercises": 120,
    "total_vocabulary_items": 500,
    "levels_covered": ["A1", "A2"],
    "categories": [
      "Greetings",
      "Numbers",
      "Colors",
      "Family",
      "Food",
      "Time",
      "Weather",
      "Shopping",
      "Directions",
      "Body Parts",
      "Clothes",
      "Home",
      "Work",
      "Hobbies",
      "Travel",
      "Health",
      "School",
      "Animals",
      "Nature",
      "Celebrations"
    ]
  },
  "processing_time_seconds": 45,
  "database_status": "healthy",
  "indexes_created": 12,
  "next_steps": [
    "Verify all lessons are searchable",
    "Test SRS algorithm with sample data",
    "Generate user statistics",
    "Create backup of database"
  ]
}
```

---

## 🔧 IMPLEMENTATION CHECKLIST

- [ ] Create parser module
- [ ] Implement regex patterns for all sections
- [ ] Build database insertion functions
- [ ] Create validation framework
- [ ] Implement error handling
- [ ] Add logging system
- [ ] Create batch ingestion script
- [ ] Generate ingestion report
- [ ] Test with sample lessons
- [ ] Test with all 500 lessons
- [ ] Optimize for performance
- [ ] Create admin dashboard for monitoring

---

## 📈 PERFORMANCE TARGETS

| Metric | Target |
|--------|--------|
| Lessons per second | 5-10 |
| Total ingestion time (500 lessons) | < 2 minutes |
| Database queries per lesson | < 10 |
| Memory usage | < 500MB |
| Error rate | < 0.1% |

---

*Lesson Ingestion Engine v1.0 | Protocol: OMEGA 777 | Authority: Manus AI*
