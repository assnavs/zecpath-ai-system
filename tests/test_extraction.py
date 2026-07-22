"""
Resume Extraction Test

Tests the resume extraction engine on all resumes
inside data/sample_resumes.
"""

import os

from parsers.resume_parser import parse_resume, save_extracted_text


INPUT_FOLDER = "data/sample_resumes"
OUTPUT_FOLDER = "data/extracted_text"
LOG_FILE = "logs/extraction.log"


def run_test():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    success = 0
    failed = 0

    with open(LOG_FILE, "w", encoding="utf-8") as log:

        log.write("Resume Extraction Test Log\n")
        log.write("=" * 40 + "\n\n")

        for file in os.listdir(INPUT_FOLDER):

            file_path = os.path.join(INPUT_FOLDER, file)

            try:

                cleaned_text = parse_resume(file_path)

                output_name = os.path.splitext(file)[0] + ".txt"

                output_path = os.path.join(
                    OUTPUT_FOLDER,
                    output_name
                )

                save_extracted_text(output_path, cleaned_text)

                log.write(f"{file} : SUCCESS\n")

                success += 1

            except Exception as e:

                log.write(f"{file} : FAILED ({e})\n")

                failed += 1

        log.write("\n")
        log.write("=" * 40 + "\n")
        log.write(f"Successful : {success}\n")
        log.write(f"Failed     : {failed}\n")

    print("Resume extraction completed.")
    print(f"Successful : {success}")
    print(f"Failed     : {failed}")


if __name__ == "__main__":
    run_test()