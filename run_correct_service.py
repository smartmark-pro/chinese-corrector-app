import logging
import torch
import json
from starlette.middleware.cors import CORSMiddleware

# 纠错模型单独启动一个内部服务

from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware


from typing import List, Union
from pydantic import BaseModel


from contextlib import asynccontextmanager
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        torch.cuda.ipc_collect()
app = FastAPI(lifespan=lifespan, openapi_url=None, title="模型服务")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health() -> Response:
    """Health check."""
    return Response(status_code=200, content="{}")
# sys.path.append('../..')
from pycorrector import NaSGECBartCorrector
from pycorrector.utils.sentence_utils import is_not_chinese_error

bc = NaSGECBartCorrector()

class CustomRequest(BaseModel):
    method:str
    length: int
    input: str
    username: str
    token: str
    requestid: str


@app.post("/app/corrector/v1/corrector")
async def step(request: CustomRequest):
    # 模型结果后处理
    result = bc.correct(request.input,ignore_function=is_not_chinese_error, max_length=request.length)
    print(result)
    return Response(status_code=200, content=json.dumps(result))



if __name__ == "__main__":
    import logging
    import uvicorn

    logger = logging.getLogger("server")
    logger.info("start ...")

    uvicorn.run(app="run_correct_service:app", host="0.0.0.0", port=9045, reload=False, workers=1)