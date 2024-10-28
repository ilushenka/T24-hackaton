import fitz  # PyMuPDF

forbidden_words = ["сука", "блять", "нахуй", "террорист", "теракт", "экстремизм", "теракты", "Усаму бен Ладен", "Абдулла Оджалан", "Мухаммад Атта", "Абу Мусаб аль-Заркави", "Серджио Дель Валье"]
# Вспомогательная функция для извлечения текста из PDF
def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    if check_forbidden_words_in_pdf(pdf_document, forbidden_words):
        print("Обработка файла отменена из-за наличия запрещенных слов.")
        return

    text_content = []

    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text("text")
        text_content.append(f"Page {page_num + 1}:\n{text}\n")

    return "\n".join(text_content)

def check_forbidden_words_in_pdf(pdf_document, forbidden_words):
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        text = page.get_text("text")
        if contains_forbidden_words(text, forbidden_words, page_num + 1):
            return True 
    return False  # Запрещенные слова не найдены

def contains_forbidden_words(text, forbidden_words, page_num=None):
    # Проверяем наличие запрещенных слов в тексте
    for word in forbidden_words:
        if word in text:
            if page_num:
                print(f"Запрещенное слово '{word}' найдено на странице {page_num + 1}.")
            else:
                print(f"Запрещенное слово '{word}' было найдено в тексте.")
            return True  # Запрещенные слова найдены
    return False  # Запрещенные слова не найдены