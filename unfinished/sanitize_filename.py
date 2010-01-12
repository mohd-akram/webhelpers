# Preliminary code for webhelpers.misc.sanitize_filename().


BAD_FILENAME_CHAR_RX = re.compile(R"[^A-Za-z0-9_-]")

def strip_path(filename):
    """Delete the directory prefix from 'filename' if present.
    Use the code below.
    """

def sanitize_filename(filename, bad_char_rx=BAD_FILENAME_CHAR_RX, 
    repl="_", exts=None, prefix=None, suffix=None, lower=True):
    """Sanitize filname helper for uploaded files.

    - Strip directory prefix.
    - Lowercase filename if lower=True.
    - Split base name and extension. (Allow a few double extensions
    like ".tar.gz" and ".tar.bz2")
    - Deny if extension not in ``exts`` (a list/tuple/set of strings).
    - If ``bad_char_rx`` and ``repl`` are both not None, apply re.sub to the 
    base name and extension separately. 
    - Add prefix and suffix to the base name if specified.
    - Join the base and extension and return the new filename.
    
    What about collision with an existing file? Could pass a list of existing
    files, and it could make a numbered suffix or deny it in that case.
    """
    filename = strip_path(filename)

def old_sanitize_filename(filename):
    """Sanitize unsafe characters in upload filename. 
    Delete directory prefix too."""

    filename = unidecode(filename)
    filename = Path(filename).name
    # On Unix, strip Windows-style directory prefix manually.
    slash_pos = filename.rfind("\\")
    if slash_pos != -1:
        filename = Path(filename[slash_pos+1:])
    # On Windows, strip Unix-style directory prefix manually.
    slash_pos = filename.rfind("/")
    if slash_pos != -1:
        filename = Path(filename[slash_pos+1:])
    # Convert unsafe characters.
    repl = "_"
    orig_ext = filename.ext
    stem = BAD_FILENAME_CHAR_RX.sub(repl, filename.stem)
    ext = BAD_FILENAME_CHAR_RX.sub(repl, filename.ext)
    if orig_ext.startswith(".") and ext.startswith(repl):
        ext = "." + ext[len(repl):]
    return stem + ext

# Attachment actions.
ADD = 'add'
KEEP = 'keep'
REPLACE = 'replace'
DELETE = 'delete'

def attachment_path(orr_id, entry_id, filename):
    static_dir = config["pylons.paths"]["static_files"]
    return Path(static_dir, orr_id, entry_id, filename)

class EntriesController(HotlineBaseController):
    controller_require_perm = "authenticated"
    # Can't require a more specific perm till we know the orr_id.

    def index(self):
        partial = bool(request.params.get("partial"))
        page = self._int_id(request.params.get("page", 1), "Page", 400)
        p = IndexParamsParser(request.params)
        c.orr_id = orr_id = p.incident.orr_id
        self._REQUIRE_PERM("view_incident", orr_id=orr_id)
        if p.category:
            if p.category.id == hc.ERD_PRIVATE_CATEGORY:
                self._REQUIRE_PERM("erd_private", orr_id=orr_id)
            q = Entry.for_category(orr_id, p.category.id, p.thumbs)
        else:
            q = Entry.list(orr_id, p.thumbs)
            if not self._has_perm("erd_private", orr_id=orr_id):
                q = q.filter(Entry.category != hc.ERD_PRIVATE_CATEGORY)
        c.title = "Browse Entries for '%s'" % p.incident.pretty_name
        c.ht_title = "Browse Entries"
        c.crumbs = [
            h.link("Hotline", "hotline"), 
            h.link("Incident", "incident", id=orr_id), 
            "Browse Entries"]
        c.category = p.category
        c.thumbs = p.thumbs
        if p.thumbs:
            recs_per_page = config["thumbs_columns"] * config["thumbs_rows"]
        else:
            recs_per_page = config["records_per_page"] 
        c.entries = Page(q, page, recs_per_page)
        return render("/hotline/browse_entries.html")

    def show(self, id):
        self._process_entry_id(id)
        orr_id = self.incident.orr_id
        self._REQUIRE_PERM("view_incident", orr_id=orr_id)
        if self.entry.category == hc.ERD_PRIVATE_CATEGORY:
            self._REQUIRE_PERM("erd_private", orr_id=orr_id)
        c.ht_title = "%s: %s" % (self.incident.name, self.entry.title)
        c.title = self.incident.pretty_name
        c.crumbs = [
            h.link("Hotline", "hotline"),
            h.link("Incident", "incident", id=orr_id),
            "Entry"]
        c.entry = self.entry
        try:
            c.category_name = literal(hc.CATEGORIES[self.entry.category].label)
        except KeyError:
            c.category_name = literal(UNKNOWN)
        c.can_add_entry = self._has_perm("add_entry", orr_id=orr_id)
        c.can_modify_entry = self._has_perm("modify_entry", orr_id=orr_id)
        c.can_delete_entry = self._has_perm("delete_entry", orr_id=orr_id)
        return render("hotline/entry.html")

    def new(self):
        """Display the add entry form, which submits to self.create()."""
        orr_id = self._require_param("orr_id")
        orr_id = self._int_id(orr_id, "query parameter 'orr_id'", 400)
        self._REQUIRE_PERM("add_entry", orr_id=orr_id)
        incident = Incident.get(orr_id)
        if not incident:
            abort(400, "Incident #%d does not exist." % orr_id)
        c.ht_title = "Add entry"
        c.title = 'Adding entry for "%s"' % incident.pretty_name
        c.crumbs = [
            h.link("Hotline", "hotline"),
            h.link("Incident", "incident", id=incident.orr_id),
            "Add Entry"]
        c.action = h.url_for("entries", orr_id=incident.orr_id)
        c.method = "POST"
        c.entry = Entry()
        c.orr_id = orr_id
        c.category_pairs = self._get_category_pairs(orr_id)
        c.can_set_public = self._has_perm("set_public", orr_id=orr_id)
        html = render("hotline/entry_form.html")
        return htmlfill.render(html, force_defaults=False)

    @validate(schema=EntryForm(), form="new")
    def create(self):
        """Create a new entry based on the form input."""
        log.debug("create() entry input: %s", self.form_result)
        orr_id = self.form_result["orr_id"]
        self._REQUIRE_PERM("add_entry", orr_id=orr_id)
        if self.form_result["category"] == hc.ERD_PRIVATE_CATEGORY:
            self._REQUIRE_PERM("erd_private", orr_id=orr_id)
        can_set_public = self._has_perm("set_public", orr_id=orr_id)
        inc = Incident.get(orr_id)
        if not inc:
            abort(400, "Can't add entry to nonexistent incident.")
        entry = self._create_entry(orr_id, 
            self.form_result["title"],
            self.form_result["category"], 
            self.form_result["content"],
            can_set_public and self.form_result["is_public"], 
            )
        file = self.form_result["attachment"]["file"]
        if file is not None:
            self._add_attachment(entry, file.filename, file.file)
        inc.last_entry_date = entry.entry_date
        Session.commit()
        h.flash("Added entry.")
        self.set_insert_id_for_testing(entry.entry_id)
        redirect_to("entry", id=entry.entry_id)

    def edit(self, id):
        """Display the modify entry form, which submits to self.update()."""
        self._process_entry_id(id)
        orr_id = self.incident.orr_id
        self._REQUIRE_PERM("modify_entry", orr_id=orr_id)
        if self.entry.category == hc.ERD_PRIVATE_CATEGORY:
            self._REQUIRE_PERM("erd_private", orr_id=orr_id)
        c.ht_title = "Modify entry"
        c.title = 'Modifying entry for "%s"' % self.incident.pretty_name
        c.crumbs = [
            h.link("Hotline", "hotline"),
            h.link("Incident", "incident", id=orr_id),
            h.link("Entry", "entry", id=self.entry_id),
            "Modify"]
        c.entry = self.entry
        c.action = h.url_for("entry", id=self.entry_id)
        c.method = "PUT"
        c.entry = self.entry
        c.orr_id = self.incident.orr_id
        c.category_pairs = self._get_category_pairs(orr_id)
        c.can_set_public = self._has_perm("set_public", orr_id=orr_id)
        html = render("hotline/entry_form.html")
        return htmlfill.render(html, force_defaults=False)

    @validate(schema=EntryForm(), form="edit")
    def update(self, id):
        """Modify the entry based on the form input."""
        log.debug("update() entry input: %s", self.form_result)
        self._process_entry_id(id)
        orr_id = self.incident.orr_id
        self._REQUIRE_PERM("modify_entry", orr_id=orr_id)
        if self.form_result["category"] == hc.ERD_PRIVATE_CATEGORY:
            self._REQUIRE_PERM("erd_private", orr_id=orr_id)
        self.entry.title = self.form_result["title"]
        self.entry.category = self.form_result["category"]
        self.entry.content = self.form_result["content"]
        if self._has_perm("set_public", orr_id=orr_id):
            self.entry.is_public = self.form_result["is_public"]
        action = self.form_result["attachment"]["action"]
        file = self.form_result["attachment"]["file"]
        if action in ["delete", "replace"]:
            self._delete_attachment(self.entry)
        if action in ["add", "replace"] and file not in [None, ""]:
            self._add_attachment(self.entry, file.filename, file.file)
        Session.commit()
        h.flash("Modified entry.")
        redirect_to("entry", id=self.entry_id)

    def ask_delete(self, id):
        """Display the delete entry form, which submits to self.delete()."""
        self._process_entry_id(id)
        self._REQUIRE_PERM("delete_entry", orr_id=self.incident.orr_id)
        if self.entry.category == hc.ERD_PRIVATE_CATEGORY:
            self._REQUIRE_PERM("erd_private", orr_id=self.incident.orr_id)
        c.ht_title = "Delete entry"
        c.title = 'Delete entry "%s"' % self.entry.title
        c.crumbs = [
            h.link("Hotline", "hotline"),
            h.link("Incident", "incident", id=self.incident.orr_id),
            h.link("Entry", "entry", id=self.entry_id),
            "Modify"]
        c.entry = self.entry
        c.incident = self.incident
        c.action = h.url_for("entry", id=self.entry.entry_id)
        c.method = "DELETE"
        return render("/hotline/delete_entry.html")

    def delete(self, id):
        """Delete the entry."""
        self._process_entry_id(id)
        self._REQUIRE_PERM("delete_entry", orr_id=self.incident.orr_id)
        if self.entry.category == hc.ERD_PRIVATE_CATEGORY:
            self._REQUIRE_PERM("erd_private", orr_id=self.incident.orr_id)
        if request.params.get("submit", "").lower() != "yes":
            h.flash("Cancelled delete operation.")
            redirect_to("entry", id=self.entry_id)
        self._delete_attachment(self.entry)
        Session.delete(self.entry)
        Session.commit()
        h.flash("Deleted entry.")
        redirect_to("incident", id=self.incident.orr_id)

    def photologger(self, orr_id):
        self._process_orr_id(orr_id)
        self._REQUIRE_PERM("add_entry", orr_id=orr_id)
        c.title = "Import from PhotoLogger"
        c.crumbs = [
            h.link("Hotline", "hotline"),
            h.link("Incident", "incident", id=self.orr_id),
            "PhotoLogger"]
        c.action = h.url_for("photologger_submit", orr_id=self.orr_id)
        c.method = "POST"
        c.orr_id = self.orr_id
        return render("/hotline/photologger_form.html")

    @validate(schema=PhotoLoggerForm(), form="photologger")
    def photologger_submit(self, orr_id):
        self._process_orr_id(orr_id)
        orr_id = self.orr_id
        self._REQUIRE_PERM("add_entry", orr_id=orr_id)
        now = datetime.datetime.now()
        wrapper = textwrap.TextWrapper(width=90)
        upload = self.form_result["file"]
        try:
            archive = zipfile.ZipFile(self.form_result["file"].file, "r")
        except zipfile.BadZipfile:
            pass   
        log.debug(archive.namelist())
        index = archive.read("index.ini")
        index_fp = StringIO(index)
        cp = ConfigParser.RawConfigParser()
        cp.readfp(index_fp)
        log.debug(cp.sections())
        count = 0
        for section in cp.sections():
            #log.debug("Section %s:", section)
            section.decode("windows-1252", "xmlcharrefreplace")
            filename = section  # Just so we don't forget.
            title = cp.get(section, "Subject").decode("windows-1252", 
                "xmlcharrefreplace")
            category = cp.getint(section, "Category")  # @@MO Should validate.
            content = cp.get(section, "Content").decode("windows-1252", 
                "xmlcharrefreplace")
            content = content.replace("Comment: ", "\nComment: ")
            content = h.wrap_long_lines(content, wrapper)
            if content.strip():
                content += "\n\n"
            content += "Imported from PhotoLogger."
            is_public = False  # @@MO Should get from form if has permission.
            entry = self._create_entry(orr_id, title, category, 
                content, is_public)
            attachment_content = archive.read(filename)
            fp = StringIO(attachment_content)
            self._add_attachment(entry, filename, fp)
            self.incident.last_entry_date = entry.entry_date
            count += 1
        Session.commit()
        what = h.plural(count, "image", "images")
        h.flash("Imported %s from PhotoLogger file." % what)
        redirect_to("incident", id=orr_id)


    # UNUSED:
    #def photologger_results(self):
    #    # Get results from session.
    #    try:
    #        c.successes = session.pop("photologger_successes")
    #        c.failures = session.pop("photologger_failures")
    #    except KeyError:
    #        abort(400, "No photologger upload found.")
    #    return render("/hotline/photologger_results.html")


    ### Private methods
    def _get_category_pairs(self, orr_id):
        if 1 or self._has_perm("erd_private", orr_id=orr_id):
            category_pairs = [(x.id, x.label) for x in hc.CATEGORIES.values()]
        else:
            category_pairs = [(x.id, x.label) for x in hc.CATEGORIES.values()
                if x.id != hc.ERD_PRIVATE_CATEGORY]
        category_pairs.sort(key=lambda x: x[1])
        return category_pairs

    def _create_entry(self, orr_id, title, category, content, is_public):
        """Create an Entry object and attach it to the database.

        Return the new entry object.

        Automatically sets ``entry_id``, ``entry_date``, and ``creator``
        attributes, and no attachment.  Saves the entry to the database
        but does not commit the transaction.
        """
        entry = Entry()
        entry.orr_id = orr_id
        entry.title = title
        entry.entry_date = datetime.datetime.now()
        entry.creator = session["user"].username
        entry.category = category
        entry.content = content
        entry.is_public = is_public
        entry.filename = ""
        entry.thumb200 = ""
        entry.doctype = ""
        entry.size = 0
        Session.save(entry)
        Session.flush()  # Write the entry to the db to assign an entry_id.
        assert entry.entry_id, "Failed to add entry to database."
        return entry

    def _add_attachment(self, entry, filename, fp):
        """Save the upload to a file and update the Entry table.
           Called when adding the attachment, and when replacing it too.

           ``entry``: the entry to attach it to.
           ``filename``: the user's preferred filename.
           ``fp``: a file-like object containing the attachment, open for
               reading and positioned at the beginning.  It will be read
               and closed.

           No return value.
        """
        log.debug("adding attachment for file %s", filename)
        filename = Path(sanitize_filename(filename))
        stem = filename.stem
        ext = filename.ext
        # PDF thumbnail routine doesn't work right if multiple "." in the
        # filename
        if "." in stem:
            stem = stem.replace(".", "_")
            filename = Path(stem + ext)
        # Make sure the filename is short enough for the database fields.
        max_length = FILENAME_LENGTH - len(ext)
        if len(stem) > max_length:
            log.info("Shortening filename %r, length %d", filename, len(filename))
            filename = stem[:max_length] + ext
            log.info("Shortened to %r, length %d", filename, len(filename))
        entry.filename = filename
        orig = h.attachment_path(entry)
        log.debug("saving attachment for entry %d to %s", entry.entry_id, orig)
        if not orig.parent.exists():
            orig.parent.mkdir(parents=True)
        self._save_upload(orig, fp)
        if orig.lower().endswith(".pdf"):
            thumb = make_pdf_thumbnail(orig, 200)
        else:
            thumb = make_thumb(orig, 200)
            # @@MO: Error making thumbnails from JPG due to palette mode.
            # I don't know if this is a limitation of PIL or we're not using
            # PIL right.
        entry.doctype = ext[1:]
        entry.size = orig.size()
        entry.thumb200 = Path(thumb).name if thumb else ""

    def _delete_attachment(self, entry):
        """Delete the attachment files and update the Entry table.
           Called when deleting the attachment, and when replacing it too.

           `entry`: the entry to delete the attachment from.
           No return value.
        """
        if not entry.filename:
            return
        dir = h.attachment_path(entry).parent
        log.debug("deleting attachment diectory '%s'", dir)
        if dir.isdir():
            try:
                dir.rmtree()
            except Exception, e:
                msg = "caught exception deleting entry directory '%s': %s: %s"
                log.warn(msg, dir, e.__class__.__name__, e)
        elif dir.isfile():
            msg = "tried to delete entry directory '%s' but it's a file"
            log.warn(msg, dir)
        # Try to delete incident directory too.
        try:
            dir.parent.rmdir()
        except OSError:
            pass   # Assume it's not empty; it probably contains other entries.
        # Else the directory doesn't exist; ignore it.
        entry.filename = ""
        entry.thumb200 = ""
        entry.doctype = ""
        entry.size = 0

        

#### Helper utilities ####
class IndexParamsParser(object):
    """Parse the query parameters used by EntryController.index.

       Instance variables:
       .incident:  model.hotline.Incident based on 'orr_id' param.
       .category:  hazpy.hotline.Category or None.
       .thumbs:    boolean. Show thumbnails view instead of list view.
    """
    def __init__(self, params):
        self.incident = self._get_incident(params)
        self.category = self._get_category(params)
        self.thumbs = self._get_thumbs(params, self.category)

    def _get_incident(self, params):
        """Fetch an incident via 'orr_id' query parameter.
           Abort if parameter is absent or refers to nonexistent incident.
        """
        try:
            orr_id = int(params["orr_id"])
        except KeyError:
            abort(400, "query parameter 'orr_id' required")
        except ValueError:
            abort(400, "query parameter 'orr_id' must be numeric")
        incident = Incident.get(orr_id)
        if not incident:
            abort(400, "incident #%d does not exist" % orr_id)
        return incident

    def _get_category(self, params):
        """Fetch a Category via 'category' query parameter.
           Return None if no category was specified.
        """
        catnum = params.get("category")
        if not catnum:
            return None  # User did not specify category.
        try:
            catnum = int(catnum)
        except ValueError:
            abort(400, "query parameter 'category' must be numeric")
        try:
            category = hc.CATEGORIES[catnum]
        except KeyError:
            abort(400, "no such category '%s'" % category) # Safe, numeric.
        return category

    def _get_thumbs(self, params, category):
        """Return the boolean 'thumbs' param, which tells whether to display
           the index as a list (false) or thumbnails (true).  If param is
           missing, use the category's default view.  If the category is None,
           return False.
        """
        if "thumbs" in params:
            return bool(params["thumbs"])
        if category:
            return category.default_thumb
        return False

