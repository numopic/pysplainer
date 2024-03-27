from io import BytesIO
from typing import List, Optional, Any
from dataclasses import dataclass, field

from pysplainer.typst_compile import typst_compile_text


@dataclass
class ExplainableResult:
    function_name: str
    comments: List[str] = field(default_factory=list)
    result: Optional[Any] = None

    def as_text(self):
        return "\n\n".join(self.comments)

    def as_pdf(
        self, template: Optional[str] = "", output: Optional[str] = None
    ) -> Optional[BytesIO]:
        text = template + self.as_text()
        return typst_compile_text(text, output=output)
