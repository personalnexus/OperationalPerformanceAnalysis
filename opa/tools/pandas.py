def fillNa(dataFrame, aggregator):
    for columnName in dataFrame.columns:
        fillNaCol(dataFrame, aggregator, columnName)


def fillNaCol(dataFrame, aggregator, columnName):
    column = dataFrame[columnName]
    value = aggregator(column)
    column.fillna(value=value, inplace=True)
    return dataFrame
