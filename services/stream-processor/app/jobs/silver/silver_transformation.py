from pyspark.sql import DataFrame

def cast_to_str(df: DataFrame, cols: list) -> DataFrame:
    for col in cols:
        df = df.withColumn(col, df[col].cast("string"))
    return df
