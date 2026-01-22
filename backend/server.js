const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Lesson data
const lessons = [
  { id: 1, title: "Greetings", titleAr: "التحيات", folder: "01-greetings", icon: "👋" },
  { id: 2, title: "Numbers", titleAr: "الأرقام", folder: "02-numbers", icon: "🔢" },
  { id: 3, title: "Colors", titleAr: "الألوان", folder: "03-colors", icon: "🎨" },
  { id: 4, title: "Family", titleAr: "العائلة", folder: "04-family", icon: "👨‍👩‍👧‍👦" },
  { id: 5, title: "Food & Drinks", titleAr: "الطعام والشراب", folder: "05-food", icon: "🍕" },
  { id: 6, title: "Time & Date", titleAr: "الوقت والتاريخ", folder: "06-time", icon: "⏰" },
  { id: 7, title: "Weather", titleAr: "الطقس", folder: "07-weather", icon: "🌤️" },
  { id: 8, title: "Shopping", titleAr: "التسوق", folder: "08-shopping", icon: "🛒" },
  { id: 9, title: "Directions", titleAr: "الاتجاهات", folder: "09-directions", icon: "🧭" },
  { id: 10, title: "Body Parts", titleAr: "أجزاء الجسم", folder: "10-body", icon: "🦵" },
  { id: 11, title: "Clothes", titleAr: "الملابس", folder: "11-clothes", icon: "👔" },
  { id: 12, title: "Home", titleAr: "المنزل", folder: "12-home", icon: "🏠" },
  { id: 13, title: "Work", titleAr: "العمل", folder: "13-work", icon: "💼" },
  { id: 14, title: "Hobbies", titleAr: "الهوايات", folder: "14-hobbies", icon: "⚽" },
  { id: 15, title: "Travel", titleAr: "السفر", folder: "15-travel", icon: "✈️" },
  { id: 16, title: "Health", titleAr: "الصحة", folder: "16-health", icon: "🏥" },
  { id: 17, title: "School", titleAr: "المدرسة", folder: "17-school", icon: "📚" },
  { id: 18, title: "Animals", titleAr: "الحيوانات", folder: "18-animals", icon: "🐕" },
  { id: 19, title: "Nature", titleAr: "الطبيعة", folder: "19-nature", icon: "🌳" },
  { id: 20, title: "Celebrations", titleAr: "الاحتفالات", folder: "20-celebrations", icon: "🎉" }
];

// API Routes
app.get('/api/lessons', (req, res) => {
  res.json(lessons);
});

app.get('/api/lessons/:id', (req, res) => {
  const lesson = lessons.find(l => l.id === parseInt(req.params.id));
  if (!lesson) return res.status(404).json({ error: 'Lesson not found' });
  
  const lessonPath = path.join(__dirname, '..', 'lessons', lesson.folder, 'lesson.md');
  try {
    const content = fs.readFileSync(lessonPath, 'utf8');
    res.json({ ...lesson, content });
  } catch (err) {
    res.json({ ...lesson, content: 'Lesson content loading...' });
  }
});

app.get('/api/exercises/:type', (req, res) => {
  const { type } = req.params;
  const validTypes = ['reading', 'writing', 'listening', 'speaking'];
  if (!validTypes.includes(type)) {
    return res.status(400).json({ error: 'Invalid exercise type' });
  }
  
  const exercisePath = path.join(__dirname, '..', 'exercises', type, `${type}_exercises.md`);
  try {
    const content = fs.readFileSync(exercisePath, 'utf8');
    res.json({ type, content });
  } catch (err) {
    res.status(404).json({ error: 'Exercises not found' });
  }
});

app.get('/api/tests', (req, res) => {
  const testPath = path.join(__dirname, '..', 'tests', 'comprehensive_tests.md');
  try {
    const content = fs.readFileSync(testPath, 'utf8');
    res.json({ content });
  } catch (err) {
    res.status(404).json({ error: 'Tests not found' });
  }
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'OK', message: 'German A1 API is running!' });
});

app.listen(PORT, () => {
  console.log(`🇩🇪 German A1 API running on port ${PORT}`);
});
