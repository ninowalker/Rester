from SimpleHTTPServer import SimpleHTTPRequestHandler
from logging import getLogger
import BaseHTTPServer
import logging
import os
import posixpath
import sys
import threading
import time
import urllib

LOG = getLogger(__name__)


class BetterHTTPRequestHandler(SimpleHTTPRequestHandler):
    working_dir = None

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                self.send_response(301)
                self.send_header("Location", self.path + "/")
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)
        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        # Don't forget explicit trailing slash when normalizing. Issue17324
        trailing_slash = path.rstrip().endswith('/')
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = self.working_dir
        for word in words:
            _drive, word = os.path.splitdrive(word)
            _head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        if trailing_slash:
            path += '/'
        return path


class HTTPFileServer(object):
    def __init__(self, directory=os.getcwd(), address="127.0.0.1", port=8001, protocol="HTTP/1.0", handler_class=BetterHTTPRequestHandler, server_class=BaseHTTPServer.HTTPServer):
        handler_class.protocol_version = protocol
        handler_class.working_dir = directory
        server_class.allow_reuse_address = True
        self.directory = directory
        self.stopped = False
        self.httpd = server_class((address, port), handler_class)

    def run(self):
        sa = self.httpd.socket.getsockname()
        LOG.info("Serving files from %s, on %s:%s...", self.directory, sa[0], sa[1])
        try:
            self.httpd.serve_forever()
        except:
            if not self.stopped:
                raise
            LOG.info("shutdown %s:%s", sa[0], sa[1])

    def stop(self):
        self.stopped = True
        sa = self.httpd.socket.getsockname()
        LOG.info("shutting down %s:%s...", sa[0], sa[1])
        self.httpd.server_close()
        time.sleep(.1)


def run(case, directory=".", port=8001, address="127.0.0.1"):
    path = os.path.join(case.root, directory)
    server = HTTPFileServer(directory=path, port=port, address=address)
    t = threading.Thread(target=server.run)
    t.daemon = True
    t.start()
    return server.stop


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    stop = None
    try:
        stop = run(os.getcwd(), sys.argv[1])
        while True:
            time.sleep(1)
    finally:
        if stop:
            LOG.warn("shutdown...")
            stop()
            time.sleep(1)
