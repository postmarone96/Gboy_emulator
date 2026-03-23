def generate_ld_rr_nn(writer, registers):
    """
    Load to the 16-bit register rr, the immediate 16-bit data nn.
    """
    # Create the rows for all register combinations
    for d_code, d_name in registers.items():
        opcode_hex = f"0x{int(f'0b00{d_code}0001', 2):X}"
        writer.writerow([opcode_hex, 1, f"LD {d_name}, nn M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"LD {d_name}, nn M2", "PC", f"REG_{d_name[1].upper()}", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 3, f"LD {d_name}, nn M3", "PC", f"REG_{d_name[0].upper()}", "REG_MEM", "NONE", "PC_INC", 1, 0, 1])

def generate_ld_nn_sp(writer):
    """
    Load to the absolute address specified by the 16-bit operand nn, data from the 16-bit SP register.
    """
    opcode_hex = "0x08"
    writer.writerow([opcode_hex, 1, f"LD nn, sp M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, f"LD nn, sp M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, f"LD nn, sp M3", "PC", "TEMP_W", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 4, f"LD nn, sp M4", "WZ", "REG_MEM", "REG_P", "NONE", "WZ_INC", 0, 1, 0])
    writer.writerow([opcode_hex, 5, f"LD nn, sp M5", "WZ", "REG_MEM", "REG_S", "NONE", "NONE", 0, 1, 1])

def generate_ld_sp_hl(writer):
    """
    Load to the 16-bit SP register, data from the 16-bit HL register.
    """
    opcode_hex = "0xF9"
    writer.writerow([opcode_hex, 1, f"LD sp, hl M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, f"LD sp, hl M2", "HL", "NONE", "NONE", "NONE", "HL_TO_SP", 0, 0, 1])

def generate_push_rr(writer, registers):
    """
    Push to the stack memory, data from the 16-bit register rr.
    """
    for d_code, d_name in registers.items():
        opcode_hex = f"0x{int(f'0b11{d_code}0101', 2):X}"
        writer.writerow([opcode_hex, 1, f"PUSH {d_name} M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"PUSH {d_name} M2", "SP", "NONE", "NONE", "NONE", "SP_DEC", 0, 0, 0])
        writer.writerow([opcode_hex, 3, f"PUSH {d_name} M3", "SP", "REG_MEM", f"REG_{d_name[0].upper()}", "NONE", "SP_DEC", 0, 1, 0])
        writer.writerow([opcode_hex, 4, f"PUSH {d_name} M4", "SP", "REG_MEM", f"REG_{d_name[1].upper()}", "NONE", "NONE", 0, 1, 1])

def generate_pop_rr(writer, registers):
    """
    Pops to the 16-bit register rr, data from the stack memory.
    This instruction does not do calculations that affect flags, but POP AF completely replaces the
    F register value, so all flags are changed based on the 8-bit data that is read from memory.
    """
    for d_code, d_name in registers.items():
        opcode_hex = f"0x{int(f'0b11{d_code}0001', 2):X}"
        writer.writerow([opcode_hex, 1, f"POP {d_name} M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"POP {d_name} M2", "SP", f"REG_{d_name[1].upper()}", "REG_MEM", "NONE", "SP_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 3, f"POP {d_name} M3", "SP", f"REG_{d_name[0].upper()}", "REG_MEM", "NONE", "SP_INC", 1, 0, 1])

def generate_ld_sp_plus_e(writer):
    """
    Load to the HL register, 16-bit data calculated by adding the signed 8-bit operand e to the 16-bit value
    of the SP register.
    """
    opcode_hex = "0xF8"
    writer.writerow([opcode_hex, 1, "LD HL, SP+e M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD HL, SP+e M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "LD HL, SP+e M3", "NONE", "NONE", "NONE", "ADD_SP_E", "NONE", 0, 0, 1])
