class Queries:
    CREATE_METER_CONSUMPTION_QUERY = '''CREATE TABLE METER_CONSUMPTION(
                            meter_id INT NOT NULL,
                            meter_usage INT NOT NULL,
                            usage_month TEXT NOT NULL,
                            CONSTRAINT METER_CONSUMPTION_FK FOREIGN KEY (meter_id) REFERENCES METERS(meter_id),
                            CONSTRAINT METER_CONSUMPTION_CH CHECK (meter_usage>=0)
                            )
                            '''
    DROP_METER_CONSUMPTION_QUERY = 'drop table METER_CONSUMPTION'

    CREATE_METERS_QUERY = '''CREATE TABLE METERS(
                            meter_id INT NOT NULL,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            street_name TEXT NOT NULL,
                            street_number INT NOT NULL,
                            zip_code INT NOT NULL,
                            city TEXT NOT NULL,
                            CONSTRAINT METERS_PK PRIMARY KEY (meter_id)
                            )
                            '''
    DROP_METERS_QUERY = 'drop table METERS'

    ADD_METER_QUERY = lambda meter: f"""insert into meters values(
                                         {meter.id},
                                         '{meter.first_name}',
                                         '{meter.last_name}',
                                         '{meter.street_name}',
                                         {meter.street_number},
                                         {meter.zip_code},
                                         '{meter.city}'
                                         )"""

    UPDATE_METER_QUERY = lambda meter: f"""update meters set  
                                            first_name = '{meter.first_name}',
                                            last_name = '{meter.last_name}', 
                                            street_name = '{meter.street_name}',
                                            street_number = {meter.street_number},
                                            zip_code = {meter.zip_code},  
                                            city = '{meter.city}'
                                            where meter_id = {meter.id}
                                            """

    DELETE_METER_QUERY = lambda meter: f"delete from METERS where METER_ID = {meter.id}"

    GET_METER_KEYS_QUERY = "select METER_ID from METERS order by METER_ID"

    GET_ALL_METERS_QUERY = "select * from METERS order by METER_ID"

    ADD_METER_CONSUMPTION_QUERY = lambda meter_consumption: f"""insert into METER_CONSUMPTION values(
                                                                 {meter_consumption.meter_id},
                                                                 {meter_consumption.value},
                                                                 '{meter_consumption.month}'
                                                                 )"""

    GET_METER_CONSUMPTION_BY_METER_QUERY = lambda \
            meter_id: f"select * from METER_CONSUMPTION where METER_ID = {meter_id}"

    GET_METER_CONSUMPTION_BY_CITY_QUERY = lambda city: f"""select METER_CONSUMPTION.*
                                                            from METER_CONSUMPTION, METERS
                                                            where METER_CONSUMPTION.meter_id = METERS.meter_id
                                                            and METERS.city = '{city}'"""

    GET_ALL_CITIES_QUERY = "select distinct city from METERS"