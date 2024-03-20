from io import BytesIO
from typing import List, Optional, Any

from pydantic import BaseModel, Field

from pysplainer.typst_compile import typst_compile_text


class ExplainableResult(BaseModel):
    result: Optional[Any] = None
    computable_comments: List[str] = Field(default_factory=list)
    function_name: str

    def get_comments_recursively(self):
        return self.computable_comments

    def as_pdf(
        self, template: Optional[str] = "", output: Optional[str] = None
    ) -> Optional[BytesIO]:
        text = template + "\n\n".join(self.computable_comments)
        return typst_compile_text(text, output=output)

    def as_markdown(self):
        raise NotImplementedError("ExplainableResult.as_markdown() not implemented")

    def as_dict(self):
        raise NotImplementedError("ExplainableResult.as_dict() not implemented")
