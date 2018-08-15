from pylatex.base_classes import Environment, CommandBase, Arguments, Options
from pylatex.package import Package
from pylatex import Document, Section, UnsafeCommand
from pylatex.utils import NoEscape

class Avm(Environment):
    """
    A class representing a custom LaTeX environment.
    """

    _latex_name = 'avm'
    packages = [Package('avm')]

class MiniBox(CommandBase):
    """
    A class representing a custom LaTeX command.
    """
    _latex_name = 'minibox'
    packages = [Package('minibox')]
    content = "\n"

    def __init__(self, framed=False):
        if framed:
            super().__init__(options=Options("frame", "pad=4pt","rule=0.1pt"))
        else:
            super().__init__(options=Options("pad=4pt","rule=0pt"))

    def CompileContent(self):
        """
        """
        self.arguments = Arguments(NoEscape(self.content.replace("#",r"\#")))




