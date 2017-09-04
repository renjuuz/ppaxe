# -*- coding: utf-8 -*-
'''
Tests for the summary/report of the analyses
'''
from ppaxe import core
from pycorenlp import StanfordCoreNLP
import json

def test_summary_totalcount():
    '''
    Tests totalcount of ProtSummary
    '''
    article_text = """
             MAPK seems to interact with chloroacetate esterase.
             However, MAPK is a better target for peroxydase.
             The thing is, Schmidtea mediterranea is a good model organism because reasons.
             However, cryoglobulin is better.
         """
    article = core.Article(pmid="1234", fulltext=article_text)
    article.extract_sentences()
    for sentence in article.sentences:
        sentence.annotate()
        sentence.get_candidates()
    summary = core.ReportSummary([article])
    summary.protsummary.makesummary()
    assert(summary.protsummary.prot_table['MAPK']['totalcount'] == 2)


def test_summary_intcount():
    '''
    Tests int_count of ProtSummary
    '''
    article_text = """
             MAPK seems to interact with chloroacetate esterase.
             However, MAPK is a better target for peroxydase.
             The thing is, Schmidtea mediterranea is a good model organism because reasons.
             However, cryoglobulin is better.
         """
    article = core.Article(pmid="1234", fulltext=article_text)
    article.extract_sentences()
    for sentence in article.sentences:
        sentence.annotate()
        sentence.get_candidates()
    summary = core.ReportSummary([article])
    summary.protsummary.makesummary()
    assert(summary.protsummary.prot_table['MAPK']['int_count']['left'] == 2)


def test_summary_prottable_tomd():
    '''
    Tests int_count of ProtSummary
    '''
    article_text = """
             MAPK seems to interact with chloroacetate esterase.
             However, MAPK is a better target for peroxydase.
             The thing is, Schmidtea mediterranea is a good model organism because reasons.
             However, cryoglobulin is better.
         """
    article = core.Article(pmid="1234", fulltext=article_text)
    article.extract_sentences()
    for sentence in article.sentences:
        sentence.annotate()
        sentence.get_candidates()
    summary = core.ReportSummary([article])
    summary.protsummary.makesummary()
    thetable = summary.protsummary.table_to_md(sorted_by="int_count")
    reftable = (
    """| PROT_SYMBOL | TOTAL_COUNT | INT_COUNT | LEFT_COUNT | RIGHT_COUNT |
| ----- | ----- | ----- | ----- | ----- |
| MAPK | 2 | 2 | 2 | 0 |
| CHLOROACETATE ESTERASE | 1 | 1 | 0 | 1 |
| PEROXYDASE | 1 | 1 | 0 | 1 |
| CRYOGLOBULIN | 1 | 0 | 0 | 0 |
"""
    )
    assert(thetable == reftable)

def test_summary_prottable_tohtml():
    '''
    Tests int_count of ProtSummary
    '''
    article_text = """
             MAPK seems to interact with chloroacetate esterase.
             However, MAPK is a better target for peroxydase.
             The thing is, Schmidtea mediterranea is a good model organism because reasons.
             However, cryoglobulin is better.
         """
    article = core.Article(pmid="1234", fulltext=article_text)
    article.extract_sentences()
    for sentence in article.sentences:
        sentence.annotate()
        sentence.get_candidates()
    summary = core.ReportSummary([article])
    summary.protsummary.makesummary()
    thetable = summary.protsummary.table_to_html(sorted_by="int_count")
    reftable = """<table>
<thead>
<tr>
<th>PROT_SYMBOL</th>
<th>TOTAL_COUNT</th>
<th>INT_COUNT</th>
<th>LEFT_COUNT</th>
<th>RIGHT_COUNT</th>
</tr>
</thead>
<tbody>
<tr>
<td>MAPK</td>
<td>2</td>
<td>2</td>
<td>2</td>
<td>0</td>
</tr>
<tr>
<td>CHLOROACETATE ESTERASE</td>
<td>1</td>
<td>1</td>
<td>0</td>
<td>1</td>
</tr>
<tr>
<td>PEROXYDASE</td>
<td>1</td>
<td>1</td>
<td>0</td>
<td>1</td>
</tr>
<tr>
<td>CRYOGLOBULIN</td>
<td>1</td>
<td>0</td>
<td>0</td>
<td>0</td>
</tr>
</tbody>
</table>"""
    assert(thetable == reftable)

def test_interaction_list():
    '''
    Tests if GraphSummary.makesummary() creates the interaction list correctly
    '''
    article_text = """
             MAPK seems to interact with MAPK4.
             However, Mapk4 interacts directly with MAPK.
             CPP3 is a molecular target of Akt3.
             AKT3 is also known to interact with CPP3.
         """
    article = core.Article(pmid="1234", fulltext=article_text)
    article.extract_sentences()
    for sentence in article.sentences:
        sentence.annotate()
        sentence.get_candidates()
        for candidate in sentence.candidates:
            candidate.predict()
    summary = core.ReportSummary([article])
    summary.graphsummary.makesummary()
    assert(
        len(summary.graphsummary.interactions) == 4 and
        summary.graphsummary.uniqinteractions == 2
    )


def test_interaction_table_md():
    '''
    Tests the markdown of the interactions table
    '''
    article_text = """
             MAPK seems to interact with MAPK4.
             However, Mapk4 interacts directly with MAPK.
             CPP3 is a molecular target of Akt3.
             AKT3 is also known to interact with CPP3.
         """
    article = core.Article(pmid="1234", fulltext=article_text)
    article.extract_sentences()
    for sentence in article.sentences:
        sentence.annotate()
        sentence.get_candidates()
        for candidate in sentence.candidates:
            candidate.predict()
    summary = core.ReportSummary([article])
    summary.graphsummary.makesummary()
    summary.graphsummary.int_table_to_md()