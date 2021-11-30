import sqlalchemy
import pandas
import os

MASTER = 'postgresql://master:master@localhost:12345/master'
SLAVE = 'postgresql://slave:slave@localhost:12346/slave'

master_engine = sqlalchemy.create_engine(MASTER)
slave_engine = sqlalchemy.create_engine(SLAVE)

master_df = pandas.DataFrame([
    {'a': 'z', 'b': 'z'},
    {'a': 'y', 'b': 'y'},
    {'a': 'x', 'b': 'x'},
])

master_df.to_sql('test', master_engine, if_exists='replace')
os.system(f'pg_dump -Fc  -d {MASTER} > master.dump')
os.system(f'pg_restore --no-owner --no-acl -d {SLAVE} master.dump')

slave_df = pandas.read_sql(f'select a,b from test', slave_engine)

assert master_df.equals(slave_df)
