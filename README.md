## CommunityQuestModerator V4

This version addresses the latest steward request by tightening source identity binding and duplicate prevention.

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
