#!/usr/bin/env python3
#
# Odoo module dependencies viewer
# Copyright (c) 2021 Phi srl
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import io
import sys
import tkinter as tk
import pygraphviz as pgv
from functools import reduce
from PIL import Image, ImageTk

import odoo

# usage:
# . venv/bin/activate
# collect-dep.py --addons-path=...

if __name__ == "__main__":
    args = sys.argv[1:]

    odoo.tools.config._parse_config(args)
    odoo.modules.initialize_sys_path()
    available_modules = set(odoo.modules.get_modules())
    required_modules = dict()
    dep_graph = {}
    for module in list(available_modules)[:]:
        if module.startswith(("test_", "hw_")):
            continue
        required_modules[module] = set(odoo.modules.load_information_from_description_file(module).get("depends"))
        dep_graph[module] = dict((k, None) for k in required_modules[module])
    missing_modules = reduce(set.union, required_modules.values(), set()) - available_modules

    missing_modules |= {"l10n_it_account"}

    #G = pgv.AGraph({"1": {"2": "color=green"},  "3": {"2": None}})
    G = pgv.AGraph(dep_graph, directed=True, rankdir="BT", ranksep=1.2, nodesep=0.3, ratio="fill")
    G.node_attr.update(color="black")

    for missing in missing_modules:
        n = G.get_node(missing)
        n.attr["color"] = "red"
        n.attr["fontcolor"] = "red"
        n.attr["penwidth"] = 2.0
        def mark_predecessors(n):
            for p in G.predecessors_iter(n):
                #p.attr["color"] = "red"
                p.attr["fontcolor"] = "red"
                e = G.get_edge(p, n)
                e.attr["color"] = "red"
                mark_predecessors(p)
        mark_predecessors(n)

    G.layout("dot")
    G.unflatten()
    png = G.draw(format="png")

    window = tk.Tk()
    frame = tk.Frame(window, bd=2)

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    xsb = tk.Scrollbar(frame, orient=tk.HORIZONTAL)
    xsb.grid(row=1, column=0, sticky=tk.E+tk.W)

    ysb = tk.Scrollbar(frame)
    ysb.grid(row=0, column=1, sticky=tk.N+tk.S)

    image = Image.open(io.BytesIO(png))
    img = ImageTk.PhotoImage(image)

    canvas = tk.Canvas(frame, height=img.height(), width=img.width(), bd=0, xscrollcommand=xsb.set, yscrollcommand=ysb.set)
    canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

    canvas.create_image(0,0,image=img, anchor="nw")
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
    xsb.config(command=canvas.xview)
    ysb.config(command=canvas.yview)

    def do_zoom(event):
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        #factor = 1.001 ** event.delta
        if event.num == 4:
            factor = 1.1
        else:
            factor = 0.91
        print("scale=", factor)
        canvas.scale(tk.ALL, x, y, factor, factor)
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
        xsb.config(command=canvas.xview)
        ysb.config(command=canvas.yview)

    canvas.bind("<MouseWheel>", do_zoom)
    canvas.bind("<Button-4>", do_zoom)
    canvas.bind("<Button-5>", do_zoom)
    canvas.bind('<ButtonPress-1>', lambda event: canvas.scan_mark(event.x, event.y))
    canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

    frame.pack()

    window.resizable(True, True)
    window.mainloop()
