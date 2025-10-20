from flask import Flask, render_template, request
import fitz
import os
import webbrowser
import threading
import sys
app = Flask(__name__)
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000")
@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        # Get form values and store in variables
        name = request.form.get('name')
        gender = request.form.get('gender')
        course = request.form.get('course')
        m1 = request.form.get('df')
        y1 = request.form.get('year_from')
        m2 = request.form.get('dt')
        y2 = request.form.get('year_to')
        frm = f"{m1} {y1}"
        t = f"{m2} {y2}"

        # For demonstration, print values in console
        #p = f"{name}_{course}.pdf"
        downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        p = os.path.join(downloads_folder, f"{name}_{course}_certificate.pdf")
        if gender == "1":
            sentence1 = f"This is to certify that Mr.{name} has completed"
        if gender == "0":
            sentence1 = f"This is to certify that Ms.{name} has completed"
        co = f" {course} Course"
        sentence2 = f"From:- {frm}  To:- {t} with good proficiency achievement"

        if getattr(sys, 'frozen', False):  # Running as .exe
            base_path = sys._MEIPASS
        else:  # Running as .py
            base_path = os.path.dirname(__file__)

        template_path = os.path.join(base_path, "certificate_template.pdf")
        output_path = p

        pdf = fitz.open(template_path)
        page = pdf[0]

        # === FONTS & SIZES ===
        name_font = "times-italic"       # Times New Roman Italic
        name_size = 36

        sentence_font = "times-roman"    # Times New Roman
        sentence_bold_font = "times-bold"
        sentence_size = 16

        # === PAGE METRICS ===
        page_width = page.rect.width

        # helper: get text width using fitz.get_text_length
        def text_width(text, fontname, fontsize):
            # fitz.get_text_length(text, fontsize=..., fontname=...) is the standard helper
            return fitz.get_text_length(text, fontsize=fontsize, fontname=fontname)

        # === POSITIONS (adjust Y values to fit your template) ===
        name_y = 290
        sentence_y = name_y + 50  # adjust vertical spacing as needed
        second_line_y = sentence_y + 30

        # --- Draw name (centered) ---
        name_w = text_width(name, name_font, name_size)
        x_name = (page_width - name_w) / 2
        page.insert_text((x_name, name_y),
                        name,
                        fontsize=name_size,
                        fontname=name_font,
                        fill=(0.6078, 0.1059, 0.1451))  

        # --- Draw sentence (part1 normal + part2 bold), center the combined string ---
        full_sentence = sentence1 + co
        full_w = text_width(full_sentence, sentence_font, sentence_size)
        x_start = (page_width - full_w) / 2

        # part1
        page.insert_text((x_start, sentence_y),
                        sentence1,
                        fontsize=sentence_size,
                        fontname=sentence_font,
                        fill=(0, 0, 0))

        # part2 (bold) — placed right after part1
        x_bold = x_start + text_width(sentence1, sentence_font, sentence_size)
        page.insert_text((x_bold, sentence_y),
                        co,
                        fontsize=sentence_size,
                        fontname=sentence_bold_font,
                        fill=(0, 0.4392, 0.7529))

        second_w = text_width(sentence2, sentence_font, sentence_size)
        x_second = (page_width - second_w) / 2
        page.insert_text((x_second, second_line_y),
                        sentence2,
                        fontsize=sentence_size,
                        fontname=sentence_font,
                        fill=(0, 0, 0))

        # Save
        pdf.save(output_path)
        pdf.close()

        print("✅ Saved:", output_path)
        
        # You can use these variables in your Python code as needed
        return render_template("success.html", name=name)

    return render_template('index.html')  # Your HTML file from previous step

if __name__ == '__main__':
    threading.Timer(1.0, open_browser).start()
    app.run(debug=True, use_reloader=False)
