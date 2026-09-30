# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
Each of my 5 questions maps directly to one specific document that clearly covers it (advising_registration.txt, housing_lottery.txt, dining_verrill_street_grill_followup.txt, admin_library_holds.txt, health_center.txt), so I expect retrieval to find the right chunk for all 5. I kept the 4-of-5 target from the starter rather than raising it to 5-of-5, since something could still go wrong with a specific phrasing even on an easy corpus.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
The starter's grounding instruction (GROUNDING_INSTRUCTION in generate.py) already requires the model to name the source document it drew from, so this should hold for every answer as long as the relevance gate correctly lets the question through in the first place. It's a structural guarantee from the prompt, not something that depends on my specific corpus.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

**Why this target:**
I expect a clean gap between my 5 in-scope questions and the 5 OUT_OF_SCOPE questions, since the out-of-scope ones (world capitals, car maintenance, sports trivia, medication dosages, programming syntax) are from completely different domains than a college campus corpus. I'll confirm the actual distances and gap size in Milestone 4 and update this note with real numbers once I've set the cutoff.

---

## 4. Chunk completeness

At least 5 of 5 sampled chunks read as one complete thought, with no sentence cut off at either end.

**Why this target:**
The campus_life corpus is made of short, self-contained student posts, and the chunker preserved each document as a single chunk in this run (88 documents, 88 chunks). Since the source documents are already concise and focused on one topic, the sampled chunks read cleanly as complete thoughts without awkward mid-sentence breaks.

> **Revised in unit 2:** At least 4 of 5 sampled chunks contain no more than
> one distinct sub-topic (e.g. one fact about a dorm's bathroom layout, not
> bathroom + laundry + noise all in one chunk).
>
> **Why revised:** "Reads as one complete thought" turned out to be a
> judgment call I couldn't reliably repeat. Looking back at my own Chunk 5
> (Innisfree Hall), it covers bathroom layout, AC, laundry cost, and noise
> all in one chunk — I scored it "complete" the first time because each
> sentence was grammatically whole, but on a second look I'd just as easily
> call it "too many topics crammed into one chunk." The original criterion
> was measuring sentence-level fragmentation, which my chunker structurally
> can't produce (it never splits mid-sentence), so it was never actually at
> risk of failing — it wasn't testing anything. The revised version asks
> about topic count instead, which is something I can count the same way
> twice.

---

## 5. Source attribution is accurate, not just present

For at least 4 of 5 test questions, the cited source document actually contains the fact used in the answer.

**Why this target:**
I kept this at 4 of 5 because each question is tied to a very specific document, but retrieval can still miss a chunk if the wording is slightly different or if similar material appears in more than one place. On this corpus, the source should usually be clear, so this target is ambitious but still realistic.

---

<!-- UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it.

     Lowering a target because you missed it is not a revision, and it costs
     you the point. A number you missed stays where it is, gets diagnosed,
     and gets a fix attempted. That's where the points are. -->
