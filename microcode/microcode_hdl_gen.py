import csv


def csv_to_vhdl(csv_file, vhdl_file):
    # Mapping register names to their 3-bit binary integer values
    reg_map = {
        "REG_B": 0, "REG_C": 1, "REG_D": 2, "REG_E": 3,
        "REG_H": 4, "REG_L": 5, "MEM_HL": 6, "REG_A": 7, "NONE": 15  # 15 is a 'null' flag
    }

    try:
        with open(csv_file, 'r') as f:
            reader = list(csv.DictReader(f))
    except FileNotFoundError:
        print(f"Error: {csv_file} not found. Run your table generator first.")
        return

    with open(vhdl_file, 'w') as f:
        # VHDL Header
        f.write("library ieee;\nuse ieee.std_logic_1164.all;\nuse ieee.numeric_std.all;\n\n")
        f.write("package microcode_pkg is\n\n")

        # The Record matches your CSV logic
        f.write("    type microcode_row is record\n")
        f.write("        reg_dest  : integer range 0 to 15;\n")
        f.write("        reg_src   : integer range 0 to 15;\n")
        f.write("        mem_read  : std_logic;\n")
        f.write("        mem_write : std_logic;\n")
        f.write("        pc_inc    : std_logic;\n")
        f.write("        is_done   : std_logic;\n")
        f.write("    end record;\n\n")

        # 2D Array: (Opcode 0-255, M_Cycle 1-4)
        f.write("    type microcode_table_t is array (0 to 255, 1 to 4) of microcode_row;\n\n")
        f.write("    constant MICROCODE_ROM : microcode_table_t := (\n")

        # Store CSV data in a lookup dictionary
        rom_data = {}
        for row in reader:
            op = int(row['Opcode'], 16)
            m = int(row['M_Cycle'])
            rom_data[(op, m)] = row

        # Build the VHDL Constant
        for op in range(256):
            f.write(f"        {op} => ( -- Opcode 0x{op:02X}\n")
            for m in range(1, 5):
                if (op, m) in rom_data:
                    r = rom_data[(op, m)]
                    dest = reg_map.get(r['Reg_Dest'], 15)
                    src = reg_map.get(r['Reg_Src'], 15)

                    line = (f"({dest}, {src}, '{r['Mem_Read']}', '{r['Mem_Write']}', "
                            f"'{r['PC_Inc']}', '{r['Is_Done']}')")
                    label = f" -- {r['Label']}"
                else:
                    # Default 'Safe' row for unimplemented opcodes
                    line = "(15, 15, '0', '0', '0', '1')"
                    label = ""

                f.write(f"            {m} => {line}{label}")
                f.write(",\n" if m < 4 else "\n")

            f.write("        ),\n" if op < 255 else "        )\n")

        f.write("    );\n\nend package;")


csv_to_vhdl('microcode.csv',
            '../gboy_emulator_hw/gboy_emulator_hw.srcs/sources_1/new/microcode_pkg.vhd')
