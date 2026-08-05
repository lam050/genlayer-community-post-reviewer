## LLM-backed Community Post Reviewer

### Purpose

This contract demonstrates a meaningful GenLayer use case by using an LLM-backed decision to review whether a community post is a valid GenLayer contribution.

### Contract

Contract file: contracts/community_post_reviewer.py  
Contract name: CommunityPostReviewer  

### Workflow

1. A user submits a community post text to the contract.
2. The contract asks an LLM to evaluate the post.
3. Validators verify whether the LLM output satisfies the stated criteria.
4. The accepted decision is stored in contract state.
5. The decision can be read through `get_decision`.

### Methods Used

- `review_post`: write method that triggers the LLM-backed evaluation.
- `get_reviewed_post`: read method that returns the submitted post.
- `get_decision`: read method that returns the accepted review result.

### Test Input

GenLayer is building an AI-powered blockchain infrastructure for Intelligent Contracts.

Unlike normal smart contracts that only execute fixed rules, GenLayer can use AI validators to reason about real-world information, language, and evidence.

This can unlock use cases such as AI agent commerce, prediction markets, decentralized verification, and dispute resolution.

### Result

Decision result: APPROVED / REJECTED according to validator consensus.

### Screenshots

- screenshots/llm-review-deploy.png
- screenshots/llm-review-decision.png
