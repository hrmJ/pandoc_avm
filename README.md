Pandoc_avm
=========

This is a pandoc filter for drawing construction grammar like box matrices
(AVMs) html and latex using a simple markup language.



Installation
------------

The latex output is based  on [Chris Manning's avm.sty](https://www1.essex.ac.uk/linguistics/external/clmt/latex4ling/avms/#6) 
( direct link [here](https://www1.essex.ac.uk/linguistics/external/clmt/latex4ling/archive/avm.sty.gz),
cf. also [here](https://nlp.stanford.edu/~manning/tex/)), which is a prerequisite.

Download the `.sty` file and place it in your TeX home directory (find it out by: `kpsewhich -var-value=TEXMFHOME`), 
e.g.  `/home/user/texmf/tex/latex/commonstuff/avm.sty`


Tweaking
--------

To enable numbering and captions, add this to your custom latex preamble:

```

\usepackage{newfloat}
\DeclareFloatingEnvironment[placement={here},name=Matrix]{avmfloat}
\captionsetup[avmfloat]{labelfont=bf}

```

To use captions and reference the matrices, you can specify in your markup 

```
    <cx caption='My fancy avm caption' label='niceavm'>
```

After that, if you compile with [bookdown](https://bookdown.org), you can use the standard
bookdown referencing method with a `tab:` prefix in the following way:

```

In matrix \@ref(mat:niceavm) we can see that...

```

So far this is implemented only in the latex output


Using the markup language
-------------------

(documentation in progress)

Here are some examples to get you started (picked from my dissertation).
Remember: these must be defined as code blocks in your markdown document i.e.
indented.


```
    <cx caption='my caption' label='lbl'>
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

