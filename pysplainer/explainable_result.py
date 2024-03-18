from typing import List, Optional, Any

from pydantic import BaseModel, Field


class ExplainableResult(BaseModel):
    result: Optional[Any] = None
    computable_comments: List[str] = Field(default_factory=list)
    function_name: str

    def get_comments_recursively(self):
        return self.computable_comments

    def as_pdf(self, template: str, output: Optional[str]):
        raise NotImplementedError("ExplainableResult.as_pdf() not implemented")

    def as_markdown(self):
        raise NotImplementedError("ExplainableResult.as_markdown() not implemented")

    def as_dict(self):
        raise NotImplementedError("ExplainableResult.as_dict() not implemented")
