## V4 Steward Request Fix

This version addresses the latest steward request.

### Authorship / source identity fix

The previous version checked whether the submitted author string appeared in the fetched content. This did not prove that the submitter actually owned or authored the evidence.

V4 removes caller-supplied `author` from the workflow. The contract now derives a source identity directly from the raw GitHub evidence URL.

Example:

`https://raw.githubusercontent.com/lam050/genlayer-community-post-reviewer/main/evidence/sample-community-post.md`

becomes:

`github:lam050/genlayer-community-post-reviewer`

Persistent points are assigned to this derived source identity, not to an unverified author label.

### Duplicate prevention fix

V4 adds duplicate prevention using:

- canonical evidence URL
- content digest
- source identity plus quest claim

This prevents the same evidence from being reviewed repeatedly through query-string or URL aliases.

### Consensus workflow

Validators independently refetch the same evidence URL and rerun the same moderation task. The contract compares stable fields:

- source_identity
- canonical_url
- content_digest
- moderation
- derived status
- derived reward points
- score tolerance

### Methods tested

- `review_submission`
- `get_submission`
- `get_source_points`
- `is_url_reviewed`
- `is_content_digest_reviewed`
- `get_next_submission_id`

### Screenshots

- screenshots/moderator-v4-deploy-finalized.png
- screenshots/review-submission-v4-finalized.png
- screenshots/submission-record-v4.png
- screenshots/source-points-v4.png
- screenshots/url-reviewed-v4.png
