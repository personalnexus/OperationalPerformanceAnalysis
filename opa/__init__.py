from datetime import date, timedelta
from typing import Iterable
from readers import BaseLogFileReader
from opa import columns
import pandas as pd


def analyze(readers: Iterable[BaseLogFileReader], relevantDates: Iterable[date]) -> pd.DataFrame:
    relevantDatesList = [d for d in relevantDates]
    result = pd.DataFrame(columns=[columns.Timestamp])
    for reader in readers:
        pd.concat(result, reader.getEntriesAsDataFrame(relevantDatesList))
    result.set_index(columns.Timestamp, inplace=True)
    return result


def allDaysBetween(minDate: date, maxDate: date) -> Iterable[date]:
    """
    Return an iterable of all date, where minDate <= date <= maxDate
    """
    while minDate <= maxDate:
        yield minDate
        minDate = minDate + timedelta(days=1)


def allWorkingDaysBetween(minDate: date, maxDate: date) -> Iterable[date]:
    """
    Return an iterable of all date, where minDate <= date <= maxDate and date is Monday-Friday
    """
    for day in allDaysBetween(minDate, maxDate):
        if day.isoweekday() not in (6, 7):
            yield day
