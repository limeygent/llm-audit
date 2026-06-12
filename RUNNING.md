> ⚠️ **DEPRECATED / RETIRED (2026-06-08).** The Mode B council orchestration in
> this file is **no longer executed.** The agency-dashboard post-audit worker
> (`scripts/run-post-audit.ts`) now orchestrates the council **in code** — it
> builds the prompt bundle, runs one local Claude seat, and shells out to
> `llm-council/council_cli.py` directly. There is no headless-Claude
> orchestrator following this playbook anymore.
>
> Why it was retired: running this prose playbook via headless `claude --print`
> was fragile (no reliable background-task completion in `--print` mode, so the
> council call was killed mid-flight and the run was marked "done" over a
> placeholder) and burned the Claude subscription quota twice per run
> (orchestrator + a local seat). The code orchestrator removes both problems.
>
> `skill.md` (the audit methodology) is still live and is used by both the solo
> auditor and the local council seat. This file is kept for historical
> reference only — do not follow Mode B below.

# Running the LLM Readability Audit

This document tells a fresh Claude Code session (e.g. `claude -p "audit https://example.com"`) HOW to execute the audit. The methodology lives in `skill.md`; this doc is the orchestration playbook.

## Two execution modes

### Mode A — Solo (DEFAULT for all invocations)
Apply `skill.md` directly to the supplied article body and emit the audit per its Output Format. Single-LLM, no council, no subagent, no `runs/` folder, no API calls beyond what your own session uses. Faster, cheaper, lower variance.

**This is what happens in `run-post-audit.ts` (the dashboard's WordPress audit worker)** and most `claude -p` invocations. It's the steady-state production path.

This file (`RUNNING.md`) is **NOT relevant to Mode A**. If you're running solo, do not read this file — just apply skill.md.

### Mode B — Council (opt-in, multi-LLM)
A multi-LLM council (Opus subagent + 3 OpenRouter models: GLM-5, Mistral-medium-3-5, DeepSeek-v4-flash) produces 4 perspectives, a peer-reviewed ranking, and a chairman synthesis (Gemini 3.1 Pro). Slower (~3-5 min), costs ~$4.24/M tokens. Reserved for high-stakes audits where multi-LLM consensus justifies the time/cost.

**Mode B requires ALL of these to be true:**
- The operator's prompt explicitly invokes council mode (literal phrase: `Mode B`, `use council mode`, `council mode`, `multi-LLM audit`, or `run the council`), OR the operator told you by name to read `RUNNING.md`
- The `Agent` tool is available in your runtime
- The `Bash` tool is available with permission to run `python3 council_cli.py ...`

If any of those is false → fall back to Mode A. Don't try to half-run Mode B; it'll hang.

The rest of this document is the Mode B orchestration playbook.

---

## Mode B — Step-by-step orchestration

### Step 0 — Initialize the run directory (do this FIRST)

Each audit creates a persistent per-run directory under `/Users/nomis/.claude/skills/llm-audit/runs/`. All artifacts go there (not `/tmp/`) so the operator can review them later, even after subsequent runs.

```bash
RUN_TS=$(date +%Y%m%d-%H%M%S)
URL_SLUG=$(echo "<URL>" | sed -E 's|^https?://(www\.)?||; s|[^a-zA-Z0-9._-]|-|g' | head -c 60)
RUN_DIR="/Users/nomis/.claude/skills/llm-audit/runs/${RUN_TS}-${URL_SLUG}"
mkdir -p "$RUN_DIR"
echo "$RUN_DIR" > /tmp/llm-audit-current-run.txt   # so subsequent steps can find the dir
```

For the rest of this document, every reference to `${RUN_DIR}` resolves to that path. Do NOT use `/tmp/` for durable artifacts — only for temporary scratch.

Files that will end up in `${RUN_DIR}` by the time the run finishes:

| File | Written by | Purpose |
|---|---|---|
| `manifest.json` | orchestrator (final step) | Run metadata: timestamp, URL, intent, models, timings, exit status, summary |
| `audit-prompt.txt` | Step 3 | Bundled prompt sent to the council |
| `audit-page.md` | Step 2 | Cleaned page content with frontmatter |
| `opus-stage1.md` | Step 4 (subagent) | Opus subagent's audit output |
| `stage1-api.json` | Step 4 (council CLI) | OpenRouter stage-1 results |
| `stage1-combined.json` | Step 6 | Merged stage-1 (API + Opus) |
| `audit-result.json` | Step 7 | Full council JSON (stage1 + stage2 + stage3 + metadata) |
| `final.md` | Step 8 | The synthesized chairman markdown the operator received |
| `orchestrator-log.md` | each step appends | Narrative of what the orchestrator did, with timestamps and any errors |

### Prerequisites (verify silently before running)
- `/Users/nomis/Desktop/codeprojects/llm-council/council_cli.py` exists and is executable
- `OPENROUTER_API_KEY` is set in `/Users/nomis/Desktop/codeprojects/llm-council/.env`
- `python3` available (system Python 3.9+ is fine for the CLI)
- `/Users/nomis/.claude/skills/llm-audit/skill.md` exists

If any prerequisite fails, fall back to Mode A and tell the operator at the end of the audit.

### Step 1 — Resolve inputs
- **URL**: required. If absent, halt and ask.
- **Primary intent**: prefer operator-supplied. If not supplied:
  - Look for an upstream `page-intent-analyzer` JSON sidecar referenced by the operator
  - Otherwise infer from URL slug + H1 + title and mark `intent_source: "INFERRED"` in JSON
  - **Never silently fabricate** — if no signal exists, halt with `INTENT_REQUIRED`
- **Industry mode**: detect per Step 1 of `skill.md` (HEALTHCARE / LEGAL / FINANCIAL / EDUCATIONAL / STANDARD)
- **Page type**: blog / service / location / comparison / landing / emergency / educational

### Step 2 — Get the page content

There are two cases:

**Case A — Body supplied inline (dashboard worker, programmatic invocation).** The orchestrator is told "do NOT fetch the URL; analyse the supplied markdown directly" and the article body is included in the prompt. **Skip this entire step's fetching logic.** Build `${RUN_DIR}/audit-page.md` directly from the supplied body + the frontmatter block below. This is the dashboard's `run-post-audit.ts` worker pattern when `POST_AUDIT_MODE=council`.

**Case B — URL only, must fetch.** When the operator gave only a URL (interactive `claude -p` invocation), fetch the page yourself:
```
WebFetch tool → if 403 or bot-protection page →
curl -s -L -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" "<URL>" -o /tmp/audit-page.html
→ extract <article> tag with python regex if site has bot protection
```

If the site is fully blocked (Cloudflare challenge), fall back to operator-supplied page content. Do NOT proceed without raw page text.

Either way, save the cleaned article markdown to `${RUN_DIR}/audit-page.md` with a frontmatter block:
```yaml
---
url: <URL>
page_type: <blog|service|...>
character_count_body: ~<N>
operator_supplied_intent: "<intent text>"
mode_expected: <healthcare|legal|...>
---

<article body in markdown>
```

### Step 3 — Build the bundled prompt
Write `${RUN_DIR}/audit-prompt.txt` with this structure:

```
You are running the LLM Readability Audit skill (full specification embedded below). Apply it strictly to the operator-provided web page (also embedded below).

OPERATOR-PROVIDED INFORMATION
- URL: <URL>
- Primary search intent the page is targeting: "<intent>"
- Intent source: <OPERATOR | INTENT_ANALYZER | INFERRED>
- Page type: <type>
- Industry mode expected: <MODE>

INSTRUCTIONS FOR THIS RUN
1. Apply the skill.md exactly as written. Do not improvise sections.
2. Do not ask the operator any clarifying questions — the intent is provided above; proceed.
3. Produce the full audit report in the format specified by the skill.md "Output Format" section, top to bottom.
4. After the markdown audit, emit the JSON appendix as specified, fenced as ```json. The JSON is mandatory.
5. Do not write a preamble or closing summary. Do NOT wrap your response in any outer code fence (no leading ```markdown). Begin with "📋 LLM Readability Audit" and end at the closing ``` of the JSON fence.
6. Do not include reasoning artifacts ("Correction:", "Withdrawing the flag", etc.) — silently revise if you change your mind, emit only the final audit.
7. Quote flagged sentences verbatim from the page content provided. Do not invent sentences.
8. Apply the mechanical rules: compute Zone 1 character count, run the Page-level Commoditization check, apply the gate-attribution rule, apply the auto-escalation rule for stripped-condition numeric claims in regulated modes.
9. Findings parity check before emitting: markdown ALL ISSUES count == JSON `findings[]` length == sum of `gate_diagnosis.G[1-3].issue_count` (derive the latter from `findings[].gate`, do not hand-author).

================================================================================
skill.md (the specification you must follow)
================================================================================

<contents of /Users/nomis/.claude/skills/llm-audit/skill.md>

================================================================================
PAGE CONTENT (the article to audit)
================================================================================

<contents of ${RUN_DIR}/audit-page.md>
```

Concretely:
```bash
# Build prompt header (in your text generation, not bash)
# Then:
cat /Users/nomis/.claude/skills/llm-audit/skill.md >> ${RUN_DIR}/audit-prompt.txt
printf '\n\n%s\n\n' '================================================================================' >> ${RUN_DIR}/audit-prompt.txt
printf '%s\n' 'PAGE CONTENT (the article to audit)' >> ${RUN_DIR}/audit-prompt.txt
printf '%s\n\n' '================================================================================' >> ${RUN_DIR}/audit-prompt.txt
cat ${RUN_DIR}/audit-page.md >> ${RUN_DIR}/audit-prompt.txt
```

### Step 4 — Fire Opus subagent + OpenRouter stage 1 IN PARALLEL

**Critical**: do this in a single message with two tool calls so they run concurrently, not sequentially. Both run ~1–2 min; parallel keeps wall clock at ~2 min.

**Both tool calls MUST be foreground (`run_in_background: false`).** This skill is run headless via `claude --print`, where background tasks do NOT deliver completion notifications back to the orchestrator — the turn would simply end and the background council call would be killed mid-flight, leaving `stage1-api.json` empty. Two foreground tool calls in a single message still execute concurrently, but the turn blocks until BOTH return, which is exactly what we need. Do NOT use `run_in_background: true` here.

The Anthropic council seat is filled by an Agent-tool subagent. The subagent inherits the orchestrator session's Opus class — whatever your `claude -p` default is (today: latest Opus, e.g. 4.7). This keeps the workflow simple: as long as the operator's CLI default is the latest/most useful Opus, the council automatically benefits from any future upgrade with no code change. Operator does NOT need to specify a version.

**Tool call A — Opus subagent**:
- `Agent` tool with `subagent_type: "general-purpose"`, `run_in_background: false`
- Prompt: full content of `${RUN_DIR}/audit-prompt.txt`
- End the prompt with: "Save your final audit (markdown body + JSON appendix, exactly as specified) to ${RUN_DIR}/opus-stage1.md using the Write tool. Output 'DONE' to the conversation when saved. Do not output the audit body to the conversation."
- Read your own system prompt to determine the actual version (e.g. "You are powered by the model named Opus 4.7") and use that for the injection label in Step 6 (e.g. `local/claude-opus-4-7`).

**Tool call B — council stage 1 (OpenRouter, 3 models in parallel)**:
- `Bash` tool with `run_in_background: false`
- Command: `cd /Users/nomis/Desktop/codeprojects/llm-council && python3 council_cli.py --stage 1 --file ${RUN_DIR}/audit-prompt.txt > ${RUN_DIR}/stage1-api.json 2> ${RUN_DIR}/stage1-api.err`

### Step 5 — Both calls have returned
Because both tool calls in Step 4 are foreground, the turn does not advance until both have completed — there is nothing to wait on. Before proceeding, confirm `${RUN_DIR}/opus-stage1.md` exists and `${RUN_DIR}/stage1-api.json` is non-empty. If `stage1-api.json` is empty, read `${RUN_DIR}/stage1-api.err` and surface the error rather than synthesising from a missing stage-1.

### Step 6 — Merge stage-1 results
Replace `<MODEL_LABEL>` with the version of Opus your session is actually running (read it from your system prompt — e.g. `local/claude-opus-4-7` if you're running 4.7, `local/claude-opus-4-6` if you're running 4.6). Do not invent a label that doesn't match.

```bash
python3 -c "
import json, pathlib
api = json.loads(pathlib.Path('${RUN_DIR}/stage1-api.json').read_text())['stage1']
opus = pathlib.Path('${RUN_DIR}/opus-stage1.md').read_text()
api.append({'model': '<MODEL_LABEL>', 'response': opus})
json.dump({'stage1': api}, open('${RUN_DIR}/stage1-combined.json', 'w'), ensure_ascii=False, indent=2)
print(f'Merged: {len(api)} stage-1 entries')
"
```

If the API call returned fewer than 3 entries (one model failed), proceed anyway — the council can synthesise from 3 of 4 stage-1 responses including Opus. Note the failure in your final response.

### Step 7 — Run stages 2-3 with the merged stage-1
```bash
cd /Users/nomis/Desktop/codeprojects/llm-council && python3 council_cli.py \
  --stage 23 \
  --file ${RUN_DIR}/audit-prompt.txt \
  --stage1-input ${RUN_DIR}/stage1-combined.json \
  --output full \
  > ${RUN_DIR}/audit-result.json 2> ${RUN_DIR}/audit-result.err
```

This call:
- Runs stage 2 (peer review) — the 3 OpenRouter models rank all 4 stage-1 responses anonymized
- Runs stage 3 (chairman synthesis) — Gemini-3.1-pro synthesises a final answer
- Outputs the full structured JSON

### Step 8 — Return to operator + write final logs
The synthesised audit lives at `result.stage3.response` in `${RUN_DIR}/audit-result.json`.

First, persist the operator-facing artifact:
```bash
python3 -c "
import json, pathlib
r = json.loads(pathlib.Path('${RUN_DIR}/audit-result.json').read_text())
pathlib.Path('${RUN_DIR}/final.md').write_text(r['stage3']['response'])
"
```

Then write the run manifest. The orchestrator (you) constructs this from observed timings + the audit-result.json contents:

```bash
python3 <<'PY'
import json, pathlib, datetime
run_dir = pathlib.Path("${RUN_DIR}")
result = json.loads((run_dir / 'audit-result.json').read_text())

# Parse the final synthesized JSON appendix from stage3.response (if present)
synth = result['stage3']['response']
synth_json = None
import re
m = re.search(r'```json\s*\n(.*?)\n```\s*$', synth, re.DOTALL)
if m:
    try:
        synth_json = json.loads(m.group(1))
    except Exception:
        synth_json = None

manifest = {
    "run_id": run_dir.name,
    "timestamp_utc": datetime.datetime.utcnow().isoformat() + "Z",
    "url": "<URL>",                                # fill from operator input
    "operator_intent": "<intent>",                 # fill from operator input
    "intent_source": "<OPERATOR|INTENT_ANALYZER|INFERRED>",
    "industry_mode": "<MODE>",                     # fill from audit
    "page_type": "<type>",
    "page_length_chars": <N>,                      # from audit
    "council_members": [s['model'] for s in result['stage1']],
    "chairman_model": result['stage3']['model'],
    "stage1_count": len(result['stage1']),
    "stage2_count": len(result['stage2']),
    "aggregate_rankings": result['metadata'].get('aggregate_rankings', []),
    "summary": {
        "commoditization_verdict": (synth_json or {}).get('commoditization_check', {}).get('verdict'),
        "dominant_gate": (synth_json or {}).get('gate_diagnosis', {}).get('dominant_gate'),
        "total_findings": len((synth_json or {}).get('findings', [])),
        "critical_count": sum(1 for f in (synth_json or {}).get('findings', []) if f.get('severity') == 'CRITICAL'),
    },
    "exit_status": "success",                      # set to partial/failed if any model dropped
    "files": {
        "audit_prompt": str(run_dir / 'audit-prompt.txt'),
        "audit_page": str(run_dir / 'audit-page.md'),
        "opus_stage1": str(run_dir / 'opus-stage1.md'),
        "stage1_api": str(run_dir / 'stage1-api.json'),
        "stage1_combined": str(run_dir / 'stage1-combined.json'),
        "audit_result": str(run_dir / 'audit-result.json'),
        "final_md": str(run_dir / 'final.md'),
        "orchestrator_log": str(run_dir / 'orchestrator-log.md'),
    },
}
(run_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
print(f"Manifest written: {run_dir / 'manifest.json'}")
PY
```

Then return to the operator:
- **For `claude -p` invocations**: print the synthesised markdown body (`final.md` content) to stdout, followed by a one-line footer noting the run directory: `(audit logged to ${RUN_DIR}/)`. Do not print stage-1 per-model audits unless asked.
- **For interactive invocations**: same, but offer to surface per-model variance if useful.

If the operator asked for the variance breakdown, also report:
- Aggregate rankings (`metadata.aggregate_rankings`)
- Per-model finding counts (parse `stage1[*].response` for the JSON `findings[]` arrays and tally)
- Notable disagreements (commoditization verdict, dominant gate, severity of top findings)

### Step 9 — Orchestrator log (write throughout, not just at end)

Throughout Steps 1–8, append a one-line entry to `${RUN_DIR}/orchestrator-log.md` at each milestone with a timestamp. This gives a reviewer (e.g. a future Claude session asked to debug a past run) a clear timeline of what happened.

Format:
```
## ${RUN_TS} orchestrator log

- HH:MM:SS  Step 1 — intent resolved (source: OPERATOR), mode: HEALTHCARE
- HH:MM:SS  Step 2 — page fetched via WebFetch, ~4200 chars
- HH:MM:SS  Step 3 — prompt assembled (~127KB)
- HH:MM:SS  Step 4 — fired subagent + council CLI in parallel
- HH:MM:SS  Step 5 — subagent completed
- HH:MM:SS  Step 5 — council CLI completed (3/3 models OK)
- HH:MM:SS  Step 6 — stage-1 merged (4 entries)
- HH:MM:SS  Step 7 — stage 2-3 completed
- HH:MM:SS  Step 8 — manifest + final.md written
- ERROR     ...      [if applicable]
```

Append entries with `echo` or `printf` — keep them terse. Errors get an `ERROR` prefix.

---

## File locations reference

### Static (skill/infrastructure files)

| Path | Purpose |
|---|---|
| `/Users/nomis/.claude/skills/llm-audit/skill.md` | Methodology spec (auditor instructions) |
| `/Users/nomis/.claude/skills/llm-audit/RUNNING.md` | This file (orchestration playbook) |
| `/Users/nomis/.claude/skills/llm-audit/fine-tuning/` | Council artifacts from spec-tuning sessions |
| `/Users/nomis/.claude/skills/llm-audit/runs/` | Per-run logs (one folder per audit, see below) |
| `/Users/nomis/Desktop/codeprojects/llm-council/council_cli.py` | Council CLI entry point |
| `/Users/nomis/Desktop/codeprojects/llm-council/backend/config.py` | OpenRouter model config |
| `/Users/nomis/Desktop/codeprojects/llm-council/.env` | `OPENROUTER_API_KEY` |

### Per-run (inside `${RUN_DIR}` = `/Users/nomis/.claude/skills/llm-audit/runs/<TS>-<slug>/`)

| File | Purpose |
|---|---|
| `manifest.json` | Run metadata: timestamp, URL, intent, models, timings, summary, exit status |
| `final.md` | The synthesised chairman markdown returned to the operator |
| `audit-prompt.txt` | Bundled prompt (skill.md + page + intent) |
| `audit-page.md` | Cleaned page content with frontmatter |
| `opus-stage1.md` | Opus subagent's audit output |
| `stage1-api.json` | OpenRouter stage-1 results (3 models) |
| `stage1-combined.json` | Merged stage-1 (3 OpenRouter + 1 Opus) |
| `audit-result.json` | Full council JSON (stage1 + stage2 + stage3 + metadata) |
| `orchestrator-log.md` | Timestamped narrative of orchestrator decisions / errors |

---

## How to review past runs (for a future Claude session)

The operator may ask: "review the audit I just ran from localhost" or "what did the audit on URL X find" without prior context.

1. **List recent runs**:
   ```bash
   ls -lt /Users/nomis/.claude/skills/llm-audit/runs/ | head -10
   ```
   Each entry is a directory named `<YYYYMMDD-HHMMSS>-<sanitized-domain>`.

2. **Read the manifest first** — it's the cheap summary:
   ```bash
   cat /Users/nomis/.claude/skills/llm-audit/runs/<run_id>/manifest.json
   ```
   Tells you the URL, intent, council members, summary verdict, exit status.

3. **For the human-readable audit**, read `final.md`. For the operator's verbatim view of what was returned, that's the file.

4. **For variance analysis across models**, read `stage1-combined.json` — contains all 4 stage-1 audits (one per council member). Compare flagged sentences, severity distributions, commoditization verdicts.

5. **For chairman synthesis details and peer rankings**, read `audit-result.json` — has full stage 2 and stage 3 plus aggregate rankings.

6. **For orchestrator debugging** (parallel timing, errors, retries), read `orchestrator-log.md`.

7. **If a past run failed or was partial**, the manifest's `exit_status` will be `partial` or `failed`. Check `orchestrator-log.md` for the `ERROR` lines and the relevant `*.err` files (e.g. `stage1-api.err`).

If the operator asks "review the last run" without specifying which, use the most recent directory by mtime.

---

## Council composition (current as of 2026-05-10)

| Slot | Model | Family | Source | Cost ($/M prompt) |
|---|---|---|---|---|
| 1 | `local/claude-opus-<version>` | Anthropic | Claude Code subagent (no API call) | $0 |
| 2 | `z-ai/glm-5` | ZhipuAI | OpenRouter | $0.60 |
| 3 | `mistralai/mistral-medium-3-5` | Mistral | OpenRouter | $1.50 |
| 4 | `deepseek/deepseek-v4-flash` | DeepSeek | OpenRouter | $0.14 |
| Chairman | `google/gemini-3.1-pro-preview` | Google | OpenRouter | $2.00 |

**Total per audit: ~$4.24/M tokens** (down from $11.99/M before optimization).

**On the Anthropic seat:** the subagent inherits the orchestrator session's Opus class (the operator's `claude -p` default — typically latest Opus). Output variance between adjacent Opus versions is small relative to cross-family variance, so locking the council seat to "whatever the operator's default Opus is" gives automatic upgrades without complexity.

If the operator ever needs a specific older version for a paid OpenRouter comparison run, add `anthropic/claude-opus-4.X` back to `COUNCIL_MODELS` in `config.py`. That makes the council 5 members (free subagent + paid OpenRouter slot).

---

## Failure modes and recovery

- **OpenRouter 402 Payment Required**: top up credits; the cheap models cost pennies but two API calls fail clean rather than partially. Fall back to Mode A if no credits.
- **Subagent timeout**: subagent should complete in ~2 min on a typical page. If still running after 5 min, cancel and proceed with 3-of-4 council members.
- **Site has Cloudflare protection**: WebFetch returns 403 → curl with browser UA → if still blocked, ask operator to paste the article text.
- **Spec-discipline violation in a stage-1 response**: noted in the variance report but does not block the run. The chairman synthesis tolerates one drifting member.
- **All 3 OpenRouter models fail**: Mode B is impossible. Fall back to Mode A using only the Opus subagent's audit.

---

## What `claude -p` operators can pass

The operator's prompt should contain at minimum a URL. Optional but useful:
- A primary intent string (`intent: "..."`)
- A page type (`type: blog`)
- A request for variance analysis (`with variance breakdown`)
- A reference to a `page-intent-analyzer` sidecar

If only a URL is given, infer the rest with the rules in Step 1. The Anthropic council seat always uses the orchestrator's Opus class (operator's CLI default), so no version specification is needed.
