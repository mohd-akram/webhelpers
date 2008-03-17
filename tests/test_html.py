from webhelpers.html import literal, quote

def test_double_quote():
    quoted = quote(u'This string is "quoted"')
    assert quoted == u'This string is &quot;quoted&quot;'
    dbl_quoted = quote(quoted)
    assert quoted == dbl_quoted

def test_literal():
    lit = literal(u'This string <>')
    other = literal(u'<other>')
    assert u'This string <><other>' == lit + other
    
    assert u'&quot;<other>' == '"' + other
    assert u'<other>&quot;' == other + '"'
    
    mod = literal('<%s>ello')
    assert u'<&lt;H&gt;>ello' == mod % '<H>'

def test_literal_dict():
    lit = literal(u'This string <>')
    unq = 'This has <crap>'
    sub = literal('%s and %s')
    assert u'This string <> and This has &lt;crap&gt;' == sub % (lit, unq)
    
    sub = literal('%(lit)s and %(lit)r')
    assert u"This string <> and literal(u'This string &lt;&gt;')" == sub % dict(lit=lit)
    sub = literal('%(unq)r and %(unq)s')
    assert u"'This has &lt;crap&gt;' and This has &lt;crap&gt;" == sub % dict(unq=unq)

def test_literal_mul():
    lit = literal(u'<>')
    assert u'<><><>' == lit * 3
    assert isinstance(lit*3, literal)

def test_literal_join():
    lit = literal(u'<>')
    assert isinstance(lit.join(['f', 'a']), literal)
    assert u'f<>a' == lit.join(('f', 'a'))

def test_literal_int():
    lit = literal(u'<%i>')
    assert u'<5>' == lit % 5

def test_html