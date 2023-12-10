
def get_orderded_df(filename):
    df = pd.read_csv(filename)
    df = df.sort_values(by=['t', 'x', 'y'])
    return df