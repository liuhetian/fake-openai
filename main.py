from fastapi import FastAPI, Request, status, HTTPException, Depends
from fastapi.responses import StreamingResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# for completion
@app.post("/chat/completions")
@app.post("/v1/chat/completions")
async def completion(request: Request):
    data = await request.json()

    if data.get("stream") == True:
        response_id = uuid.uuid4().hex
        sentence = "Hello this is a test response from a fixed OpenAI endpoint."
        words = sentence.split(" ")

        async def stream_response():
            for i, word in enumerate(words):
                chunk = {
                    "id": f"chatcmpl-{response_id}",
                    "object": "chat.completion.chunk",
                    "created": 1677652288,
                    "model": "gpt-3.5-turbo-0125",
                    "choices": [{"index": 0, "delta": {"content": word}}],
                }
                yield json.dumps(chunk, indent=4).encode()
                await asyncio.sleep(0.0001)  # For demo purpose

        return StreamingResponse(stream_response(), media_type="text/event-stream")

    else:
        response_id = uuid.uuid4().hex
        response = {
            "id": f"chatcmpl-{response_id}",
            "object": "chat.completion",
            "created": 1677652288,
            "model": "gpt-3.5-turbo-0125",
            "system_fingerprint": "fp_44709d6fcb",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "\n\nHello there, how may I assist you today?",
                    },
                    "logprobs": None,
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 9, "completion_tokens": 12, "total_tokens": 21},
        }
        return response



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)