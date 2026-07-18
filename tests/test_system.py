from parsers.resume_parser import ResumeParser

parser = ResumeParser()

print(parser.parse_resume("resume.pdf"))