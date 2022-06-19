from constants.sql import Queries
from models.meter import Meter
from models.meter_consumption import DataPoint
from utils.color import print_message
from utils.connector import Connector


class Database:
    connection = Connector.GetConnection()

    @staticmethod
    def AddMeter(meter: Meter):
        Database.ProcessQuery(Queries.ADD_METER_QUERY(meter), commit=True)

    @staticmethod
    def UpdateMeter(meter):
        Database.ProcessQuery(Queries.UPDATE_METER_QUERY(meter), commit=True)

    @staticmethod
    def DeleteMeter(meter):
        Database.ProcessQuery(Queries.DELETE_METER_QUERY(meter), commit=True)

    @staticmethod
    def GetMeterKeys():
        results = Database.ProcessQuery(Queries.GET_METER_KEYS_QUERY, fetchall=True)

        keys = []
        for result in results:
            keys.append(result[0])

        return keys

    @staticmethod
    def GetAllMeters():
        return Database.ProcessQuery(Queries.GET_ALL_METERS_QUERY, fetchall=True)

    @staticmethod
    def AddMeterConsumption(meter_consumption: DataPoint):
        Database.ProcessQuery(Queries.ADD_METER_CONSUMPTION_QUERY(meter_consumption), commit=True)

    @staticmethod
    def GetMeterConsumptionByMeter(meter_id):
        results = Database.ProcessQuery(Queries.GET_METER_CONSUMPTION_BY_METER_QUERY(meter_id), fetchall=True)

        meter_consumptions = []
        for result in results:
            meter_consumptions.append(DataPoint(result[0], result[1], result[2]))

        return meter_consumptions

    @staticmethod
    def GetMeterConsumptionByCity(city):
        results = Database.ProcessQuery(Queries.GET_METER_CONSUMPTION_BY_CITY_QUERY(city), fetchall=True)

        meter_consumptions = []
        for result in results:
            meter_consumptions.append(DataPoint(result[0], result[1], result[2]))

        return meter_consumptions

    @staticmethod
    def GetAllCities():
        return Database.ProcessQuery(Queries.GET_ALL_CITIES_QUERY, fetchall=True)

    @staticmethod
    def ProcessQuery(query, commit=False, fetchall=False, fetchone=False):
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
