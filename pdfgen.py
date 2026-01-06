from reportlab.graphics import renderPDF
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Flowable, Indenter, Paragraph, Table

pdfmetrics.registerFont(TTFont('OpenSansR', 'fonts/OpenSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('OpenSansL', 'fonts/OpenSans-Light.ttf'))
pdfmetrics.registerFont(TTFont('OpenSansB', 'fonts/OpenSans-Bold.ttf'))
pdfmetrics.registerFont(TTFont('OpenSansI', 'fonts/OpenSans-Italic.ttf'))
pdfmetrics.registerFont(TTFont('OpenSansBI', 'fonts/OpenSans-BoldItalic.ttf'))
registerFontFamily('OpenSans', normal='OpenSansR', bold='OpenSansB', italic='OpenSansI', boldItalic='OpenSansBI')
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER
from svglib.svglib import svg2rlg

FontSize = 9
TextFieldLabelSizeAdjust = 0.60

style = ParagraphStyle(
    name='Normal',
    fontName='OpenSansR',
    fontSize=FontSize,
)
spacer = ParagraphStyle(
    name='Normal',
    fontName='OpenSansR',
    spaceAfter=1,
)
spacer_s = ParagraphStyle(
    name='Normal',
    fontName='OpenSansR',
    spaceAfter=0,
    fontSize=FontSize/2,
)
spacer2 = ParagraphStyle(
    name='Normal',
    fontName='OpenSansR',
    spaceBefore=6,
    spaceAfter=6,
)
title = ParagraphStyle(name='Title',
                       parent=style,
                       fontSize=FontSize + 8,
                       fontName='OpenSansBI',
                       leading=17,
                       alignment=TA_CENTER,
                       spaceAfter=3)
subtitle = ParagraphStyle(name='SubTitle',
                          parent=style,
                          fontSize=FontSize + 2,
                          fontName='OpenSansBI',
                          # leading=22,
                          # alignment=TA_CENTER,
                          spaceAfter=6)
small = ParagraphStyle(name='Small',
                       parent=style,
                       fontSize=FontSize - 3,
                       fontName='OpenSansR',
                       spaceBefore=3,
                       leading=8,
                       spaceAfter=0)
indent18 = Indenter(left=18)
dedent18 = Indenter(left=-18)


class TextField(Flowable):
    def __init__(self, **options):
        Flowable.__init__(self)
        self.options = options
        # Use Reportlab's default size if not user provided
        self.width = options.get('width', 0)
        self.height = 0

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        x, y = self.canv.absolutePosition(0, 0)
        self.options['y'] = y - FontSize
        self.options['fillColor'] = colors.white
        self.options['borderWidth'] = 0.25
        if 'offset' in self.options:
            self.options['x'] = x + self.options['offset']
            del self.options['offset']
        form.textfield(**self.options)
        self.canv.restoreState()


class CheckBox(Flowable):
    def __init__(self, **options):
        Flowable.__init__(self)
        self.options = options
        # Use Reportlab's default size if not user provided
        self.width = options.get('width', 0)
        self.height = options.get('height', 0)
        self.options['fillColor'] = colors.white
        self.options['borderWidth'] = 0.25
        if 'width' in options:
            del options['width']
        if 'height' in options:
            del options['height']

    def draw(self):
        self.canv.saveState()
        form = self.canv.acroForm
        x, y = self.canv.absolutePosition(0, 0)
        self.options['y'] = y - FontSize * 0.8
        self.options['size'] = FontSize * 1.2
        self.options['shape'] = 'square'
        self.options['buttonStyle'] = 'cross'
        if 'offset' in self.options:
            self.options['x'] = x + self.options['offset']
            del self.options['offset']
        form.radio(**self.options)
        self.canv.restoreState()


class Label(Flowable):
    def __init__(self, **options):
        Flowable.__init__(self)
        self.options = options
        # Use Reportlab's default size if not user provided
        self.width = options.get('width', 0)
        self.height = options.get('height', 0)

    def draw(self):
        self.canv.saveState()
        x, y = self.canv.absolutePosition(0, 0)
        if 'offset' in self.options:
            x += self.options['offset']
            del self.options['offset']
        y = -5  # FontSize * 2.5
        if 'yoffset' in self.options:
            y += self.options['yoffset']
            del self.options['yoffset']
        self.canv.setFont(self.options.get('font') if 'font' in self.options else 'OpenSansR',
                          self.options.get('font_size') if 'font_size' in self.options else FontSize)
        self.canv.drawString(x, y, self.options.get('text'), )
        self.canv.restoreState()


class Rect(Flowable):
    def __init__(self, **options):
        Flowable.__init__(self)
        self.options = options
        # Use Reportlab's default size if not user provided
        self.width = options.get('width', 0)
        self.height = 0

    def draw(self):
        self.canv.saveState()
        x, y = self.canv.absolutePosition(self.canv._x, self.canv._y)
        self.canv.setLineWidth(0.25)
        self.canv.rect(x - 75, 0, self.options['width'], -self.options['height'], stroke=1, fill=0)
        self.canv.restoreState()


class Logo(Flowable):
    def __init__(self, **options):
        Flowable.__init__(self)
        self.options = options
        # Use Reportlab's default size if not user provided
        self.width = options.get('width', 0)
        self.height = 0

    def draw(self):
        self.canv.saveState()
        x, y = self.canv.absolutePosition(self.canv._x, self.canv._y)
        logo = svg2rlg('./media/logo.svg')
        logo.width = 0  # logo.minWidth() * 0.5
        logo.height = 0  # logo.height * 0.5
        logo.scale(0.25, 0.25)
        renderPDF.draw(logo, self.canv, 450, -40)
        # logo._drawOn(self.canv)
        self.canv.restoreState()


def main():
    c = SimpleDocTemplate('tsv.pdf', pagesize=A4,
                          rightMargin=2 * cm, leftMargin=2 * cm,
                          topMargin=0.75 * cm, bottomMargin=1 * cm)

    paragraphs = [
        Logo(),
        Paragraph(f'<b><i>Eintrittserklärung</i></b>', title),
        Paragraph(f'Hiermit erkläre ich meine Mitgliedschaft beim <b>TSV Berlin-Wedding 1862 e.V.</b>', spacer2),

        Label(text='Als: ', font='OpenSansB', offset=-30),
        CheckBox(value='aktiv', name='mitgliedschaft', tooltip='aktives Mitglied', borderWidth=2, forceBorder=True, offset=55),
        Label(text='aktives', font='OpenSansR', offset=10),
        CheckBox(value='passiv', name='mitgliedschaft', tooltip='passives Mitglied', borderWidth=2, forceBorder=True, offset=125),
        Label(text='passives Mitglied', font='OpenSansR', offset=80),

        # Paragraph(' ', spacer),
        Paragraph(' ', spacer),
        Label(text='Abteilung:', font='OpenSansB', offset=-62),

        CheckBox(name='Abteilung', value='Badminton', tooltip='Badminton', borderWidth=2, forceBorder=True, offset=55),
        Label(text='Badminton', font='OpenSansR', offset=10),

        CheckBox(name='Abteilung', value='Ultimate-Frisbee', tooltip='Ultimate-Frisbee', borderWidth=2, forceBorder=True, offset=125),
        Label(text='Ultimate-Frisbee', font='OpenSansR', offset=80),

        CheckBox(name='Abteilung', value='Frauengymnastik', tooltip=' Frauengymnastik', borderWidth=2, forceBorder=True, offset=220),
        Label(text='Frauengymnastik', font='OpenSansR', offset=173),

        CheckBox(name='Abteilung', value='Kinderturnen', tooltip='Kinderturnen', borderWidth=2, forceBorder=True, offset=320),
        Label(text='Kinderturnen', font='OpenSansR', offset=277),

        CheckBox(name='Abteilung', value='Volleyball', tooltip='Kinderturnen', borderWidth=2, forceBorder=True, offset=405),
        Label(text='Volleyball', font='OpenSansR', offset=360),

        Paragraph(' ', spacer),

        TextField(name='Name', tooltip='Vorname und Nachname', height=FontSize * 1.5, width=230, offset=0),
        TextField(name='Erziehungsberechtigte', tooltip='Erziehungsberechtigte', height=FontSize * 1.5, width=230, offset=240),
        Paragraph(' ', spacer),
        Label(text='Vorname und Nachname', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=-60, yoffset=3),
        Label(text='bei Jugendlichen Vor + Nachnamen des/der Erziehungsberechtigten deutlich in Druckschrift!', font='OpenSansL',
              font_size=FontSize * TextFieldLabelSizeAdjust, offset=180, yoffset=3),

        Paragraph(' ', spacer),

        TextField(name='Strasse', tooltip='Straße, Hausnummer', height=FontSize * 1.5, width=230, offset=0),
        TextField(name='Ort', tooltip='Postleitzahl, Wohnort', height=FontSize * 1.5, width=230, offset=240),
        Paragraph(' ', spacer),
        Label(text='Straße, Hausnummer', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=-60, yoffset=3),
        Label(text='Postleitzahl, Wohnort', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=180, yoffset=3),

        Paragraph(' ', spacer),

        TextField(name='Geburtsdatum', tooltip='Geburtsdatum', height=FontSize * 1.5, width=230, offset=0),
        TextField(name='Telefon', tooltip='Telefon', height=FontSize * 1.5, width=230, offset=240),
        Paragraph(' ', spacer),
        Label(text='Geburtsdatum', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=-60, yoffset=3),
        Label(text='Telefon', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=180, yoffset=3),

        Paragraph(' ', spacer),

        TextField(name='EMail', tooltip='Geburtsdatum', height=FontSize * 1.5, width=230, offset=0),
        Paragraph(' ', spacer),
        Label(text='E-Mail (z.B. für elektronische Beitragsrechnung bei Bankeinzug)', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=-60, yoffset=3),
        

        Paragraph(' ', spacer),

        Label(text='Geschlecht: ', font='OpenSansB', offset=-62),
        CheckBox(name='Geschlecht', value='männlich', tooltip='männlich', borderWidth=2, forceBorder=True, offset=60),
        Label(text='männlich', font='OpenSansR', offset=15),
        CheckBox(name='Geschlecht', value='weiblich', tooltip='weiblich', borderWidth=2, forceBorder=True, offset=130),
        Label(text='weiblich', font='OpenSansR', offset=85),
        CheckBox(name='Geschlecht', value='divers', tooltip='divers', borderWidth=2, forceBorder=True, offset=220),
        Label(text='divers', font='OpenSansR', offset=175),
        
        Paragraph(' ', spacer),

        Label(text='Ich bin:', font='OpenSansB', offset=-62),
        CheckBox(name='Status', value='berufstätig', tooltip='berufstätig', borderWidth=2, forceBorder=True, offset=60),
        Label(text='berufstätig', font='OpenSansR', offset=15),
        CheckBox(name='Status', value='z.Zt. erwerbslos', tooltip='z.Zt. erwerbslos', borderWidth=2, forceBorder=True, offset=130),
        Label(text='z.Zt. erwerbslos', font='OpenSansR', offset=85),
        CheckBox(name='Status', value='u18', tooltip='Kind/Schüler bis 18. Lj.', borderWidth=2, forceBorder=True,
                 offset=220),
        Label(text='Kind/Schüler bis 18. Lj.', font='OpenSansR', offset=175),
        CheckBox(name='Status', value='student_azubi', tooltip='Student/Azubi bis 27. Lj.', borderWidth=2, forceBorder=True,
                 offset=340),
        Label(text='Student/Azubi bis 27. Lj.', font='OpenSansR', offset=295),

        Paragraph(' ', spacer),

        Paragraph('<b>Beitragszahlung:</b>', spacer2),
        
        Paragraph('''Der Beitrag wird jährlich bis zum 31. März von meinem Konto abgebucht werden''', style),

        Paragraph(' ', spacer),
        Rect(width=495, height=70),
        Paragraph('<b>Einzugsermächtigung:</b>', style),

        Paragraph(' ', spacer),
        TextField(name='Name der Bank:', tooltip='Name der Bank', height=FontSize * 1.5, width=230, offset=0),
        TextField(name='Kontoinhaber', tooltip='Kontoinhaber', height=FontSize * 1.5, width=230, offset=240),
        Paragraph(' ', spacer),
        Label(text='Name der Bank', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=-60, yoffset=3),
        Label(text='Kontoinhaber', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=180, yoffset=3),

        Paragraph(' ', spacer),

        TextField(name='IBAN', tooltip='IBAN', height=FontSize * 1.5, width=230, offset=0),
        TextField(name='Datum/Unterschrift des Kontoinhabers', tooltip='Datum/Unterschrift des Kontoinhabers', height=FontSize * 1.5, width=230,
                  offset=240),
        Paragraph(' ', spacer),
        Label(text='IBAN', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=-60, yoffset=3),
        Label(text='Datum/Unterschrift des Kontoinhabers', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=180, yoffset=3),

        Paragraph(' ', spacer),
        
        CheckBox(name='Zahlung', value='Satzung', tooltip='Die Vereinssatzung erkenne ich an.', borderWidth=2, forceBorder=True, offset=-0),
        CheckBox(name='Zahlung', value='dummy', tooltip='', borderWidth=2, forceBorder=True, offset=-0),
        Label(text='Die Vereinssatzung erkenne ich an.', font='OpenSansR', offset=-45),

        Paragraph(' ', spacer),

        TextField(name='Ort/Datum ', tooltip='Ort/Datum ', height=FontSize * 1.5, width=150, offset=0),
        TextField(name='Unterschrift', tooltip='Unterschrift', height=FontSize * 1.5, width=310, offset=160),
        Paragraph(' ', spacer),
        Label(text='Ort/Datum ', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust, offset=-60, yoffset=3),
        Label(text='Unterschrift (bei Jugendlichen die Unterschrift des/der Erziehungsberechtigten)', font='OpenSansL', font_size=FontSize * TextFieldLabelSizeAdjust,
              offset=100, yoffset=3),

        Paragraph(
            ' - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -',
            spacer),

        Paragraph('<b>Für die Unterlagen des neuen Mitglieds</b>'),
        Paragraph('<b>Auszug aus der Satzung des TSV Berlin Wedding 1862 e.V.</b>'),
        Paragraph('§6 Beiträge'),
        Paragraph('''
        Zur Deckung der Vereinsausgaben wird von jedem Mitglied ein Beitrag erhoben, der jährlich zu entrichten ist. Der Beitrag ist bis zum 31. März des laufenden
Geschäftsjahres auf das Konto des Vereins oder in bar an den Hauptkassierer bzw. vom Vereinsvorstand benannte andere Personen zu zahlen. Die Höhe des Beitrages wird
von der Mitgliederversammlung festgesetzt. Bei Eintritt in den Verein innerhalb des laufenden Jahres ist der Beitrag vom Monat des Eintritts an anteilmäßig bis zum
Jahresende im Voraus zu entrichten. Auf Antrag kann der Beitrag vom Vereinsvorstand ermäßigt oder erlassen werden. Mitglieder bis zum vollendeten 18. Lebensjahr zahlen
einen ermäßigten Beitrag. Besondere Umlagen müssen von der Mitgliederversammlung beschlossen werden. Alle Mittel des Vereins dienen der Förderung aller Mitglieder im
Sinne dieser Satzung (§§2 u. 3).''', small),
        Paragraph('''Kommt ein Vereinsmitglied in Zahlungsverzug, ergehen zwei schriftliche Mahnungen. Sind diese Mahnungen erfolglos, wird das gerichtliche Mahnverfahren eingeleitet, was
zusätzliche Kosten verursacht. Auf Antrag ist hiermit der Ausschluss aus dem Verein verbunden.''', small),
        Paragraph('§7 Ende der Mitgliedschaft'),
        Paragraph('''1.Mitglieds- und Funktionärsausweise sowie Sportkleidung und Geräte, die vom Verein zur Verfügung gestellt wurden, bleiben Eigentum des Vereins und müssen beim
Austritt oder Ausschluss zurückgegeben werden. Der Austritt erfolgt durch schriftliche Mitteilung per Einschreiben an die Geschäftsstelle und kann nur am jeweiligen
Jahresende erfolgen. Die schriftliche Kündigung muss bis spätestens 30. September eingegangen sein.''', small),
        Paragraph('''2. Ausschluss eines Mitgliedes erfolgt durch den Vereinsvorstand, wenn es gegen den Zweck des Vereins (§2) gröblich verstößt, das Ansehen des Vereins schädigt oder
seiner Beitragspflicht nach Mahnung nicht nachgekommen ist. Dem Mitglied steht gegen den Ausschluss das Recht des Einspruchs beim Vereinsvorstand zu. Über diesen
Einspruch entscheidet das Vereinsgericht. Das Vereinsgericht setzt sich aus je einem Mitglied jeder Abteilung zusammen. Die Mitglieder des Ehrengerichts dürfen nicht dem
Vereinsvorstand angehören.''', small),

        Paragraph('Beiträge (Stand 1. Januar 2026)', subtitle),
        Paragraph('<b>Einmalige Aufnahmegebühr: ein Monatsbeitrag</b>', small),
        
        Table(spaceAfter=6, spaceBefore=-3, rowHeights=FontSize*1.8,
            data=[
                ['', 'Monatlich', 'Jährlich'],
                ['aktives Mitglied', '9,00 €', '108,00 €'],
                ['Studenten/Azubis (max. nur bis zum 27. Lebensjahr)', '6,50 €', '78,00 €'],
                ['Frauen-Gymnastik', '6,00 €', '72,00 €'], ['Kinder / Schüler', '5,50 €', '66,00 €'],
                ['Arbeitslose', '5,00 €', '60,00 €'], ['passives Mitglied', '3,50 €', '42,00 €'],
                ['Paare', '12,00 €', '144,00 €'], ['Familie (2 Kinder)', '17,00 €', '204,00 €'], ],
            style=[
                ('GRID', (0, 1), (-1, -1), 1, colors.gray), # frame/grid for body
                ('LINEAFTER', (0, 0), (4, -1), 1, colors.gray), # vertical lines in header
                ('FONTNAME', (0, 0), (-1, 0), 'OpenSansB'),  # header
                ('FONTNAME', (0, 1), (-1, -1), 'OpenSansL'),  # body
                ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 1), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), FontSize - 2),                
            ]
        ),
        Paragraph('''In den Abteilungen Badminton und Volleyball wird ein Zusatzbeitrag erhoben, der z.Zt. 24,00 € für volljähige, aktive Mitglieder und 12,00 € für
         jugendliche und passive Mitglieder beträgt.
         In der Tennisabteilung wird die Höhe der Beiträge sowie Zahlungsweise in der Mitgliederversammlung dieser Abteilung festgelegt. (siehe dort)''',
                  small),      
        Paragraph(' ', spacer_s),
        Paragraph('''Das Eintrittsformular bitte bei der Abteilungsleitung abgeben oder in Abstimmung senden an TSV Berlin-Wedding 1862 e.V. c/o Hüske,
Niederbarnimstraße 6, 10247 Berlin''', style),

    ]

    c.build(paragraphs)


if __name__ == '__main__':
    main()
