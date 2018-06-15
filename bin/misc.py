def convert_size(sb):
    """
    Attempts to convert byte count into easily digestible values such as 10 GB
    :param sb:
    :returns str:
    """
    if sb <= 1023:
        return f'{sb} B'
    elif len(str(sb)) >= 10:
        sb = sb>>20
        return f'{str(sb)[0]}.{str(sb)[1:]} GB'
    elif len(str(sb)) >= 7:
        sb = sb>>10
        return f'{sb} MB'

def fmt_percent(pcnt:float, invert:bool=False, fmt='{}%'):
    """
    Formats values into a percentage-friendly string
    :param pcnt:
    :param invert:
    :param fmt:
    :return:
    """
    if invert: # inverts value for use with "amount left" scenarios
        pcnt = float(str(pcnt - 100).replace('-',''))
    s = str(pcnt).split('.')
    d = s[1] # d means decimal value
    d += '0'
    if d[1]:
        if int(d[1]) >= 5:
            d = str(int(d) + 1)
        d = d[0]
    s[1] = d
    pcnt = '.'.join(s)
    del s, d
    return fmt.format(pcnt)
