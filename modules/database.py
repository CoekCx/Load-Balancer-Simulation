from constants.sql import Queries
from utils.color import print_message
from utils.connector import Connector


class Database:
    connection = Connector.GetConnection()

    def AddMeterConsumption(self, meter_consumption):
        pass

    def AddMeter(self, meter):
        pass

    def UpdateMeter(self, meter):
        pass

    def DeleteMeter(self, meter):
        pass

    def GetAllMeters(self):
        pass

    @staticmethod
    def __ProcessQuery(query, commit=False, fetchall=False, fetchone=False):
        results = None
        cur = Database.connection.cursor()
        cur.execute(query)
        if commit:
            cur.execute('commit')
        if fetchall:
            results = cur.fetchall()
        elif fetchone:
            results = cur.fetchone()
        cur.close()
        return results

    @staticmethod
    def CreateTable(create_meters_table=True, create_meters_consumption_table=True):
        if create_meters_table:
            try:
                cur = Database.connection.cursor()
                cur.execute(Queries.CREATE_METER_CONSUMPTION_QUERY)
                print_message('Created Meter Consumption table')
            except:
                cur.execute(Queries.DROP_METER_CONSUMPTION_QUERY)
                print_message('Dropped Meter Consumption table')
                Database.CreateTable()
            finally:
                cur.close()

        if create_meters_consumption_table:
            try:
                cur = Database.connection.cursor()
                cur.execute(Queries.CREATE_METERS_QUERY)
                print_message('Created Meters table')
            except:
                cur.execute(Queries.DROP_METERS_QUERY)
                print_message('Dropped Meters table')
                Database.CreateTable()
            finally:
                cur.close()
