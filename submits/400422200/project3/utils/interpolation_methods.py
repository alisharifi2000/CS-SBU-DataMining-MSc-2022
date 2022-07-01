def linear_interpolation(data, config):
    if config['time'] == 'daily':
        data = data.set_index('time')
        data = data.resample('D').bfill(limit=1)
        if (config['skip_holiday']==True):
            data = data.drop(data[data.index.strftime('%A')=='Thursday'].index)
            data = data.drop(data[data.index.strftime('%A')=='Friday'].index)        
        data = data.interpolate(method=config['interpolation'])
        data.reset_index(inplace=True)

    elif config['time'] == 'monthly':
        data = data.set_index('time')
        data = data.resample('M').ffill(limit=1)
        data = data.interpolate(method=config['interpolation'])
        data.reset_index(inplace=True)
    elif config['time'] == 'hourly':
        data = data.set_index('time')
        data = data.resample('H').bfill(limit=1)
        if (config['skip_holiday']==True):
            data = data.drop(data[data.index.strftime('%A')=='Thursday'].index)
            data = data.drop(data[data.index.strftime('%A')=='Friday'].index)
        data = data.interpolate(method=config['interpolation'])
        data.reset_index(inplace=True)
    elif config['time'] == 'minutes':
        data = data.set_index('time')
        data = data.resample('1min').bfill(limit=1)
        if (config['skip_holiday']==True):
            data = data.drop(data[data.index.strftime('%A')=='Thursday'].index)
            data = data.drop(data[data.index.strftime('%A')=='Friday'].index)
        data = data.interpolate(method=config['interpolation'])
        data.reset_index(inplace=True)

    else:
        data = None

    return data


