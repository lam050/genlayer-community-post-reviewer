## V3 Steward Request Fix

This version addresses the steward request from Aug 21, 2026.

### Fixes added

1. Validator reruns the same moderation task:
   - `validator_fn` now calls `leader_fn()` again.
   - It compares stable decision fields instead of only validating structure.

2. Deterministic reward derivation:
   - The LLM only returns `score`, `moderation`, and `reason`.
   - The contract derives `status` and `reward_points` deterministically.

3. Consistency enforcement:
   - Spam or off-topic content always becomes rejected.
   - Low-effort content becomes needs_revision.
   - Approved content must be clean and high-score.
   - Reward points are only granted for approved clean submissions.

4. Repeat farming prevention:
   - Duplicate `evidence_url` is blocked.
   - Duplicate `author + quest_name` claim is blocked.

5. Authorship and evidence binding:
   - The contract fetches the actual `evidence_url`.
   - The fetched evidence must include the submitted author and quest name.
   - The contract no longer trusts caller-supplied post text.

### Methods tested

- `review_submission`
- `get_submission`
- `get_author_points`
- `get_next_submission_id`
- `is_evidence_reviewed`

### Screenshots

- screenshots/moderator-v3-deploy-finalized.png
- screenshots/review-submission-v3-finalized.png
- screenshots/submission-record-v3.png
- screenshots/author-points-v3.png
- screenshots/duplicate-prevention-v3.png
