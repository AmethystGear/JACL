import re
from collections import OrderedDict 

BEGIN_ARRAY = '['
END_ARRAY = ']'

BEGIN_MAP = '{'
END_MAP = '}'

BEGIN_ORDERED_MAP = '[{'
END_ORDERED_MAP = '}]'

BEGIN_OBJECT = '('
END_OBJECT = ')'
OBJECT_TYPE = type('', (), {})

DELIM = ':'

STRING = '"'
RAW_STRING = 'r"'

# taken from https://stackoverflow.com/questions/249791/regex-for-quoted-string-with-escaping-quotes
# Marc-André Poulin's answer.
ESCAPEABLE_QUOTE_REGEX = r'"(?:[^"\\]*(?:\\.)?)*"'

BEGIN_COMMENT = '/*'
END_COMMENT = '*/'
COMMENT_REGEX = r'/*(.*?)*/'

class Scanner:
    def __init__(self, s):
        self.s = s
        self.offset = 0
        self.prev = []

    def eos(self):
        return self.offset == len(self.s)

    def scan(self, pattern):
        if isinstance(pattern, str):
            pattern = re.compile(pattern, re.DOTALL)
        match = pattern.match(self.s, self.offset)
        if match is not None:
            self.prev.append(self.offset)
            self.offset = match.end()
            return match.group(0)
        return None

    def undo(self):
        if len(self.prev) > 0:
            self.offset = self.prev.pop()

class Identifier:
    def __init__(self, name):
        if not name.isidentifier():
            raise ValueError('name ' + str(name) + ' is not identifier!')
        self.name = name

class Empty:
    def __init__(self):
        pass

def nextToken(s):
    s.scan(r'\s+')
    return s.scan(r'\S+')

def parse_bool(tok):
    if tok == "true" or tok == "false":
        return tok == "true"

    return None

def parse_int(tok):
    try:
        return int(tok)
    except ValueError:
        return None

def parse_float(tok):
    try:
        return float(tok)
    except ValueError:
        return None


def replace_escapes(s):
    return s.replace('\\\"', '\"').replace('\\\\', '\\')

def parse_string(tok, s):
    if tok[0] == STRING:
        s.undo()
        match = s.scan(ESCAPEABLE_QUOTE_REGEX)
        if match is None or '\n' in match:
            s.undo()
            nextToken(s)
            raise ValueError('broken string!')
        else:
            return replace_escapes(match)[1:-1]
    elif len(tok) >= 2 and tok[0:2] == RAW_STRING:
        s.undo()
        s.scan(r'r')
        return replace_escapes(s.scan(ESCAPEABLE_QUOTE_REGEX))[1:-1]
    
    return None

def parse_array(tok, s):
    if tok != BEGIN_ARRAY:
        return None

    tok = nextToken(s)
    arr = []
    while tok != END_ARRAY:
        val = parse_next(tok, s)
        if not isinstance(val, Empty):
            if isinstance(val, Identifier):
                raise ValueError('expected value, not identifier!')
            arr.append(val)

        if s.eos():
            raise ValueError('array was never terminated!')

        tok = nextToken(s)

    return arr

def parse_map(tok, s):
    begin = tok
    if tok != BEGIN_MAP and tok != BEGIN_ORDERED_MAP:
        return None
    
    tok = nextToken(s)
    if begin == BEGIN_MAP:
        _map = {}
        end = END_MAP
    else:
        _map = OrderedDict()
        end = END_ORDERED_MAP

    key = None
    while tok != end:
        val = parse_next(tok, s)
        if not isinstance(val, Empty):
            if isinstance(val, Identifier):
                raise ValueError('expected value, not identifier!')

            if key is None:
                if not isinstance(val, str):
                    raise ValueError('keys must be strings!')

                key = val

                delim = nextToken(s)
                if delim != DELIM:
                    raise ValueError('expected ' + str(DELIM))
            else:
                _map[key] = val
                key = None

        if s.eos():
            raise ValueError('map was never terminated!')

        tok = nextToken(s)

    return _map

def parse_object(tok, s):
    if tok != BEGIN_OBJECT:
        return None

    tok = nextToken(s)
    obj = OBJECT_TYPE()
    key = None
    while tok != END_OBJECT:
        val = parse_next(tok, s)
        if not isinstance(val, Empty):
            if key is None:
                if not isinstance(val, Identifier):
                    raise ValueError('object properties must be identifiers!')

                key = val

                delim = nextToken(s)
                if delim != DELIM:
                    raise ValueError('expected ' + str(DELIM))
            else:
                setattr(obj, key.name, val)
                key = None
        
        if s.eos():
            raise ValueError('object was never terminated!')

        tok = nextToken(s)
            
    return obj

def parse_comment(tok, s):
    if tok != BEGIN_COMMENT:
        return None
    
    s.undo()
    match = s.scan(COMMENT_REGEX)
    if match:
        return Empty()
    else:
        return None

def parse_next(tok, s):
    single_fns = [parse_bool, parse_int, parse_float]
    for fn in single_fns:
        val = fn(tok)
        if val is not None:
            return val

    mult_fns = [parse_comment, parse_string, parse_array, parse_map, parse_object]
    for fn in mult_fns:
        val = fn(tok, s)
        if val is not None:
            return val

    return Identifier(tok)

def parse(file):
    data = file.read().replace(',', ' ')
    s = Scanner(data)
    tok = nextToken(s)
    
    val = parse_next(tok, s)
    tok = nextToken(s)
    sc = None

    # these shorten syntax significantly when in early stages.
    if isinstance(val, Identifier):
        sc = Scanner("(\n" + data + "\n)")
    elif isinstance(val, str) and tok == DELIM:
        sc = Scanner("{\n" + data + "\n}")
    elif tok is not None:
        sc = Scanner("[\n" + data + "\n]")

    if sc is None:
        return val
    else:
        tok = nextToken(sc)
        return parse_next(tok, sc)

def print_data(data):
    if isinstance(data, OBJECT_TYPE):
        print(vars(data))
    else:
        print(data)

with open("test.jacl", 'r') as f:
    data = parse(f)
    print_data(data)
    