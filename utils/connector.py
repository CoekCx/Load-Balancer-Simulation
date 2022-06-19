from mysql import connector


class Connector:
    @staticmethod
    def GetConnection():  # pragma: no cover
        return connector.connect(host='localhost', user='student', passwd='password', database='res')
