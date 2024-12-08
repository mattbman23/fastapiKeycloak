from ibm_watson_machine_learning.foundation_models import Model
from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from pydantic import BaseModel
from utils.config import WX_API_KEY, WX_PROJECT_ID, WX_URL


class InputRequest(BaseModel):
    text: str


router = APIRouter(prefix="/wxai", tags=["wxai"])

model = Model(
    model_id="ibm/granite-3-8b-instruct",
    params={
        "decoding_method": "sample",
        "temperature": 0,
        "top_p": 1,
        "top_k": 10,
        "random_seed": 42,
        "max_new_tokens": 100,
        "repetition_penalty": 1,
    },
    credentials={
        "url": WX_URL,
        "apikey": WX_API_KEY,
    },
    project_id=WX_PROJECT_ID,
)


@router.post("/generate_text")
def general_llm(input: InputRequest):
    generated_response = model.generate_text(input.text)
    return generated_response


@router.post("/generate_text_stream")
def general_llm(input: InputRequest):
    return StreamingResponse(
        model.generate_text_stream(prompt=input.text),
        media_type="text/event-stream",
    )
