# ascii

`ascii` is small CLI tool to display information on the ASCII characters as a table.

If called with no options it will display the decimal, hexadecimal and name
in 2 sets of columns (0-127 in the first and 128-255 in the second)

```
┏━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Dec ┃ Hex  ┃ Name                        ┃ Dec ┃ Hex  ┃ Name                                       ┃
┡━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 00  │ 0x00 │ Null                        │ 128 │ 0x80 │ Padding Character                          │
│ 01  │ 0x01 │ Start Of Heading            │ 129 │ 0x81 │ High Octet Preset                          │
│ 02  │ 0x02 │ Start Of Text               │ 130 │ 0x82 │ Break Permitted Here                       │
│ 03  │ 0x03 │ End Of Text                 │ 131 │ 0x83 │ No Break Here                              │
│ 04  │ 0x04 │ End Of Transmission         │ 132 │ 0x84 │ Index                                      │
│ 05  │ 0x05 │ Enquiry                     │ 133 │ 0x85 │ Next Line                                  │
│ 06  │ 0x06 │ Acknowledge                 │ 134 │ 0x86 │ Start Of Selected Area                     │
│ 07  │ 0x07 │ Alert                       │ 135 │ 0x87 │ End Of Selected Area                       │
│ 08  │ 0x08 │ Backspace                   │ 136 │ 0x88 │ Character Tabulation Set                   │
│ 09  │ 0x09 │ Character Tabulation        │ 137 │ 0x89 │ Character Tabulation With Justification    │
│ 10  │ 0x0A │ Line Feed                   │ 138 │ 0x8A │ Line Tabulation Set                        │

...

│ 127 │ 0x7F │ Delete                      │ 255 │ 0xFF │ Latin Small Letter Y With Diaeresis        │
└─────┴──────┴─────────────────────────────┴─────┴──────┴────────────────────────────────────────────┘
```

If passed with the flag `--aliases` then the table will be displayed with a row for each character
including a list of the aliases for the character.

```
ASCII Code Points
┏━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Dec ┃ Hex  ┃ Name                                  ┃ Aliases                                       ┃
┡━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ 00  │ 0x00 │ Null                                  │ NUL                                           │
│ 01  │ 0x01 │ Start Of Heading                      │ SOH                                           │
│ 02  │ 0x02 │ Start Of Text                         │ STX                                           │
│ 03  │ 0x03 │ End Of Text                           │ ETX                                           │
│ 04  │ 0x04 │ End Of Transmission                   │ EOT                                           │
│ 05  │ 0x05 │ Enquiry                               │ ENQ                                           │
│ 06  │ 0x06 │ Acknowledge                           │ ACK                                           │
│ 07  │ 0x07 │ Alert                                 │ BEL                                           │
│ 08  │ 0x08 │ Backspace                             │ BS                                            │
│ 09  │ 0x09 │ Character Tabulation                  │ Horizontal Tabulation, HT, TAB                │
│ 10  │ 0x0A │ Line Feed                             │ New Line, End Of Line, LF, NL, EOL            │

...

│ 255 │ 0xFF │ Latin Small Letter Y With Diaeresis   │                                               │
└─────┴──────┴───────────────────────────────────────┴───────────────────────────────────────────────┘
```

Uses the [rich](https://rich.readthedocs.io/en/latest/) library for the fancy table formattting.

The aliases are taken from the `NameAliases.txt` file provided as part of the Unicode UCD
and is [© 2020 Unicode®, Inc.](https://www.unicode.org/copyright.html)
