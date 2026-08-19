## Corrected Project: Community Quest Moderator

The previous version was rejected because it only stored a single global verdict and did not include durable per-post records, moderation, eligibility, reward consequence, or explicit output parsing.

This corrected version adds a new contract:

`contracts/community_quest_moderator.py`

## Improvements

- Durable per-post records using submission IDs.
- Explicit output parsing into structured fields:
  - status
  - score
  - reward_points
  - moderation
  - reason
- Eligibility decision:
  - approved
  - needs_revision
  - rejected
- Moderation decision:
  - clean
  - low_effort
  - spam
  - off_topic
- Reward consequence:
  - approved posts update author reward points.
- Real community workflow:
  - review a GenLayer Special Quest post.
  - store the validated decision.
  - allow users to query submission records and author points.

## Methods Tested

- `review_submission`
- `get_submission`
- `get_author_points`
- `get_next_submission_id`

## Screenshots

- screenshots/moderator-deploy-finalized.png
- screenshots/review-submission-finalized.png
- screenshots/submission-record.png
- screenshots/author-points.png
