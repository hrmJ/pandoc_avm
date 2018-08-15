from dominate.tags import *
from .texnodes import MiniBox
import re
from pylatex.utils import NoEscape

class NodeGroup():

    cxtype = "html"

    def __init__(self, nodelist, statuses=None, cxtype="html"):
        self.cxtype = cxtype
        self.nodelist = nodelist
        self.statuses = statuses


    def AttachMembers(self):
        if self.cxtype == "tex":
            innerbox = MiniBox()
            self.CountNodeHeights()
            for node in self.nodelist:
                addedheight = self.maxheight - node.height
                if addedheight > 0:
                    #giving a bit more height to the lower nodes
                    addedheight += 0.5
                node.features.content += "\n" + r"\vspace{" + "{}".format(addedheight if addedheight else 0.3) + "em}\n"
                innerbox.content += "\n" + node.Output()
            innerbox.CompileContent()
            self.innerbox = innerbox.dumps_as_content()
        else:
            pass

    def CountNodeHeights(self):
        [node.CountHeight() for node in self.nodelist]
        self.maxheight = max([node.height for node in self.nodelist])

class Node():
    def __init__(self, is_dashed=False):
        """
        @param dict features dictionary of atrributes and values
        """
        self.is_dashed = is_dashed
        self.CreateFeatures()


class TexNode(Node):

    def CreateFeatures(self):
        self.features = MiniBox(framed=True)

    def AddFeature(self, feature):
        self.features.content += "\n" + feature

    def CountHeight(self):
        self.height = len(re.findall(r"\\{2}",self.features.content))

    def Output(self):
        #Trying to balance the height of the nodes
        self.features.CompileContent()
        return NoEscape(self.features.dumps_as_content())

class HtmlNode(Node):

    def CreateFeatures(self):
        self.features = div(cls="node dashed" if self.is_dashed else "node")

    def AddFeature(self, feature):
        self.features += feature

    def Output(self):
        return self.features


class Box(NodeGroup):
    """
    A box surrounding a group of nodes
    - nodelist: nodes inside the box (as Node objects)
    - statuses: print a statusline?
    - cxtype: html or tex
    """

    def BuildOutput(self):
        if self.cxtype == "html":
            containerbox = div(cls="containerbox")
            outerbox = div(cls="outerbox")
            innerbox = div(cls="innerbox")
            for node in self.nodelist:
                innerbox += node.Output()
            # attributes concerning the whole box
            if self.statuses:
                for status in self.statuses:
                    outerbox += div(status,cls="statusline")

            outerbox += innerbox
            containerbox += outerbox

            self.out = containerbox
        elif self.cxtype == "tex":
            self.AttachMembers()
            Outerbox = MiniBox(framed=True)
            if self.statuses:
                for status in self.statuses:
                    Outerbox.content += "\n" + status.replace("&"," ") + r" \\" + "\n"
            Outerbox.content += self.innerbox
            Outerbox.CompileContent()
            self.out = Outerbox.dumps_as_content()


class Nobox(NodeGroup):
    """
    A node or a group of nodes not connected by a box
    """

    def BuildOutput(self):
        if self.cxtype == "html":
            innerbox = div(cls="innerbox")
            for node in self.nodelist:
                innerbox += node.Output()
            self.out = innerbox
        elif self.cxtype == "tex":
            self.AttachMembers()
            self.out = self.innerbox


