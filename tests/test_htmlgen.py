from webhelpers.htmlgen import html

def test_html():
    assert html('<foo>') == '<foo>'
    assert html.escape('<foo>') == '&lt;foo&gt;'
    assert str(html.br) == '<br />'
    assert html.a(href='url', c='whatever') == '<a href="url">whatever</a>'
    assert html.a('whatever', href='url', class_=None) == '<a href="url">whatever</a>'
    assert html.a(a=1, b_=2) in ('<a a="1" b="2"></a>', '<a b="2" a="1"></a>')
    
