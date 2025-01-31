import azure.cognitiveservices.speech as speechsdk


def get_pronunciation_errors(audio_file, reference_text, subscription_key, region):
    """Returns words with pronunciation errors and their error types"""
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=region)
    speech_config.output_format = speechsdk.OutputFormat.Detailed
    
    pronunciation_config = speechsdk.PronunciationAssessmentConfig(
        reference_text=reference_text,
        grading_system=speechsdk.PronunciationAssessmentGradingSystem.HundredMark,
        granularity=speechsdk.PronunciationAssessmentGranularity.Word,
        enable_miscue=True
    )

    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)
    
    speech_recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config, 
        audio_config=audio_config
    )

    pronunciation_config.apply_to(speech_recognizer)
    
    errors = []
    total_duration_seconds = 1
    added_words = set()
    skip_words = {'is', 'a', 'an', 'the', 'he', 'she', 'it', 'we', 'they', 'i', 'you','them','us','our','his','her','their','my','your','mine','yours','ours','theirs','hers','his','its','whose','whom','who','which','what','where','when','why','how'}
    
    recognition_result = speech_recognizer.recognize_once()
    
    if recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        pronunciation_result = speechsdk.PronunciationAssessmentResult(recognition_result)

        total_duration_seconds = recognition_result.duration / 10000000
        
        for word in pronunciation_result.words:
            word_text = word.word.lower()
            if (word.error_type != "None" and 
                len(word_text) > 2 and 
                word_text not in skip_words and 
                word_text not in added_words):
                
                error_info = {
                    'word': word.word,
                    'error_type': word.error_type,
                    'accuracy_score': word.accuracy_score
                }
                errors.append(error_info)
                added_words.add(word_text)
                
    return errors, total_duration_seconds

