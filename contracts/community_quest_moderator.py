# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *


class CommunityQuestModerator(gl.Contract):
    next_submission_id: u32
    submissions: TreeMap[str, str]
    source_points: TreeMap[str, u32]
    reviewed_canonical_urls: TreeMap[str, str]
    reviewed_content_digests: TreeMap[str, str]
    source_quest_claims: TreeMap[str, str]

    def __init__(self):
        self.next_submission_id = u32(1)

    def _canonicalize_url(self, evidence_url: str) -> str:
        clean_url = evidence_url.strip()
        clean_url = clean_url.split("#")[0]
        clean_url = clean_url.split("?")[0]
        return clean_url

    def _source_identity_from_url(self, canonical_url: str) -> str:
        prefix = "https://raw.githubusercontent.com/"

        if not canonical_url.startswith(prefix):
            raise gl.UserError("Evidence URL must be a raw GitHub content URL.")

        path = canonical_url[len(prefix):]
        parts = path.split("/")

        if len(parts) < 4:
            raise gl.UserError("Raw GitHub URL must include owner, repo, branch, and file path.")

        owner = parts[0].lower()
        repo = parts[1].lower()

        return "github:" + owner + "/" + repo

    def _source_quest_key(self, source_identity: str, quest_name: str) -> str:
        return source_identity.strip().lower() + "|" + quest_name.strip().lower()

    def _content_digest(self, content: str) -> str:
        h = 2166136261

        for ch in content:
            h = h ^ ord(ch)
            h = (h * 16777619) % 4294967296

        return str(h) + ":" + str(len(content))

    def _derive_status(self, score: int, moderation: str) -> str:
        moderation = str(moderation).lower()

        if moderation in ["spam", "off_topic"]:
            return "rejected"

        if moderation == "low_effort":
            return "needs_revision"

        if score >= 75:
            return "approved"

        if score >= 50:
            return "needs_revision"

        return "rejected"

    def _derive_reward_points(self, status: str, score: int, moderation: str) -> u32:
        status = str(status).lower()
        moderation = str(moderation).lower()

        if status != "approved":
            return u32(0)

        if moderation != "clean":
            return u32(0)

        if score >= 90:
            return u32(100)

        if score >= 80:
            return u32(75)

        return u32(50)

    def _validate_decision(self, data) -> bool:
        if not isinstance(data, dict):
            return False

        moderation = str(data.get("moderation", "")).lower()
        reason = str(data.get("reason", ""))
        source_identity = str(data.get("source_identity", ""))
        canonical_url = str(data.get("canonical_url", ""))
        content_digest = str(data.get("content_digest", ""))

        try:
            score = int(data.get("score", -1))
        except Exception:
            return False

        if not source_identity.startswith("github:"):
            return False

        if not canonical_url.startswith("https://raw.githubusercontent.com/"):
            return False

        if ":" not in content_digest:
            return False

        if moderation not in ["clean", "low_effort", "spam", "off_topic"]:
            return False

        if score < 0 or score > 100:
            return False

        if len(reason) < 20 or len(reason) > 300:
            return False

        return True

    @gl.public.write
    def review_submission(
        self,
        quest_name: str,
        evidence_url: str
    ) -> u32:
        canonical_url = self._canonicalize_url(evidence_url)
        source_identity = self._source_identity_from_url(canonical_url)
        source_quest_key = self._source_quest_key(source_identity, quest_name)

        if self.reviewed_canonical_urls.get(canonical_url.lower(), "") == "reviewed":
            raise gl.UserError("This canonical evidence URL has already been reviewed.")

        if self.source_quest_claims.get(source_quest_key, "") == "claimed":
            raise gl.UserError("This source identity has already claimed this quest.")

        submission_id = self.next_submission_id

        def leader_fn():
            response = gl.nondet.web.get(canonical_url)
            evidence_text = response.body.decode("utf-8")

            if len(evidence_text) < 120:
                raise gl.UserError("Evidence content is too short.")

            if quest_name.lower() not in evidence_text.lower():
                raise gl.UserError("Evidence does not include the submitted quest name.")

            fetched_digest = self._content_digest(evidence_text)
            fetched_source_identity = self._source_identity_from_url(canonical_url)

            prompt = f"""
You are reviewing a GenLayer community quest submission.

The contract fetched the evidence from this public URL:
{canonical_url}

The source identity is derived from the raw GitHub URL:
{fetched_source_identity}

Quest name:
{quest_name}

Fetched evidence content:
{evidence_text}

Evaluate the quality of this submission.

Return ONLY a JSON object with exactly these keys:
- score: integer from 0 to 100
- moderation: one of "clean", "low_effort", "spam", "off_topic"
- reason: short explanation between 20 and 300 characters

Evaluation rules:
- High score requires a clear explanation of GenLayer or Intelligent Contracts.
- High score requires at least one relevant use case such as AI agents, dispute resolution, prediction markets, decentralized verification, community moderation, or evidence-based adjudication.
- "clean" means useful and relevant.
- "low_effort" means related but too vague or incomplete.
- "spam" means promotional spam, airdrop farming spam, or meaningless content.
- "off_topic" means not about GenLayer or relevant use cases.
"""
            llm_decision = gl.nondet.exec_prompt(prompt, response_format="json")

            if not isinstance(llm_decision, dict):
                raise gl.UserError("LLM did not return a JSON object.")

            return {
                "source_identity": fetched_source_identity,
                "canonical_url": canonical_url,
                "content_digest": fetched_digest,
                "score": llm_decision.get("score"),
                "moderation": llm_decision.get("moderation"),
                "reason": llm_decision.get("reason")
            }

        def validator_fn(leader_result) -> bool:
            if not isinstance(leader_result, gl.vm.Return):
                return False

            leader_decision = leader_result.calldata

            if not self._validate_decision(leader_decision):
                return False

            validator_decision = leader_fn()

            if not self._validate_decision(validator_decision):
                return False

            leader_score = int(leader_decision["score"])
            validator_score = int(validator_decision["score"])

            leader_moderation = str(leader_decision["moderation"]).lower()
            validator_moderation = str(validator_decision["moderation"]).lower()

            leader_status = self._derive_status(leader_score, leader_moderation)
            validator_status = self._derive_status(validator_score, validator_moderation)

            leader_reward = int(self._derive_reward_points(leader_status, leader_score, leader_moderation))
            validator_reward = int(self._derive_reward_points(validator_status, validator_score, validator_moderation))

            if leader_decision["source_identity"] != validator_decision["source_identity"]:
                return False

            if leader_decision["canonical_url"] != validator_decision["canonical_url"]:
                return False

            if leader_decision["content_digest"] != validator_decision["content_digest"]:
                return False

            if leader_moderation != validator_moderation:
                return False

            if leader_status != validator_status:
                return False

            if leader_reward != validator_reward:
                return False

            if abs(leader_score - validator_score) > 15:
                return False

            return True

        decision = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)

        score = int(decision["score"])
        moderation = str(decision["moderation"]).lower()
        reason = str(decision["reason"])
        final_source_identity = str(decision["source_identity"])
        final_canonical_url = str(decision["canonical_url"])
        final_content_digest = str(decision["content_digest"])

        if self.reviewed_content_digests.get(final_content_digest, "") == "reviewed":
            raise gl.UserError("This evidence content has already been reviewed.")

        status = self._derive_status(score, moderation)
        reward_points = self._derive_reward_points(status, score, moderation)

        record = (
            "submission_id=" + str(submission_id) + "\n"
            + "source_identity=" + final_source_identity + "\n"
            + "quest_name=" + quest_name + "\n"
            + "canonical_url=" + final_canonical_url + "\n"
            + "content_digest=" + final_content_digest + "\n"
            + "status=" + status + "\n"
            + "score=" + str(score) + "\n"
            + "reward_points=" + str(reward_points) + "\n"
            + "moderation=" + moderation + "\n"
            + "reason=" + reason
        )

        self.submissions[str(submission_id)] = record
        self.reviewed_canonical_urls[final_canonical_url.lower()] = "reviewed"
        self.reviewed_content_digests[final_content_digest] = "reviewed"
        self.source_quest_claims[source_quest_key] = "claimed"

        if status == "approved":
            current_points = self.source_points.get(final_source_identity, u32(0))
            self.source_points[final_source_identity] = u32(int(current_points) + int(reward_points))

        self.next_submission_id = u32(int(self.next_submission_id) + 1)

        return submission_id

    @gl.public.view
    def get_submission(self, submission_id: u32) -> str:
        return self.submissions.get(str(submission_id), "Submission not found")

    @gl.public.view
    def get_source_points(self, source_identity: str) -> u32:
        return self.source_points.get(source_identity, u32(0))

    @gl.public.view
    def get_next_submission_id(self) -> u32:
        return self.next_submission_id

    @gl.public.view
    def is_url_reviewed(self, evidence_url: str) -> str:
        canonical_url = self._canonicalize_url(evidence_url)
        return self.reviewed_canonical_urls.get(canonical_url.lower(), "not_reviewed")

    @gl.public.view
    def is_content_digest_reviewed(self, content_digest: str) -> str:
        return self.reviewed_content_digests.get(content_digest, "not_reviewed")
