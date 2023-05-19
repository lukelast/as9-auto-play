"""
Calibrated for Elise 220.
"""
to_the_docks = {
    4: 'right',
    9: 'right',
    12: 'nitro2',
    26: 'left',
    29: 'nitro2',
    33: 'nitro-stop',

    # Initial drift left.
    #3: 'drift-start',
    #8: ('drift-stop', 'nitro2'),

    # Nitro bottle
    #11: 'left',

    # Switch to yellow nitro.
    #13: ('nitro-stop', 'nitro'),

    # Double nitro bottle
    #24: 'right',

    # Turn right.
    37: 'drift-start',
    # Double nitro bottle on right.
    41: ('right', 'drift-stop', 'nitro2'),

    # Left drift into S route
    46: 'drift-start',
    47: 'left',
    50: 'drift-stop',

    # In S road.
    54: 'nitro2',

    # Left out of S
    57: 'drift-start',
    59: ('drift-stop', 'nitro'),
    62: 'nitro',  # Try for blue nitro.

    # Slight right, see if we can skip the drift.
    #63: ('nitro-stop', 'nitro'),

    # Super sharp left corner
    68: 'drift-start',
    73: ('drift-stop', 'nitro2'),

    # Slight right corner
    77: 'drift-start',
    79: 'left',
    82: ('drift-stop', 'nitro2'),

    # Final left corner
    84: 'drift-start',
    88: ('drift-stop', 'nitro2'),
}

