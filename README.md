Pandoc_avm
=========

This is a pandoc filter for drawing construction grammar like box matrices
(AVMs) html and latex using a simple markup language.

Installation
------------



Using the markup language
-------------------

(documentation in progress)

Here are some examples to get you started (picked from my dissertation).
Remember: these must be defined as code blocks in your markdown document i.e.
indented.


```
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

```

```
    <cx>
        <box>
            [
                [[ds=act+]]
                [
                    [[gf=subj]]
                    [[syn=[cat=V][val=#1,#2]]]
                    [[#1=¤][gf=obj]]
                ]
            ]
        </box>
        <nobox>
            [
                [[gf=adv][sem=aika]]
                [[#2=¤][prag=[df=foc]]]
            ]
        </nobox>
    </cx>
```

```
    <cx>
        <box>
            [
                [[df=foc]]
                [
                    [[gf=subj]]
                    [[cat=V]]
                    [[gf=obj]]
                ]
            ]
        </box>
        <nobox>
            [
                [[gf=adv][sem=aika][prag=[df=-focus]]]
            ]
        </nobox>
    </cx>
```


See also the file `test_text.Rmd` to get an idea of how the blocks are
implemented in the text.


Using the filter
----------------

An example yaml block of your Rmd or md file:

```
output:
  pdf_document2: 
    latex_engine: xelatex
    pandoc_args:
      - --filter
      - pandoc_avm
```

