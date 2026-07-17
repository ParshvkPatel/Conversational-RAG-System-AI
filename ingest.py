import fitz
import os
import json

DATA_FOLDER = "data"

documents = []
pdf_count = 0

for root, dirs, files in os.walk(DATA_FOLDER):

    for file in files:

        if file.lower().endswith(".pdf"):

            pdf_count += 1

            pdf_path = os.path.join(root, file)

            print(f"Reading ({pdf_count}): {file}")

            try:
                doc = fitz.open(pdf_path)

                path_parts = os.path.normpath(pdf_path).split(os.sep)

                # Example:
                # data/English/Std10/Science.pdf
                language = path_parts[1] if len(path_parts) > 1 else "Unknown"
                standard = path_parts[2] if len(path_parts) > 2 else "Unknown"

                for page_number in range(len(doc)):

                    page = doc.load_page(page_number)
                    text = page.get_text().strip()

                    if text:

                        documents.append({
                            "language": language,
                            "standard": standard,
                            "source": file,
                            "page": page_number + 1,
                            "text": text
                        })

            except Exception as e:

                print(f"Error reading {file}")
                print(e)

# Save all extracted data
with open("documents.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=2)

print("\n===================================")
print(f"Total PDFs  : {pdf_count}")
print(f"Total Pages : {len(documents)}")
print("Saved File  : documents.json")
print("===================================")