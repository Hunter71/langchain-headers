from fastapi import FastAPI, Request, Header
from google.generativeai.types.answer_types import FinishReason
from pydantic import BaseModel

RESPONSE_TEXT = (
    "Maria Salomea Skłodowska-Curie, known simply as Marie Curie, "
    "was a Polish and naturalised-French physicist and chemist "
    "who conducted pioneering research on radioactivity."
    "She was the first woman to win a Nobel Prize, "
    "the first person to win a Nobel Prize twice, "
    "and the only person to win a Nobel Prize in two scientific fields."
    # source: https://en.wikipedia.org/wiki/Marie_Curie
)

app = FastAPI()


class Content(BaseModel):
    text: str


class ContentPart(BaseModel):
    parts: list[Content]
    role: str


class RequestBody(BaseModel):
    contents: list[ContentPart]


@app.get("/")
async def live():
    return {"hello": "world!"}


@app.post("/{version}/models/{model}")
async def chat_gemini(
    request: Request,
    version: str,
    model: str,
    body: RequestBody,
    user_custom_param_1: str = Header(..., alias="X-User-Header"),
    user_custom_param_2: str = Header(..., alias="X-User-Header2"),
):
    return {
        "candidates": [
            {
                "content": {"parts": [{"text": RESPONSE_TEXT}], "role": "model"},
                "finish_reason": FinishReason.STOP,
                "safety_ratings": [],
                "token_count": 0,
                "grounding_attributions": []
            }
        ],
    }
