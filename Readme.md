# Minimal Blender + Molecular Nodes CLI

## Running

Takes a PDB file and an output location and returns a GIF of the protein animated by B-factor.

```sh
pixi run help

# ✨ Pixi task (help): python wobble/api.py --help
# Usage: api.py [OPTIONS] PDB_CODE OUTPUT_PATH
#
#  Create a protein animation from a PDB code and save it to the specified
#  output path.
#
# Options:
#  --frames INTEGER      Number of frames for the animation
#  --resolution INTEGER  Resolution of the output image
#  --samples INTEGER     Number of Cycles samples
#  --help                Show this message and exit.


pixi run example  # this makes the example in this directory ...
pixi run wobble
```

## Result

![](./1FAP_animation.gif)

## Background

This is a distilled version of [mol-nodes utils](https://github.com/zachcp/molnodes-utils). Basically, you need only extract a node gorup of interest
and register it as a class for it to be available for use as a node in a scriptable environment. It opens up the possibility o making
custom, reproducible figures on top of Molecular Nodes
