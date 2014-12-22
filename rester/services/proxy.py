from __future__ import absolute_import
from libmproxy import controller
from libmproxy.proxy.server import ProxyServer
from libmproxy.proxy import ProxyConfig
from logging import getLogger
import datetime
import os
import sys
import threading

LOG = getLogger(__name__)


class InterceptingMaster(controller.Master):
    def __init__(self, server):
        controller.Master.__init__(self, server)
        self._flows = []
        self.__shutdown = False

    def run(self):
        while not self.__shutdown:
            try:
                LOG.info("Starting proxy...")
                controller.Master.run(self)
            except KeyboardInterrupt:
                print 'KeyboardInterrupt received. Shutting down'
                self.shutdown()
                sys.exit(0)
            except Exception, e:
                print "Exception", e
                LOG.exception("Proxy error")
                pass

    def handle_request(self, flow):
        if flow.request.pretty_host(hostheader=True).endswith("dsr.livefyre.com"):
            print flow.request.pretty_host(hostheader=True)
            flow.request.host = "127.0.0.1"
            flow.request.port = 8001
            flow.request.update_host_header()
        msg = flow.request
        request_url = '%s://%s%s' % (msg.scheme, msg.host, msg.path)
        LOG.info("%s %s", msg.method, request_url)
        self._flows.append(msg)
        flow.reply()

    def shutdown(self):
        if not self.__shutdown:
            self.__shutdown = True
            LOG.info("shutting down proxy...")
            LOG.info("%s flows handled", len(self._flows))
        super(InterceptingMaster, self).shutdown()


def run(case, **config):
    config.setdefault('port', 3128)
    config.setdefault('host', '127.0.0.1')
    port = config['port']
    opts = case.request_opts.copy()
    opts['proxies'] = {"http": "http://localhost:%s" % port,
                       "https": "http://localhost:%s" % port}
    case.variables.add_variable('request_opts', opts)

    for svc in case.services:
        name, conf = svc.items()[0]
        if name == 'webdriver':
            conf.profile_preferences = {'network.proxy.type': 1,
                                        'network.proxy.http': '127.0.0.1',
                                        'network.proxy.http_port': port}

    cfg = ProxyConfig(**config)
    server = ProxyServer(cfg)
    master = InterceptingMaster(server)
    t = threading.Thread(target=master.run)
    t.daemon = True
    t.start()
    return master.shutdown
