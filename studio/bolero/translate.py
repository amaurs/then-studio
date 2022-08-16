from googletrans import Translator

file = open("boleros_en.txt","w") 

with open("boleros2.txt") as f:
    content = f.readlines()
    for line in content:
        translator = Translator()
        translation = translator.translate(line, src='es', dest='en')
        file.write(translation.text.strip() + "\n") 