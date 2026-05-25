import os
from dotenv import load_dotenv

load_dotenv()

user_1c = os.environ["1C_USER"]
pass_1c = os.environ["1C_PASSWORD"]
host_1c = os.environ["1C_HOST"]
rac_path = os.environ["RAC_PATH"]

id_test_cluster = os.environ["ID_TEST_CLUSTER"]
port_test = os.environ["PORT_TEST"]
id_demo_cluster = os.environ["ID_DEMO_CLUSTER"]
port_demo = os.environ["PORT_DEMO"]

pg_user = os.environ["PGUSER"]
pg_pass = os.environ["PGPASSWORD"]
pg_host = os.environ["PGHOST"]
pg_port = os.environ["PGPORT"]

custom_env = os.environ.copy()
custom_env["PGPASSWORD"] = pg_pass
custom_env["PGUSER"] = pg_user
custom_env["PGHOST"] = pg_host
custom_env["PGPORT"] = pg_port
custom_env["1C_USER"] = user_1c
custom_env["1C_PASSWORD"] = pass_1c
custom_env["1C_HOST"] = host_1c
custom_env["RAC_PATH"] = rac_path
custom_env["ID_TEST_CLUSTER"] = id_test_cluster
custom_env["PORT_TEST"] = port_test
custom_env["ID_DEMO_CLUSTER"] = id_demo_cluster
custom_env["PORT_DEMO"] = port_demo
