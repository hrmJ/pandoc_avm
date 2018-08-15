#from prepandoc import stylestring
from pyparsing import nestedExpr, originalTextFor
#from lxml import etree
from xml.dom.minidom import parse, parseString
#from prepandoc import *
import unittest
import re
from pandoc_avm import Texconstruction, ParseConstruction, NodeGroup, Nobox

def Output(html):
    print("<html><head><style> " + stylestring + "</style></head><body>\n\n" + html + "</body></html>")

#import bs4

class CxTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._cxraw = """

        <cx>
            <nobox>
                [
                    [[gf=adv][prag=[df=muu]][sem=aika,muutos]]
                    [[gf=subj]]
                    [[cat=V]]
                    [[gf=compl]]
                ]
            </nobox>
        </cx>

        """

    def test_create_cxg_tex(self):

        x = parseString(self._cxraw)
        cx = Texconstruction()
        cxtype = "tex"
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

        #cx.Output()
        #print(cx.Output())

        #Output(cx.Output())

        #afterbox = Node()
        #for featureline in cx_string[0][1][0]:
        #    afterbox.AddFeature(ParseNodeFeature(featureline))
        #cxg = Construction(nodes, status, afterbox)



if __name__ == '__main__':
    unittest.main()



