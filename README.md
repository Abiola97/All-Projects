# Open-Ended Survey Response Coding (Q38, Q39, Q40)

A lightweight, rule-based pipeline that cleans open-ended survey responses and codes them into a small set of named themes. It was built for a survey on human rights activism in Nigeria, and no heavy NLP models are needed: just `pandas`, `openpyxl` and regular expressions.

The three questions it handles:

| Question | Topic |
|---|---|
| Q38 | Which approaches by activists are most constructive for improving policy outcomes in Nigeria? |
| Q39 | Which human rights campaign in Nigeria was particularly effective, and what made it effective? |
| Q40 | Which approaches to human rights campaigns are counterproductive, and why? |

## What it does

1. **Cleans** each response: trims whitespace, normalises apostrophes, capitalises the first letter.
2. **Recodes non-answers to "Don't know".** This covers explicit non-answers ("can't remember", "none", "nil", "no idea") and responses that do not answer the question as asked (single unrelated words, vague praise, or the opposite of what was asked). Blank cells stay blank.
3. **Codes each valid response into themes** using a transparent keyword codebook. Each question has a maximum of 15 labels: 13 themes, plus "Other / unclassified" and "Don't know".
4. **Writes a new workbook** with the cleaned and coded columns placed beside each original question.

### Output columns

For each question the output sheet contains:

| Column | Meaning |
|---|---|
| Original question column | Untouched |
| `New Qxx (cleaned)` | Cleaned text, with non-answers set to "Don't know" |
| Original themes column | Your earlier coding, kept for comparison |
| `New Qxx themes (reclustered)` | Up to 3 themes per response, strongest first, separated by semicolons |
| `New Qxx primary theme` | The single strongest theme (use this for counts and charts) |

Two extra sheets are added:

- **Theme_Summary**: respondents per primary theme, % of valid answers, number of mentions across all labels, and an example response.
- **Cleaning_Log**: every response recoded to "Don't know", with counts and a flag for whether it was a standard non-answer or a judgement call, so each decision can be reviewed.

The original sheet is preserved as `Sheet 1 (original)`.

## Themes

**Q38 (constructive approaches)**
Dialogue and direct engagement with government · Coalitions, stakeholders and community/traditional leaders · Evidence-based advocacy and research · Policy proposals, legislative engagement and lobbying · Public awareness, sensitisation and civic education · Media and social media advocacy · Peaceful protest, petitions and public pressure · Legal action, due process and lawful conduct · Accountability, transparency and policy monitoring · Rights-based advocacy for expanded protections · Honesty, respect and constructive conduct · People-centred development, economic and empowerment approaches · No approach works or opposed to the campaign

**Q39 (what made a campaign effective)**
Youth mobilisation and social media · Unity, broad participation and strong organisation · Sustained pressure and persistence · Public awareness and enlightenment · Media coverage, international attention and human stories · Clear demands, realistic solutions and evidence · Peaceful, orderly conduct and credible leadership · Tangible policy or legal change and government response · Legal action, dialogue and institutional engagement · Community and grassroots involvement · Campaign named, reason not given · Rights-issue remarks, no mechanism stated · No effective campaign / sceptical

**Q40 (counterproductive approaches)**
Violence, rioting and destruction · Confrontation, aggression and public shaming of government · Misinformation, exaggeration and weak evidence · Politicisation, partisanship and hijacking · Ignoring local culture, religion and context · Excluding or not engaging communities and affected people · Poor planning, weak leadership and no follow-up · Refusing dialogue or bypassing government engagement and due process · Street protests, shutdowns and disruption of public life · Extending rights to criminals and bandits · Corruption, greed and lack of credibility · Over-reliance on legal action and litigation · Neglecting victims (no after-care, exposure, not believed)

## How the coding works

- Every theme is a list of regular expressions in `recode_book1.py`. A response can match several themes.
- The **primary theme** is the one with the most pattern matches. Ties are broken by a priority list that puts specific themes ahead of generic ones (for example, litigation ahead of general dialogue).
- Question-specific rules handle special cases, such as negation in Q38 ("instead of protesting" is not counted as protest), and positive statements in Q40 that describe what works rather than what backfires.
- Because it is rule-based, every label can be traced to the exact words that triggered it.

## Requirements

- Python 3.9 or later
- `pandas`
- `openpyxl`

```bash
pip install pandas openpyxl
```

## Usage

Place your survey workbook anywhere, then run:

```bash
python build_book1.py path/to/input.xlsx path/to/output.xlsx
```

The input workbook should have one sheet with these columns in this order:

1. Raw Q38 responses
2. Q38 responses (working copy)
3. Q38 existing themes
4. Q39 responses
5. Q39 existing themes
6. Q40 responses
7. Q40 existing themes

If your layout differs, adjust the column indexes near the top of `build_book1.py`.

To run only the coding step and save the results as a pickle for inspection:

```bash
python recode_book1.py path/to/input.xlsx path/to/codes.pkl
```

## Project structure

```
.
├── recode_book1.py     # Cleaning rules, codebooks and the coding engine
├── build_book1.py      # Builds the output workbook (new columns, summary, log)
└── README.md
```

## Adapting it to another survey

1. Open `recode_book1.py` and find the codebook dictionaries (`Q38`, `Q39`, `Q40`).
2. Replace the theme names and patterns with ones that fit your questions.
3. Update the priority lists in `PRIORITY` so specific themes win ties.
4. Run the pipeline, then read the responses that land in "Other / unclassified" and add patterns until coverage is high (aim for under 5% unclassified).
5. Review the **Cleaning_Log** sheet before treating the "Don't know" recodes as final.

## Limitations

- Keyword matching cannot fully understand meaning. A response like "not violent" can still be tagged under violence if the wording is unusual. Spot-check a sample of responses per theme before reporting results.
- The "Don't know" recoding includes judgement calls. Most are in Q40, where many respondents described what they support instead of what is counterproductive. These are listed in the Cleaning_Log so you can reverse any you disagree with.
- The codebooks reflect the vocabulary in this particular survey and will need tuning for new data.

## Data privacy

Survey responses can contain personal or sensitive information. **Do not commit raw survey data or output workbooks to a public repository.** Add data files to `.gitignore`:

```
*.xlsx
*.csv
*.pkl
```

## License

Add a license of your choice (for example MIT) before publishing.
