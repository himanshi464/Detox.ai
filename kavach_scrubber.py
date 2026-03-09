from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

# 1. Custom Indian Patterns
pan_pattern = Pattern(name="pan", regex=r"\b[A-Z]{5}\d{4}[A-Z]{1}\b", score=0.95)
ifsc_pattern = Pattern(name="ifsc", regex=r"\b[A-Z]{4}0[A-Z0-9]{6}\b", score=0.95)
bank_pattern = Pattern(name="bank_acc", regex=r"\b\d{9,18}\b", score=0.6)

# 2. Add to Analyzer
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_PAN", patterns=[pan_pattern]))
analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_IFSC", patterns=[ifsc_pattern]))
analyzer.registry.add_recognizer(PatternRecognizer(supported_entity="IN_BANK_ACC", patterns=[bank_pattern]))

anonymizer = AnonymizerEngine()

def scrub_text(text):
    results = analyzer.analyze(text=text, language='en', 
                                entities=["PERSON", "IN_AADHAAR", "IN_PAN", "IN_IFSC", "IN_BANK_ACC"])
    return anonymizer.anonymize(text=text, analyzer_results=results).text