import os
import re
import glob

def convert_js_to_json():
    input_dir = './in'
    output_dir = './out'

    # Vytvoření výstupní složky, pokud neexistuje
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Najít všechny .txt soubory ve složce ./in
    files = glob.glob(os.path.join(input_dir, '*.txt'))

    if not files:
        print("Ve složce './in' nebyly nalezeny žádné .txt soubory.")
        return

    for file_path in files:
        filename = os.path.basename(file_path)
        print(f"Zpracovávám: {filename}...")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Regex: Najde slova následovaná dvojtečkou (klíče) a dá je do uvozovek
        # \b\w+\b najde celé slovo, (?=\s*:) je lookahead, který kontroluje dvojtečku
        transformed = re.sub(r'(\b\w+\b)(?=\s*:)', r'"\1"', content)

        # 2. Regex: Odstraní přebytečné čárky před koncem objektu nebo pole (trailing commas)
        # JSON standard je zakazuje, zatímco v JS jsou běžné
        transformed = re.sub(r',\s*([\]}])', r'\1', transformed)

        # Uložení do výstupní složky se stejným názvem
        output_path = os.path.join(output_dir, filename)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(transformed)

    print(f"\nHotovo! Všechny soubory byly uloženy do '{output_dir}'.")

if __name__ == "__main__":
    convert_js_to_json()