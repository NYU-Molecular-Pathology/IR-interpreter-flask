#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module for creating reports from Ion Reporter exported .tsv file
"""
import os
from jinja2 import FileSystemLoader, Environment, select_autoescape
import ir
import pmkb
import argparse

template_dir = os.path.join(os.path.dirname(__file__), "templates")
loader = FileSystemLoader(template_dir)
environment = Environment(
    loader = loader,
    autoescape = select_autoescape(['html'])
    )
template = environment.get_template('report.html')

def make_report(input, output = None):
    """
    Makes an HTML report out of an input file.

    Parameters
    ----------
    input: str
        path to input .tsv file
    output: str
        path to output .html to create

    Notes
    -----
    Output file will be overwritten if it already exists.
    """
    if not output:
        output = os.path.splitext(input)[0] + ".html"

    # initialize objects for parsing table and database
    IRtable = ir.IRTable(source = input)
    db = pmkb.PMKB()
    IRtable.lookup_all_interpretations(db = db)

    #  render output
    parsed = template.render(IRtable = IRtable)

    # write output
    with open(output, "w") as f:
        f.write(parsed)

def main(**kwargs):
    """
    Main control function for the script
    """
    input = kwargs.pop('input')[0]
    output = kwargs.pop('output', None)
    make_report(input = input, output = output)

def parse():
    """
    Parses script args
    """
    parser = argparse.ArgumentParser(description='Creates a report from an input .tsv file')
    parser.add_argument('input', nargs=1, help="Ion Reporter .tsv table input file")
    parser.add_argument("-o", "--output", default = None, dest = 'output', help="Output file path")

    args = parser.parse_args()

    main(**vars(args))

if __name__ == '__main__':
    parse()