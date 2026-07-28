"""
Unit Test for Certification Parser
"""

import json

from parsers.certification_parser import CertificationParser


def test_certification_parser():

    sample_resume = """
    Google Data Analytics - 2024

    AWS Cloud Practitioner - 2023

    Cisco CCNA

    Certified Ethical Hacker - 2025
    """

    parser = CertificationParser()

    result = parser.extract(sample_resume)

    print("\n===== Certification Parsing Result =====\n")
    print(json.dumps(result, indent=4))

    assert result["certification_count"] == 4

    extracted = [
        item["certificate"]
        for item in result["certifications"]
    ]

    assert "Google Data Analytics" in extracted
    assert "AWS Cloud Practitioner" in extracted
    assert "Cisco CCNA" in extracted
    assert "Certified Ethical Hacker" in extracted

    print("\nAll Certification Parser Tests Passed.\n")


if __name__ == "__main__":
    test_certification_parser()