"""Simple function to send email ported from pythonweb.org web.mail by James Gardner <james@jimmyg.org>
    
The mail module provides a simple function ``mail()`` which can be used to send emails as shown in the example below::

    mail(
        msg        = "Hello!",
        to         = 'james@example.com',
        reply_name  = 'James Gardner',
        reply_email = 'james@example.com',
        subject    = 'Test Email',
        sendmail   = '/usr/bin/sendmail',
        method     = 'sendmail'
    )

To send the same email via SMTP instead of using Sendmail you would use::

    mail(
        msg        = "Hello James!",
        to         = 'james@example.com',
        reply_name  = 'James Gardner',
        reply_email = 'james@example.com',
        subject    = 'Test Email',
        smtp       = 'smtp.ntlworld.com',
        method     = 'smtp'
    )

If you get an error like ``socket.error: (10060, 'Operation timed out')`` it is likely that the SMTP address you specified either doesn't exist or will not give you access.

Function definition for mail():

    ``msg``
        Text of the message

    ``to``
        A list of recipient addresses in the form: addr@addr.com

    ``subject``
        Email subject line, defualts to empty string ``''``.

    ``method``
        Describes which method to use to send the email. Can be ``'smtp'`` or ``'sendmail'`` but ``method`` only needs to be specified if both ``smtp`` and ``sendmail`` parameters are specified otherwise the method that is defined is used and the value of ``method`` is ignored.

    ``smtp``
        SMTP server address

    ``sendmail``
        Sendmail path

    ``blind``
        Should be set to ``True`` if recipients are to be blocked from seeing who else the email was sent to (ie recipeints are bcc'd)

    ``reply_name``
        The name of the person sending the email. Only available if ``reply`` is not specified.

    ``reply_email``
        The email address of the person sending the email. Only available if ``reply`` is not specified.

    ``reply``
        The name and email address of the person sending the email in the form: ``"sender name <addr@example.com>"``. Should only be specified if ``reply_name`` and ``reply_email`` are not specified.

    ``type``
        The second part of the content-type, eg ``'plain'`` for a plain text email, ``'html'`` for an HTML email.

The module also provides a method ``build_reply()`` which can be used to put the name and email address into the format required for the ``reply`` parameter of the ``mail()`` helper::

    >>> mail.build_reply('James Gardner, 'james@example.com')
    James Gardner <james@example.com>
    
    
For more advanced functionality look at the modules included with the Python standard library.
"""

def build_reply(name, email):
    return '%s <%s>'%(name, email)
    
def mail(**params):#msg, me, to, subject, smtpServer, blind=False
    """Function to send a text only email via SMTP.
        msg         - Text of the message.
        to          - A list of recipient email addresses in the form: addr@addr.com.
        subject     - Email subject.
        smtp        - SMTP server address.
        sendmail    - Sendmail path.
        method      - Which method to use if smtp or sendmail aren't specified.
        blind       - Whether to send the emails blind or not.
        reply       - The name and address of the person sending the email in the form: "sender name <addr@example.com>"
        reply_name
        reply_email
        type        - The second part of the content-type, eg 'plain' for 'Content-type: text/plain\n\n'
    """
    # imports
    import StringIO
    import smtplib
    from email.MIMEText import MIMEText
    from email.MIMEBase import MIMEBase
    import email.Utils
    
    if params.has_key('reply_name') and not params.has_key('reply_email'):
        raise Exception("You must specify a 'reply_email' as well as a 'reply_name'.")
    elif params.has_key('reply_email') and not params.has_key('reply_name'):
        raise Exception("You must specify a 'reply_name' as well as a 'reply_email'.")
    if params.has_key('reply') and (params.has_key('reply_email') or params.has_key('reply_name')):
        raise Exception("You cannot specify 'reply' as well as a 'reply_name' and 'reply_email'.")
    if not params.has_key('reply'):
        params['reply'] = "%s <%s>"%(params['reply_name'], params['reply_email'])
    
    if not params.has_key('blind'):
        params['blind'] = False
    if params['blind'] not in [True, False]:
        raise Exception("'blind' can only be True or False.")
    # Make sure the essential attributes are there
    for p in ['msg', 'to', 'subject']:
        if not params.has_key(p):
            raise Exception("You must specify the attribute '%s' to send an email."%p)
    # Make sure they are stings
    for p in ['msg', 'subject']:
        if type(params[p]) <> type(''):
            raise Exception("The attribute '%s' must be a string."%p)
    # Check method
    if not (params.has_key('smtp') or params.has_key('sendmail')) and not params.has_key('method'):
        raise Exception("You must specify an SMTP server or sendmail path")
    if not params.has_key('method'):
        if params.has_key('smtp') and params.has_key('sendmail'):
            raise Exception("You must specify which method you want to use to send the email")
        elif params.has_key('smtp'):
            params['method'] = 'smtp'
        else:
            params['method'] = 'sendmail'
    if params['method'] not in ['sendmail','smtp']:
        raise Exception("The method parameter cannot be '%s'."%params['method'])
    # Open a plain text file for reading.  For this example, assume that
    # the text file contains only ASCII characters.
    fp = StringIO.StringIO(params['msg'])
    if not params.has_key('type'):
        msg = MIMEText(fp.read())
    else:
        msg = MIMEBase('text',params['type'])
        msg.set_payload(fp.read())
    fp.close()
    msg['From'] = params['reply']
    msg['Subject'] = params['subject']
    if type(params['to']) == type(''):
        params['to']=[params['to']]
    if params['method'] == 'sendmail':
        if params['blind'] == True:
            msg['Bcc'] = ', '.join(params['to'])
        else:
            msg['To'] = ', '.join(params['to'])
        import os
        if not os.path.exists(params['sendmail']):
            raise Exception("The path '%s' doesn't exist. Please check the location of sendmail."%params['sendmail'])
        fp = os.popen(params['sendmail']+" -t", 'w')
        fp.write(msg.as_string())
        error = fp.close()
        if error:
            raise Exception("Error sending mail: Sendmail Error '%s'."% error)
    elif params['method'] == 'smtp':
        if params['blind'] == True:
            msg['To'] = ''
        else:
            msg['To'] = ', '.join(params['to'])
        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP()
        #s.set_debuglevel(100) 
        s.connect(params['smtp'])
        result = s.sendmail(params['reply'], params['to'], msg.as_string())
        s.quit()
        if result:
            for r in result.keys():
                error+= "Error sending to"+ str(r)
                rt = result[r]
                error+= "Code"+ str(rt[0])+":"+ str(rt[1])
            raise Exception("Error sending mail: %s"% error)
