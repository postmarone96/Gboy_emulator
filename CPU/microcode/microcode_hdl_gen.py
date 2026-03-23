import csv



# Mapping for Registers and Address Selection
reg_map = {"REG_B": 0, "REG_C": 1, "REG_D": 2, "REG_E": 3,
           "REG_H": 4, "REG_L": 5, "REG_A": 7, "REG_F": 8, "REG_MEM": 9,
           "TEMP_Z": 10, "TEMP_W": 11, "REG_P":12, "REG_S":13,
           "REG_PC_H": 14, "REG_PC_L": 15, "NONE": 16}

addr_map = {"PC": 0, "HL": 1, "BC": 2, "DE": 3, "WZ": 4,
            "FF00_C":5, "FF00_Z":6, "SP":7, "NONE": 8}

alu_map = {"NONE": 0, "ADD": 1, "SUB": 2, "ADD_SP_E": 3, "ADC": 4, "SBC": 5, "CP": 6,
           "INC": 7, "DEC": 8, "AND": 9, "OR": 10, "XOR": 11, "CCF": 12, "SCF": 13,
           "DAA": 14, "CPL": 15, "ADD16_HL": 16, "ADD_SP_E_LOW": 17, "ADD_SP_E_HIGH": 18,
           "RLCA": 19, "RRCA": 20, "RLA": 21, "RRA": 22, "RLC": 23, "RRC": 24, "RL": 25,
           "RR": 26, "SLA": 27, "SRA": 28, "SWAP": 29, "SRL": 30, "BIT": 31, "RES": 32, "SET": 33,
           "CHECK_CC": 34, "JR_ADD": 35, }

idu_map = {"NONE": 0, "PC_INC": 1,
           "SP_INC": 2, "SP_DEC": 3,
           "HL_INC": 4, "HL_DEC": 5,
           "DE_INC": 6, "DE_DEC": 7,
           "BC_INC": 8, "BC_DEC": 9,
           "WZ_INC": 10, "HL_TO_SP": 11,
           "WZ_TO_PC": 12, "HL_TO_PC": 13,
           "RETI_DONE": 14, "RST_PC":15,
           "HALT_START": 16, "GET_INT_VECTOR": 17,
           "DI_OP": 18, "EI_OP": 19,
           }

def _load_rom(csv_file):
    try:
        with open(csv_file, "r") as f:
            return {(int(row["Opcode"], 16), int(row["M_Cycle"])): row for row in csv.DictReader(f)}
    except FileNotFoundError:
        print(f"Error: {csv_file} not found.")
        return None

def _write_rom(f, rom_name, rom_data):
    f.write(f"    constant {rom_name} : microcode_table_t := (\n")
    for op in range(257):
        f.write(f"        {op} => ( -- Opcode 0x{op:02X}\n")
        for m in range(1, 7):
            if (op, m) in rom_data:
                r = rom_data[(op, m)]
                addr_sel = r.get("Addr_Sel", "NONE")
                reg_dest = r.get("Reg_Dest", "NONE")
                reg_src = r.get("Reg_Src", "NONE")
                alu_op = r.get("ALU_Op", "NONE")
                idu_op = r.get("IDU_Op", "NONE")

                if addr_sel not in addr_map:
                    raise ValueError(f"Unknown Addr_Sel '{addr_sel}' in {rom_name} opcode 0x{op:02X} M{m}")
                if reg_dest not in reg_map:
                    raise ValueError(f"Unknown Reg_Dest '{reg_dest}' in {rom_name} opcode 0x{op:02X} M{m}")
                if reg_src not in reg_map:
                    raise ValueError(f"Unknown Reg_Src '{reg_src}' in {rom_name} opcode 0x{op:02X} M{m}")
                if alu_op not in alu_map:
                    raise ValueError(f"Unknown ALU_Op '{alu_op}' in {rom_name} opcode 0x{op:02X} M{m}")
                if idu_op not in idu_map:
                    raise ValueError(f"Unknown IDU_Op '{idu_op}' in {rom_name} opcode 0x{op:02X} M{m}")

                addr = addr_map[addr_sel]
                dest = reg_map[reg_dest]
                src = reg_map[reg_src]
                alu = alu_map[alu_op]
                idu = idu_map[idu_op]
                line = f"({addr}, {dest}, {src}, {alu}, {idu}, '{r['Mem_Read']}', '{r['Mem_Write']}', '{r['Is_Done']}')"
                label = f" -- {r['Label']}"
            else:
                line = "(8, 16, 16, 0, 0, '0', '0', '1')"
                label = ""

            terminator = "," if m < 6 else ""
            f.write(f"            {m} => {line}{terminator}{label}\n")

        f.write("        ),\n" if op < 256 else "        )\n")
    f.write("    );\n\n")

def csv_to_vhdl(csv_file, cb_csv_file, vhdl_file):
    rom_data = _load_rom(csv_file)
    cb_rom_data = _load_rom(cb_csv_file)

    if rom_data is None or cb_rom_data is None:
        return

    with open(vhdl_file, "w") as f:
        f.write("library ieee;\nuse ieee.std_logic_1164.all;\nuse ieee.numeric_std.all;\n\n")
        f.write("package microcode_pkg is\n\n")
        f.write("    type microcode_row is record\n")
        f.write("        addr_sel  : integer range 0 to 8;\n")
        f.write("        reg_dest  : integer range 0 to 16;\n")
        f.write("        reg_src   : integer range 0 to 16;\n")
        f.write("        alu_op    : integer range 0 to 35;\n")
        f.write("        idu_op    : integer range 0 to 19;\n")
        f.write("        mem_read  : std_logic;\n")
        f.write("        mem_write : std_logic;\n")
        f.write("        is_done   : std_logic;\n")
        f.write("    end record;\n\n")
        f.write("    type microcode_table_t is array (0 to 256, 1 to 6) of microcode_row;\n\n")

        _write_rom(f, "MICROCODE_ROM", rom_data)
        _write_rom(f, "CB_MICROCODE_ROM", cb_rom_data)

        f.write("end package;")



