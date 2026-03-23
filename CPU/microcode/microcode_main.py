import os
from microcode_csv_creator import csv_gen
from microcode_hdl_gen import csv_to_vhdl


def main():
    dest_dir = "../../gboy_emulator_hw/gboy_emulator_hw.srcs/sources_1/new"
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    csv_gen('microcode.csv', 'cb_microcode.csv')
    csv_to_vhdl('microcode.csv', 'cb_microcode.csv',
                os.path.join(dest_dir, 'microcode_pkg.vhd'))

if __name__ == "__main__":
    main()