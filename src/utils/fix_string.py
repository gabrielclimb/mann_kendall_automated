# -*- coding: utf-8 -*-


def string_to_float(x):
    if isinstance(x, str):
        return round(float(x.replace("<", "").strip()), 3)
    return x


def string_test(value):
    try:
        float(value)
    except ValueError:
        return value
    except TypeError:
        pass


def get_columns_with_incorrect_values(df):
    str_cols = df.select_dtypes(object).columns[2:]
    string_in_float = [
        df
        for df in [df[col].apply(string_test).dropna() for col in str_cols]
        if len(df) > 0
    ]
    if len(string_in_float):
        for s in string_in_float:
            print(f"Column name: {s.name}\nValues: {s.values}\n")
        return True
