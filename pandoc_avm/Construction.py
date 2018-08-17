from dominate.tags import *
from .texnodes import Avm, MiniBox, Options, NoEscape, Arguments
import sys
import re



class Construction():
    """
    A complete construction notation consisting of boxes and noboxes
    """
    def __init__(self, caption="", label=""):
        self.CreateOuterNode()
        self.CreateContentNode()
        self.label = label
        self.caption = caption


class Htmlconstruction(Construction):

    def CreateOuterNode(self):
        self.out = div(cls="outerbox cxg")

    def CreateContentNode(self):
        self.content = div(cls="containerbox")

    def AddNodes(self, content):
        """
        Add nodes either wrapped in boxes or independently
        """
        self.content += content.out


    def Output(self):
        """
        Combine status and content and return a representation
        of the construction as a whole
        """
        self.out += self.content

        return self.out.render(pretty=False)

    def AddStatus(self, statuses):
        """
        Add attributes concerning the construction as a whole
        """
        for status in statuses:
            self.out += div(status,cls="statusline")

class Texconstruction(Construction):

    def CreateOuterNode(self):
        self.out = Avm()

    def CreateContentNode(self):
        self.content = MiniBox(True)

    def AddNodes(self, content):
        """
        Add nodes either wrapped in boxes or independently
        """
        #print("CHECK this out: >>>>>\n\n")
        #print(content)
        #print(content.out)
        self.content.content += content.out

    def Output(self):
        """
        Combine status and content and return a representation
        of the construction as a whole
        """
        self.content.CompileContent()
        self.out.append(self.content)
        out = re.sub(r"\\+#",r"\#",self.out.dumps_as_content())
        out = re.sub(r"¤",r" ",out)
        return """
        \\vspace{{0.4cm}}
        
        \\scriptsize 

        \\FloatBarrier


        \\begin{{avmfloat}}[h]%
        \\centering

            {output}
        
        \\caption{{\\label{{mat:{lab}}} {cap} }}
        \\end{{avmfloat}}

        \\FloatBarrier

        \\normalsize

        
        \\vspace{{0.4cm}}
        
        """.format(output=out, cap=self.caption, lab=self.label)

    def AddStatus(self, statuses):
        """
        Add attributes concerning the construction as a whole
        """
        sstring = ""
        for status in statuses:
            sstring += status.replace("&"," ") + r" \\" + "\n"
        sstring += "\n"
        self.content.content += "\n" + sstring + "\n"


