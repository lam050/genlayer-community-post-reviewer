## GenLayer Community Quest Moderator

This repository includes a stronger GenLayer Intelligent Contract called `CommunityQuestModerator`.

The contract demonstrates a real community workflow for reviewing quest submissions:

1. A user submits a community post with author, quest name, post URL, and post text.
2. The contract uses an LLM-backed decision to evaluate the submission.
3. Validators independently verify the decision using the same evidence and criteria.
4. The result is parsed into explicit output fields:
   - status
   - score
   - reward_points
   - moderation
   - reason
5. Each post is stored as a durable per-submission record.
6. Approved submissions update the author's internal reward points.

This project demonstrates GenLayer's value for subjective, language-based, and evidence-based community moderation workflows.
