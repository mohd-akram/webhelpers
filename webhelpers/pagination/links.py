"""Pagination Link Generators"""

def pagelist(page, pages):
    """PHPbb style Pagination Links
    
    Example (Using Kid)::
    
        <div py:def="display_pager(url, page, pages)" class="pager">Page ${page} of ${pages}:
            <span py:if="page != 1">
            <a href="${url + str(page-1)}">&lt;&lt; Previous</a>
            </span>
            <span py:for="i in pagelist(page, pages)"> 
                    <span py:if="i == None">...</span>
                            <a py:if="i != page and i != None" href="${url + str(i)}">${i}</a>
                            <span py:if="i == page">${i}</span>
                    </span>
                    <span py:if="page != pages">
                             <a href="${url + str(page+1)}">Next &gt;&gt;</a>
                    </span>
            </span>
        </div>
    """
    page = max(min(page, pages), 1)
    topstart = pages < 1 + 3 and pages or 4
    botmid = page-1 < 1 and 1 or page - 1
    topmid = page+2 < pages and page+2 or pages
    bottop = pages-2 < 1 and 1 or pages - 2
    startpastmid = topstart >= botmid
    midpasttop = topmid >= bottop
    if startpastmid:
        if midpasttop:
            display = range(1, pages+1)
        else:
            display = range(1, topmid+1) + [None] + range(bottop, pages+1)
    else:
        if midpasttop:
            display = range(1, topstart) + [None] + range(botmid-1, pages+1)
        else:
            display = (
                    range(1, topstart) + [None] + range(botmid, topmid) + [None] +
                    range(bottop, pages+1))
    return display
