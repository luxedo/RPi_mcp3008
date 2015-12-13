#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
RPi_mcp3008 example file
'''
import mcp3008

if __name__ == '__main__':
    with mcp3008.MCP3008() as chip:
        print(chip.read_all(4.35))
        print(chip.read_all())
    with mcp3008.MCP3008.fixed([CH0]) as chip:
        print(chip())
        print(chip(4.35))
