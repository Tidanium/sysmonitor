def convert_size(sb):
    if sb <= 1023:
        return f'{sb} B'
    elif len(str(sb)) >= 10:
        sb = sb>>20
        return f'{str(sb)[0]}.{str(sb)[1:]} GB'
    elif len(str(sb)) >= 7:
        sb = sb>>10
        return f'{sb} MB'

def fmt_percent(pcnt):
    return str(pcnt - 100).replace('-','')
