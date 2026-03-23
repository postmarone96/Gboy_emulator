def inc_rr(registers, writer):
    for code, name in registers.items():
        opcode_hex = f"0x{int(f'0b00{code}0011', 2):X}"
        writer.writerow([opcode_hex, 1, f"INC {name} M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"INC {name} M2", "NONE", "NONE", "NONE", "NONE", f"{name}_INC", 0, 0, 1])

def dec_rr(registers, writer):
    for code, name in registers.items():
        opcode_hex = f"0x{int(f'0b00{code}1011', 2):X}"
        writer.writerow([opcode_hex, 1, f"DEC {name} M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"DEC {name} M2", "NONE", "NONE", "NONE", "NONE", f"{name}_DEC", 0, 0, 1])

def add_hl_rr(registers, writer):
    for code, name in registers.items():
        opcode_hex = f"0x{int(f'0b00{code}1001', 2):X}"
        writer.writerow([opcode_hex, 1, f"ADD HL,{name} M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"ADD HL,{name} M2", "NONE", "NONE", f"REG_{name[0]}", "ADD16_HL", "NONE", 0, 0, 1])


def add_sp_e(writer):
    opcode_hex = "0xE8"
    writer.writerow([opcode_hex, 1, "ADD SP,e M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "ADD SP,e M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "ADD SP,e M3", "NONE", "NONE", "TEMP_Z", "ADD_SP_E_LOW", "NONE", 0, 0, 0])
    writer.writerow([opcode_hex, 4, "ADD SP,e M4", "NONE", "NONE", "TEMP_Z", "ADD_SP_E_HIGH", "NONE", 0, 0, 1])
