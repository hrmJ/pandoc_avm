from .Node import TexNode, HtmlNode
from dominate.tags import *

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


