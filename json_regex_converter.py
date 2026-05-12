import os
import re
import glob

def convert_js_to_json():
    input_dir = './in'
    output_dir = './out'

    # Vytvoření výstupní složky, pokud neexistuje
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Najít všechny .txt soubory
    files = glob.glob(os.path.join(input_dir, '*.txt'))

    if not files:
        print("Ve složce './in' nebyly nalezeny žádné .txt soubory.")
        return

    for file_path in files:
        # Získání názvu souboru bez cesty
        base_name = os.path.basename(file_path)
        # Rozdělení na jméno a (původní) příponu
        name_without_ext, _ = os.path.splitext(base_name)
        
        # Nový název s příponou .json
        new_filename = f"{name_without_ext}.json"
        
        print(f"Zpracovávám: {base_name} -> {new_filename}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # OPRAVENÝ REGEX:
        # Hledáme slovo následované dvojtečkou, ALE:
        # 1. (?<=[\{,])  -> Musí mu předcházet buď složená závorka { nebo čárka , (případně mezery)
        # 2. \s* -> Mezi tím mohou být mezery
        # 3. (\w+)       -> Samotný název klíče
        # 4. (?=\s*:)    -> Za ním musí následovat dvojtečka
        
        transformed = re.sub(r'(?<=[\{,])\s*(\w+)(?=\s*:)', r' "\1"', content)

        # 2. Regex: Odstraní přebytečné čárky před koncem objektu nebo pole (trailing commas)
        # JSON standard je zakazuje, zatímco v JS jsou běžné
        transformed = re.sub(r',\s*([\]}])', r'\1', transformed)

        # Uložení jako .json
        output_path = os.path.join(output_dir, new_filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transformed)

    print(f"\nHotovo! Všechny soubory byly uloženy do '{output_dir}'.")

if __name__ == "__main__":
    convert_js_to_json()