import sqlite3

DB_NAME = "reminders.db"


class Database:
    CONNECTION = sqlite3.connect(DB_NAME)
    CURSOR = CONNECTION.cursor()

    @staticmethod
    def get_classname(obj):
        return obj.__class__.__name__

    @staticmethod
    def to_column_list(record):
        result = []
        for attr in record:
            if attr != "id":
                result.append(f"{attr} {Database.get_classname(record[attr])}")
            else:
                result.append(
                    f"{attr} {Database.get_classname(record[attr])} "
                    "primary key "
                )
        return result

    @staticmethod
    def create_table(table_name, record, force=False):

        record = record.to_dict(to_str=True)
        column_string = ", ".join(Database.to_column_list(record))
        query_string = f"CREATE TABLE {table_name} ({column_string})"
        print(query_string)
        try:
            Database.CURSOR.execute(query_string)
        except sqlite3.OperationalError as e:
            if force:
                Database.CURSOR.execute(f"DROP TABLE {table_name}")
                Database.CURSOR.execute(query_string)
            else:
                raise e

    @staticmethod
    def add_record(table_name, record):
        values = tuple(record.to_dict(to_str=True).values())
        query_string = f"INSERT INTO {table_name} VALUES ({', '.join('?' * len(values))})"
        Database.CURSOR.execute(query_string, values)

    @staticmethod
    def to_dict(column_names, record):
        return {column: value for column, value in zip(column_names, record)}

    @staticmethod
    def get_all_records(table_name, decoder_func=None):

        result = list(Database.CURSOR.execute(f"SELECT * from {table_name}"))

        if decoder_func:
            column_names = [description[0]
                            for description in Database.CURSOR.description]
            result = [Database.to_dict(column_names, record)
                      for record in result]

        return result


if __name__ == "__main__":
    from reminders import Reminder

    # Table to work with
    table_name = "Reminders"

    # Create a Record for Testing
    record = Reminder("Hello", 15)
    record2 = Reminder("Hello", 15)

    # Force Creating the Table (Drops existing Table)
    force = True

    # Create Table
    Database.create_table(table_name=table_name, record=record, force=True)

    # Insert Record in Table
    Database.add_record(table_name=table_name, record=record)
    Database.add_record(table_name=table_name, record=record2)

    print(Database.get_all_records(table_name))

    print((result := Database.get_all_records(
        table_name, decoder_func=Reminder.from_dict)))

    assert Reminder.from_dict(result[0]) == record
    assert Reminder.from_dict(result[1]) == record2
