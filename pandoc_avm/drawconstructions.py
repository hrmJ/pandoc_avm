from dominate.tags import *
#from texnodes import Avm, MiniBox, Options, NoEscape, Arguments
import sys
import re



class Construction():
    """
    A complete construction notation consisting of boxes and noboxes
    """
    def __init__(self):
        self.CreateOuterNode()
        self.CreateContentNode()


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
        return "\n\n" + r"\vspace{0.4cm}" + "\n\n" +  r"\scriptsize " + "\n\n" + out + "\n\n" + r"\normalsize" + "\n\n" + r"\vspace{0.4cm}" + "\n\n"

    def AddStatus(self, statuses):
        """
        Add attributes concerning the construction as a whole
        """
        sstring = ""
        for status in statuses:
            sstring += status.replace("&"," ") + r" \\" + "\n"
        sstring += "\n"
        self.content.content += "\n" + sstring + "\n"


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


def Feature(avlist, cxtype="html"):
    if isinstance(avlist[1],str):
        avlist[1] = avlist[1].replace("¤"," ")

    if cxtype == "html":
        line = div(cls="featureline")
        line += div(avlist[0], cls="fleft")
        line += div(avlist[1])
    elif cxtype == "tex":
        line = "{} & {}".format(avlist[0], avlist[1])

    return line


def ParseConstruction(cx, cxtype="html"):
    """
    Parse a string and try to separate boxes and features of the construction
    matrix.
    """
    nodes = list()
    is_dashed = False
    for node in cx:
        #"node" here means one line in the source string, e.g.
        # [[gf=obj][prag=[ds=act-][df=foc]]] 
        # but NOTE, that it's not a string but a bit like a list, e.g
        # "['gf=obj']" , "['prag=', ['ds=act-'], ['df=foc']]"
        # 
        if node == "*":
            is_dashed = True
        else:
            if is_dashed:
                is_dashed = False
                n = AddNode(cxtype, True)
            else:
                n = AddNode(cxtype, False)
            for featureline in node:
                n.AddFeature(ParseNodeFeature(featureline, cxtype))
            nodes.append(n)
    return nodes

def AddNode(cxtype="html", is_dashed=False):
    """
    Just a small wrapper for determining which type of node to produce
    -cxtype: html or tex
    """
    if cxtype == "html":
        return HtmlNode(is_dashed)
    elif cxtype == "tex":
        return TexNode(is_dashed)

def ParseNodeFeature(featureline, cxtype = 'html'):
    #featureline represents one attribute-value pair inside a node, e.g.
    # "['gf=obj']"
    fullfeature = featureline
    if not isinstance(featureline, str):
        featureline = featureline[0]
    avm = featureline.split("=")

    if not(avm[1]):
       #nested cases
        subfcont = None
        if cxtype == 'html':
            subfcont = div(cls="matrixfeat")
        for subfeature in fullfeature:
            if not isinstance(subfeature, str):
                if cxtype == 'tex':
                    if not subfcont:
                        subfcont = r"\[ "
                    else:
                        subfcont += r" \\" + "\n"
                subfcont += Feature(subfeature[0].split("="), cxtype)
        if cxtype == 'tex':
            subfcont += r" \\" + "\n" + r"\] \\[5pt]" + "\n\n"
            return "\n" + avm[0] + " " + subfcont
        else:
            return Feature([avm[0],subfcont], cxtype)
    else:
        #non-nested ones
        if cxtype == 'tex':
            return "{} {} ".format(*avm) + r"\\[5pt]" + "\n\n"
        else:
            return Feature(avm, cxtype)

def ParseStatus(bundles, cxtype="html"):
    statuses = list()
    for bundle in bundles:
        subfcont = None
        if cxtype == "html":
            subfcont = div(cls="matrixfeat")
        try:
            for featurepair in bundle[1]:
                if cxtype == 'tex':
                    if not subfcont:
                        subfcont = r"\[ "
                    else:
                        subfcont += r" \\" + "\n"
                subfcont += Feature(featurepair[0].split("="), cxtype)
            statuses.append(Feature([bundle[0],subfcont], cxtype))
        except IndexError:
            feats = bundle[0].split("=")
            statuses.append(Feature([feats[0],feats[1]], cxtype))
    return statuses

