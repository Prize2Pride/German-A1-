#!/usr/bin/env python3
"""
Prize2Pride German Course - Weather Lesson PDF Generator
Creates a colorful, branded PDF with Professor Roued
"""

from fpdf import FPDF
import os

class WeatherPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
        
    def header(self):
        # Brand colors
        self.set_fill_color(15, 15, 26)  # Dark background
        self.rect(0, 0, 210, 25, 'F')
        
        # Logo text
        self.set_font('DejaVu', 'B', 14)
        self.set_text_color(0, 245, 255)  # Cyan
        self.set_xy(10, 8)
        self.cell(0, 10, 'Prize2Pride German Course', 0, 0, 'L')
        
        # Professor name
        self.set_font('DejaVu', '', 10)
        self.set_text_color(255, 255, 255)
        self.set_xy(150, 8)
        self.cell(0, 10, 'Professor Roued', 0, 0, 'R')
        
        self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Prize2Pride German Course | Page {self.page_no()}', 0, 0, 'C')
        
    def chapter_title(self, title, color=(0, 245, 255)):
        self.set_font('DejaVu', 'B', 18)
        self.set_text_color(*color)
        self.cell(0, 15, title, 0, 1, 'C')
        self.ln(5)
        
    def section_title(self, title, color=(255, 0, 255)):
        self.set_font('DejaVu', 'B', 14)
        self.set_text_color(*color)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
        
    def add_vocab_table(self, data, headers):
        # Table header
        self.set_fill_color(30, 30, 50)
        self.set_text_color(0, 245, 255)
        self.set_font('DejaVu', 'B', 10)
        
        col_widths = [45, 45, 45, 45]
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, 1, 0, 'C', True)
        self.ln()
        
        # Table rows
        self.set_font('DejaVu', '', 9)
        fill = False
        for row in data:
            if fill:
                self.set_fill_color(25, 25, 40)
            else:
                self.set_fill_color(20, 20, 35)
            
            self.set_text_color(255, 255, 255)
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, cell, 1, 0, 'C', True)
            self.ln()
            fill = not fill
        self.ln(5)
        
    def add_dialogue(self, speaker, german, english, arabic, color):
        self.set_fill_color(*color)
        self.set_text_color(255, 255, 255)
        self.set_font('DejaVu', 'B', 10)
        self.cell(20, 7, speaker, 0, 0, 'L')
        self.set_font('DejaVu', '', 10)
        self.multi_cell(0, 7, german)
        
        self.set_text_color(180, 180, 180)
        self.set_font('DejaVu', '', 8)
        self.cell(20, 5, '', 0, 0)
        self.multi_cell(0, 5, f"({english})")
        
        self.set_text_color(0, 245, 255)
        self.cell(20, 5, '', 0, 0)
        self.multi_cell(0, 5, arabic)
        self.ln(3)

def create_main_lesson_pdf():
    pdf = WeatherPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Cover Page
    pdf.add_page()
    pdf.set_fill_color(15, 15, 26)
    pdf.rect(0, 25, 210, 272, 'F')
    
    pdf.set_y(60)
    pdf.set_font('DejaVu', 'B', 36)
    pdf.set_text_color(0, 245, 255)
    pdf.cell(0, 20, 'Das Wetter', 0, 1, 'C')
    
    pdf.set_font('DejaVu', 'B', 24)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 15, 'The Weather', 0, 1, 'C')
    
    pdf.set_font('DejaVu', '', 20)
    pdf.set_text_color(255, 0, 255)
    pdf.cell(0, 15, 'Lesson 7 | A1 Level', 0, 1, 'C')
    
    pdf.ln(20)
    pdf.set_font('DejaVu', '', 14)
    pdf.set_text_color(57, 255, 20)
    pdf.cell(0, 10, 'Three Learning Modes:', 0, 1, 'C')
    
    pdf.set_text_color(255, 107, 53)
    pdf.cell(0, 10, '1. Informal (German Dialects)', 0, 1, 'C')
    pdf.set_text_color(0, 245, 255)
    pdf.cell(0, 10, '2. Formal (Professional)', 0, 1, 'C')
    pdf.set_text_color(57, 255, 20)
    pdf.cell(0, 10, '3. Comedy (Hilarious)', 0, 1, 'C')
    
    pdf.ln(30)
    pdf.set_font('DejaVu', 'B', 16)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'Instructor: Professor Roued', 0, 1, 'C')
    
    # Part 1: Informal
    pdf.add_page()
    pdf.chapter_title('PART 1: INFORMAL GERMAN', (255, 107, 53))
    pdf.section_title('German Dialects & Casual Speech')
    
    pdf.set_font('DejaVu', '', 10)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(0, 6, 'Learn how Germans really talk about weather in everyday life!')
    pdf.ln(5)
    
    # Vocabulary table
    pdf.section_title('Basic Weather Vocabulary', (0, 245, 255))
    vocab_data = [
        ['Das Wetter', 'das VET-ter', 'The weather', "s'Wetter"],
        ['Die Sonne', 'dee ZON-ne', 'The sun', "D'Sunn"],
        ['Der Regen', 'dair RAY-gen', 'The rain', 'Der Schauer'],
        ['Der Schnee', 'dair SHNAY', 'The snow', "s'Schnee"],
        ['Der Wind', 'dair VINT', 'The wind', "s'weht"],
        ['Die Wolke', 'dee VOL-ke', 'The cloud', "D'Wolkn"],
        ['Der Nebel', 'dair NAY-bel', 'The fog', "s'ist diesig"],
        ['Das Gewitter', 'ge-VIT-ter', 'Thunderstorm', "s'donnert"],
    ]
    pdf.add_vocab_table(vocab_data, ['German', 'Pronunciation', 'English', 'Dialect'])
    
    # Weather expressions
    pdf.section_title('Weather Expressions', (255, 0, 255))
    expressions = [
        ['Es ist sonnig', "It's sunny", 'Es ist bewolkt', "It's cloudy"],
        ['Es regnet', "It's raining", 'Es ist windig', "It's windy"],
        ['Es schneit', "It's snowing", 'Es ist neblig', "It's foggy"],
        ['Es ist heiss', "It's hot", 'Es ist kalt', "It's cold"],
    ]
    pdf.add_vocab_table(expressions, ['German', 'English', 'German', 'English'])
    
    # Informal dialogue
    pdf.add_page()
    pdf.section_title('Informal Dialogue: At a Cafe in Berlin', (255, 107, 53))
    
    dialogues = [
        ('Max:', 'Hey, wie ist das Wetter heute draussen?', "Hey, how's the weather outside today?", 'هاي، كيف الطقس بالخارج اليوم؟'),
        ('Lisa:', 'Ach, total beschissen! Es regnet wie aus Eimern!', "Oh, totally crappy! It's raining cats and dogs!", 'آخ، سيء جداً! المطر ينهمر بغزارة!'),
        ('Max:', 'Mist! Ich hab meinen Regenschirm vergessen.', 'Crap! I forgot my umbrella.', 'تباً! نسيت مظلتي.'),
        ('Lisa:', 'Typisch deutsch, oder? Gestern wars noch mega sonnig!', 'Typical German weather, right? Yesterday it was super sunny!', 'طقس ألماني نموذجي، صح؟ أمس كان مشمس جداً!'),
    ]
    
    for speaker, german, english, arabic in dialogues:
        color = (255, 107, 53) if 'Max' in speaker else (255, 0, 255)
        pdf.add_dialogue(speaker, german, english, arabic, color)
    
    # Part 2: Formal
    pdf.add_page()
    pdf.chapter_title('PART 2: FORMAL GERMAN', (0, 245, 255))
    pdf.section_title('Professional & Official Language')
    
    pdf.set_font('DejaVu', '', 10)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(0, 6, 'Learn the formal German used in weather reports, business, and official settings.')
    pdf.ln(5)
    
    formal_vocab = [
        ['Die Witterung', 'VIT-te-rung', 'Weather conditions', 'Official'],
        ['Die Niederschlage', 'NEE-der-shlay-ge', 'Precipitation', 'Forecast'],
        ['Die Temperatur', 'tem-pe-ra-TOOR', 'Temperature', 'Scientific'],
        ['Luftfeuchtigkeit', 'LUFT-foysh-tish', 'Humidity', 'Meteorology'],
        ['Der Hochdruck', 'HOKH-drook', 'High pressure', 'Weather map'],
        ['Der Tiefdruck', 'TEEF-drook', 'Low pressure', 'Weather map'],
    ]
    pdf.add_vocab_table(formal_vocab, ['German', 'Pronunciation', 'English', 'Context'])
    
    # Formal dialogue
    pdf.section_title('Formal Dialogue: TV Weather Report', (0, 245, 255))
    
    formal_dialogues = [
        ('Moderator:', 'Guten Abend, meine Damen und Herren. Hier ist die Wettervorhersage.', 'Good evening, ladies and gentlemen. Here is the weather forecast.', 'مساء الخير سيداتي وسادتي. إليكم توقعات الطقس.'),
        ('Meteorologe:', 'Morgen erwarten wir im Norden uberwiegend bewolktes Wetter.', 'Tomorrow we expect predominantly cloudy weather in the north.', 'غداً نتوقع طقساً غائماً في الغالب في الشمال.'),
        ('Moderator:', 'Und wie sieht es im Suden aus?', 'And how does it look in the south?', 'وكيف الوضع في الجنوب؟'),
        ('Meteorologe:', 'Im Suden werden die Temperaturen bei 22 Grad liegen.', 'In the south, temperatures will be around 22 degrees.', 'في الجنوب ستكون درجات الحرارة حوالي 22 درجة.'),
    ]
    
    for speaker, german, english, arabic in formal_dialogues:
        color = (0, 245, 255) if 'Moderator' in speaker else (100, 200, 255)
        pdf.add_dialogue(speaker, german, english, arabic, color)
    
    # Part 3: Comedy
    pdf.add_page()
    pdf.chapter_title('PART 3: COMEDY GERMAN', (57, 255, 20))
    pdf.section_title('Hilarious Weather Expressions!', (255, 255, 0))
    
    pdf.set_font('DejaVu', '', 10)
    pdf.set_text_color(200, 200, 200)
    pdf.multi_cell(0, 6, 'Learn German through laughter! These funny expressions will help you remember!')
    pdf.ln(5)
    
    funny_expressions = [
        ['Es regnet Bindfaden', 'Raining strings', 'Heavy rain'],
        ['Hundewetter', 'Dog weather', 'Terrible weather'],
        ['Affenkalte', 'Monkey cold', 'Freezing cold'],
        ['Bullenhitze', 'Bull heat', 'Extremely hot'],
        ['Sauwetter', 'Pig weather', 'Awful weather'],
    ]
    pdf.add_vocab_table(funny_expressions, ['German', 'Literal', 'Meaning'])
    
    # Comedy dialogue excerpt
    pdf.add_page()
    pdf.section_title('Comedy Dialogue: Hans & Greta', (57, 255, 20))
    
    comedy_dialogues = [
        ('Hans:', 'Greta! Schau mal aus dem Fenster! Die Sonne scheint!', 'Greta! Look out the window! The sun is shining!', 'غريتا! انظري من النافذة! الشمس تشرق!'),
        ('Greta:', 'Was?! In Deutschland?! Das muss ein Fehler sein!', 'What?! In Germany?! That must be a mistake!', 'ماذا؟! في ألمانيا؟! لا بد أن هذا خطأ!'),
        ('Hans:', 'Schnell, mach ein Foto! Das glaubt uns sonst keiner!', 'Quick, take a photo! Otherwise no one will believe us!', 'بسرعة، التقط صورة! وإلا لن يصدقنا أحد!'),
        ('Greta:', 'Oh nein, jetzt regnet es wieder. Ha! Das ist Deutschland!', 'Oh no, now its raining again. Ha! Thats Germany!', 'أوه لا، الآن تمطر مرة أخرى. ها! هذه ألمانيا!'),
    ]
    
    for speaker, german, english, arabic in comedy_dialogues:
        color = (57, 255, 20) if 'Hans' in speaker else (255, 255, 0)
        pdf.add_dialogue(speaker, german, english, arabic, color)
    
    # Jokes page
    pdf.add_page()
    pdf.section_title('German Weather Jokes', (255, 255, 0))
    
    jokes = [
        ('Q: Warum tragen Deutsche immer einen Regenschirm?', 'A: Weil die Sonne in Deutschland eine Legende ist!', 'Why do Germans always carry an umbrella? Because the sun in Germany is a legend!'),
        ('Q: Was ist der Unterschied zwischen Sommer und Winter?', 'A: Im Sommer regnet es warmer!', 'Whats the difference between summer and winter? In summer it rains warmer!'),
        ('Q: Wie viele Jahreszeiten hat Deutschland?', 'A: Eine: Regenzeit!', 'How many seasons does Germany have? One: Rainy season!'),
    ]
    
    for q, a, translation in jokes:
        pdf.set_font('DejaVu', 'B', 11)
        pdf.set_text_color(57, 255, 20)
        pdf.multi_cell(0, 7, q)
        pdf.set_font('DejaVu', '', 11)
        pdf.set_text_color(255, 255, 0)
        pdf.multi_cell(0, 7, a)
        pdf.set_font('DejaVu', '', 9)
        pdf.set_text_color(180, 180, 180)
        pdf.multi_cell(0, 6, f'({translation})')
        pdf.ln(5)
    
    # Save PDF
    output_path = '/home/ubuntu/German-A1-/lessons/07-weather/Prize2Pride_Weather_Lesson.pdf'
    pdf.output(output_path)
    print(f'PDF created: {output_path}')
    return output_path

def create_questions_pdf():
    pdf = WeatherPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Cover
    pdf.add_page()
    pdf.set_fill_color(15, 15, 26)
    pdf.rect(0, 25, 210, 272, 'F')
    
    pdf.set_y(60)
    pdf.set_font('DejaVu', 'B', 28)
    pdf.set_text_color(255, 0, 255)
    pdf.cell(0, 20, 'Weather Lesson', 0, 1, 'C')
    pdf.set_font('DejaVu', 'B', 24)
    pdf.set_text_color(0, 245, 255)
    pdf.cell(0, 15, 'EXERCISES & QUESTIONS', 0, 1, 'C')
    
    pdf.ln(20)
    pdf.set_font('DejaVu', '', 14)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 10, 'Prize2Pride German Course', 0, 1, 'C')
    pdf.cell(0, 10, 'Professor Roued', 0, 1, 'C')
    
    # Section 1: Vocabulary
    pdf.add_page()
    pdf.chapter_title('Section 1: Vocabulary Exercises', (0, 245, 255))
    
    pdf.section_title('Exercise 1: Match the Words')
    pdf.set_font('DejaVu', '', 10)
    pdf.set_text_color(255, 255, 255)
    
    questions = [
        '1. Die Sonne = _____ (a. rain  b. sun  c. snow  d. wind)',
        '2. Der Regen = _____ (a. cloud  b. fog  c. rain  d. storm)',
        '3. Der Schnee = _____ (a. snow  b. ice  c. cold  d. winter)',
        '4. Der Wind = _____ (a. warm  b. wind  c. weather  d. wet)',
        '5. Die Wolke = _____ (a. sun  b. moon  c. cloud  d. star)',
    ]
    
    for q in questions:
        pdf.multi_cell(0, 8, q)
    pdf.ln(5)
    
    pdf.section_title('Exercise 2: Fill in the Blanks')
    fill_blanks = [
        '1. Es ist _______ (sunny) heute. = Es ist sonnig heute.',
        '2. Es _______ (is raining) stark. = Es regnet stark.',
        '3. Das Wetter ist _______ (cold). = Das Wetter ist kalt.',
        '4. Morgen wird es _______ (warm). = Morgen wird es warm.',
        '5. Es ist sehr _______ (windy). = Es ist sehr windig.',
    ]
    
    for q in fill_blanks:
        pdf.multi_cell(0, 8, q)
    pdf.ln(5)
    
    # Section 2: Dialogue Comprehension
    pdf.add_page()
    pdf.chapter_title('Section 2: Dialogue Comprehension', (255, 0, 255))
    
    pdf.section_title('Read the dialogue and answer:')
    pdf.set_font('DejaVu', '', 10)
    pdf.set_text_color(200, 200, 200)
    
    dialogue_text = '''
Max: Hey, wie ist das Wetter heute?
Lisa: Es regnet wie aus Eimern!
Max: Mist! Ich hab meinen Regenschirm vergessen.
Lisa: Typisch deutsch! Gestern war es noch sonnig!
'''
    pdf.multi_cell(0, 7, dialogue_text)
    pdf.ln(5)
    
    pdf.set_text_color(255, 255, 255)
    comp_questions = [
        '1. What is the weather like? _______________________',
        '2. What did Max forget? _______________________',
        '3. How was the weather yesterday? _______________________',
        '4. What expression means "raining heavily"? _______________________',
    ]
    
    for q in comp_questions:
        pdf.multi_cell(0, 10, q)
    
    # Section 3: Comedy Questions
    pdf.add_page()
    pdf.chapter_title('Section 3: Comedy Section', (57, 255, 20))
    
    pdf.section_title('Translate these funny expressions:')
    funny_q = [
        '1. "Hundewetter" literally means ____________, but actually means ____________',
        '2. "Affenkalte" literally means ____________, but actually means ____________',
        '3. "Sauwetter" literally means ____________, but actually means ____________',
        '4. "Bullenhitze" literally means ____________, but actually means ____________',
    ]
    
    for q in funny_q:
        pdf.multi_cell(0, 10, q)
    pdf.ln(5)
    
    pdf.section_title('Complete the joke:')
    pdf.set_font('DejaVu', '', 10)
    pdf.set_text_color(255, 255, 255)
    pdf.multi_cell(0, 8, 'Q: Wie viele Jahreszeiten hat Deutschland?')
    pdf.multi_cell(0, 8, 'A: ________________________________')
    
    # Answer Key
    pdf.add_page()
    pdf.chapter_title('ANSWER KEY', (255, 107, 53))
    
    pdf.section_title('Section 1 Answers:')
    pdf.set_font('DejaVu', '', 10)
    pdf.set_text_color(57, 255, 20)
    answers = ['1. b (sun)', '2. c (rain)', '3. a (snow)', '4. b (wind)', '5. c (cloud)']
    for a in answers:
        pdf.cell(0, 7, a, 0, 1)
    
    pdf.ln(5)
    pdf.section_title('Section 2 Answers:')
    answers2 = [
        '1. It is raining heavily',
        '2. His umbrella (Regenschirm)',
        '3. It was sunny',
        '4. "Es regnet wie aus Eimern"'
    ]
    for a in answers2:
        pdf.cell(0, 7, a, 0, 1)
    
    pdf.ln(5)
    pdf.section_title('Section 3 Answers:')
    answers3 = [
        '1. Dog weather = Terrible weather',
        '2. Monkey cold = Freezing cold',
        '3. Pig weather = Awful weather',
        '4. Bull heat = Extremely hot',
        'Joke answer: Eine: Regenzeit! (One: Rainy season!)'
    ]
    for a in answers3:
        pdf.cell(0, 7, a, 0, 1)
    
    output_path = '/home/ubuntu/German-A1-/lessons/07-weather/Prize2Pride_Weather_Questions.pdf'
    pdf.output(output_path)
    print(f'Questions PDF created: {output_path}')
    return output_path

if __name__ == '__main__':
    create_main_lesson_pdf()
    create_questions_pdf()
    print('All PDFs generated successfully!')
