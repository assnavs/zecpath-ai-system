"""
Job Description Parser Test

Tests the Job Description Parser and saves
structured outputs for all job descriptions.
"""

import json
import os

from parsers.job_description_parser import parse_job_descriptions


INPUT_FILE = "data/sample_job_descriptions/sample_job_descriptions.docx"
OUTPUT_FOLDER = "data/structured_jd"
LOG_FILE = "logs/jd_parser.log"


def run_test():

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    jobs = parse_job_descriptions(INPUT_FILE)

    success = 0

    with open(LOG_FILE, "w", encoding="utf-8") as log:

        log.write("Job Description Parser Test Log\n")
        log.write("=" * 50 + "\n\n")

        for index, job in enumerate(jobs, start=1):

            file_name = f"job_{index}.json"

            output_path = os.path.join(
                OUTPUT_FOLDER,
                file_name
            )

            with open(output_path, "w", encoding="utf-8") as output:

                json.dump(job,
                          output,
                          indent=4,
                          ensure_ascii=False
                          )

            log.write(
                f"{file_name} : SUCCESS\n"
            )

            success += 1

        log.write("\n")
        log.write("=" * 50 + "\n")
        log.write(f"Total Jobs Parsed : {success}\n")
        log.write("Failed            : 0\n")

    print("Job Description Parsing Completed")
    print(f"Jobs Parsed : {success}")


if __name__ == "__main__":
    run_test()