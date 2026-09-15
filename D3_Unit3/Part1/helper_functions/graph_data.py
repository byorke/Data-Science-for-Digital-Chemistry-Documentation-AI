import pandas as pd
import numpy as np


def get_task9_data():
    df = pd.read_csv(r"./files/aspirin_ir.csv")
    return (df[df.columns[0]].to_list(), df[df.columns[1]].to_list())
