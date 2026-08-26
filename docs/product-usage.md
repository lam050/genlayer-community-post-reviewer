# Product Usage: GenLayer Community Quest Moderator

## What is this product?

GenLayer Community Quest Moderator is a reusable adjudication module for community quest platforms.

It is designed to sit between a user's submitted evidence and the final reward or leaderboard update.

It is not meant to be randomly "latched onto" every application. Instead, it is used as a verification checkpoint for workflows where a community team needs to decide whether a submitted post, proof, or quest entry should be approved, rejected, or sent back for revision.

## Who uses it?

There are three main users:

1. Quest organizers  
   Community teams, campaign managers, or ecosystem programs that need to review submissions.

2. Participants  
   Users who submit public evidence for a quest, such as a GitHub evidence file, social post, article, tutorial, or campaign proof.

3. Frontend or backend integrators  
   Quest platforms, dashboards, or campaign apps that call the contract, read the decision, and update their own UI, leaderboard, badge, or reward system.

## Where does it fit in a product workflow?

The contract is used after a participant submits evidence and before a reward is granted.

Typical flow:

1. A campaign defines a quest and evidence format.
2. A participant creates public evidence.
3. The quest platform submits the quest name and evidence URL to the contract.
4. The contract fetches the public evidence.
5. The LLM evaluates the evidence.
6. Validators independently refetch the same evidence and reassess the result.
7. The contract stores a durable decision record.
8. The frontend or backend reads the result.
9. The platform uses the result to approve, reject, request revision, update points, issue a badge, or update a leaderboard.

## What does the contract take as input?

The contract takes:

- `quest_name`: the name of the quest being reviewed.
- `evidence_url`: a public raw GitHub evidence URL.

The contract does not trust a caller-supplied author string. Instead, it derives a source identity from the evidence URL.

Example:

```text
https://raw.githubusercontent.com/lam050/genlayer-community-post-reviewer/main/evidence/sample-community-post.md
