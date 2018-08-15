#!/usr/bin/python3
import sys
import panflute as pf
from xml.dom.minidom import parse, parseString
from pandoc_avm import Texconstruction, Htmlconstruction, ParseConstruction, NodeGroup, Nobox
from pyparsing import nestedExpr, originalTextFor

def CreateAvm(raw, cxtype):
    """
    Outputs the avm 

    -- raw: the source string (<cx>...</cx>)
    -- cxtype: tex or html

    """

    x = parseString(raw)
    label = x.childNodes[0].getAttribute("label")
    caption = x.childNodes[0].getAttribute("caption")

    if cxtype == "tex":
        cx = Texconstruction(caption, label)
    elif cxtype == "html":
        cx = Htmlconstruction()

    for node in x.childNodes[0].childNodes:
        if node.nodeName != "#text":
            cx_string = nestedExpr('[',']').parseString(node.childNodes[0].data)
            if node.nodeName == "box":
                nodes = ParseConstruction(cx_string[0][1], cxtype)
                status = ParseStatus(cx_string[0][0], cxtype)
                grouped = Box(nodes, status, cxtype)
                grouped.BuildOutput()
                cx.AddNodes(grouped)
            elif node.nodeName == "nobox":
                nodes = ParseConstruction(cx_string[0], cxtype)
                grouped = Nobox(nodes, cxtype=cxtype)
                grouped.BuildOutput()
                cx.AddNodes(grouped)
            elif node.nodeName == "status":
                cx.AddStatus(ParseStatus(cx_string[0][0], cxtype))
    return cx.Output()


def avm(elem, doc):
    """
    The actual panflute style pandoc filter
    """
    if isinstance(elem, pf.CodeBlock):
        if "<cx" in elem.text:
            if doc.format == 'latex':
                return pf.RawBlock(CreateAvm(elem.text,"tex"),"latex")
            elif doc.format == 'html':
                return pf.RawBlock(CreateAvm(elem.text,"html"),"html")

def main(doc=None):
    return pf.run_filter(avm, doc=doc) 


if __name__ == '__main__':
    main()

