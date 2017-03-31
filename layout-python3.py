#!/usr/bin/python
"""
Create a json file using http://www.keyboard-layout-editor.com/

Use that file to create a kicad schematic and pcb with the switches.
"""

import six
import json
import codecs
import os
from time import time
from pprint import pprint

#
# footprint_name is used to look up the pcb template below
#
# The following are currently defined:
#
# mx                - MX, no mounting holes, no LEDs
# mx_pcb            - MX, includes mounting holes, but no LEDs
# mx_led            - MX, includes LEDs and mounting holes
# mxalps            - mx merged with alps using slots (w/LEDs + holes)
# mxalps-no_pcb     - mx merged with alps using slots (w/LEDs, but no holes)
# mxalps-reversed   - mx merged with alps rotated 180 no LEDs or holes
# mxalps-no-led     - mx merged with alps, but no LEDs or holes
#
footprint_name = "mxalps"

# If 0 the LED slot will be at the top, if you're not using LEDs
# rotating 180 will orient the switch in the standard cherry way
# which is apparently more compatible with some key caps.
switch_rotate = 180

# Path to the json file downloaded from http://www.keyboard-layout-editor.com/
layout_file_name = "EL87.json"

# name that will be prepended to all output
project_name = "EL87"

# output directory
output_directory = os.path.join(os.getcwd(), project_name)

# project file
project_file_name = os.path.join(output_directory, project_name + ".pro")

# schematic file
schematic_file_name = os.path.join(output_directory, project_name + ".sch")

# pcb file
pcb_file_name = os.path.join(output_directory, project_name + ".kicad_pcb")

# PCB - Basics
pcb_spacing = 19.05  # 19.05mm aka .75"
x_origin = 2.0
y_origin = 1.5

# PCB - Diode placement relative to the switch
#
# WARNING: You almost certainly need to move some diodes manually. In
# particular check for overlap with stabilizers.
#
# Through hole examples:
#   Left side:
#     diode_rotate = 270
#     diode_x_offset = -9
#     diode_y_offset = -5
#     diode_label_rotate = 0
#     diode_label_x_offset = 3 * 2.54
#     diode_label_y_offset = -1.6
#   Top:
#     diode_rotate = 0
#     diode_x_offset = -7.62
#     diode_y_offset = -8.1
#   Bottom:
#     diode_rotate = 180
#     diode_x_offset = 3 * 2.54
#     diode_y_offset = 8.1

diode_template = "diode_MiniMELF"
# diode_template = "diode_SOD-123"  # 'diode_MiniMELF' 'diode_SOD-123' or 'diode_DO-35'

diode_rotate = 90
diode_x_offset = -2 * 2.54
diode_y_offset = 2 * 2.54

diode_label_rotate = 90
diode_label_x_offset = 0
diode_label_y_offset = -1.8

# Schematic
#   Switches
sw_spacing = 1000
sw_x_origin = 100
sw_y_origin = 100
#   LEDs
led_spacing = 1000
led_x_origin = 100
led_y_origin = 6000


#
# End of config variables
#

pcb_header = """(kicad_pcb (version 4) (host pcbnew 4.0.2-stable)

  (general
    (links 539)
    (no_connects 522)
    (area 0 0 0 0)
    (thickness 1.6)
    (drawings 0)
    (tracks 47)
    (zones 0)
    (modules 202)
    (nets 134)
  )

  (page A2)
  (layers
    (0 F.Cu signal)
    (31 B.Cu signal)
    (32 B.Adhes user)
    (33 F.Adhes user)
    (34 B.Paste user)
    (35 F.Paste user)
    (36 B.SilkS user)
    (37 F.SilkS user)
    (38 B.Mask user)
    (39 F.Mask user)
    (40 Dwgs.User user)
    (41 Cmts.User user)
    (42 Eco1.User user)
    (43 Eco2.User user)
    (44 Edge.Cuts user)
    (45 Margin user)
    (46 B.CrtYd user)
    (47 F.CrtYd user)
    (48 B.Fab user)
    (49 F.Fab user)
  )

  (setup
    (last_trace_width 0.254)
    (user_trace_width 0.254)
    (user_trace_width 0.3048)
    (user_trace_width 0.381)
    (trace_clearance 0.2032)
    (zone_clearance 0.508)
    (zone_45_only no)
    (trace_min 0.2032)
    (segment_width 0.2)
    (edge_width 0.15)
    (via_size 0.6096)
    (via_drill 0.3048)
    (via_min_size 0.6096)
    (via_min_drill 0.3048)
    (uvia_size 0.4572)
    (uvia_drill 0.3048)
    (uvias_allowed no)
    (uvia_min_size 0.4572)
    (uvia_min_drill 0.3048)
    (pcb_text_width 0.3)
    (pcb_text_size 1.5 1.5)
    (mod_edge_width 0.15)
    (mod_text_size 1 1)
    (mod_text_width 0.15)
    (pad_size 1.524 1.524)
    (pad_drill 0.762)
    (pad_to_mask_clearance 0.04)
    (solder_mask_min_width 0.1)
    (aux_axis_origin 0 0)
    (visible_elements FFFFF77F)
    (pcbplotparams
      (layerselection 0x00030_80000001)
      (usegerberextensions false)
      (excludeedgelayer true)
      (linewidth 0.150000)
      (plotframeref false)
      (viasonmask false)
      (mode 1)
      (useauxorigin false)
      (hpglpennumber 1)
      (hpglpenspeed 20)
      (hpglpendiameter 15)
      (hpglpenoverlay 2)
      (psnegative false)
      (psa4output false)
      (plotreference true)
      (plotvalue true)
      (plotinvisibletext false)
      (padsonsilk false)
      (subtractmaskfromsilk false)
      (outputformat 1)
      (mirror false)
      (drillshape 1)
      (scaleselection 1)
      (outputdirectory ""))
  )

  (net_class Default "This is the default net class."
    (clearance 0.2032)
    (trace_width 0.381)
    (via_dia 0.6096)
    (via_drill 0.3048)
    (uvia_dia 0.4572)
    (uvia_drill 0.3048)
  )

  (net_class 10m ""
    (clearance 0.2032)
    (trace_width 0.254)
    (via_dia 0.6096)
    (via_drill 0.3048)
    (uvia_dia 0.4572)
    (uvia_drill 0.3048)
  )

  (net_class 20m ""
    (clearance 0.254)
    (trace_width 0.508)
    (via_dia 0.6096)
    (via_drill 0.3048)
    (uvia_dia 0.4572)
    (uvia_drill 0.3048)
  )"""

pcb_footer = """)
"""

#
# mx                - Standard, includes mounting holes, but no LEDs
# mx_led            - Standard, includes LEDs and mounting holes
# mxalps            - mx merged with alps using slots (w/LEDs + holes)
# mxalps-reversed   - mx merged with alps rotated 180 no LEDs or holes
# mxalps-no-led     - mx merged with alps, but no LEDs or holes
#
footprints = {
    #
    # Standard, includes mounting holes, but no LEDs
    #
    "mx": """(module MX locked (layer F.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr MX)
    (tags MX)
    (fp_text reference {reference} (at 0 3) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.2)) (justify mirror))
    )
    (fp_text value {reference} (at 0 8.2) (layer F.SilkS) hide
      (effects (font (thickness 0.3048)))
    )
    (fp_line (start -6.35 -6.35) (end 6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 -6.35) (end 6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 6.35) (end -6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -6.35 6.35) (end -6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -9.398 -9.398) (end 9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 -9.398) (end 9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 9.398) (end -9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -9.398 9.398) (end -9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -6.35 -6.35) (end -4.572 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 4.572 -6.35) (end 6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 -6.35) (end 6.35 -4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 4.572) (end 6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 6.35) (end 4.572 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -4.572 6.35) (end -6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 6.35) (end -6.35 4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 -4.572) (end -6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.985 -6.985) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 -6.985) (end 6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 6.985) (end -6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (pad SW2 thru_hole circle (at 2.54 -5.08) (size 2.5 2.5) (drill 1.4986) (layers *.Cu *.SilkS *.Mask))
    (pad SW1 thru_hole circle (at -3.81 -2.54) (size 2.5 2.5) (drill 1.4986) (layers *.Cu *.SilkS *.Mask))
    (pad "" np_thru_hole circle (at 0 0) (size 3.9878 3.9878) (drill 3.9878) (layers *.Cu))
  )""",
    "mx_pcb": """(module MX_PCB locked (layer F.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr MX_PCB)
    (tags MX_PCB)
    (fp_text reference {reference} (at 0 3) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.2)) (justify mirror))
    )
    (fp_text value {reference} (at 0 8.2) (layer F.SilkS) hide
      (effects (font (thickness 0.3048)))
    )
    (fp_line (start -6.35 -6.35) (end 6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 -6.35) (end 6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 6.35) (end -6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -6.35 6.35) (end -6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -9.398 -9.398) (end 9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 -9.398) (end 9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 9.398) (end -9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -9.398 9.398) (end -9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -6.35 -6.35) (end -4.572 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 4.572 -6.35) (end 6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 -6.35) (end 6.35 -4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 4.572) (end 6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 6.35) (end 4.572 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -4.572 6.35) (end -6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 6.35) (end -6.35 4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 -4.572) (end -6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.985 -6.985) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 -6.985) (end 6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 6.985) (end -6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (pad SW2 thru_hole circle (at 2.54 -5.08) (size 2.5 2.5) (drill 1.4986) (layers *.Cu *.SilkS *.Mask))
    (pad SW1 thru_hole circle (at -3.81 -2.54) (size 2.5 2.5) (drill 1.4986) (layers *.Cu *.SilkS *.Mask))
    (pad "" np_thru_hole circle (at 0 0) (size 3.9878 3.9878) (drill 3.9878) (layers *.Cu))
    (pad HOLE np_thru_hole circle (at -5.08 0) (size 1.7018 1.7018) (drill 1.7018) (layers *.Cu))
    (pad "" np_thru_hole circle (at 5.08 0) (size 1.7018 1.7018) (drill 1.7018) (layers *.Cu))
  )""",
    #
    # Standard, includes LEDs and mounting holes
    #
    "mx_led": """(module MX_LED locked (layer F.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr MX_LED)
    (tags MX_LED)
    (fp_text reference {reference} (at 0 3) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.2)) (justify mirror))
    )
    (fp_text value {reference} (at 0 8.2) (layer F.SilkS) hide
      (effects (font (thickness 0.3048)))
    )
    (fp_line (start -0.762 6.731) (end -0.762 6.35) (layer F.SilkS) (width 0.15))
    (fp_line (start -0.762 6.35) (end -0.762 6.223) (layer F.SilkS) (width 0.15))
    (fp_line (start -0.762 3.429) (end -0.762 3.937) (layer F.SilkS) (width 0.15))
    (fp_arc (start 0.127 5.334) (end 1.524 6.223) (angle 90) (layer F.SilkS) (width 0.15))
    (fp_arc (start 0.127 4.826) (end -0.762 3.429) (angle 90) (layer F.SilkS) (width 0.15))
    (fp_arc (start 0.127 5.461) (end 0.889 6.223) (angle 90) (layer F.SilkS) (width 0.15))
    (fp_arc (start 0.127 4.699) (end -0.635 3.937) (angle 90) (layer F.SilkS) (width 0.15))
    (fp_text user A (at 2.794 5.08) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
    )
    (fp_text user K (at -2.794 5.08) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
    )
    (fp_text user A (at 2.794 5.08) (layer F.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_text user K (at -2.794 5.08) (layer F.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_line (start -6.35 -6.35) (end 6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 -6.35) (end 6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 6.35) (end -6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -6.35 6.35) (end -6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -9.398 -9.398) (end 9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 -9.398) (end 9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 9.398) (end -9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -9.398 9.398) (end -9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -6.35 -6.35) (end -4.572 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 4.572 -6.35) (end 6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 -6.35) (end 6.35 -4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 4.572) (end 6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 6.35) (end 4.572 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -4.572 6.35) (end -6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 6.35) (end -6.35 4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 -4.572) (end -6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.985 -6.985) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 -6.985) (end 6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 6.985) (end -6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (pad A thru_hole circle (at 1.27 5.08) (size 2 2) (drill 1) (layers *.Cu *.SilkS *.Mask))
    (pad K thru_hole rect (at -1.27 5.08) (size 2 2) (drill 1) (layers *.Cu *.SilkS *.Mask))
    (pad SW2 thru_hole circle (at 2.54 -5.08) (size 2.5 2.5) (drill 1.4986) (layers *.Cu *.SilkS *.Mask))
    (pad SW1 thru_hole circle (at -3.81 -2.54) (size 2.5 2.5) (drill 1.4986) (layers *.Cu *.SilkS *.Mask))
    (pad "" np_thru_hole circle (at 0 0) (size 3.9878 3.9878) (drill 3.9878) (layers *.Cu))
    (pad HOLE np_thru_hole circle (at -5.08 0) (size 1.7018 1.7018) (drill 1.7018) (layers *.Cu))
    (pad "" np_thru_hole circle (at 5.08 0) (size 1.7018 1.7018) (drill 1.7018) (layers *.Cu))
  )""",
    #
    # mx merged with alps using slots (w/LEDs, but no holes)
    #
    "mxalps-no_pcb": """(module MXALPS locked (layer F.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr MXALPS)
    (tags MXALPS)
    (fp_text reference {reference} (at 0 7) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.2)) (justify mirror))
    )
    (fp_text value {reference} (at 0 8.2) (layer F.SilkS) hide
      (effects (font (thickness 0.3048)))
    )
    (fp_text user A (at 2.794 5.08) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
    )
    (fp_text user K (at -2.794 5.08) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
    )
    (fp_text user A (at 2.794 5.08) (layer F.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_text user K (at -2.794 5.08) (layer F.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_line (start -6.35 -6.35) (end 6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 -6.35) (end 6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 6.35) (end -6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -6.35 6.35) (end -6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -9.398 -9.398) (end 9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 -9.398) (end 9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 9.398) (end -9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -9.398 9.398) (end -9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -6.35 -6.35) (end -4.572 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 4.572 -6.35) (end 6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 -6.35) (end 6.35 -4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 4.572) (end 6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 6.35) (end 4.572 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -4.572 6.35) (end -6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 6.35) (end -6.35 4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 -4.572) (end -6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.985 -6.985) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end 6.985 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.4) (end 7.75 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 -6.4) (end -6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 -6.4) (end -6.985 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 6.4) (end -7.75 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 7.75 6.4) (end 7.75 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 6.4) (end -6.985 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 6.4) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 7.75 -6.4) (end 6.985 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 -6.4) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (pad "" np_thru_hole circle (at 0 0) (size 3.98781 3.98781) (drill 3.9878) (layers *.Cu *.Mask F.SilkS)
      (clearance 0.1524))
    (pad SW1 thru_hole oval (at -3.405 -3.27 330.95) (size 2.5 4.17) (drill oval 1.5 3.17) (layers *.Cu *.Mask F.SilkS))
    (pad SW2 thru_hole oval (at 2.52 -4.79 356.1) (size 2.5 3.08) (drill oval 1.5 2.08) (layers *.Cu *.Mask F.SilkS))
    (pad K thru_hole rect (at -1.27 5.08) (size 2 2) (drill 1) (layers *.Cu *.SilkS *.Mask))
    (pad A thru_hole circle (at 1.27 5.08) (size 2 2) (drill 1) (layers *.Cu *.SilkS *.Mask))
  )""",
    #
    # mx merged with alps using slots (w/LEDs + holes)
    #
    "mxalps": """(module MXALPS locked (layer F.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr MXALPS)
    (tags MXALPS)
    (fp_text reference {reference} (at 0 7) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.2)) (justify mirror))
    )
    (fp_text value {reference} (at 0 8.2) (layer F.SilkS) hide
      (effects (font (thickness 0.3048)))
    )
    (fp_text user A (at 2.794 5.08) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
    )
    (fp_text user K (at -2.794 5.08) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
    )
    (fp_text user A (at 2.794 5.08) (layer F.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_text user K (at -2.794 5.08) (layer F.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_line (start -6.35 -6.35) (end 6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 -6.35) (end 6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 6.35) (end -6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -6.35 6.35) (end -6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -9.398 -9.398) (end 9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 -9.398) (end 9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 9.398) (end -9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -9.398 9.398) (end -9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -6.35 -6.35) (end -4.572 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 4.572 -6.35) (end 6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 -6.35) (end 6.35 -4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 4.572) (end 6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 6.35) (end 4.572 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -4.572 6.35) (end -6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 6.35) (end -6.35 4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 -4.572) (end -6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.985 -6.985) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end 6.985 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.4) (end 7.75 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 -6.4) (end -6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 -6.4) (end -6.985 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 6.4) (end -7.75 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 7.75 6.4) (end 7.75 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 6.4) (end -6.985 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 6.4) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 7.75 -6.4) (end 6.985 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 -6.4) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (pad "" np_thru_hole circle (at 0 0) (size 3.98781 3.98781) (drill 3.9878) (layers *.Cu *.Mask F.SilkS)
      (clearance 0.1524))
    (pad "" np_thru_hole circle (at -5.08 0) (size 1.70181 1.70181) (drill 1.7018) (layers *.Cu *.Mask F.SilkS)
      (clearance 0.1524))
    (pad "" np_thru_hole circle (at 5.08 0) (size 1.70181 1.70181) (drill 1.7018) (layers *.Cu *.Mask F.SilkS)
      (clearance 0.1524))
    (pad SW1 thru_hole oval (at -3.405 -3.27 330.95) (size 2.5 4.17) (drill oval 1.5 3.17) (layers *.Cu *.Mask F.SilkS))
    (pad SW2 thru_hole oval (at 2.52 -4.79 356.1) (size 2.5 3.08) (drill oval 1.5 2.08) (layers *.Cu *.Mask F.SilkS))
    (pad K thru_hole rect (at -1.27 5.08) (size 2 2) (drill 1) (layers *.Cu *.SilkS *.Mask))
    (pad A thru_hole circle (at 1.27 5.08) (size 2 2) (drill 1) (layers *.Cu *.SilkS *.Mask))
  )""",
    #
    # mx merged with alps rotated 180 no LEDs or holes
    #
    "mxalps-reversed": """(module MXALPS-REVERSED locked (layer F.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr MXALPS-REVERSED)
    (tags MXALPS-REVERSED)
    (fp_text reference {reference} (at 0 6.731) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.2)) (justify mirror))
    )
    (fp_text value {reference} (at 0 8.2) (layer F.SilkS) hide
      (effects (font (thickness 0.3048)))
    )
    (fp_line (start -6.35 -6.35) (end 6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 -6.35) (end 6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 6.35) (end -6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -6.35 6.35) (end -6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -9.398 -9.398) (end 9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 -9.398) (end 9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 9.398) (end -9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -9.398 9.398) (end -9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -6.35 -6.35) (end -4.572 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 4.572 -6.35) (end 6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 -6.35) (end 6.35 -4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 4.572) (end 6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 6.35) (end 4.572 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -4.572 6.35) (end -6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 6.35) (end -6.35 4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 -4.572) (end -6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.985 -6.985) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end 6.985 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.4) (end 7.75 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 -6.4) (end -6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 -6.4) (end -6.985 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 6.4) (end -7.75 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 7.75 6.4) (end 7.75 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 6.4) (end -6.985 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 6.4) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 7.75 -6.4) (end 6.985 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 -6.4) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (pad "" np_thru_hole circle (at 0 0) (size 3.98781 3.98781) (drill 3.9878) (layers *.Cu *.Mask F.SilkS)
      (clearance 0.1524))
    (pad SW1 thru_hole circle (at -3.81 -2.54) (size 2.5 2.5) (drill 1.5) (layers *.Cu *.SilkS *.Mask))
    (pad SW2 thru_hole circle (at 2.54 -5.08) (size 2.5 2.5) (drill 1.5) (layers *.Cu *.SilkS *.Mask))
    (pad SW1 thru_hole circle (at -2.5 4.5) (size 2.5 2.5) (drill 1.5) (layers *.Cu *.SilkS *.Mask))
    (pad SW2 thru_hole circle (at 2.5 4) (size 2.5 2.5) (drill 1.5) (layers *.Cu *.SilkS *.Mask))
  )""",
    #
    # mx merged with alps, but no LEDs or holes
    #
    "mxalps-no-led": """(module MXALPS-NOLED locked (layer F.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr MXALPS-NOLED)
    (tags MXALPS-NOLED)
    (fp_text reference {reference} (at 0 3.5) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.2)) (justify mirror))
    )
    (fp_text value {reference} (at 0 8.2) (layer F.SilkS) hide
      (effects (font (thickness 0.3048)))
    )
    (fp_line (start -6.35 -6.35) (end 6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 -6.35) (end 6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start 6.35 6.35) (end -6.35 6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -6.35 6.35) (end -6.35 -6.35) (layer Cmts.User) (width 0.1524))
    (fp_line (start -9.398 -9.398) (end 9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 -9.398) (end 9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start 9.398 9.398) (end -9.398 9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -9.398 9.398) (end -9.398 -9.398) (layer Dwgs.User) (width 0.1524))
    (fp_line (start -6.35 -6.35) (end -4.572 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 4.572 -6.35) (end 6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 -6.35) (end 6.35 -4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 4.572) (end 6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start 6.35 6.35) (end 4.572 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -4.572 6.35) (end -6.35 6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 6.35) (end -6.35 4.572) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.35 -4.572) (end -6.35 -6.35) (layer F.SilkS) (width 0.381))
    (fp_line (start -6.985 -6.985) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.985) (end 6.985 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 6.4) (end 7.75 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 -6.4) (end -6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 -6.4) (end -6.985 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 6.4) (end -7.75 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 7.75 6.4) (end 7.75 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -7.75 6.4) (end -6.985 6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start -6.985 6.4) (end -6.985 6.985) (layer Eco2.User) (width 0.1524))
    (fp_line (start 7.75 -6.4) (end 6.985 -6.4) (layer Eco2.User) (width 0.1524))
    (fp_line (start 6.985 -6.4) (end 6.985 -6.985) (layer Eco2.User) (width 0.1524))
    (pad "" np_thru_hole circle (at 0 0) (size 3.98781 3.98781) (drill 3.9878) (layers *.Cu *.Mask F.SilkS)
      (clearance 0.1524))
    (pad SW1 thru_hole oval (at -3.405 -3.27 330.95) (size 2.5 4.17) (drill oval 1.5 3.17) (layers *.Cu *.Mask F.SilkS))
    (pad SW2 thru_hole oval (at 2.52 -4.79 356.1) (size 2.5 3.08) (drill oval 1.5 2.08) (layers *.Cu *.Mask F.SilkS))
  )""",
    "diode_SOD-123": """(module Diodes_SMD:SOD-123 (layer B.Cu) (tedit 5530FCB9) (tstamp 57436F4A)
    (at {x_pos} {y_pos} {rotate})
    (descr SOD-123)
    (tags SOD-123)
    (attr smd)
    (fp_text reference {reference} (at {label_x_pos} {label_y_pos} {label_rotate}) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
    )
    (fp_text value {reference} (at {label_x_pos} {label_y_pos} {label_rotate}) (layer B.Fab) hide
      (effects (font (size 1 1) (thickness 0.15)) (justify mirror))
    )
    (fp_line (start 0.3175 0) (end 0.6985 0) (layer B.SilkS) (width 0.15))
    (fp_line (start -0.6985 0) (end -0.3175 0) (layer B.SilkS) (width 0.15))
    (fp_line (start -0.3175 0) (end 0.3175 0.381) (layer B.SilkS) (width 0.15))
    (fp_line (start 0.3175 0.381) (end 0.3175 -0.381) (layer B.SilkS) (width 0.15))
    (fp_line (start 0.3175 -0.381) (end -0.3175 0) (layer B.SilkS) (width 0.15))
    (fp_line (start -0.3175 0.508) (end -0.3175 -0.508) (layer B.SilkS) (width 0.15))
    (fp_line (start -2.25 1.05) (end 2.25 1.05) (layer B.CrtYd) (width 0.05))
    (fp_line (start 2.25 1.05) (end 2.25 -1.05) (layer B.CrtYd) (width 0.05))
    (fp_line (start 2.25 -1.05) (end -2.25 -1.05) (layer B.CrtYd) (width 0.05))
    (fp_line (start -2.25 1.05) (end -2.25 -1.05) (layer B.CrtYd) (width 0.05))
    (fp_line (start -2 -0.9) (end 1.54 -0.9) (layer B.SilkS) (width 0.15))
    (fp_line (start -2 0.9) (end 1.54 0.9) (layer B.SilkS) (width 0.15))
    (pad 1 smd rect (at -1.635 0 270) (size 0.91 1.22) (layers B.Cu B.Paste B.Mask))
    (pad 2 smd rect (at 1.635 0 270) (size 0.91 1.22) (layers B.Cu B.Paste B.Mask))
  )

    """,
    "diode_DO-35": """(module Diode_DO-35_SOD27_Horizontal_RM10 locked (layer F.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr "Diode, DO-35,  SOD27, Horizontal, RM 10mm")
    (tags "Diode, DO-35, SOD27, Horizontal, RM 10mm, 1N4148,")
    (fp_text reference {reference} (at {label_x_pos} {label_y_pos} {label_rotate}) (layer F.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_text value {reference} (at {label_x_pos} {label_y_pos} {label_rotate}) (layer F.Fab) hide
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_line (start 7.36652 -0.00254) (end 8.76352 -0.00254) (layer F.SilkS) (width 0.15))
    (fp_line (start 2.92152 -0.00254) (end 1.39752 -0.00254) (layer F.SilkS) (width 0.15))
    (fp_line (start 3.30252 -0.76454) (end 3.30252 0.75946) (layer F.SilkS) (width 0.15))
    (fp_line (start 3.04852 -0.76454) (end 3.04852 0.75946) (layer F.SilkS) (width 0.15))
    (fp_line (start 2.79452 -0.00254) (end 2.79452 0.75946) (layer F.SilkS) (width 0.15))
    (fp_line (start 2.79452 0.75946) (end 7.36652 0.75946) (layer F.SilkS) (width 0.15))
    (fp_line (start 7.36652 0.75946) (end 7.36652 -0.76454) (layer F.SilkS) (width 0.15))
    (fp_line (start 7.36652 -0.76454) (end 2.79452 -0.76454) (layer F.SilkS) (width 0.15))
    (fp_line (start 2.79452 -0.76454) (end 2.79452 -0.00254) (layer F.SilkS) (width 0.15))
    (pad 2 thru_hole circle (at 10.16052 -0.00254 180) (size 1.69926 1.69926) (drill 0.70104) (layers *.Cu *.Mask F.SilkS))
    (pad 1 thru_hole rect (at 0.00052 -0.00254 180) (size 1.69926 1.69926) (drill 0.70104) (layers *.Cu *.Mask F.SilkS))
    (model Diodes_ThroughHole.3dshapes/Diode_DO-35_SOD27_Horizontal_RM10.wrl
      (at (xyz 0.2 0 0))
      (scale (xyz 0.4 0.4 0.4))
      (rotate (xyz 0 0 180))
    )
  )""",
    "diode_MiniMELF": """(module Diodes_SMD:MiniMELF_Standard (layer B.Cu) (tedit {tedit}) (tstamp {tstamp})
    (at {x_pos} {y_pos} {rotate})
    (descr "Diode Mini-MELF Standard")
    (tags "Diode Mini-MELF Standard")
    (attr smd)
    (fp_text reference {reference} (at {label_x_pos} {label_y_pos} {label_rotate}) (layer B.SilkS)
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_text value {reference} (at {label_x_pos} {label_y_pos} {label_rotate}) (layer B.Fab) hide
      (effects (font (size 1 1) (thickness 0.15)))
    )
    (fp_line (start -2.55 1) (end 2.55 1) (layer B.CrtYd) (width 0.05))
    (fp_line (start 2.55 1) (end 2.55 -1) (layer B.CrtYd) (width 0.05))
    (fp_line (start 2.55 -1) (end -2.55 -1) (layer B.CrtYd) (width 0.05))
    (fp_line (start -2.55 -1) (end -2.55 1) (layer B.CrtYd) (width 0.05))
    (fp_line (start -0.40024 -0.0508) (end 0.60052 0.85) (layer B.SilkS) (width 0.15))
    (fp_line (start 0.60052 0.85) (end 0.60052 -0.85) (layer B.SilkS) (width 0.15))
    (fp_line (start 0.60052 -0.85) (end -0.40024 0) (layer B.SilkS) (width 0.15))
    (fp_line (start -0.40024 0.85) (end -0.40024 -0.85) (layer B.SilkS) (width 0.15))
    (pad 1 smd rect (at -1.75006 0 90) (size 1.30048 1.69926) (layers B.Cu B.Paste B.Mask))
    (pad 2 smd rect (at 1.75006 0 90) (size 1.30048 1.69926) (layers B.Cu B.Paste B.Mask))
    (model Diodes_SMD.3dshapes/MiniMELF_Standard.wrl
      (at (xyz 0 0 0))
      (scale (xyz 0.3937 0.3937 0.3937))
      (rotate (xyz 0 0 0))
    )
  )
  """,
}

schem_template_header = """EESchema Schematic File Version 2
LIBS:cherrymx
EELAYER 25 0
EELAYER END
$Descr A2 11693 8268
encoding utf-8
Sheet 1 1
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr"""

schem_template_footer = "$EndSCHEMATC"

project_template = """update=Friday, March 25, 2016 'PMt' 09:12:47 PM
version=1
last_client=kicad
[pcbnew]
version=1
LastNetListRead=
UseCmpFile=1
PadDrill=0.600000000000
PadDrillOvalY=0.600000000000
PadSizeH=1.500000000000
PadSizeV=1.500000000000
PcbTextSizeV=1.500000000000
PcbTextSizeH=1.500000000000
PcbTextThickness=0.300000000000
ModuleTextSizeV=1.000000000000
ModuleTextSizeH=1.000000000000
ModuleTextSizeThickness=0.150000000000
SolderMaskClearance=0.040000000000
SolderMaskMinWidth=0.100000000000
DrawSegmentWidth=0.200000000000
BoardOutlineThickness=0.100000000000
ModuleOutlineThickness=0.150000000000
[cvpcb]
version=1
NetIExt=net
[general]
version=1
[eeschema]
version=1
LibDir=
[eeschema/libraries]
LibName1=../kicad-libs/device
LibName2=../kicad-libs/cherrymx
LibName3=device
"""

component_templates = {
    "switch": """$Comp
L MX_LED %(ref)s
U %(pkg)d 1 %(timestamp)x
P %(x)d %(y)d
F 0 "%(ref)s" H %(x)d %(ref_y)d 60  0000 C CNN
F 1 "MX_LED" H %(x)d %(y)d 60  0001 C CNN
F 2 "" H %(x)d %(y)d 60  0000 C CNN
F 3 "" H %(x)d %(y)d 60  0000 C CNN
    %(pkg)d    %(x)d %(y)d
    1    0    0    -1
$EndComp""",
    "led": """$Comp
L MX_LED %(ref)s
U %(pkg)d 1 %(timestamp)x
P %(x)d %(y)d
F 0 "%(ref)s" H %(x)d %(ref_y)d 60  0000 C CNN
F 1 "MX_LED" H %(x)d %(y)d 60  0001 C CNN
F 2 "" H %(x)d %(y)d 60  0000 C CNN
F 3 "" H %(x)d %(y)d 60  0000 C CNN
    %(pkg)d    %(x)d %(y)d
    0    1    1    0
$EndComp""",
    "diode": """$Comp
L D D%(ref)s
U %(pkg)d 1 %(timestamp)x
P %(x)d %(y)d
F 0 "%(ref)s" H %(ref_x)d %(ref_y)d 60  0000 C CNN
F 1 "D" H %(x)d %(y)d 60  0001 C CNN
F 2 "" H %(x)d %(y)d 60  0000 C CNN
F 3 "" H %(x)d %(y)d 60  0000 C CNN
    %(pkg)d    %(x)d %(y)d
    0    -1   -1   0
$EndComp"""
}


def add_to_schematic(schem, x, y, timestamp=None, reference=None):
    if reference is None:
        reference = "%d_%d" % (x, y)
    schem.write(component_templates["switch"] % {
        "x": int((x * sw_spacing + sw_x_origin) / 100) * 100,
        "y": int((y * sw_spacing + sw_y_origin) / 100) * 100,
        "ref_y": y * sw_spacing + sw_y_origin - 100,
        "pkg": 1,
        "ref": str(reference),
        "timestamp": time() if timestamp is None else timestamp
    })
    schem.write(component_templates["led"] % {
        "x": int((x * led_spacing + led_x_origin) / 100) * 100,
        "y": int((y * led_spacing + led_y_origin) / 100) * 100,
        "ref_y": y * led_spacing + led_y_origin - 150,
        "pkg": 2,
        "ref": str(reference),
        "timestamp": time() if timestamp is None else timestamp + 1
    })
    schem.write(component_templates["diode"] % {
        "x": int((x * sw_spacing + sw_x_origin) / 100) * 100 + 400,
        "y": int((y * sw_spacing + sw_y_origin) / 100) * 100 + 150,
        "ref_x": int((x * sw_spacing + sw_x_origin) / 100) * 100 + 400,
        "ref_y": int((y * sw_spacing + sw_y_origin) / 100) * 100 + 250,
        "pkg": 1,
        "ref": str(reference.replace("SW_", "D")),
        "timestamp": time() if timestamp is None else timestamp
    })


def place_text_footprint(pcb_text, x, y, reference=None, i=None, timestamp=None):
    if reference is None:
        reference = "SW%d_%d" % (x, y)
    pcb_text.write(footprints[footprint_name].format(
        reference=str(reference),
        x_pos=x * pcb_spacing,
        y_pos=y * pcb_spacing,
        rotate=switch_rotate,
        tstamp=str(time() if timestamp is None else timestamp),
        tedit=str(time() if timestamp is None else timestamp)
    ))
    if i is not None:
        reference = "D%d" % (i)
    if reference is None:
        reference = "D%d_%d" % (x, y)
    pcb_text.write(footprints[diode_template].format(
        reference=str(reference),
        x_pos=x * pcb_spacing + diode_x_offset,
        y_pos=y * pcb_spacing + diode_y_offset,
        rotate=diode_rotate,
        label_x_pos=diode_label_x_offset,
        label_y_pos=diode_label_y_offset,
        label_rotate=diode_label_rotate,
        tstamp=str(time() if timestamp is None else timestamp),
        tedit=str(time() if timestamp is None else timestamp)
    ))


def main():
    if not os.path.exists(output_directory):
        os.mkdir(output_directory)
    if os.path.exists(project_file_name):
        print("Project exists, destroy it (y/n)?")
        if input().lower() == "y":
            with open(project_file_name, mode="w") as project_file:
                project_file.write(project_template)
    else:
        with open(project_file_name, mode="w") as project_file:
            project_file.write(project_template)
    sch_name = schematic_file_name
    if os.path.exists(sch_name):
        print("Schematic exists, destroy it (y/n)?")
        if input().lower() == "n":
            sch_name = os.devnull
    switch_sch = codecs.open(sch_name, mode="w", encoding='utf-8')
    pcb_name = pcb_file_name
    if os.path.exists(pcb_name):
        print("PCB exists, destroy it (y/n)?")
        if input().lower() == "n":
            pcb_name = os.devnull
    pcb_txt = codecs.open(pcb_name, mode="w", encoding='utf-8')
    with open(layout_file_name) as layout_file:
        layout = json.load(layout_file)
    switch_sch.write(schem_template_header)
    pcb_txt.write(pcb_header)
    x, y = x_origin, y_origin
    i = 1
    timestamp = int(time())
    for row in layout:
        if not isinstance(row, list):
            continue
        x = x_origin
        y_offset = 0.0
        width = 1.0
        for col in row:
            if isinstance(col, dict):
                y_offset = (float(col.get("h", 1)) - 1) / 2
                width = float(col.get("w", 1))
                x += float(col.get("x", 0))
                y += float(col.get("y", 0))
            elif isinstance(col, six.string_types):
                ref = "SW_X%dY%d" % (x, y)
                if col.split() and col.split()[0].isalnum():
                    ref = "SW_" + col.split()[0]
                ref += "_%d" % i
                ref = "SW_%d" % i  # just want them numbered by order
                x_offset = (width - 1.0) / 2
                place_text_footprint(pcb_txt, x + x_offset, y + y_offset, ref, i, timestamp + i)
                add_to_schematic(switch_sch, x + x_offset, y + y_offset, timestamp + i, ref)
                x += width
                width = 1.0
                i += 1
        y += 1
    switch_sch.write(schem_template_footer)
    switch_sch.close()
    pcb_txt.write(pcb_footer)
    pcb_txt.close()


if __name__ == "__main__":
    main()
