from sqlalchemy import create_engine
from sqlalchemy import inspect
from pprint import pprint

engine = create_engine("sqlite:///../Resources/hawaii.sqlite")
inspector = inspect(engine)

table_names = inspector.get_table_names()
for table_name in table_names:
    print(table_name)
    columns = inspector.get_columns(table_name)
    pprint(columns)