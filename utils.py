import tempfile

import sqlalchemy
from loguru import logger
from testcontainers.mysql import MySqlContainer

ROOT_PASSWORD = 'game_over'


def create_mysql_container(tag: str, database: str) -> MySqlContainer:
    """
    Create a mysql container for testing purposes only.
    """
    mysql = MySqlContainer(f"mysql:{tag}", username="root", root_password=ROOT_PASSWORD)
    mysql.start()
    engine = sqlalchemy.create_engine(mysql.get_connection_url())
    with engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("select version()"))
        version, = result.fetchone()
        logger.success("Successfully created a MySQL {} container.", version)
        connection.execute(sqlalchemy.text(f"create database {database}"))
    return mysql


def create_mysql_table(mysql: MySqlContainer, database: str, table: str, schema: list[tuple[str, str]]) -> None:
    """
    Initialize a MySQL table.
    """
    engine = sqlalchemy.create_engine(mysql.get_connection_url())
    with engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            f"create table {database}.{table} (" + ", ".join([f"{column} {typ}" for column, typ in schema]) + ")"))
        logger.success("Successfully created table {}#{}.", database, table)


def insert_data_records(mysql: MySqlContainer, database: str, table: str, rows: list[list[str]]) -> None:
    """
    Spam data records into a table.
    """
    engine = sqlalchemy.create_engine(mysql.get_connection_url())
    with engine.begin() as connection:
        connection.execute(sqlalchemy.text(
            f"insert into {database}.{table} values " + ", ".join([f"({', '.join(row)})" for row in rows]) + ";"))
        logger.success("Successfully inserted {} rows into {}#{}.", len(rows), database, table)


def eval_pipeline_file(pipeline_file: str, kv: dict) -> str:
    """
    Read given pipeline file content, replace kv pairs and generate a temporary file for usage.
    """
    new_file = tempfile.NamedTemporaryFile(delete=False, delete_on_close=False)
    with open(pipeline_file) as f:
        content = f.read()

    for key, value in kv.items():
        content = content.replace("${{" + key + "}}", str(value))

    new_file.write(content.encode())
    return new_file.name


_TEMPORARY_PATH = './tmp.yaml'
