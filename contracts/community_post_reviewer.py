# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }

from genlayer import *
import typing


class CommunityPostReviewer(gl.Contract):
    reviewed_post: str
    decision: str

    def __init__(self):
        self.reviewed_post = ""
        self.decision = ""

    @gl.public.write
    def review_post(self, post_text: str) -> typing.Any:
        def get_input() -> str:
            return f"""
            Review this GenLayer community post:

            {post_text}
            """

        result = gl.eq_principle.prompt_non_comparative(
            get_input,
            task="""
            Decide whether the submitted post is a valid GenLayer community contribution.
            Return one short result starting with APPROVED or REJECTED, followed by a brief reason.
            """,
            criteria="""
            The result must evaluate whether the post:
            - explains GenLayer or Intelligent Contracts in a meaningful way
            - mentions at least one relevant use case such as AI agents, dispute resolution,
              prediction markets, decentralized verification, or web-based adjudication
            - is coherent and useful for a real community audience
            - is not only low-effort airdrop/token spam
            - begins with APPROVED or REJECTED and includes a short reason
            """
        )

        self.reviewed_post = post_text
        self.decision = result

    @gl.public.view
    def get_reviewed_post(self) -> str:
        return self.reviewed_post

    @gl.public.view
    def get_decision(self) -> str:
        return self.decision
