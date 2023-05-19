"""
Calibrated for D-Etense.
"""
metro = {
    # Get clear of the AI.
    6: 'nitro2',
    # Slight left corner.
    16: 'drift-start',
    18: 'drift-stop',
    # Start long nitro run.
    19: 'nitro',
    # Collect all the bottles.
    20: 'left',
    25: 'right',
    30: 'left',
    35: ('nitro-stop', 'nitro'),  # For low nitro cars.
    41: 'right',
    47: 'left',
    75: 'nitro2',  # Jump
    # Final chicane then barrel.
    79: 'drift-start',
    83: ('drift-stop', 'nitro2'),
    86: 'right',
    95: 'nitro',  # For low nitro cars.
}
