from __future__ import annotations

from typing import List, Optional, Type

from pydantic import BaseModel, Extra
from abc import ABC

from langchain.chat_models.base import BaseChatModel
from langchain.tools.base import BaseTool



class BaseFlow(BaseModel, ABC):
    task: str


    @classmethod
    def from_llm_and_tools(
        cls,
        llm: BaseChatModel,
        tools: List[BaseTool],
    ) -> BaseFlow:
        raise NotImplementedError


