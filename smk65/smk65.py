#!/usr/bin/env python3
import os
from collections import defaultdict
from pprint import pprint
import builtins

if "KISYSMOD" not in os.environ:
    # os.environ["KISYSMOD"] = "~/dev/mechkeys/kicad-libs/:~/dev/kicad-library/library/:/Library/Application\ Support/kicad/library/"
    os.environ["KISYSMOD"] = "/Users/swilson/dev/mechkeys/kicad-libs/:/Users/swilson/dev/kicad-library/library/:/Library/Application\ Support/kicad/library/"
from skidl import (
    Net,
    Part,
    generate_netlist,
    TEMPLATE,
)

switch = Part('/Users/swilson/dev/mechkeys/kicad-libs/cherrymx.lib', 'MX_LED', TEMPLATE, footprint="Keyboard:MXALPS")
diode = Part('/Users/swilson/dev/mechkeys/kicad-libs/cherrymx.lib', '1SS309', TEMPLATE, footprint="Keyboard:SC-74A")

nets = defaultdict(Net)
row_nets = []
col_nets = []
diode_nets = []

# Don't use: D0, D1, C6, PE2

matrix_to_mcu = {
    "R1": "PB7",
    "R2": "PF7",
    "R3": "PF6",
    "R4": "PF5",
    "R5": "PF4",
    "C1": "PF0",
    "C2": "PF1",
    "C3": "PD2",
    "C4": "PD3",
    "C5": "PD5",
    "C6": "PD4",
    "C7": "PD6",
    "C8": "PD7",
    "C9": "PB4",
    "C10": "PB5",
    "C11": "PB6",
    "C12": "PC7",
    "C13": "PB3",
    "C14": "PB2",
    "C15": "PB1",
    "C16": "PB0",
}


parts = {
    'S1': switch(ref='S1', d_ref='D1', d_pin=5, row=1, col=1),
    'S2': switch(ref='S2', d_ref='D1', d_pin=4, row=1, col=2),
    'S3': switch(ref='S3', d_ref='D1', d_pin=3, row=1, col=3),
    'S4': switch(ref='S4', d_ref='D1', d_pin=1, row=1, col=4),
    'S5': switch(ref='S5', d_ref='D2', d_pin=3, row=1, col=5),
    'S6': switch(ref='S6', d_ref='D2', d_pin=4, row=1, col=6),
    'S7': switch(ref='S7', d_ref='D2', d_pin=5, row=1, col=7),
    'S8': switch(ref='S8', d_ref='D2', d_pin=1, row=1, col=8),
    'S9': switch(ref='S9', d_ref='D3', d_pin=3, row=1, col=9),
    'S10': switch(ref='S10', d_ref='D3', d_pin=4, row=1, col=10),
    'S11': switch(ref='S11', d_ref='D3', d_pin=5, row=1, col=11),
    'S12': switch(ref='S12', d_ref='D3', d_pin=1, row=1, col=12),
    'S13': switch(ref='S13', d_ref='D4', d_pin=3, row=1, col=13),
    'S14': switch(ref='S14', d_ref='D4', d_pin=4, row=1, col=14),
    'S15': switch(ref='S15', d_ref='D4', d_pin=5, row=1, col=15),
    'S115': switch(ref='S115', clone='S15'),
    'S16': switch(ref='S16', d_ref='D4', d_pin=1, row=1, col=16),

    'S17': switch(ref='S17', d_ref='D5', d_pin=1, row=2, col=1),
    'S18': switch(ref='S18', d_ref='D5', d_pin=3, row=2, col=2),
    'S19': switch(ref='S19', d_ref='D5', d_pin=4, row=2, col=3),
    'S20': switch(ref='S20', d_ref='D5', d_pin=5, row=2, col=4),
    'S21': switch(ref='S21', d_ref='D6', d_pin=3, row=2, col=5),
    'S22': switch(ref='S22', d_ref='D6', d_pin=4, row=2, col=6),
    'S23': switch(ref='S23', d_ref='D6', d_pin=5, row=2, col=7),
    'S24': switch(ref='S24', d_ref='D6', d_pin=1, row=2, col=8),
    'S25': switch(ref='S25', d_ref='D7', d_pin=3, row=2, col=9),
    'S26': switch(ref='S26', d_ref='D7', d_pin=4, row=2, col=10),
    'S27': switch(ref='S27', d_ref='D7', d_pin=5, row=2, col=11),
    'S28': switch(ref='S28', d_ref='D7', d_pin=1, row=2, col=12),
    'S29': switch(ref='S29', d_ref='D8', d_pin=4, row=2, col=13),
    'S30': switch(ref='S30', d_ref='D8', d_pin=5, row=2, col=15),
    'S31': switch(ref='S31', d_ref='D8', d_pin=1, row=2, col=16),

    'S32': switch(ref='S32', d_ref='D9', d_pin=3, row=3, col=1),
    'S132': switch(ref='S132', clone='S32', reversed=True),
    'S33': switch(ref='S33', d_ref='D9', d_pin=4, row=3, col=2),
    'S34': switch(ref='S34', d_ref='D9', d_pin=5, row=3, col=3),
    'S35': switch(ref='S35', d_ref='D9', d_pin=1, row=3, col=4),
    'S36': switch(ref='S36', d_ref='D10', d_pin=3, row=3, col=5),
    'S37': switch(ref='S37', d_ref='D10', d_pin=4, row=3, col=6),
    'S38': switch(ref='S38', d_ref='D10', d_pin=5, row=3, col=7),
    'S39': switch(ref='S39', d_ref='D10', d_pin=1, row=3, col=8),
    'S40': switch(ref='S40', d_ref='D11', d_pin=3, row=3, col=9),
    'S41': switch(ref='S41', d_ref='D11', d_pin=4, row=3, col=10),
    'S42': switch(ref='S42', d_ref='D11', d_pin=5, row=3, col=11),
    'S43': switch(ref='S43', d_ref='D11', d_pin=1, row=3, col=12),
    'S44': switch(ref='S44', d_ref='D12', d_pin=5, row=3, col=13),
    'S45': switch(ref='S45', d_ref='D12', d_pin=4, row=3, col=15),
    'S145': switch(ref='S145', clone='S45'),
    'S245': switch(ref='S245', clone='S45', reversed=True),
    'S345': switch(ref='S345', clone='S45'),
    'S46': switch(ref='S46', d_ref='D12', d_pin=3, row=3, col=16),

    'S47': switch(ref='S47', d_ref='D13', d_pin=5, row=4, col=1),
    'S147': switch(ref='S147', clone='S47'),
    'S48': switch(ref='S48', d_ref='D13', d_pin=4, row=4, col=2),
    'S49': switch(ref='S49', d_ref='D13', d_pin=3, row=4, col=3),
    'S50': switch(ref='S50', d_ref='D13', d_pin=1, row=4, col=4),
    'S51': switch(ref='S51', d_ref='D14', d_pin=3, row=4, col=5),
    'S52': switch(ref='S52', d_ref='D14', d_pin=4, row=4, col=6),
    'S53': switch(ref='S53', d_ref='D14', d_pin=5, row=4, col=7),
    'S54': switch(ref='S54', d_ref='D14', d_pin=1, row=4, col=8),
    'S55': switch(ref='S55', d_ref='D15', d_pin=3, row=4, col=9),
    'S56': switch(ref='S56', d_ref='D15', d_pin=4, row=4, col=10),
    'S57': switch(ref='S57', d_ref='D15', d_pin=5, row=4, col=11),
    'S58': switch(ref='S58', d_ref='D15', d_pin=1, row=4, col=12),
    'S59': switch(ref='S59', d_ref='D16', d_pin=4, row=4, col=13),
    'S159': switch(ref='S159', clone='S59'),
    'S60': switch(ref='S60', d_ref='D16', d_pin=5, row=4, col=15),
    'S61': switch(ref='S61', d_ref='D16', d_pin=3, row=4, col=16),

    'S62': switch(ref='S62', d_ref='D17', d_pin=4, row=5, col=1),
    'S162': switch(ref='S162', clone='S62', reversed=True),
    'S63': switch(ref='S63', d_ref='D17', d_pin=3, row=5, col=2),
    'S163': switch(ref='S163', clone='S63', reversed=True),
    'S263': switch(ref='S263', clone='S63', reversed=True),
    'S64': switch(ref='S64', d_ref='D17', d_pin=5, row=5, col=3, reversed=True),
    'S164': switch(ref='S164', clone='S64'),
    'S65': switch(ref='S65', d_ref='D17', d_pin=1, row=5, col=7),
    'S165': switch(ref='S165', clone='S65', reversed=True),
    'S265': switch(ref='S265', clone='S65'),

    'S66': switch(ref='S66', d_ref='D18', d_pin=4, row=5, col=11, reversed=True),
    'S166': switch(ref='S166', clone="S66", reversed=True),
    'S266': switch(ref='S266', clone="S66"),
    'S67': switch(ref='S67', d_ref='D18', d_pin=1, row=5, col=12),
    'S167': switch(ref='S167', clone="S67", reversed=True),
    'S68': switch(ref='S68', d_ref='D18', d_pin=3, row=5, col=13),
    'S168': switch(ref='S168', clone="S68", reversed=True),
    'S69': switch(ref='S69', d_ref='D18', d_pin=5, row=5, col=14),


    'S70': switch(ref='S70', d_ref='D12', d_pin=1, row=3, col=14),
    'S71': switch(ref='S71', d_ref='D16', d_pin=1, row=4, col=14),


    'D1': diode(ref='D1', row=1),
    'D2': diode(ref='D2', row=1),
    'D3': diode(ref='D3', row=1),
    'D4': diode(ref='D4', row=1),

    'D5': diode(ref='D5', row=2),
    'D6': diode(ref='D6', row=2),
    'D7': diode(ref='D7', row=2),
    'D8': diode(ref='D8', row=2),

    'D9': diode(ref='D9', row=3),
    'D10': diode(ref='D10', row=3),
    'D11': diode(ref='D11', row=3),
    'D12': diode(ref='D12', row=3),

    'D13': diode(ref='D13', row=4),
    'D14': diode(ref='D14', row=4),
    'D15': diode(ref='D15', row=4),
    'D16': diode(ref='D16', row=4),

    'D17': diode(ref='D17', row=5),
    'D18': diode(ref='D18', row=5),
}


def row_from_diode_net(net):
    diodes = [pin.part for pin in net.pins if pin.part.ref.startswith("D")]
    if len(diodes) != 1:
        print("WTF {} is connected to multiple diodes")
        return
    cathode_pins = diodes[0]["K"]
    cathode_row = cathode_pins[0].nets[0]  # At least one cathode is a member of this net
    if cathode_row not in row_nets:
        print("Diode {} is not connected to any row")
    # List of all nets connected to cathodes on this diode
    for pin in cathode_pins:
        for net in pin.nets:
            if net != cathode_row:
                print("More than one net attached to diode's cathode")
    return cathode_row


def validate_switches():
    matrix_check = defaultdict(list)
    for ref, switch in ((ref, switch) for (ref, switch) in parts.items() if ref.startswith("S")):
        pins = {
            "SW1": {
                "column": None,
                "diode": None,
                "row": None
            },
            "SW2": {
                "column": None,
                "diode": None,
                "row": None
            }
        }
        switch_valid = True
        for pin in pins:
            valid_row = False
            valid_col = False
            # find the pins connected to columns
            pin_nets = [net for net in switch[pin].nets if net in col_nets]
            if len(pin_nets) > 1:
                print("WTF {} is connected to multiple columns")
            elif len(pin_nets) == 1:
                pins[pin]["column"] = pin_nets[0].name
                if switch.col != int(pins[pin]["column"][1:]):
                    print("ERR: {ref} nets do not match definition:".format(ref=ref))
                    print("     Expected C{}, found {}".format(switch.col, pins[pin]["column"]))
                    break
                else:
                    valid_col = True

            pin_nets = [net for net in switch[pin].nets if net in diode_nets]
            if len(pin_nets) > 1:
                print("WTF {} is connected to multiple columns")
            elif len(pin_nets) == 1:
                if len(pin_nets[0].pins) > 2:
                    print('more than one pin net')
                pins[pin]["diode"] = pin_nets[0].name
                if len(pin_nets[0]) > 2:
                    print("Warn: multiple switches connected to {diode_net}:".format(diode_net=pin_nets[0].name))
                    print("      {}".format(pin_nets))
                pins[pin]["row"] = row_from_diode_net(pin_nets[0]).name
                if switch.row != int(pins[pin]["row"][1:]):
                    print("ERR: {ref} nets do not match definition:".format(ref=ref))
                    print("     Expected R{}, found {}".format(switch.row, pins[pin]["row"]))
                    break
                else:
                    valid_col = True
            if valid_row == valid_col:  # aka XNOR, pin must be connected to a row or column, but not both
                switch_valid = False
        if not switch_valid:
            print("ERR: {ref} did not pass validation:".format(ref=ref))
            # print(pins)
            # print(switch)
        matrix_check[(switch.col, switch.row)].append(switch)
    # pprint(matrix_check)
    for location, switch_list in matrix_check.items():
        if len(switch_list) > 1:
            print("Warn: multiple switches found on C{col} R{row}:".format(col=location[0], row=location[1]))
            print("      {}".format(", ".join((sw.ref for sw in switch_list))))


def validate_leds():
    for ref, switch in ((ref, switch) for (ref, switch) in parts.items() if ref.startswith("S")):
        k_nets = switch["K"].nets
        a_nets = switch["A"].nets
        if not k_nets:
            print("Warn: {ref} LED cathode is not connected:".format(ref=ref))
            continue
        elif len(k_nets) > 1:
            print("Warn: {ref} LED cathode connected to more than one net:".format(ref=ref))
        if not a_nets:
            print("Warn: {ref} LED anode is not connected:".format(ref=ref))
            continue
        elif len(a_nets) > 1:
            print("Warn: {ref} LED anode connected to more than one net:".format(ref=ref))

        k_pins = set(k_nets[0].pins)
        a_pins = set(a_nets[0].pins)
        if k_pins & a_pins:
            print("Warn: something is fucky:")
            print(switch)
            print(k_pins)
            print(a_pins)


def connect_switch_matrix():
    # Connect the diodes to their row
    for d in (v for (k, v) in parts.items() if k.startswith("D")):
        row = "R{}".format(d.row)
        for pin in d["k"]:
            nets[row] += pin

    # Connect switches
    for sw in (v for (k, v) in parts.items() if k.startswith("S")):
        # Switch to column
        pins = ("SW1", "SW2")
        if getattr(sw, "reversed", False):
            pins = ("SW2", "SW1")
        if(hasattr(sw, "clone")):
            parent = parts[sw.clone]
            col = "C{}".format(parent.col)
            d_ref = parent.d_ref
            d_pin = parent.d_pin
            parent["K"] += sw["K"]
            parent["A"] += sw["A"]
            setattr(sw, "row", parent.row)
            setattr(sw, "col", parent.col)
        else:
            col = "C{}".format(sw.col)
            d_ref = sw.d_ref
            d_pin = sw.d_pin
        nets[col] += sw[pins[0]]
        # Switch to diode
        net_name = "Matrix-{switch_ref}-{diode_ref}-{diode_pin}".format(
            switch_ref=sw.ref, diode_ref=d_ref, diode_pin=d_pin)
        nets[net_name] += sw[pins[1]]
        nets[net_name] += parts[d_ref][d_pin]


def set_name_names():
    # Name all of the nets by their dict key, and create sublists as needed
    for (key, net) in nets.items():
        net.name = key
        if key.startswith("C"):
            col_nets.append(net)
        if key.startswith("R"):
            row_nets.append(net)
        if key.startswith("Matrix"):
            diode_nets.append(net)


def add_controller():
    nets["+5v"] = Net("+5v")
    nets["GND"] = Net("GND")
    parts["U1"] = Part('/Users/swilson/dev/kicad-library/library/atmel.lib', 'ATMEGA32U4-AU', ref="U1", footprint='Housings_QFP:TQFP-44_10x10mm_Pitch0.8mm')
    for c in ("C4",):
        parts[c] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'C', ref=c, value="1µF", footprint='Capacitors_SMD:C_0805')
    for c in ("C3", "C7", "C6", "C8", "C9"):
        parts[c] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'C', ref=c, value="0.1µF", footprint='Capacitors_SMD:C_0805')
    for c in ("C1", "C2"):
        parts[c] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'C', ref=c, value="18pF", footprint='Capacitors_SMD:C_0805')
    parts["C5"] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'C', ref="C5", value="4.7µF", footprint='Capacitors_SMD:C_1206')
    for r in ("R1",):
        parts[r] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'R', ref=r, value="10k", footprint='Resistors_SMD:R_0805')
    for r in ("R4", "R5"):
        parts[r] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'R', ref=r, value="22", footprint='Resistors_SMD:R_0805')
    for r in ("R2", "R3"):
        parts[r] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'R', ref=r, value="4.7k", footprint='Resistors_SMD:R_0805')
    # for r in ("R7", "R8"):
    #     parts[r] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'R', ref=r, value="120", footprint='Resistors_SMD:R_0805')
    # parts["R6"] = Part('/Users/swilson/dev/kicad-library/library/device.lib', 'R', ref="R6", value="150", footprint='Resistors_SMD:R_0805')
    parts["F1"] = Part('/Users/swilson/dev/mechkeys/kicad-libs/device.lib', 'FP_Small', ref="F1", footprint='Capacitors_SMD:C_1206')
    parts["P1"] = Part('/Users/swilson/dev/kicad-library/library/conn.lib', 'USB_OTG', ref="P1", footprint='Capacitors_SMD:C_1206')
    parts["Y1"] = Part('/Users/swilson/dev/mechkeys/kicad-libs/device.lib', 'CRYSTAL_SMD', ref="Y1", footprint='Crystals:Crystal_SMD_5032_4Pads')
    parts["RESET"] = Part('/Users/swilson/dev/mechkeys/kicad-libs/device.lib', 'SW_PUSH', ref="S1", footprint='Buttons_Switches_SMD:SW_SPST_EVQP0')
    # parts["RGB33"] = Part('/Users/swilson/dev/mechkeys/kicad-libs/device.lib', 'Led_RGB_CA', ref="RGB33", footprint='Keyboard:SMP4-RGB-PIPE')

    # Power
    nets["+5v"] += parts["U1"]["VCC,VBUS"]
    nets["+5v"] += parts["F1"][2]
    # nets["+5v"] += parts["RGB33"][1]
    nets["+5v"] += parts["R1"][1]
    nets["GND"] += parts["U1"]["GND"]
    nets["GND"] += parts["U1"]["PE2"]
    for ref in ("C5", "C6", "C7", "C8", "C9"):
        nets["+5v"] += parts[ref][1]
        nets["GND"] += parts[ref][2]

    # XTAL
    parts["U1"]["XTAL1"] += parts["Y1"][1]
    parts["U1"]["XTAL1"] += parts["C1"][2]
    parts["U1"]["XTAL2"] += parts["Y1"][2]
    parts["U1"]["XTAL2"] += parts["C2"][2]
    nets["GND"] += parts["Y1"]["case"]
    nets["GND"] += parts["C1"][1]
    nets["GND"] += parts["C2"][1]

    # USB
    nets["VBUS"] += parts["P1"]["VBUS"]
    nets["VBUS"] += parts["F1"][1]
    nets["USB-"] += parts["P1"]["D-"]
    nets["USB-"] += parts["R4"][2]
    nets["USB+"] += parts["P1"]["D\+"]
    nets["USB+"] += parts["R5"][2]
    nets["D-"] += parts["R4"][1]
    nets["D-"] += parts["U1"]["D-"]
    nets["D+"] += parts["R5"][1]
    nets["D+"] += parts["U1"]["D\+"]
    nets["GND"] += parts["P1"]["GND"]
    nets["GND"] += parts["P1"]["shield"]

    # MCU
    parts["U1"]["UCAP"] += parts["C3"][1]
    nets["GND"] += parts["C3"][2]
    parts["U1"]["AREF"] += parts["C4"][1]
    nets["GND"] += parts["C4"][2]
    nets["RESET"] += parts["U1"]["RESET"]
    nets["RESET"] += parts["RESET"][1]
    nets["RESET"] += parts["R1"][2]
    nets["GND"] += parts["RESET"][2]
    for k, v in matrix_to_mcu.items():
        print(k, v)
        nets[k] += parts["U1"][v]

    # I2C
    nets["+5v"] += parts["R2"][1]
    nets["LED_SCL"] += parts["R2"][2]
    nets["LED_SCL"] += parts["U1"]["SCL/"]
    nets["+5v"] += parts["R3"][1]
    nets["LED_SDA"] += parts["R3"][2]
    nets["LED_SDA"] += parts["U1"]["SDA/"]

    # USB Connector
    parts["P2"] = Part('/Users/swilson/dev/kicad-library/library/conn.lib', 'CONN_01X05', ref="P2", footprint='Connectors_JST:JST_SH_SM05B-SRSS-TB_05x1.00mm_Angled')
    nets["VBUS"] += parts["P2"][5]
    nets["USB-"] += parts["P2"][4]
    nets["USB+"] += parts["P2"][3]
    nets["GND"] += parts["P2"][1]

    # ISP Connector
    parts["P3"] = Part('/Users/swilson/dev/kicad-library/library/conn.lib', 'CONN_02X03', ref="P3", footprint='Connectors_JST:JST_SH_SM06B-SRSS-TB_06x1.00mm_Angled')
    nets["+5v"] += parts["P3"][2]
    nets["GND"] += parts["P3"][6]
    nets["RESET"] += parts["P3"][5]
    parts["P3"][1] += parts["U1"]["MISO"]
    parts["P3"][3] += parts["U1"]["SCLK"]
    parts["P3"][4] += parts["U1"]["MOSI"]

    # USB Connector
    parts["P4"] = Part('/Users/swilson/dev/kicad-library/library/conn.lib', 'CONN_01X03', ref="P4", footprint='Connectors_JST:JST_SH_SM03B-SRSS-TB_03x1.00mm_Angled')
    nets["+5v"] += parts["P4"][2]
    nets["GND"] += parts["P4"][1]
    parts["P4"][3] += parts["U1"]["PC6"]

    # # Layer LED
    # parts["U1"]["PB5"] += parts["R6"][1]
    # parts["U1"]["PB6"] += parts["R7"][1]
    # parts["U1"]["PB7"] += parts["R8"][1]
    # nets["+5v"] += parts["RGB33"][1]
    # parts["RGB33"]["R"] += parts["R6"][2]
    # parts["RGB33"]["G"] += parts["R7"][2]
    # parts["RGB33"]["B"] += parts["R8"][2]


add_controller()
connect_switch_matrix()
set_name_names()
validate_switches()
generate_netlist()
