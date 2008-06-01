"""MIMEType helpers"""
import mimetypes
import webob

class MIMETypes(object):
    aliases = {}
    
    def init(cls):
        mimetypes.init()
    init = classmethod(init)
    
    def add_alias(cls, alias, mimetype):
        cls.aliases[alias] = mimetype
    add_alias = classmethod(add_alias)
    
    def __init__(self, environ):
        self.env = environ
    
    def _set_responce_conetent_type(self, mimetype):
        if 'pylons.pylons' in self.env:
            self.env['pylons.pylons'].response.content_type = mimetype
        return mimetype
        
    def mimetype(self, mimetype):
        if mimetype in MIMETypes.aliases:
            mimetype = MIMETypes.aliases[mimetype]
        path = self.env['PATH_INFO']
        guess_from_url = mimetypes.guess_type(path)[0]
        possible_from_accept_header = None
        has_extension = False
        if len(path.split('/')) > 1:
            last_part = path.split('/')[-1]
            if '.' in last_part:
                has_extension = True
        if 'HTTP_ACCEPT' in self.env:
            possible_from_accept_header = webob.acceptparse.MIMEAccept('ACCEPT', 
                self.env['HTTP_ACCEPT'])
        if has_extension == False:
            if possible_from_accept_header is None:
                return self._set_responce_conetent_type(mimetype)
            elif mimetype in possible_from_accept_header:
                return self._set_responce_conetent_type(mimetype)
            else:
                return False
        if mimetype == guess_from_url:
            # Guessed same mimetype
            return self._set_responce_conetent_type(mimetype)
        elif guess_from_url is None and mimetype in possible_from_accept_header:
            return self._set_responce_conetent_type(mimetype)
        else:
            return False