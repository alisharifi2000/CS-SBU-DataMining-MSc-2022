import pandas as pd
from khayyam import JalaliDate

def hijri_to_georgian(string):
    y,m,d = string.split('-')
    jalali = JalaliDate(int(y), int(m), int(d))
    return jalali.todate().strftime('%Y-%m-%d')

def georgian_to_hijri(datetime):
    return JalaliDate(datetime).strftime('%Y-%m-%d')

def miladi_base(df, config):
    resample_period = { 'minute': 'T', 'hourly': 'H', 'daily': 'D', 'monthly': 'M'}
    df = df.resample(resample_period[config['time']]).mean()

    if 'order' in config.keys():
        order = config['order']
    else:
        order = 1
    
    df.interpolate(method=config['interpolation'], order=order, inplace=True)

    df.reset_index(inplace=True)

    str_format = {'minute':'%Y-%m-%d %H:%M:00' ,'hourly':'%Y-%m-%d %H:00:00', 
                    'daily':'%Y-%m-%d', 'monthly':'%Y-%m-01'}
    df['time'] = df['time'].dt.strftime(str_format[config['time']]) 
    return df

def shamsi_base(df, config):
    df['georg'] = df['time'].apply(hijri_to_georgian)
    df['georg'] = pd.to_datetime(df['georg'])
    df.set_index('georg', inplace=True)

    if 'order' in config.keys():
        order = config['order']
    else:
        order = 1
    
    if 'skip_holiday' in config.keys():
        skip_holiday = config['skip_holiday']
    else:
        skip_holiday = False

    if config['time'] == 'daily':
        df = df.resample('D').mean()
        if skip_holiday:
            df['weekday'] = df.index.map(lambda x: JalaliDate(x).weekday())
            df = df[(df.weekday != 5) & (df.weekday != 6)]
        df.interpolate(method=config['interpolation'], order=order, inplace=True)
        df['time'] = df.index.map(georgian_to_hijri)
        df.reset_index(inplace=True)
        return df[['time', 'vol']]

    elif config['time'] == 'monthly':
        df = df.resample('D').mean()
        df['ym'] = df.index.map(lambda x: f'{str(JalaliDate(x).year)}-{str(JalaliDate(x).month)}')
        df['weekday'] = df.index.map(lambda x: JalaliDate(x).weekday())
        if skip_holiday:
            df = df[(df.weekday != 5) & (df.weekday != 6)]
        df = df.groupby('ym')[['vol', 'ym']].apply(lambda x: x.interpolate(method=config['interpolation'], order=order, limit_direction="both"))
        df = df.groupby(['ym']).mean().interpolate(method=config['interpolation'], order=order)
        df.reset_index(inplace=True)
        df['time'] = df['ym'].apply(lambda x: f"{x.split('-')[0]}-{x.split('-')[1].zfill(2)}-01")
        return df[['time', 'vol']]


def miladi(data, config):
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'])
    df = df.set_index('time')
    return miladi_base(df, config).to_json()

def shamsi(data, config):
    if config['service'] == 1:
        return shamsi_base(pd.DataFrame(data), config).to_json()
    if config['service'] == 2:
        df = pd.DataFrame(data)
        df['time'] = df['time'].apply(lambda x: georgian_to_hijri(pd.to_datetime(x)))
        return shamsi_base(df, config).to_json()