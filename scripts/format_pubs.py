"""
Heavily inspired by dfm/cv/scripts/render.py
"""

import ads
from datetime import date
from operator import itemgetter
import json
import importlib.util
import os

here = os.path.abspath('')
spec = importlib.util.spec_from_file_location(
    "utf8totex", os.path.join(here, "utf8totex.py")
)
utf8totex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(utf8totex)


JOURNAL_MAP = {
    "ArXiv e-prints": "ArXiv",
    "arXiv e-prints": "ArXiv",
    "Monthly Notices of the Royal Astronomical Society": "\\mnras",
    "The Astrophysical Journal": "\\apj",
    "The Astronomical Journal": "\\aj",
    "Publications of the Astronomical Society of the Pacific": "\\pasp",
    "IAU General Assembly": "IAU",
    "Astronomy and Astrophysics": "\\aanda",
    "American Astronomical Society Meeting Abstracts": "AAS",
}


def check_inpress(pub):
    """
    Checks whether a given paper is in the inpress data file.
    If so, it should go under "peer-reviewed" in the CV — with the 
    caveat that it's in press.

    Inputs
    -------
    :pub: (dict) publication object. Needs to have 'title' key.
    """

    # read in the in press data
    f = open('../data/in_press.txt')
    in_press = f.readlines()
    f.close()
    
    for i, press in enumerate(in_press):
        in_press[i] = press.split('\n')[0]

    return pub['title'] in in_press

def check_studentpaper(pub):
    """
    Checks whether a given paper is in the inpress data file.
    If so, it should go under "peer-reviewed" in the CV — with the 
    caveat that it's in press.

    Inputs
    -------
    :pub: (dict) publication object. Needs to have 'title' key.
    """
    f = open('../data/student_papers.txt')
    student_papers = f.readlines()
    f.close()

    return pub['title'] in student_papers

def format_pub(args):
    ind, pub = args

    # add asterisk ahead of student papers
    if check_studentpaper(pub):
        fmt += '*'

    fmt = "\\item[{{\\color{{numcolor}}\\scriptsize{0}}}] ".format(ind)
    n = [
        i
        for i in range(len(pub["authors"]))
        if "Savel" in pub["authors"][i]
    ][0]
    pub["authors"][n] = "\\textbf{Savel, Arjun}"
    
    pub_title = pub["title"].replace('{\\&}amp;', '\&') # for latex literal interp.
    
    if len(pub["authors"]) > 5:
        fmt += "; ".join(pub["authors"][:4])
        fmt += "; \\etal"
        if n >= 4:
            others = len(pub['authors']) - 4
            fmt += "\\ ({{{0}}} other co-authors, ".format(others)
            fmt += "incl.\\ \\textbf{Savel, Arjun})"
    elif len(pub["authors"]) > 1:
        fmt += "; ".join(pub["authors"][:-1])
        fmt += "; \\& " + pub["authors"][-1]
    else:
        fmt += pub["authors"][0]

    fmt += ", {0}".format(pub["year"])

    if pub["doi"] is not None:
        fmt += ", \\doi{{{0}}}{{{1}}}".format(pub["doi"], pub_title)
    else:
        fmt += ", \\emph{{{0}}}".format(pub_title)

    if not pub["pub"] in [None, "ArXiv e-prints"]:
        fmt += ", " + JOURNAL_MAP.get(
            pub["pub"].strip("0123456789# "), pub["pub"]
        )

    if pub["volume"] is not None:
        fmt += ", {{{0}}}".format(pub["volume"])

    if pub["page"] is not None:
        fmt += ", {0}".format(pub["page"])

    if pub["arxiv"] is not None:
        fmt += " (\\arxiv{{{0}}})".format(pub["arxiv"])

    if check_inpress(pub):
        # need to add caveat!
        fmt += ' (in press)'
        
    if pub["url"] is not None and pub["citations"] == 1:
        fmt += " [\\href{{{0}}}{{{1} citation}}]".format(
            pub["url"], pub["citations"]
        )
        
    elif pub["url"] is not None and pub["citations"] > 1:
        fmt += " [\\href{{{0}}}{{{1} citations}}]".format(
            pub["url"], pub["citations"]
        )
        
    #elif pub["url"] is not None and pub["citations"] == 0: 
    #   fmt += " [\\href{{{0}}}]".format(
    #          pub["url"]
    # )

    return fmt


if __name__ == "__main__":
    with open("../data/ads_scrape.json", "r") as f:
        pubs = json.load(f)
    

    pubs = sorted(pubs, key=itemgetter("pubdate"), reverse=True)
    
    # want to include articles and preprints, but not Zenodo repos.
    pubs = [
        p
        for p in pubs
        if (
            p["doctype"] in ["article", "eprint"]
            and p["pub"] != "Zenodo Software Release"
        )
    ]
    
    # want to include in press articles under refereed
    for pub in pubs:
        if check_inpress(pub):
            print(pub["title"])
            pub["doctype"] = "article"
    
    ref = [p for p in pubs if p["doctype"] == "article"]
    unref = [p for p in pubs if p["doctype"] == "eprint"]

    # Compute citation stats
    npapers = len(ref)
    nfirst = sum(1 for p in pubs if "Savel" in p["authors"][0])
    cites = sorted((p["citations"] for p in pubs), reverse=True)
    ncitations = sum(cites)
    hindex = sum(c > i for i, c in enumerate(cites))


    summary = (
        "citations: {1} / "
        "h-index: {2} ({0}) /"
        "{3} first-author"
    ).format(date.today(), ncitations, hindex, nfirst)
    with open("../supp_tex/pubs_summary.tex", "w") as f:
        f.write(summary)

    ref = list(map(format_pub, zip(range(len(ref), 0, -1), ref)))
    unref = list(map(format_pub, zip(range(len(unref), 0, -1), unref)))

    # now check whether 

    with open("../supp_tex/pubs_ref.tex", "w") as f:
        f.write("\n\n".join(ref))
    with open("../supp_tex/pubs_unref.tex", "w") as f:
        f.write("\n\n".join(unref))
        
