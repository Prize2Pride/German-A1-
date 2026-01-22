#!/usr/bin/env python3
"""
Prize2Pride German Course - Weather Lesson PDF Generator (CORRECTED)
The Adventures of Mr. Iheb in Tunisia
- WHITE BACKGROUND
- Arabic RTL (Right-to-Left)
- Only text colored (Dark Red Bold, Dark Blue Bold, Light Red)
"""

from fpdf import FPDF
from arabic_reshaper import reshape
import os

class IhebWeatherPDFCorrected(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
        self.add_font('Arabic', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
        
        # Color definitions
        self.DARK_RED = (139, 0, 0)        # Important expressions - Bold
        self.DARK_BLUE = (0, 0, 139)       # Formal/Grammar - Bold
        self.LIGHT_RED = (205, 92, 92)     # Mistakes to avoid - Not bold
        self.BLACK = (0, 0, 0)             # Regular text
        self.WHITE_BG = (255, 255, 255)    # WHITE BACKGROUND
        
    def header(self):
        # WHITE background
        self.set_fill_color(255, 255, 255)
        self.rect(0, 0, 210, 15, 'F')
        
        self.set_font('DejaVu', 'B', 11)
        self.set_text_color(0, 0, 0)
        self.set_xy(10, 5)
        self.cell(0, 5, 'Prize2Pride German Course | Professor Roued', 0, 0, 'L')
        self.ln(15)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f'The Adventures of Mr. Iheb | Page {self.page_no()}', 0, 0, 'C')
        
    def title_page(self):
        self.add_page()
        # WHITE background
        self.set_fill_color(255, 255, 255)
        self.rect(0, 15, 210, 282, 'F')
        
        self.set_y(40)
        self.set_font('DejaVu', 'B', 36)
        self.set_text_color(*self.DARK_RED)
        self.cell(0, 15, 'Das Wetter', 0, 1, 'C')
        
        self.set_font('DejaVu', 'B', 18)
        self.set_text_color(0, 0, 0)
        self.cell(0, 12, 'The Weather', 0, 1, 'C')
        
        self.set_font('DejaVu', '', 14)
        self.set_text_color(*self.DARK_BLUE)
        self.cell(0, 10, 'الطقس', 0, 1, 'C')
        
        self.ln(10)
        self.set_font('DejaVu', 'B', 18)
        self.set_text_color(*self.DARK_BLUE)
        self.cell(0, 12, 'The Adventures of Mr. Iheb', 0, 1, 'C')
        
        self.set_font('DejaVu', '', 12)
        self.set_text_color(*self.DARK_RED)
        self.cell(0, 10, 'مغامرات السيد إيهاب', 0, 1, 'C')
        
        self.ln(10)
        self.set_font('DejaVu', '', 11)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 8, 'A Winter Day in Tunisia with All Kinds of Weather', 0, 'C')
        
        self.set_font('DejaVu', '', 11)
        self.set_text_color(*self.DARK_RED)
        self.multi_cell(0, 8, 'يوم شتوي في تونس مع جميع أنواع الطقس', 0, 'C')
        
        self.ln(15)
        self.set_font('DejaVu', 'B', 13)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'Three Learning Modes:', 0, 1, 'C')
        
        self.set_font('DejaVu', '', 11)
        self.set_text_color(*self.DARK_RED)
        self.cell(0, 8, '1. Informal (Casual German)', 0, 1, 'C')
        self.set_text_color(*self.DARK_BLUE)
        self.cell(0, 8, '2. Formal (Professional German)', 0, 1, 'C')
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, '3. Comedy (Hilarious German)', 0, 1, 'C')
        
        self.ln(15)
        self.set_font('DejaVu', 'B', 13)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, 'Instructor: Professor Roued', 0, 1, 'C')
        
        # Color legend
        self.ln(12)
        self.set_font('DejaVu', 'B', 10)
        self.set_text_color(0, 0, 0)
        self.cell(0, 8, 'Color Guide:', 0, 1, 'C')
        
        self.set_font('DejaVu', 'B', 9)
        self.set_text_color(*self.DARK_RED)
        self.cell(0, 6, 'Dark Red Bold = Important Expressions', 0, 1, 'C')
        self.set_text_color(*self.DARK_BLUE)
        self.cell(0, 6, 'Dark Blue Bold = Grammar & Formal', 0, 1, 'C')
        self.set_font('DejaVu', '', 9)
        self.set_text_color(*self.LIGHT_RED)
        self.cell(0, 6, 'Light Red = Mistakes to Avoid', 0, 1, 'C')

    def section_title(self, title, color='dark_red'):
        self.ln(4)
        if color == 'dark_red':
            self.set_text_color(*self.DARK_RED)
        elif color == 'dark_blue':
            self.set_text_color(*self.DARK_BLUE)
        else:
            self.set_text_color(0, 0, 0)
        self.set_font('DejaVu', 'B', 13)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(2)
        
    def important_text(self, text):
        """Dark Red Bold - Important expressions"""
        self.set_font('DejaVu', 'B', 10)
        self.set_text_color(*self.DARK_RED)
        self.multi_cell(0, 6, text)
        
    def formal_text(self, text):
        """Dark Blue Bold - Formal/Grammar"""
        self.set_font('DejaVu', 'B', 10)
        self.set_text_color(*self.DARK_BLUE)
        self.multi_cell(0, 6, text)
        
    def mistake_text(self, text):
        """Light Red Not Bold - Mistakes to avoid"""
        self.set_font('DejaVu', '', 9)
        self.set_text_color(*self.LIGHT_RED)
        self.multi_cell(0, 5, text)
        
    def normal_text(self, text):
        """Black regular text"""
        self.set_font('DejaVu', '', 9)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, text)
        
    def arabic_text(self, text):
        """Arabic translation - Right-to-Left"""
        self.set_font('DejaVu', '', 9)
        self.set_text_color(0, 0, 0)
        # Arabic text is naturally RTL in Unicode
        self.multi_cell(0, 5, text, 0, 'R')
        
    def vocab_table(self, data, headers):
        self.set_font('DejaVu', 'B', 8)
        self.set_fill_color(200, 200, 200)
        self.set_text_color(0, 0, 0)
        
        col_width = 190 / len(headers)
        for header in headers:
            self.cell(col_width, 7, header, 1, 0, 'C', True)
        self.ln()
        
        self.set_font('DejaVu', '', 8)
        fill = False
        for row in data:
            if fill:
                self.set_fill_color(240, 240, 240)
            else:
                self.set_fill_color(255, 255, 255)
            
            for i, cell in enumerate(row):
                if i == 0:  # German word - Dark Red Bold
                    self.set_font('DejaVu', 'B', 8)
                    self.set_text_color(*self.DARK_RED)
                else:
                    self.set_font('DejaVu', '', 8)
                    self.set_text_color(0, 0, 0)
                self.cell(col_width, 6, cell, 1, 0, 'C', True)
            self.ln()
            fill = not fill
        self.ln(4)

def create_iheb_lesson_corrected():
    pdf = IhebWeatherPDFCorrected()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # Title Page
    pdf.title_page()
    
    # ==================== VOCABULARY PAGE ====================
    pdf.add_page()
    pdf.section_title('Weather Vocabulary', 'dark_red')
    
    vocab = [
        ['das Wetter', 'the weather', 'الطقس'],
        ['die Sonne', 'the sun', 'الشمس'],
        ['der Regen', 'the rain', 'المطر'],
        ['der Schnee', 'the snow', 'الثلج'],
        ['der Wind', 'the wind', 'الرياح'],
        ['die Wolke', 'the cloud', 'السحابة'],
        ['der Nebel', 'the fog', 'الضباب'],
        ['das Gewitter', 'thunderstorm', 'العاصفة الرعدية'],
        ['der Blitz', 'lightning', 'البرق'],
        ['der Donner', 'thunder', 'الرعد'],
        ['der Hagel', 'hail', 'البرد'],
        ['der Sturm', 'storm', 'العاصفة'],
    ]
    pdf.vocab_table(vocab, ['German', 'English', 'Arabic'])
    
    pdf.section_title('Weather Expressions', 'dark_blue')
    
    expressions = [
        ['Es ist sonnig', 'It is sunny', 'الجو مشمس'],
        ['Es regnet', 'It is raining', 'إنها تمطر'],
        ['Es schneit', 'It is snowing', 'إنها تثلج'],
        ['Es ist windig', 'It is windy', 'الجو عاصف'],
        ['Es ist bewolkt', 'It is cloudy', 'الجو غائم'],
        ['Es ist neblig', 'It is foggy', 'الجو ضبابي'],
        ['Es ist heiss', 'It is hot', 'الجو حار'],
        ['Es ist kalt', 'It is cold', 'الجو بارد'],
        ['Es ist warm', 'It is warm', 'الجو دافئ'],
        ['Es ist kuhl', 'It is cool', 'الجو منعش'],
    ]
    pdf.vocab_table(expressions, ['German', 'English', 'Arabic'])
    
    # ==================== PART 1: INFORMAL ====================
    pdf.add_page()
    pdf.section_title('PART 1: INFORMAL - The Adventures of Mr. Iheb', 'dark_red')
    pdf.arabic_text('الجزء الأول: غير رسمي - مغامرات السيد إيهاب')
    pdf.ln(3)
    
    pdf.normal_text('It was a crazy winter morning in Tunis. Mr. Iheb woke up and looked out the window.')
    pdf.arabic_text('كان صباحاً شتوياً مجنوناً في تونس. استيقظ السيد إيهاب ونظر من النافذة.')
    pdf.ln(2)
    
    pdf.important_text('Herr Iheb wachte auf und schaute aus dem Fenster.')
    pdf.normal_text('(Mr. Iheb woke up and looked out the window.)')
    pdf.arabic_text('استيقظ السيد إيهاب ونظر من النافذة.')
    pdf.ln(2)
    
    pdf.important_text('"Mensch! Was fur ein Wetter heute!"')
    pdf.normal_text('("Man! What kind of weather today!")')
    pdf.arabic_text('"يا رجل! يا له من طقس اليوم!"')
    pdf.ln(2)
    
    pdf.normal_text('The sun was shining brightly when he left his house in La Marsa.')
    pdf.important_text('Die Sonne schien hell, als er sein Haus in La Marsa verliess.')
    pdf.arabic_text('كانت الشمس تشرق بشكل ساطع عندما غادر منزله في المرسى.')
    pdf.ln(2)
    
    pdf.important_text('"Super! Es ist sonnig! Perfektes Wetter fur einen Spaziergang!"')
    pdf.normal_text('("Great! It is sunny! Perfect weather for a walk!")')
    pdf.arabic_text('"رائع! الجو مشمس! طقس مثالي للتنزه!"')
    pdf.ln(2)
    
    pdf.normal_text('But after only 10 minutes, dark clouds appeared.')
    pdf.important_text('Aber nach nur zehn Minuten kamen dunkle Wolken.')
    pdf.arabic_text('لكن بعد عشر دقائق فقط، ظهرت سحب داكنة.')
    pdf.ln(2)
    
    pdf.important_text('"Oh nein! Es wird bewolkt! Das sieht nicht gut aus!"')
    pdf.normal_text('("Oh no! It is getting cloudy! That does not look good!")')
    pdf.arabic_text('"أوه لا! الجو يصبح غائماً! هذا لا يبدو جيداً!"')
    pdf.ln(2)
    
    pdf.normal_text('Suddenly, it started to rain heavily!')
    pdf.important_text('Plotzlich fing es an, stark zu regnen!')
    pdf.arabic_text('فجأة، بدأت تمطر بغزارة!')
    pdf.ln(2)
    
    pdf.important_text('"Mist! Es regnet! Ich habe keinen Regenschirm!"')
    pdf.normal_text('("Damn! It is raining! I have no umbrella!")')
    pdf.arabic_text('"تباً! إنها تمطر! ليس لدي مظلة!"')
    pdf.ln(3)
    
    # Mistakes to avoid
    pdf.section_title('Mistakes to Avoid', 'dark_red')
    pdf.mistake_text('WRONG: "Das Wetter regnet" - Weather does not rain!')
    pdf.mistake_text('CORRECT: "Es regnet" - It rains (impersonal)')
    pdf.arabic_text('خطأ: "الطقس يمطر" - الطقس لا يمطر!')
    pdf.arabic_text('صحيح: "إنها تمطر" - صيغة غير شخصية')
    pdf.ln(2)
    pdf.mistake_text('WRONG: "Ich bin kalt" - This means you are a cold person!')
    pdf.mistake_text('CORRECT: "Mir ist kalt" - I feel cold')
    pdf.arabic_text('خطأ: "أنا بارد" - هذا يعني أنك شخص بارد!')
    pdf.arabic_text('صحيح: "أشعر بالبرد" - I feel cold')
    
    # ==================== PART 1 CONTINUED ====================
    pdf.add_page()
    pdf.section_title('Mr. Iheb\'s Adventure Continues...', 'dark_red')
    
    pdf.normal_text('Mr. Iheb ran to a cafe to escape the rain. He ordered a hot coffee.')
    pdf.important_text('Herr Iheb rannte in ein Cafe, um dem Regen zu entkommen. Er bestellte einen heissen Kaffee.')
    pdf.arabic_text('ركض السيد إيهاب إلى مقهى للهروب من المطر. طلب قهوة ساخنة.')
    pdf.ln(2)
    
    pdf.important_text('"Ein heisser Kaffee, bitte! Draussen ist es so kalt!"')
    pdf.normal_text('("A hot coffee, please! Outside it is so cold!")')
    pdf.arabic_text('"قهوة ساخنة، من فضلك! الجو بارد جداً في الخارج!"')
    pdf.ln(2)
    
    pdf.normal_text('While drinking his coffee, the wind started blowing strongly.')
    pdf.important_text('Wahrend er seinen Kaffee trank, begann der Wind stark zu wehen.')
    pdf.arabic_text('بينما كان يشرب قهوته، بدأت الرياح تهب بقوة.')
    pdf.ln(2)
    
    pdf.important_text('"Wow! Es ist sehr windig! Die Baume biegen sich!"')
    pdf.normal_text('("Wow! It is very windy! The trees are bending!")')
    pdf.arabic_text('"واو! الجو عاصف جداً! الأشجار تنحني!"')
    pdf.ln(2)
    
    pdf.normal_text('Then something incredible happened - it started to snow!')
    pdf.important_text('Dann passierte etwas Unglaubliches - es begann zu schneien!')
    pdf.arabic_text('ثم حدث شيء لا يصدق - بدأت تثلج!')
    pdf.ln(2)
    
    pdf.important_text('"Was?! Es schneit?! In Tunesien?! Das ist veruckt!"')
    pdf.normal_text('("What?! It is snowing?! In Tunisia?! That is crazy!")')
    pdf.arabic_text('"ماذا؟! إنها تثلج؟! في تونس؟! هذا جنون!"')
    pdf.ln(2)
    
    pdf.normal_text('Mr. Iheb took photos with his phone. Nobody would believe him!')
    pdf.important_text('Herr Iheb machte Fotos mit seinem Handy. Niemand wurde ihm glauben!')
    pdf.arabic_text('التقط السيد إيهاب صوراً بهاتفه. لن يصدقه أحد!')
    pdf.ln(2)
    
    pdf.important_text('"Ich muss Fotos machen! Das ist historisch!"')
    pdf.normal_text('("I must take photos! This is historic!")')
    pdf.arabic_text('"يجب أن ألتقط صوراً! هذا تاريخي!"')
    pdf.ln(2)
    
    pdf.normal_text('After 20 minutes, the snow stopped and fog appeared.')
    pdf.important_text('Nach zwanzig Minuten horte der Schnee auf und Nebel erschien.')
    pdf.arabic_text('بعد عشرين دقيقة، توقف الثلج وظهر الضباب.')
    pdf.ln(2)
    
    pdf.important_text('"Jetzt ist es neblig! Ich kann nichts sehen!"')
    pdf.normal_text('("Now it is foggy! I cannot see anything!")')
    pdf.arabic_text('"الآن الجو ضبابي! لا أستطيع رؤية أي شيء!"')
    
    # ==================== PART 2: FORMAL ====================
    pdf.add_page()
    pdf.section_title('PART 2: FORMAL - The Adventures of Mr. Iheb', 'dark_blue')
    pdf.arabic_text('الجزء الثاني: رسمي - مغامرات السيد إيهاب')
    pdf.ln(3)
    
    pdf.formal_text('Sehr geehrte Damen und Herren, ich mochte Ihnen von meinem aussergewohnlichen Tag berichten.')
    pdf.normal_text('(Dear ladies and gentlemen, I would like to report about my extraordinary day.)')
    pdf.arabic_text('سيداتي وسادتي الأعزاء، أود أن أخبركم عن يومي الاستثنائي.')
    pdf.ln(2)
    
    pdf.formal_text('Am Morgen des 15. Januar erwachte ich in meiner Residenz in La Marsa, Tunesien.')
    pdf.normal_text('(On the morning of January 15th, I awoke in my residence in La Marsa, Tunisia.)')
    pdf.arabic_text('في صباح الخامس عشر من يناير، استيقظت في مقر إقامتي في المرسى، تونس.')
    pdf.ln(2)
    
    pdf.formal_text('Die meteorologischen Bedingungen waren zunachst ausserordentlich gunstig.')
    pdf.normal_text('(The meteorological conditions were initially extraordinarily favorable.)')
    pdf.arabic_text('كانت الظروف الجوية في البداية مواتية للغاية.')
    pdf.ln(2)
    
    pdf.formal_text('Die Sonne schien mit einer Intensitat von ungefahr 800 Watt pro Quadratmeter.')
    pdf.normal_text('(The sun was shining with an intensity of approximately 800 watts per square meter.)')
    pdf.arabic_text('كانت الشمس تشرق بشدة تقارب 800 واط لكل متر مربع.')
    pdf.ln(2)
    
    pdf.formal_text('Jedoch anderten sich die Wetterbedingungen innerhalb kurzer Zeit dramatisch.')
    pdf.normal_text('(However, the weather conditions changed dramatically within a short time.)')
    pdf.arabic_text('ومع ذلك، تغيرت الظروف الجوية بشكل كبير في وقت قصير.')
    pdf.ln(2)
    
    pdf.formal_text('Es kam zu erheblichen Niederschlagen, gefolgt von starken Windböen.')
    pdf.normal_text('(There was significant precipitation, followed by strong wind gusts.)')
    pdf.arabic_text('حدث هطول كبير، تلته رياح عاتية.')
    pdf.ln(2)
    
    pdf.formal_text('Zu meiner grossen Uberraschung begann es anschliessend zu schneien.')
    pdf.normal_text('(To my great surprise, it subsequently began to snow.)')
    pdf.arabic_text('ولدهشتي الكبيرة، بدأت تتساقط الثلوج بعد ذلك.')
    pdf.ln(2)
    
    pdf.formal_text('Dieses Phanomen ist in Tunesien ausserst selten und bemerkenswert.')
    pdf.normal_text('(This phenomenon is extremely rare and remarkable in Tunisia.)')
    pdf.arabic_text('هذه الظاهرة نادرة للغاية وملفتة للنظر في تونس.')
    
    # ==================== PART 3: COMEDY ====================
    pdf.add_page()
    pdf.section_title('PART 3: COMEDY - The Adventures of Mr. Iheb', 'dark_red')
    pdf.arabic_text('الجزء الثالث: كوميدي - مغامرات السيد إيهاب')
    pdf.ln(3)
    
    pdf.important_text('Herr Iheb wachte auf und dachte: "Was fur ein schoner Tag!"')
    pdf.normal_text('(Mr. Iheb woke up and thought: "What a beautiful day!")')
    pdf.arabic_text('استيقظ السيد إيهاب وفكر: "يا له من يوم جميل!"')
    pdf.ln(2)
    
    pdf.important_text('Funf Minuten spater: "Warum regnet es auf meinen Kopf?!"')
    pdf.normal_text('(Five minutes later: "Why is it raining on my head?!")')
    pdf.arabic_text('بعد خمس دقائق: "لماذا تمطر على رأسي؟!"')
    pdf.ln(2)
    
    pdf.important_text('Zehn Minuten spater: "Ist das... SCHNEE?! In TUNESIEN?!"')
    pdf.normal_text('(Ten minutes later: "Is that... SNOW?! In TUNISIA?!")')
    pdf.arabic_text('بعد عشر دقائق: "هل هذا... ثلج؟! في تونس؟!"')
    pdf.ln(2)
    
    pdf.important_text('Herr Iheb rief seine Mutter an:')
    pdf.normal_text('(Mr. Iheb called his mother:)')
    pdf.arabic_text('اتصل السيد إيهاب بأمه:')
    pdf.ln(1)
    
    pdf.important_text('"Mama! Es schneit!"')
    pdf.important_text('"Iheb, hast du wieder zu viel Kaffee getrunken?"')
    pdf.important_text('"Nein Mama, ich schwore! Es schneit wirklich!"')
    pdf.important_text('"Mein Sohn ist veruckt geworden..."')
    pdf.ln(2)
    
    pdf.normal_text('(Mom! It is snowing! / Iheb, did you drink too much coffee again? / No Mom, I swear! It is really snowing! / My son has gone crazy...)')
    pdf.arabic_text('ماما! إنها تثلج! / إيهاب، هل شربت الكثير من القهوة مرة أخرى؟ / لا ماما، أقسم! إنها تثلج حقاً! / ابني أصبح مجنوناً...')
    pdf.ln(2)
    
    pdf.important_text('Dann kam der Nebel. Herr Iheb konnte seine eigene Nase nicht sehen!')
    pdf.normal_text('(Then came the fog. Mr. Iheb could not see his own nose!)')
    pdf.arabic_text('ثم جاء الضباب. لم يستطع السيد إيهاب رؤية أنفه!')
    pdf.ln(2)
    
    pdf.important_text('"Hallo? Ist da jemand? Ich bin verloren... in meinem eigenen Garten!"')
    pdf.normal_text('("Hello? Is anyone there? I am lost... in my own garden!")')
    pdf.arabic_text('"مرحباً؟ هل من أحد هناك؟ أنا ضائع... في حديقتي الخاصة!"')
    
    # ==================== SUMMARY PAGE ====================
    pdf.add_page()
    pdf.section_title('Lesson Summary', 'dark_blue')
    
    pdf.formal_text('Key Vocabulary Learned:')
    pdf.normal_text('• das Wetter (weather), die Sonne (sun), der Regen (rain)')
    pdf.normal_text('• der Schnee (snow), der Wind (wind), die Wolke (cloud)')
    pdf.normal_text('• der Nebel (fog), das Gewitter (thunderstorm)')
    pdf.ln(2)
    
    pdf.formal_text('Key Expressions Learned:')
    pdf.normal_text('• Es ist sonnig/bewolkt/windig/neblig (It is sunny/cloudy/windy/foggy)')
    pdf.normal_text('• Es regnet/schneit (It is raining/snowing)')
    pdf.normal_text('• Es ist heiss/kalt/warm (It is hot/cold/warm)')
    pdf.ln(2)
    
    pdf.section_title('Common Mistakes to Avoid', 'dark_red')
    pdf.mistake_text('1. "Das Wetter regnet" → WRONG! Use "Es regnet"')
    pdf.mistake_text('2. "Ich bin kalt" → WRONG! Use "Mir ist kalt"')
    pdf.mistake_text('3. "Es ist sonnig Wetter" → WRONG! Use "Es ist sonnig"')
    pdf.mistake_text('4. "Der Wetter" → WRONG! Weather is neutral: "das Wetter"')
    pdf.ln(3)
    
    pdf.formal_text('Congratulations! You have completed the Weather lesson!')
    pdf.arabic_text('تهانينا! لقد أكملت درس الطقس!')
    pdf.ln(2)
    pdf.normal_text('Prize2Pride German Course | Professor Roued')
    pdf.normal_text('The Adventures of Mr. Iheb - A Winter Day in Tunisia')
    
    # Save PDF
    output_path = '/home/ubuntu/German-A1-/lessons/07-weather/Prize2Pride_MrIheb_Weather_Corrected.pdf'
    pdf.output(output_path)
    print(f'PDF created: {output_path}')
    return output_path

if __name__ == '__main__':
    create_iheb_lesson_corrected()
    print('Mr. Iheb Weather Lesson PDF (CORRECTED) generated successfully!')
