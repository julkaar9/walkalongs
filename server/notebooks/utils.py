from typing import Union
import re
from decimal import Decimal
import pandas as pd
from django.db import connection


def orm_to_df(record: any) -> pd.DataFrame:
    try:
        iter(record)
    except:
        record = [record]
    if isinstance(record, dict):
        record = [record]
    df = pd.DataFrame.from_records(record)
    return df


def sql_to_df(raw_qs: Union[dict, list[dict]]) -> pd.DataFrame:
    if not isinstance(raw_qs, list):
        raw_qs = [raw_qs]
    df = pd.DataFrame(raw_qs)
    return df


def dec_to_float(value: any, precision: int = 2):
    if isinstance(value, Decimal):
        return round(float(value), precision)
    return value


def round_(record: Union[float, any], precision=2):
    if isinstance(record, float):
        return round(float(record), precision)
    return record


def equal(sqlq, ormq) -> None:
    try:
        iter(ormq)
    except:
        ormq = [ormq]

    if isinstance(ormq, dict):
        ormq = [ormq]

    ormq = list(ormq)

    if not isinstance(sqlq, list):
        sqlq = [sqlq]

    pattern = re.compile(r"(?<!^)(?=[A-Z])")
    sqlq = [
        {pattern.sub("_", k).lower(): round_(v) for k, v in dict_.items()}
        for dict_ in sqlq
    ]
    ormq = [{k: dec_to_float(v) for k, v in dict_.items()} for dict_ in ormq]
    if sqlq == ormq:
        print("Equal ✔️")
    else:
        print("Unequal ❌")


def dictfetchall(cursor) -> list[dict]:
    """
    Return all rows from a cursor as a dict.
    Assume the column names are unique.
    """
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def sql_raw(raw_query: str) -> list[dict]:
    with connection.cursor() as c:
        sqlq = dictfetchall(c.execute(raw_query))
    return sqlq
