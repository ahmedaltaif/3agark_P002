import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper
from django.conf import settings
from reportlab.lib.colors import HexColor
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
import re

# تسجيل خط العربي
FONT_PATH = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Noto_Naskh_Arabic', 'NotoNaskhArabic-VariableFont_wght.ttf')
pdfmetrics.registerFont(TTFont('NotoNaskhArabic', FONT_PATH))

class PDFGenerator:
    def __init__(self, contract, terms_list):
        self.contract = contract
        self.terms_list = terms_list
        self.width, self.height = A4
        self.primary_color = HexColor('#fe7a36')
        self.bg_color = HexColor('#f8f9fa')
        self.margin = 50
        self.current_y = self.height - self.margin
        self.page_number = 1
        
        # إنشاء ملف PDF
        self.output_path = os.path.join(settings.MEDIA_ROOT, f'contract_{contract.contract_num}.pdf')
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        self.c = canvas.Canvas(self.output_path, pagesize=A4)
        self.setup_styles()
    
    def setup_styles(self):
        """إعداد أنماط الفقرات المستخدمة في المستند"""
        self.title_style = ParagraphStyle(
            name='TitleStyle',
            fontName='NotoNaskhArabic',
            fontSize=30,
            alignment=1,  # TA_CENTER = 1
            textColor=self.primary_color
        )
        # باقي الأنماط تظل كما هي

        
        self.section_style = ParagraphStyle(
            name='SectionStyle',
        fontName='NotoNaskhArabic',
            fontSize=16,
        alignment=TA_RIGHT,
            textColor=self.primary_color
        )
        self.notes_style = ParagraphStyle(
            name='NotesStyle',
        fontName='NotoNaskhArabic',
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,
        rightIndent=15,
        leftIndent=15,
        spaceAfter=8,
        textColor=colors.black,
            backColor=self.bg_color
        )
        
        self.detail_style = ParagraphStyle(
            name='DetailStyle',
        fontName='NotoNaskhArabic',
        fontSize=12,
        leading=16,
        alignment=TA_RIGHT,
        rightIndent=10,
        leftIndent=10,
            textColor=colors.black
        )
        
        self.term_style = ParagraphStyle(
            name='TermStyle',
        fontName='NotoNaskhArabic',
        fontSize=12,
        leading=18,
        alignment=TA_RIGHT,
        rightIndent=15,
        leftIndent=15,
            spaceAfter=8,
            textColor=colors.black
        )
    
    def reshape_arabic(self, text):
        """معالجة النص العربي للعرض الصحيح"""
        try:
            reshaped_text = arabic_reshaper.reshape(str(text))
            return get_display(reshaped_text)
        except:
            return str(text)
    
    def add_page_border(self):
        """إضافة إطار للصفحة"""
        self.c.setStrokeColor(self.primary_color)
        self.c.setLineWidth(2)
        self.c.rect(30, 30, self.width - 60, self.height - 60)
    
    def add_page_number(self):
        """إضافة رقم الصفحة"""
        text = self.reshape_arabic(f"صفحة {self.page_number}")
        self.c.saveState()
        self.c.setFont('NotoNaskhArabic', 9)
        self.c.setFillColor(colors.black)
        text_width = self.c.stringWidth(text, 'NotoNaskhArabic', 9)
        self.c.drawString((self.width - text_width) / 2, 35, text)
        self.c.restoreState()
    
    def add_logo(self):
        """إضافة الشعار إذا وجد"""
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'admin', 'assets', 'images', 'logo.png')
        if os.path.exists(logo_path):
            self.c.drawImage(logo_path, self.width / 2 - 60, self.current_y - 60, width=120, height=60, mask='auto')
            self.current_y -= 80
    
    def add_title(self):
        """إضافة عنوان العقد في منتصف الصفحة أسفل الشعار مباشرة"""
        # إنشاء فقرة العنوان
        title_text = self.reshape_arabic("عقد إيجار")
        title = Paragraph(title_text, self.title_style)

        # حساب أبعاد العنوان بدقة
        title_width, title_height = title.wrap(self.width - 2 * self.margin, self.height)

        # حساب الموضع الأفقي (التوسيط الكامل)
        x_position = (self.width - title_width) / 2

        # حساب الموضع الرأسي (أسفل الشعار مباشرة بمسافة 30 نقطة)
        y_position = self.current_y - 1  # بعد إضافة الشعار وتحديث current_y

        # رسم العنوان في الموضع المحسوب
        title.drawOn(self.c, x_position, y_position)

        # إضافة خط تحت العنوان بمسافة 10 نقاط
        underline_y = y_position - 30
        self.c.setStrokeColor(self.primary_color)
        self.c.setLineWidth(1)
        self.c.line(x_position, underline_y, x_position + title_width, underline_y)

        # تحديث الموضع الحالي ليكون أسفل الخط بمسافة 40 نقطة
        self.current_y = underline_y - 40


    
    def add_section(self, title):
        """إضافة قسم جديد مع خط أسفل العنوان بمسافة مناسبة"""
        if self.current_y < 150:  # إذا لم يتبق مساحة كافية
            self.add_new_page()

        # إنشاء الفقرة وحساب أبعادها
        section = Paragraph(self.reshape_arabic(title), self.section_style)
        section_width, section_height = section.wrap(self.width - 100, self.height)

        # حساب الموضع الرأسي مع مراعاة ارتفاع النص
        text_y_position = self.current_y - section_height + 5 # تعديل موضع النص

        # رسم عنوان القسم
        section.drawOn(self.c, self.width - section_width - self.margin, text_y_position)

        # إضافة خط تحت العنوان بمسافة 8 نقاط من أسفل النص
        line_y_position = text_y_position - 10
        self.c.setStrokeColor(self.primary_color)
        self.c.setLineWidth(1)
        self.c.line(
            self.width - section_width - self.margin, 
            line_y_position,
            self.width - self.margin, 
            line_y_position
        )

        # تحديث الموضع الرأسي مع ترك مسافة إضافية بعد القسم
        self.current_y = line_y_position - 2  # مسافة 15 نقطة بعد الخط
        self.current_y -= 30
    
    def add_details(self, details):
        """إضافة تفاصيل القسم"""
        # حساب المساحة المطلوبة
        paragraphs = [Paragraph(self.reshape_arabic(detail), self.detail_style) for detail in details]
        total_height = sum(p.wrap(self.width - 2 * self.margin, self.height)[1] for p in paragraphs)
        
        # التحقق من المساحة المتاحة
        if self.current_y - total_height - 20 < self.margin:
            self.add_new_page()
        
        # رسم خلفية التفاصيل
        self.c.setFillColor(self.bg_color)
        self.c.rect(self.margin, self.current_y - total_height - 10, 
                    self.width - 2 * self.margin, total_height + 10, fill=1, stroke=0)
        self.c.setFillColor(colors.black)
        
        # إضافة التفاصيل
        frame = Frame(self.margin, self.current_y - total_height - 10, 
                     self.width - 2 * self.margin, total_height + 10, showBoundary=0)
        frame.addFromList(paragraphs, self.c)
        
        self.current_y -= (total_height + 40)

    def add_notes(self):
        if not self.contract.notes or not self.contract.notes.strip():
            return
    
        if self.current_y < 150:
            self.add_new_page()
    
        self.add_section("الملاحظات")
    
        # تقسيم يدوي حسب الفاصلة أو النقطة
        lines = re.split(r'(،|\.)', self.contract.notes)
        
        # تجميع الجمل الكاملة بعد الفصل
        sentences = []
        temp = ""
        for part in lines:
            temp += part
            if part in ["،", "."]:
                sentences.append(temp.strip())
                temp = ""
        if temp.strip():
            sentences.append(temp.strip())
    
        # إنشاء الفقرات
        paragraphs = [
            Paragraph(self.reshape_arabic(f"• {sentence}"), self.notes_style)
            for sentence in sentences if sentence.strip()
        ]
    
        while paragraphs:
            frame_height = self.current_y - self.margin - 20
            frame = Frame(
                self.margin,
                self.margin + 10,
                self.width - 2 * self.margin,
                frame_height,
                showBoundary=0
            )
            paragraphs = frame.addFromList(paragraphs, self.c)
            self.current_y = self.margin + 20
            if paragraphs:
                self.add_new_page()
                self.add_section("الملاحظات (تابع)")


    
    def add_terms(self):
        """إضافة شروط العقد مع دعم الانتقال التلقائي بين الصفحات"""
        # التحقق مما إذا كنا في بداية صفحة جديدة
        if self.current_y == self.height - self.margin:
            self.add_section("شروط العقد")
        else:
            # إذا لم تكن بداية صفحة، نضيف عنوان "شروط العقد (تابع)"
            self.add_section("شروط العقد (تابع)")

        # إعداد إطار للشروط مع مساحة أكبر
        frame_width = self.width - 2 * self.margin
        frame_height = self.current_y - self.margin - 20  # ترك مساحة للتوقيعات

        # إنشاء قائمة الفقرات
        paragraphs = []
        for term in self.terms_list:
            # معالجة كل شرط كفقرة منفصلة
            p = Paragraph(self.reshape_arabic(term), self.term_style)
            paragraphs.append(p)

        # إنشاء الإطار وإضافة الفقرات
        frame = Frame(
            self.margin, 
            self.margin + 10,  # ترك مساحة للتوقيعات في الأسفل
            frame_width, 
            frame_height,
            leftPadding=0,
            rightPadding=0,
            topPadding=0,
            bottomPadding=0,
            showBoundary=0
        )

        # محاولة إضافة كل الفقرات
        remaining_paragraphs = frame.addFromList(paragraphs, self.c)

        # إذا بقي هناك فقرات لم يتم عرضها
        while remaining_paragraphs:
            self.add_new_page()
            self.add_section("شروط العقد (تابع)")

            # إعادة حساب ارتفاع الإطار للصفحة الجديدة
            frame_height = self.current_y - self.margin - 20

            frame = Frame(
                self.margin, 
                self.margin + 20,
                frame_width, 
                frame_height,
                leftPadding=0,
                rightPadding=0,
                topPadding=0,
                bottomPadding=0,
                showBoundary=0
            )

            remaining_paragraphs = frame.addFromList(remaining_paragraphs, self.c)

        # تحديث الموضع الحالي بعد إضافة الشروط
        self.current_y = self.margin + 20
    

    
    def add_signatures(self):
        """إضافة قسم التوقيعات"""
        if self.current_y < 150:
            self.add_new_page()
        
        self.add_section("التوقيعات")
        
        # إضافة خلفية قسم التوقيعات
        self.c.setFillColor(self.bg_color)
        self.c.rect(self.margin, self.current_y - 60, self.width - 2 * self.margin, 60, fill=1, stroke=0)
        self.c.setFillColor(colors.black)
        
        # إضافة نص التوقيع
        signature_text = self.reshape_arabic("المستأجر")
        self.c.setFont('NotoNaskhArabic', 12)
        text_width = self.c.stringWidth(signature_text, 'NotoNaskhArabic', 12)
        self.c.drawString(3 * self.width / 4 - text_width / 2, self.current_y - 40, signature_text)
        
        self.current_y -= 100
    
    def add_new_page(self):
        """إضافة صفحة جديدة"""
        self.c.showPage()
        self.page_number += 1
        self.current_y = self.height - self.margin
        self.add_page_border()
        self.add_page_number()
    
    def generate(self):
        """إنشاء ملف PDF"""
        # Debug print for notes
        print(f"Contract notes value: {self.contract.notes}")
        
        # الصفحة الأولى
        self.add_page_border()
        self.add_page_number()
        self.add_logo()
        self.add_title()
        
        # معلومات العقد
        self.add_section("معلومات العقد")
        contract_details = [
            f"رقم العقد: {self.contract.contract_num}",
            f"تاريخ الإصدار: {self.contract.issue_date}",
            f"تاريخ الدخول: {self.contract.checkin_date}",
            f"مدة العقد: {self.contract.duration_days} يوم",
            f"سعر الإيجار: {self.contract.rent_price} SDG",
            f"طريقة الدفع: {self.contract.payment_method}"
        ]
        self.add_details(contract_details)
        
        # معلومات المستأجر
        self.add_section("معلومات المستأجر")
        tenant_details = [
            f"الاسم: {self.contract.tenant.full_name}",
            f"رقم الهاتف: {self.contract.tenant.tenant_numer}",
            f"نوع الهوية: {self.contract.tenant.id_type}",
            f"رقم الهوية: {self.contract.tenant.id_number}",
            f"هوية المستأجر: {self.contract.tenant.id_number}"
        ]
        self.add_details(tenant_details)
        
        # إضافة الملاحظات
        self.add_notes()
        
        # الانتقال للصفحة الثانية لشروط العقد
        self.add_new_page()
        self.add_terms()
        
        # التوقيعات
        if self.current_y < 200:  # إذا لم يتبق مساحة كافية للتوقيعات
            self.add_new_page()
        self.add_signatures()
        
        # حفظ الملف
        self.c.save()
        return self.output_path


# دالة الاستدعاء الرئيسية
def generate_contract_pdf(contract, terms_list):
    generator = PDFGenerator(contract, terms_list)
    return generator.generate()