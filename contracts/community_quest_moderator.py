# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import typing
import json


class CommunityQuestModerator(gl.Contract):
    next_submission_id: int
    submissions: dict
    author_points: dict

    def __init__(self):
        self.next_submission_id = 1
        self.submissions = {}
        self.author_points = {}

    def _is_valid_decision(self, data: typing.Any) -> bool:
        try:
            status = str(data.get("status", "")).lower()
            moderation = str(data.get("moderation", "")).lower()
            score = int(data.get("score", -1))
            reward_points = int(data.get("reward_points", -1))
            reason = str(data.get("reason", ""))

            return (
                status in ["approved", "needs_revision", "rejected"]
                and moderation in ["clean", "low_effort", "spam", "off_topic"]
                and 0 <= score <= 100
                and reward_points in [0, 25, 50, 75, 100]
                and len(reason) >= 20
                and len(reason) <= 300
            )
        except Exception:
            return False

    @gl.public.write
    def review_submission(
        self,
        author: str,
        quest_name: str,
        post_url: str,
        post_text: str
    ) -> int:
        submission_id = self.next_submission_id

        def leader_fn():
            prompt = f"""
You are reviewing a GenLayer community quest submission.

Quest name:
{quest_name}

Author:
{author}

Post URL:
{post_url}

Submitted post text:
{post_text}

Evaluate whether this post should be accepted for a GenLayer community quest.

Return ONLY a JSON object with exactly these keys:
- status: one of "approved", "needs_revision", "rejected"
- score: integer from 0 to 100
- reward_points: one of 0, 25, 50, 75, 100
- moderation: one of "clean", "low_effort", "spam", "off_topic"
- reason: short explanation between 20 and 300 characters

Evaluation rules:
- approved: the post clearly explains GenLayer or Intelligent Contracts and includes at least one relevant use case.
- needs_revision: the post is related to GenLayer but too vague or missing important details.
- rejected: the post is off-topic, spammy, misleading, or only talks about token/airdrop farming.
- reward_points must reflect quality and usefulness.
- high score requires clear explanation, relevant use case, and useful community value.
"""
            return gl.nondet.exec_prompt(prompt, response_format="json")

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            leader_decision = leader_result.calldata

            if not self._is_valid_decision(leader_decision):
                return False

            validator_decision = leader_fn()

            if not self._is_valid_decision(validator_decision):
                return False

            try:
                leader_status = str(leader_decision["status"]).lower()
                validator_status = str(validator_decision["status"]).lower()

                leader_moderation = str(leader_decision["moderation"]).lower()
                validator_moderation = str(validator_decision["moderation"]).lower()

                leader_reward = int(leader_decision["reward_points"])
                validator_reward = int(validator_decision["reward_points"])

                leader_score = int(leader_decision["score"])
                validator_score = int(validator_decision["score"])

                return (
                    leader_status == validator_status
                    and leader_moderation == validator_moderation
                    and leader_reward == validator_reward
                    and abs(leader_score - validator_score) <= 20
                )
            except Exception:
                return False

        decision = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        status = str(decision["status"]).lower()
        score = int(decision["score"])
        reward_points = int(decision["reward_points"])
        moderation = str(decision["moderation"]).lower()
        reason = str(decision["reason"])

        record = {
            "submission_id": submission_id,
            "author": author,
            "quest_name": quest_name,
            "post_url": post_url,
            "post_text": post_text,
            "status": status,
            "score": score,
            "reward_points": reward_points,
            "moderation": moderation,
            "reason": reason
        }

        self.submissions[str(submission_id)] = json.dumps(record, sort_keys=True)

        if status == "approved":
            current_points = int(self.author_points.get(author, 0))
            self.author_points[author] = current_points + reward_points

        self.next_submission_id = self.next_submission_id + 1

        return submission_id

    @gl.public.view
    def get_submission(self, submission_id: int) -> str:
        return self.submissions.get(str(submission_id), "Submission not found")

    @gl.public.view
    def get_author_points(self, author: str) -> int:
        return int(self.author_points.get(author, 0))

    @gl.public.view
    def get_next_submission_id(self) -> int:
        return self.next_submission_id
