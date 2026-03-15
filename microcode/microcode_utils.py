def generate_nop(writer):
    """
    NOP (0x00): No Operation.
    """
    writer.writerow(["0x00", 1, "NOP M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 1])

def generate_ld_r_r(registers, writer):
    """
    Load to the 8-bit register r, data from the 8-bit register r'.
    """
    # Create the rows for all register combinations
    for d_code, d_name in registers.items():
        for s_code, s_name in registers.items():
            opcode_int = 0x40 | (d_code << 3) | s_code
            opcode_hex = f"0x{opcode_int:02X}"
            writer.writerow([
                opcode_hex, 1, f"LD {d_name}, {s_name} M1", "PC", f"REG_{d_name}", f"REG_{s_name}", "NONE", "PC_INC", 1, 0, 1
            ])

def generate_ld_r_n(registers, writer):
    """
    Load to the 8-bit register r, the immediate data n.
    """
    # Create the rows for all registers
    for code, name in registers.items():
        opcode_int = (code << 3) | 0x06
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([opcode_hex, 1, f"LD {name}, n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"LD {name}, n M2", "PC", f"REG_{name}", "REG_MEM", "NONE",
                         "PC_INC", 1, 0, 1])

def generate_ld_r_hl(registers, writer):
    """
    Load to the 8-bit register r, data from the absolute address specified by the 16-bit register HL.
    """
    # Create the rows for all registers
    for code, name in registers.items():
        opcode_int = 0x40 | (code << 3) | 0x06
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([
            opcode_hex, 1, f"LD {name},HL M1",
            "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0
        ])
        writer.writerow([
            opcode_hex, 2, f"LD {name},HL M2",
            "HL", f"REG_{name}", "REG_MEM", "NONE", "NONE", 1, 0, 1
        ])

def generate_ld_hl_r(registers, writer):
    """
    Load to the absolute address specified by the 16-bit register HL, data from the 8-bit register r.
    """
    # Create the rows for all registers
    for code, name in registers.items():
        opcode_int = 0x70 | code
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([
            opcode_hex, 1, f"LD HL,{name} M1",
            "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0
        ])
        writer.writerow([
            opcode_hex, 2, f"LD HL,{name} M2",
            "HL", "REG_MEM", f"REG_{name}", "NONE", "NONE", 0, 1, 1
        ])

def generate_ld_hl_n(writer):
    """
    Load to the absolute address specified by the 16-bit register HL, the immediate data n.
    """
    opcode_hex = "0x36"
    writer.writerow([opcode_hex, 1, "LD HL, n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD HL, n M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "LD HL, n M3", "HL", "REG_MEM", "TEMP_Z", "NONE", "NONE", 0, 1, 1])

def generate_ld_a_bc(writer):
    """
    Load to the 8-bit A register, data from the absolute address specified by the 16-bit register BC.
    """
    opcode_hex = f"0x0A"
    writer.writerow([opcode_hex, 1, "LD A, BC M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD A, BC M2", "BC", "REG_A", "REG_MEM", "NONE", "NONE", 1, 0, 1])

def generate_ld_a_de(writer):
    """
    Load to the 8-bit A register, data from the absolute address specified by the 16-bit register DE.
    """
    opcode_hex = "0x1A"
    writer.writerow([opcode_hex, 1, "LD A, DE M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD A, DE M2", "DE", "REG_A", "REG_MEM", "NONE", "NONE", 1, 0, 1])

def generate_ld_bc_a(writer):
    """
    Load to the absolute address specified by the 16-bit register BC, data from the 8-bit A register.    
    """
    opcode_hex = "0x02"
    writer.writerow([opcode_hex, 1, "LD BC, A M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD BC, A M2", "BC", "REG_MEM", "REG_A", "NONE", "NONE", 0, 1, 1])

def generate_ld_de_a(writer):
    """
    Load to the absolute address specified by the 16-bit register DE, data from the 8-bit A register.
    """
    opcode_hex = f"0x12"
    writer.writerow([opcode_hex, 1, "LD DE, A M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD DE, A M2", "DE", "REG_MEM", "REG_A", "NONE", "NONE", 0, 1, 1])

def generate_ld_a_nn(writer):
    """
    Load to the 8-bit A register, data from the absolute address specified by the 16-bit operand nn.    
    """
    opcode_hex = f"0xFA"
    writer.writerow([opcode_hex, 1, "LD A, nn M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD A, nn M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "LD A, nn M3", "PC", "TEMP_W", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 4, "LD A, nn M4", "WZ", "REG_A", "REG_MEM", "NONE", "NONE", 1, 0, 1])

def generate_ld_nn_a(writer):
    """
    Load to the absolute address specified by the 16-bit operand nn, data from the 8-bit A register.
    """
    opcode_hex = "0xEA"
    writer.writerow([opcode_hex, 1, "LD nn, A M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD nn, A M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "LD nn, A M3", "PC", "TEMP_W", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 4, "LD nn, A M4", "WZ", "REG_MEM", "REG_A", "NONE", "NONE", 0, 1, 1])

def generate_ldh_a_c(writer):
    """
    Load to the 8-bit A register, data from the address specified by the 8-bit C register. The full
    16-bit absolute address is obtained by setting the most significant byte to 0xFF and the least
    significant byte to the value of C, so the possible range is 0xFF00-0xFFFF.
    """
    opcode_hex = "0xF2"
    writer.writerow([opcode_hex, 1, "LDH A, C M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LDH A, C M3", "FF00_C", "REG_A", "REG_MEM", "NONE", "NONE", 1, 0, 1])

def generate_ldh_c_a(writer):
    """
    Load to the address specified by the 8-bit C register, data from the 8-bit A register. The full
    16-bit absolute address is obtained by setting the most significant byte to 0xFF and the least
    significant byte to the value of C, so the possible range is 0xFF00-0xFFFF.
    """
    opcode_hex = "0xE2"
    writer.writerow([opcode_hex, 1, "LDH C, A M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LDH C, A M2", "FF00_C", "REG_MEM", "REG_A", "NONE", "NONE", 0, 1, 1])

def generate_ldh_a_n(writer):
    """
    Load to the 8-bit A register, data from the address specified by the 8-bit immediate data n. The
    full 16-bit absolute address is obtained by setting the most significant byte to 0xFF and the
    least significant byte to the value of n, so the possible range is 0xFF00-0xFFFF.
    """
    opcode_hex = "0xF0"
    writer.writerow([opcode_hex, 1, "LDH A, n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LDH A, n M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "LDH A, n M3", "FF00_Z", "REG_A", "REG_MEM", "NONE", "NONE", 1, 0, 1])

def generate_ldh_n_a(writer):
    """
    Load to the 8-bit A register, data from the address specified by the 8-bit immediate data n. The
    full 16-bit absolute address is obtained by setting the most significant byte to 0xFF and the
    least significant byte to the value of n, so the possible range is 0xFF00-0xFFFF.
    """
    opcode_hex = "0xE0"
    writer.writerow([opcode_hex, 1, "LD n, A M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "LD n, A M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "LD n, A M3", "FF00_Z", "REG_MEM", "REG_A", "NONE", "NONE", 0, 1, 1])