from pydantic import BaseModel, PrivateAttr
from langchain.tools import BaseTool
import io, contextlib, traceback
from typing import Any, Type

class PythonExecutionContext:
    def __init__(self, globals: dict[str, Any] = None,
                 locals: dict[str, Any] = None):
        self.globals = globals if globals is not None else {}
        self.locals = locals if locals is not None else {}

    def run_code(self, code: str) -> str:
        if code.strip().startswith("```"):
            code = "\n".join(
                line for line in code.strip().splitlines()
                if not line.strip().startswith("```")
            )

        stdout = io.StringIO()
        result = None

        try:
            with contextlib.redirect_stdout(stdout):
                exec(code, self.globals, self.locals)
                lines = code.strip().split('\n')
                if lines and lines[-1] and not lines[-1].startswith((' ', '\t')):
                    try:
                        result = eval(lines[-1], self.globals)
                    except:
                        result = None
        except Exception:
            return f"[Erro] {traceback.format_exc()}"

        output = stdout.getvalue()
        if result is not None:
            output += f"\n=> {result}"
        return output.strip()

class PythonInput(BaseModel):
    code: str

class StatefulPythonREPLTool(BaseTool):
    name: str = "Stateful Python Interpreter"
    description: str = (
        "Executa código Python com memória persistente entre chamadas. "
        "Ideal para cálculos, manipulação de dados, consultas em banco de dados e execuções multi-etapas."
    )
    args_schema: Type[BaseModel] = PythonInput
    _context: PythonExecutionContext = PrivateAttr()

    def __init__(self, context: PythonExecutionContext, **kwargs):
        super().__init__(**kwargs)
        self._context = context

    def _run(self, code: str) -> str:
        return self._context.run_code(code)

    def _arun(self, code: str):
        raise NotImplementedError("Execução assíncrona não suportada")
