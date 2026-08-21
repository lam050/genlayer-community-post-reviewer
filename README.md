## CommunityQuestModerator V3

This corrected version addresses the steward request by improving the consensus and reward workflow.

### Key improvements

- Validators rerun the same moderation task instead of only checking the leader output format.
- Validators compare stable decision fields:
  - moderation
  - derived status
  - derived reward points
  - score tolerance
- Reward points are derived deterministically from the validated status and score.
- The LLM no longer chooses reward points independently.
- Each submission is stored as a durable per-submission record.
- Repeated reward farming is prevented by checking:
  - duplicate evidence URL
  - duplicate author plus quest claim
- The contract fetches the actual public evidence URL instead of trusting caller-supplied post text.
- Authorship binding is enforced by requiring the fetched evidence to include the submitted author and quest name.

### Workflow

1. The user submits an author, quest name, and public evidence URL.
2. The contract fetches the evidence content from the URL.
3. The LLM evaluates the fetched content and returns only score, moderation, and reason.
4. The validator fetches the same evidence and reruns the same evaluation.
5. The contract compares stable decision fields.
6. The contract derives status and reward points deterministically.
7. The result is stored in a durable submission record.
8. Approved submissions update the author's internal reward points.
