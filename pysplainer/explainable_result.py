from io import BytesIO
from typing import List, Optional, Any

from pydantic import BaseModel, Field

from pysplainer.typst_compile import typst_compile_text


class ExplainableResult(BaseModel):
    result: Optional[Any] = None
    comments: List[str] = Field(default_factory=list)
    function_name: str

    def as_text(self):
        return "\n\n".join(self.comments)

    def as_pdf(
        self, template: Optional[str] = "", output: Optional[str] = None
    ) -> Optional[BytesIO]:
        text = template + self.as_text()
        return typst_compile_text(text, output=output)
