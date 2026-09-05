## V5 update: revision flow, source reputation, and SHA-256 evidence binding

This version addresses the latest steward request.

### Changes

- `needs_revision` is no longer terminal.
- Revised evidence can be submitted again through a new commit-pinned evidence URL.
- Duplicate evidence is still blocked by canonical URL and SHA-256 content digest.
- The contract no longer treats the submitter as an authenticated participant.
- The project uses a source reputation model:
  - anyone may nominate public evidence;
  - points are assigned to the derived GitHub source identity;
  - a real integrating platform must authenticate the user with GitHub before mapping source reputation to participant XP.
- The contract now requires commit-pinned raw GitHub URLs instead of mutable branch URLs.
- The contract uses SHA-256 content digest instead of a 32-bit FNV-style digest.
- The moderation prompt fences user-controlled evidence inside an untrusted evidence block to reduce prompt injection risk.
- Reward points are incremental: a revised approved submission only adds the improvement over the previous best reward for the same source identity and quest.

### Product model

This contract is not a standalone quest platform. It is a GenLayer-powered review layer.

A quest platform can use it like this:

1. Authenticate a user with GitHub.
2. Confirm that the authenticated GitHub identity matches the submitted GitHub source identity.
3. Submit a commit-pinned raw GitHub evidence URL to the contract.
4. Read the contract decision.
5. Apply product logic such as approval, revision request, XP, badge eligibility, leaderboard update, or spam flagging.


## CommunityQuestModerator V4

This version addresses the latest steward request by tightening source identity binding and duplicate prevention.

## How people use this product

GenLayer Community Quest Moderator is used as a decision layer for community quest platforms.

It is not a standalone app and it is not something that is randomly attached to any product. It is integrated into the point where a platform needs to review a user's quest evidence before giving XP, badges, leaderboard points, or moderation results.

A typical workflow is:

1. A quest platform creates a campaign.
2. A participant submits a public evidence URL.
3. The platform calls `review_submission`.
4. The GenLayer contract fetches and reviews the evidence.
5. Validators independently reassess the same evidence.
6. The contract stores a structured decision.
7. The platform reads the decision using `get_submission`.
8. The platform uses the result to approve, reject, request revision, give XP, issue a badge, or update a leaderboard.

More details:

- `docs/product-usage.md`
- `examples/quest-platform-workflow.md`
### Key V4 improvements

- Removed caller-supplied `author` from the contract workflow.
- The contract now derives `source_identity` from the raw GitHub evidence URL.
- Persistent points are assigned to the derived source identity, not to an unverified caller-provided author string.
- The contract fetches the actual public evidence URL and validates the fetched content.
- Validators independently refetch the same evidence and rerun the same moderation task.
- Validators compare stable fields:
  - source_identity
  - canonical_url
  - content_digest
  - moderation
  - derived status
  - derived reward points
  - score tolerance
- Reward points are derived deterministically from validated status, score, and moderation.
- Duplicate farming is blocked by:
  - canonical evidence URL
  - evidence content digest
  - source identity plus quest claim
- The evidence file explains that the system does not claim real-world authorship. It binds the review to a source identity derived from the GitHub repository URL.

### Workflow

1. A user submits a quest name and public raw GitHub evidence URL.
2. The contract canonicalizes the URL.
3. The contract derives a source identity from the URL.
4. The contract fetches the evidence content.
5. The LLM evaluates the fetched evidence.
6. Validators refetch the same evidence and rerun the same evaluation.
7. The contract compares stable decision fields.
8. The contract derives status and reward points deterministically.
9. The submission is stored as a durable record.
10. Approved submissions update points for the derived source identity.
