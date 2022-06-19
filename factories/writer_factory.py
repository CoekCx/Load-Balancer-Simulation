from modules.writer import Writer


class WriterFactory:
    @staticmethod
    def MakeWriter(count: int, keys, writers):
        new_writer_id = 1
        for i in range(count):
            while new_writer_id in keys:
                new_writer_id += 1
            new_writer = Writer(new_writer_id)
            writers[new_writer_id] = new_writer
