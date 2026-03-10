import pandas as pd

# import pandas as pd

def checker(file):

    if file.lower().endswith(".csv"):
        df = pd.read_csv(file)

    elif file.lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)

    else:
        raise ValueError("Unsupported file format")

    return df


# def data_loader(acquirer, target):

#     df1 = checker(acquirer)
#     df2 = checker(target)

#     return df1, df2

def data_loader(acquirer,target):
    df1=checker(acquirer)
    df2=checker(target)
    return df1,df2

def extract_schema(df):

    schema = []

    for col in df.columns:
        schema.append({
            "column_name": col,
            "dtype": str(df[col].dtype),
            "null_percentage": df[col].isnull().mean()*100,
            "unique_values": df[col].nunique()
        })

    return pd.DataFrame(schema)

def compare(our_schema,target_schema):
    comparison = []

    for col in our_schema["column_name"]:

        if col in target_schema["column_name"].values:
            target_dtype = target_schema[target_schema["column_name"]==col]["dtype"].values[0]

            comparison.append({
                "column": col,
                "status": "Match",
                "our_dtype": our_schema[our_schema["column_name"]==col]["dtype"].values[0],
                "target_dtype": target_dtype
            })

        else:
            comparison.append({
                "column": col,
                "status": "Missing in Target"
            })
    return comparison


