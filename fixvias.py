#!/usr/bin/python
"""
Create a json file using http://www.keyboard-layout-editor.com/

Use that file to create a kicad schematic and pcb with the switches.
"""

import six
import json
import codecs
from time import time
from pprint import pprint

# export PYTHONPATH=/usr/local/kicad/Frameworks/python/site-packages
import pcbnew
kicad = pcbnew.IO_MGR.PluginFind(pcbnew.IO_MGR.KICAD)


# def place_footprint(pcb, x, y, reference=None, i=None):
#     # Place the switch
#     fp = kicad.FootprintLoad()
#     pcb.Add(fp)
#     fp.Rotate(pcbnew.wxPoint(0, 0), 1800)
#     fp.SetPosition(pcbnew.wxPoint(x * spacing, y * spacing))
#     if reference is None:
#         reference = "SW%d_%d" % (x, y)
#     fp.SetReference(reference)
#     fp.SetValue(reference)
#     fp.SetLocked(True)
#     # Place the diode
#     fp = kicad.FootprintLoad(diode_lib, diode_part)
#     pcb.Add(fp)
#     fp.Rotate(pcbnew.wxPoint(0, 0), 2700)
#     fp.SetPosition(pcbnew.wxPoint(x * spacing + diode_x_offset, y * spacing + diode_y_offset))
#     if i is not None:
#         reference = "D%d" % (i)
#     if reference is None:
#         reference = "D%d_%d" % (x, y)
#     fp.SetReference(reference)
#     fp.SetValue(reference)
#     fp.SetLocked(True)


def main():
    pcb = pcbnew.LoadBoard("test.kicad_pcb")
    # pprint(dir(pcbnew))
    for module in pcb.GetModules():
        if module.GetValue() == "GND Via":
            # pprint(dir(module))
            # help(module.Pads())
            pads = module.Pads()
            for p in pads:
                p.SetNetCode(108)
                # pprint(dir(p))
                print p.GetNetCode(), p.GetNetname()
    pcb.Save("test-out.kicad_pcb")

if __name__ == "__main__":
    main()
