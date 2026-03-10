import csv


def csv_to_vhdl(csv_file, vhdl_file):
    # Mapping for Registers and Address Selection
    reg_map = {"REG_B": 0, "REG_C": 1, "REG_D": 2, "REG_E": 3, "REG_H": 4, "REG_L": 5, "REG_A": 7, "MEM_DATA": 8,
               "TEMP_Z": 9, "TEMP_W": 10, "NONE": 15}
    addr_map = {"PC": 0, "HL": 1, "BC": 2, "DE": 3, "WZ": 4, "FF00_C":5, "SP":6}

    try:
        with open(csv_file, 'r') as f:
            reader = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
        return

    with open(vhdl_file, 'w') as f:
        f.write("library ieee;\nuse ieee.std_logic_1164.all;\nuse ieee.numeric_std.all;\n\n")
        f.write("package microcode_pkg is\n\n")

        f.write("    type microcode_row is record\n")
        f.write("        addr_sel  : integer range 0 to 7;\n")
        f.write("        reg_dest  : integer range 0 to 15;\n")
        f.write("        reg_src   : integer range 0 to 15;\n")
        f.write("        mem_read  : std_logic;\n")
        f.write("        mem_write : std_logic;\n")
        f.write("        pc_inc    : std_logic;\n")
        f.write("        is_done   : std_logic;\n")
        f.write("    end record;\n\n")

        f.write("    type microcode_table_t is array (0 to 255, 1 to 4) of microcode_row;\n\n")
        f.write("    constant MICROCODE_ROM : microcode_table_t := (\n")

        rom_data = {(int(row['Opcode'], 16), int(row['M_Cycle'])): row for row in reader}

        for op in range(256):
            f.write(f"        {op} => ( -- Opcode 0x{op:02X}\n")
            for m in range(1, 5):
                if (op, m) in rom_data:
                    r = rom_data[(op, m)]
                    addr = addr_map.get(r.get('Addr_Sel', 'PC'), 0)
                    dest = reg_map.get(r['Reg_Dest'], 15)
                    src = reg_map.get(r['Reg_Src'], 15)

                    # Fix: Comma now correctly placed AFTER the parenthesis
                    line = f"({addr}, {dest}, {src}, '{r['Mem_Read']}', '{r['Mem_Write']}', '{r['PC_Inc']}', '{r['Is_Done']}')"
                    label = f" -- {r['Label']}"
                else:
                    line = "(0, 15, 15, '0', '0', '0', '1')"
                    label = ""

                # Comma logic for array elements
                terminator = "," if m < 4 else ""
                f.write(f"            {m} => {line}{terminator}{label}\n")

            f.write("        ),\n" if op < 255 else "        )\n")

        f.write("    );\n\nend package;")


csv_to_vhdl('microcode.csv',
            '../gboy_emulator_hw/gboy_emulator_hw.srcs/sources_1/new/microcode_pkg.vhd')
