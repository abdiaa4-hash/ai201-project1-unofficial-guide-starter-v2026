# The Unofficial Guide — campus_life

## What This Does

This is a RAG system built over the `campus_life` corpus — 88 short, real
student posts about dining halls, dorms, course workloads, registration
deadlines, advising, and campus services. It answers specific, factual
questions a student would actually ask, like "how long is the wait at
Verrill Street Grill on Friday evenings?" or "is the housing lottery random?",
by retrieving the most relevant post(s) and generating an answer grounded
only in those posts, with the source file named. Questions clearly outside
the corpus (general trivia, unrelated how-tos) are refused rather than
answered from the model's own knowledge.

## Chunking Strategy

The starter's default chunker (`fallback_split`) splits documents into fixed
800-character windows with overlap. Running it against `campus_life` showed
88 documents producing exactly 88 chunks — no document in this corpus is
long enough to ever get split, since posts average 317 characters and the
longest is 549. That result was the real finding: for this corpus, one post
already is the natural unit of meaning, so a fixed-size splitter was doing
nothing useful here — it just happened not to matter yet.

I replaced `split_documents()` in `chunker.py` to chunk by whole document
instead of by character count: each post becomes exactly one chunk, with no
character-based slicing. This guarantees no sentence is ever cut in half,
since real posts here are short and single-topic (a dorm review, a course
workload report, a dining hall wait-time post). The trade-off is that a post
covering more than one sub-point (e.g. a dorm review mentioning AC, laundry
cost, and noise together) stays as one slightly denser chunk rather than
being split apart — I accepted this because splitting it would separate
facts that are still about the same dorm and the same underlying question.

Re-indexing with the new chunker produced the same 88 documents → 88 chunks,
317 characters average (shortest 178, longest 549) — identical numbers to
the fallback, but now `produced_by` correctly reports
`chunker.py::split_documents`, confirming the new function is running and
that the "one post = one chunk" behavior is a deliberate choice rather than
an accident of an 800-character window.

## Sample Chunks

**Chunk 1** — source: `admin_add_drop_deadline.txt#0` — produced by: `chunker.py::split_documents`
> You can add a course through the end of the second week. Dropping is a longer window — through the end of week six — but a drop after week two shows as a W on your transcript. Nothing anywhere on the registrar's site says this plainly, and students find out from each other.

**Chunk 2** — source: `course_biol_160.txt#0` — produced by: `chunker.py::split_documents`
> BIOL 160 Cell Biology. I lived here my sophomore year. Format is lecture three times a week with a weekly lab. Assessment: four unit tests and a cumulative final. Not curved. Expect 9 to 11 hours a week, the heaviest first-year course by reputation. The one piece of advice: the unit tests come fast, roughly every three weeks; falling behind once is very hard to recover from.

**Chunk 3** — source: `course_hist_118_workload.txt#0` — produced by: `chunker.py::split_documents`
> Workload for HIST 118 Modern World History. People keep asking so: a lot of reading, about 120 pages a week, but no problem sets. That's real time, not optimistic time. It's front-loaded — the first month is heavier than the rest, partly because you're learning the format.

**Chunk 4** — source: `dining_pellew_dining_hall_followup.txt#0` — produced by: `chunker.py::split_documents`
> Re: Pellew Dining Hall. Adding to what people have said about Pellew Dining Hall. The wait figure of 12 to 18 minutes at peak matches what I've seen. If you're trying to eat between classes, go before 11:45 and it's a different building entirely. Also worth saying: the furthest hall from anywhere, next to the athletics centre. Nobody tells you this at orientation.

**Chunk 5** — source: `housing_innisfree_hall.txt#0` — produced by: `chunker.py::split_documents`
> Innisfree Hall — what it's actually like. Transferred in last year, so take this with a grain of salt. Built 1991, renovated 2022. Rooms are doubles arranged as pairs sharing one bathroom between two rooms. The good: the shared-bathroom-between-two-rooms arrangement is the best compromise on campus. The bad: no air conditioning, which matters for the first three weeks of September. Laundry costs $1.75 wash, $1.75 dry, app-based. On noise: moderate; the building is L-shaped and the short wing is much quieter.

## Sample Answer

**Question:** is the housing lottery random?

**Answer:** The housing lottery is not entirely random in the way most people assume. While rising sophomores get a number drawn at random, juniors and seniors are ordered by accumulated credit hours first, with a random tie-break only used if necessary.

**Source:** `admin_housing_lottery.txt`

**Relevance cutoff:** 0.6 (the starter's default, kept deliberately).

**Distance groups observed:**
- In-scope questions (5 of my own test questions): 0.148, 0.173, 0.265, 0.278, 0.366
- Out-of-scope questions (the 5 in `OUT_OF_SCOPE`): 0.825, 0.844, 0.886, 0.896, 0.934

There's a clean, wide gap between the two groups — in-scope tops out at
0.366, out-of-scope bottoms out at 0.825 — so 0.6 sits comfortably in the
middle with room on both sides. All 5 out-of-scope questions were correctly
refused; all 5 in-scope questions were correctly answered with the right
source.

## How I Used AI

1. I used Claude to help me set up my development environment — creating the
   Python 3.11 virtual environment, diagnosing a broken venv with no working
   `python`/`pip` binaries, and fixing a `.env` file where my API key had been
   pasted incorrectly (once with literal placeholder text still in it, once
   with a shell command accidentally saved as file content instead of being
   run). I had to actually inspect file contents directly and compare them
   against what tools reported, since an automated coding assistant in my
   editor was giving unreliable, fabricated status summaries instead of real
   command output — switching to a plain Terminal window fixed this.

2. I asked Claude to help me think through my chunking decision rather than
   write it for me. I described what the starter's fallback chunker actually
   produced on my corpus (88 docs → 88 chunks, nothing ever split), and Claude
   helped me see that meant the real design decision was "chunk by document"
   rather than inventing an arbitrary character size. I wrote the actual
   `split_documents()` function and the acceptance criteria myself; Claude's
   role was pointing out that my criterion 4 draft (5 of 5, no fragmentation)
   didn't address a different question (multi-topic chunks like Innisfree
   Hall), which I decided to accept as a known trade-off rather than fix.
