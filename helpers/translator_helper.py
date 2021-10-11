
from googletrans import Translator
translator = Translator()

def translate_data(target_lg, *data):
    data = ' '.join(data)
    return translator.translate(data, dest=target_lg)