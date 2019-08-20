from spyne import Application, rpc, ServiceBase, Integer, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from lxml import etree #для вывода входящего xml-запроса

class SampleSoapService(ServiceBase):
    @rpc(Unicode, Integer, Unicode, _returns=Unicode) #параметры: типы переменных во входящем запросе + типы переменных в ответе сервера
    def msg(ctx, name, id, msg): #сtx (расшифровать), переменные-члены нашего комплексного типа (см. схему)
        print(etree.tostring(ctx.in_document)) #печать входящего xml-запроса
        return "Hello from SPYNE!" #возвращает эту строку


application = Application([SampleSoapService], 'SampleSoapService', #передаем созданный класс в Application, даем название схеме
                          in_protocol=Soap11(validator='lxml'), #указываем, что протокол входящего и выходящего сообщений - SOAP11
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application) #наш скрипт должен работать через wsgi


if __name__ == '__main__':
    import logging
    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
