import os
import re
import pyperclip
from time import sleep
from googletrans import Translator


class Clipboard:
    """
    Clase que modifica el clipboard dándole un nuevo formato
    """

    def __init__(self):
        self.original_text = ""

    def get_paste_buffer(self) -> str:
        """
        Obtiene el texto copiado del clipboard

        Returns:
        string: Texto obtenido desde el clipboard
        """

        result = pyperclip.paste()
        return result

    def modified_clipboard_event(self) -> bool:
        """
        Devuelve True cuando el texto del clipboard fue
        modificado

        Returns:
        bool: True si el clipboard fue modificado
        """
        aux = self.get_paste_buffer()
        return self.original_text != aux


class CustomTranslator:
    """
    Clase que permite formatear un texto y traducirlo
    """

    def __init__(self, text="Hi!"):
        self.original_text = text
        self.modified_text = ""
        self.translated_text = ""

    def remove_breaklines(self) -> str:
        """
        Remueve los saltos de linea y los retorno de carro de un texto

        Parameters:
        text (string): Texto para formatear

        Returns:
        string: Texto formateado
        """
        # self.modified_text = self.original_text.replace("\n", " ").replace(
        #   "\r", ""
        # )
        self.modified_text = re.sub("\.\n", ".<br><br>", self.original_text)
        self.modified_text = re.sub("\n", "\r", self.modified_text)

    def translate_text(self, src: str = "en", dest: str = "es") -> str:
        """
        Traduce el texto ingresado desde el idioma de origen
        al idioma de destino

        Parameters:
        text (string): Texto para traducir
        src (string): Lenguaje de origen del texto
        dest (string): Lenguaje de destino del textO

        Returns:
        string: Texto traducido
        """

        self.remove_breaklines()
        translator = Translator()
        while True:
            try:
                result = translator.translate(
                    self.modified_text, src=src, dest=dest
                )
                break
            except Exception as e:
                sleep(0.5)
                translator = Translator()

        self.translated_text = result.text
        self.create_html()

    def create_html(self) -> None:
        html_template = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Translator</title>
            </head>
            <body style="font-size: 28px; font-family: cambria">
                <div class="box" 
                    style="width: 60vw; 
                            margin: auto; 
                            margin-top: 10vh; 
                            padding: 25px; 
                            border: 1px solid #000">
                    <p>{ self.translated_text }</p>
               </div>
            </body>
            </html>
        """

        with open("./output/index.html", "w+", encoding="utf-8") as f:
            f.write(html_template)


if __name__ == "__main__":

    if not os.path.exists("output"):
        os.makedirs("output")

    cp = Clipboard()
    trans = CustomTranslator()

    while True:
        if cp.modified_clipboard_event():
            cp.original_text = cp.get_paste_buffer()
            trans.original_text = cp.original_text
            trans.translate_text(src="en", dest="es")
        sleep(1)
