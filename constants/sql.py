class Queries:
    CREATE_METER_CONSUMPTION_QUERY = '''CREATE TABLE METER_CONSUMPTION(
                            meter_id INT NOT NULL,
                            meter_usage INT NOT NULL,
                            usage_month TEXT NOT NULL,
                            CONSTRAINT METER_CONSUMPTION_FK FOREIGN KEY (meter_id) REFERENCES METERS(meter_id),
                            CONSTRAINT METER_CONSUMPTION_CH CHECK (meter_usage>=0)
                            )
                            '''

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
