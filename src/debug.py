import sys

COLORS = {
    'black': '\033[30m',
    'red': '\033[31m',
    'green': '\033[32m',
    'yellow': '\033[33m',
    'blue': '\033[34m',
    'magenta': '\033[35m',
    'cyan': '\033[36m',
    'white': '\033[37m',
    'reset': '\033[0m',
    'orange': '\033[33m'
}


def debug(message, color='green', *args, **kwargs):
    """Print a debug message using a named ANSI color."""
    color_code = COLORS.get(color.lower(), '')
    reset_code = COLORS['reset'] if color_code else ''
    prefix = '[DEBUG]'
    if args:
        print(f"{color_code}{prefix} {message}{reset_code}", *args, **kwargs)
    else:
        print(f"{color_code}{prefix} {message}{reset_code}", **kwargs)


def debug_error(message, *args, **kwargs):
    return debug(message, 'red', *args, **kwargs)


def debug_warning(message, *args, **kwargs):
    return debug(message, 'yellow', *args, **kwargs)


def debug_info(message, *args, **kwargs):
    return debug(message, 'blue', *args, **kwargs)

def debug_success(message, *args, **kwargs):
    return debug(message, 'green', *args, **kwargs)
