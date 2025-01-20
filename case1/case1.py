import os
from random import randbytes

from utils import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def case_1() -> None:
    """
    Just a normal case.
    """
    mysql = create_mysql_container("8.0", "fallen")

    create_mysql_table(mysql, "fallen", "gabriel", [("id", "int"), ("name", "varchar(255)")])
    insert_data_records(mysql, "fallen", "gabriel", [[str(i + 1), f"'{randbytes(3).hex()}'"] for i in range(100000)])

    pipeline_def = eval_pipeline_file('./pipeline.yml',
                                      {
                                          'username': 'root',
                                          'password': ROOT_PASSWORD,
                                          'host': mysql.get_container_host_ip(),
                                          'port': mysql.port,
                                          'parallelism': 4
                                      })

    logger.info(open(pipeline_def).read())

    os.system(f"../opt/flink-cdc/bin/flink-cdc.sh --flink-home ../opt/flink/ {pipeline_def}")
    mysql.stop()

case_1()
