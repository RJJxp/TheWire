import io
import os
import sys
import argparse

from subtitle_process import *

def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-path', type=str, help='Enter the input TheWire subtitle file.')
    parser.add_argument('--output-dir', type=str, help='Enter the directory of the output')
    args = parser.parse_args()
    print ("parse args complete")
    return args

if __name__ == "__main__":
    args = getArgs()
    input_path = args.input_path
    output_dir = args.output_dir
    spro = SubtitleProcess()
    spro.input_path = input_path
    spro.output_dir = output_dir
    spro.sub_type = "the_wire"
    spro.getLaTeXCommand()