"""Define types 
"""
from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class QueryBody(BaseModel):
    query: str
    user_id: str
    query_type: Literal["kendra", "llm"]


class SearchCondition(BaseModel):
    hogehoge: str


class RinnaModelKwargs(BaseModel):
    max_new_tokens: int = Field(128)
    temperature: float = Field(0.3)
    do_sample: bool = Field(True)
    pad_token_id: int = Field(0)
    bos_token_id: int = Field(2)
    eos_token_id: int = Field(3)


class RinnaPlaygroundReqBody(BaseModel):
    query: str = Field(None, description="ユーザーからの質問内容を指定する")
    input_template: str = Field(
        """AIは資料から抜粋して質問に答えます。資料にない内容は答えず「わかりません」と答えます。
{context}
上記の資料に基づき以下の質問について資料から抜粋して回答してください。資料にない内容は答えず「わかりません」と答えてください。
""",
        description=(
            "Rinna の input に入れたい文字列を入力する。 {context} と"
            " {question} と入れることで Kendra の検索結果およびユーザーの質問内容を入れることができる。"
        ),
    )
    instruction_template: str = Field(
        "{question}",
        description=(
            "Rinna の instruction に入れたい文字列を入力する。 {context} と"
            " {question} と入れることで Kendra の検索結果およびユーザーの質問内容を入れることができる。"
        ),
    )
    model_kwargs: RinnaModelKwargs


class KendraDocument(BaseModel):
    excerpt: str
    title: str = Field(description="ドキュメントのタイトル. QUESTION_ANSWER の場合は質問文がここに入る想定")
    content: str
    type: Literal["DOCUMENT", "QUESTION_ANSWER", "ANSWER"]


class ChatHistory(BaseModel):
    utterance: str
    type: Literal["AI", "Human"]


class LLMWithDocReqBody(BaseModel):
    userUtterance: str = Field(description="ユーザーの発言内容")
    history: List[ChatHistory] = Field(description="AI とユーザーとのやり取りの履歴")
    documents: List[KendraDocument]
