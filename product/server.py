from twisted.internet import reactor, protocol
import os
import csv
from contextlib import contextmanager

class Echo(protocol.Protocol):
    """This is just about the simplest possible protocol"""

    def dataReceived(self, data):
        self.callThis()
        self.transport.write(data)

    def callThis(self):
        with working_directory('./test'):
            with open('test.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

@contextmanager
def working_directory(directory):
    '''Decorator that defines a directory iterator, reverts back to original
       directory when the iterator is complete
    '''
    owd = os.getcwd()
    try:
        os.chdir(directory)
        yield directory
    finally:
        os.chdir(owd)

def main():
    """This runs the protocol on port 8000"""
    factory = protocol.ServerFactory()
    factory.protocol = Echo
    reactor.listenTCP(80,factory)
    reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
    main()
