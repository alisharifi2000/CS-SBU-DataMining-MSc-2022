def clean_data(df):
    y = df['class']
    if 'id' in df.columns:
        df.drop(['id'], axis=1, inplace=True)

    if 'class' in df.columns:
        df.drop(['class'], axis=1, inplace=True)

    columns = df.columns

    return df.values, y.values, columns






