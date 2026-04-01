from datetime import date

def get_date() -> int:
    """ Este método é responsável por gerar uma seed utilizando a data atual. """
    _today = date.today().toordinal()
    return _today

def set_seed(date: int) -> int:
    """ Este método é responsável por gerar a seed. """
    seed = date ^ (date >> 30)
    seed *= 0xbf58476d1ce4e5b9
    seed = seed ^ (seed >> 27)
    seed *= 0x94d049bb133111eb
    seed = seed ^ (seed >> 31)

    return seed & 0xFFFFFFFFFFFFFFFF

def get_seed() -> int:
    """ Este método é responsável por gerar a seed utilizando a data atual. """
    seed = get_date()
    return set_seed(seed)