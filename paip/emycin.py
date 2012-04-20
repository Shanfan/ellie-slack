# -----------------------------------------------------------------------------
# Certainty factors

class CF(object):
    """Important certainty factor values."""
    true = 1.0
    false = -1.0
    unknown = 0.0
    cutoff = 0.2

def cf_or(a, b):
    """
    Compute the certainty factor of (A or B), where the certainty factors of A
    and B are a and b, respectively.
    """
    if a > 0 and b > 0:
        return a + b - a * b
    elif a < 0 and b < 0:
        return a + b + a * b
    else:
        return (a + b) / (1 - min(abs(a), abs(b)))

def cf_and(a, b):
    """
    Compute the certainty of (A and B), where the certainty factors of A and B
    are a and b, respectively.
    """
    return min(a, b)

def is_cf(x):
    """Is x a valid certainty factor; ie, is (false <= x <= true)?"""
    return CF.false <= x <= CF.true

def cf_true(x):
    """Do we consider x true?"""
    return is_cf(x) and x > CF.cutoff

def cf_false(x):
    """Do we consider x false?"""
    return is_cf(x) and x < (CF.cutoff - 1)


# -----------------------------------------------------------------------------
# Contexts

class Context(object):
    
    """A type of thing that can be reasoned about."""
    
    def __init__(self, name):
        self.count = 0 # track instances with numerical IDs
        self.name = name
    
    def instantiate(self):
        """Create and return a unique instance of the form (ctx_name, id)."""
        inst = (self.name, self.count)
        self.count += 1
        return inst


# -----------------------------------------------------------------------------
# Parameters

class Parameter(object):
    
    """A property type of a context instance."""
    
    def __init__(self, name, ctx=None, valid_type=lambda x: True, ask_first=False):
        self.name = name
        self.ctx = ctx
        self.valid_type = valid_type
        self.ask_first = ask_first
    
    def valid(self, thing):
        return self.valid_type(thing)


# -----------------------------------------------------------------------------
# Conditions
    
# A condition is a statement of the form (param inst op val), read as "the value
# of inst's param parameter satisfies the relation op(v, val)", where param is
# the name of a Parameter object, inst is a Context instance, op is a function
# that compares two parameter values to determine if the condition is true, and
# val is the parameter value.  A condition's truth is represented by a certainty
# factor.

def eval_condition(condition, values):
    """
    Determines the certainty factor of the condition (param, inst, op, val)
    using a list of values already associated with the param parameter of inst.
    values is of the form [(val1, cf1), (val2, cf2), ...].
    """
    param, inst, op, val = condition
    return sum(cf for known_val, cf in values if op(known_val, val))
