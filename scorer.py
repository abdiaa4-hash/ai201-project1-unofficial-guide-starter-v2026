"""
Decides whether an answer counts as correct.

My rule: the expects phrase must appear in the answer text, case-insensitive.
This is a simple substring match - it doesn't check that the phrase is used
correctly in context, only that it's present. A model could theoretically
include the right words while getting the actual meaning wrong, and this
scorer would still mark it correct. I accepted that limitation because for
my corpus (short factual posts with specific numbers/phrases like "two weeks"
or "30 minutes"), the expects phrase is specific enough that its presence is
a strong signal the answer is actually right.
"""


def judge(question, expects, answer, results):
    """Return True if expects appears in answer, case-insensitive."""
    return expects.strip().lower() in answer.strip().lower()
