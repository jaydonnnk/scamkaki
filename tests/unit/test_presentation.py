def test_transcript_turns_preserve_speakers_continuations_and_unlabelled_text():
    from scamkaki.app.presentation import transcript_turns

    turns = transcript_turns(
        "Unlabelled introduction\nassistant: Hello <script>\ncontinued\n"
        "user: नमस्ते\nदूसरी पंक्ति\noperator: no guessed speaker"
    )
    assert [(t.speaker, t.text) for t in turns] == [
        ("unlabelled", "Unlabelled introduction"),
        ("ah_ma", "Hello <script>\ncontinued"),
        ("caller", "नमस्ते\nदूसरी पंक्ति\noperator: no guessed speaker"),
    ]
    assert transcript_turns("  \n ") == []
