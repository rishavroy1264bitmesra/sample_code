import codecs
import datetime
from utils.tags import Tag
import tornado.web
import setup_log
from src.pipeline_executor import Executor
import logging

logger = logging.getLogger(__name__)


class service_check_handler(tornado.web.RequestHandler):
    def get(self):
        self.write('CI Service is up')


class ParaExtraction(tornado.web.RequestHandler):
    def post(self):
        reader = codecs.getreader("utf-8")
        jstr = (self.request.body).decode('ISO-8859-1')
        arguments = self.request.headers
        Client_Name = Tag.GENERIC.value
        if Tag.CLIENT_NAME.value in arguments:
            Client_Name = arguments[Tag.CLIENT_NAME.value]
        logger.info("Request received at : %s", datetime.datetime.now())
        logger.info("Client Name: %s", Client_Name)
        extract = Executor(Client_Name)
        outputJson = extract.normalresponse(jstr)
        self.write(outputJson)
        logger.info("Response sent !")
        self.finish()

class HTMLParaExtraction(tornado.web.RequestHandler):
    def post(self):
        reader = codecs.getreader("utf-8")
        jstr = (self.request.body).decode('ISO-8859-1')
        arguments = self.request.headers
        Client_Name = Tag.GENERIC.value
        if Tag.CLIENT_NAME.value in arguments:
            Client_Name = arguments[Tag.CLIENT_NAME.value]
        logger.info("Request received at : %s", datetime.datetime.now())
        logger.info("Client Name: %s", Client_Name)
        extract = Executor(Client_Name)
        outputJson = extract.htmlresponse(jstr)
        self.write(outputJson)
        logger.info("Response sent !")
        self.finish()

class FlatResponseGenerator(tornado.web.RequestHandler):
    def post(self):
        reader = codecs.getreader("utf-8")
        jstr = (self.request.body).decode('ISO-8859-1')
        arguments = self.request.headers
        Client_Name = Tag.GENERIC.value
        if Tag.CLIENT_NAME.value in arguments:
            Client_Name = arguments[Tag.CLIENT_NAME.value]
        logger.info("Request received at : %s", datetime.datetime.now())
        logger.info("Client Name: %s", Client_Name)
        extract = Executor(Client_Name)
        outputJson = extract.flatresponse(jstr)
        self.write(outputJson)
        logger.info("Response sent !")
        self.finish()


class LineIdsResponseGenerator(tornado.web.RequestHandler):
    def post(self):
        reader = codecs.getreader("utf-8")
        jstr = (self.request.body).decode('ISO-8859-1')
        arguments = self.request.headers
        Client_Name = Tag.GENERIC.value
        if Tag.CLIENT_NAME.value in arguments:
            Client_Name = arguments[Tag.CLIENT_NAME.value]
        logger.info("Request received at : %s", datetime.datetime.now())
        logger.info("Client Name: %s", Client_Name)
        extract = Executor(Client_Name)
        outputJson = extract.sub_section_lineids_response(jstr)
        self.write(outputJson)
        logger.info("Response sent !")
        self.finish()


# End points
application = tornado.web.Application([(r"/holmes4business/contract_intel/v2/sectionExtract", ParaExtraction),
                                       (r"/holmes4business/contract_intel/v2/flatResponse", FlatResponseGenerator),
                                       (r"/holmes4business/contract_intel/v2/lineidsResponse",LineIdsResponseGenerator),
                                       (r"/holmes4business/contract_intel/v2/htmlResponse",HTMLParaExtraction)],
                                      debug=True)

if __name__ == "__main__":
    application.on_close(8885)
    setup_log.setup_logging()
    application.listen(8885, max_buffer_size=1048576000)
    logger.info(
        "Generic Document Alignment Service is Up, Please pass key=Client and value=Client name to run Dynamically.")
    tornado.ioloop.IOLoop.instance().start()
