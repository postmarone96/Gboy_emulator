def rlca(writer):
    opcode_hex = "0x07"
    writer.writerow([opcode_hex, 1, "RLCA M1", "PC", "NONE", "NONE", "RLCA", "PC_INC", 1, 0, 1])

def rrca(writer):
    opcode_hex = "0x0F"
    writer.writerow([opcode_hex, 1, "RRCA M1", "PC", "NONE", "NONE", "RRCA", "PC_INC", 1, 0, 1])

def rla(writer):
    opcode_hex = "0x17"
    writer.writerow([opcode_hex, 1, "RLA M1", "PC", "NONE", "NONE", "RLA", "PC_INC", 1, 0, 1])

def rra(writer):
    opcode_hex = "0x1F"
    writer.writerow([opcode_hex, 1, "RRA M1", "PC", "NONE", "NONE", "RRA", "PC_INC", 1, 0, 1])

def cb_prefix(writer):
    writer.writerow(["0xCB", 1, "PREFIX CB M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 1])

def rlc_r(registers, writer):
    for code, name in registers.items():
        opcode_hex = f"0x{code:02X}"
        writer.writerow([opcode_hex, 1, f"RLC {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"RLC", "PC_INC", 1, 0, 1])

def rlc_hl(writer):
    opcode_hex = "0x06"
    writer.writerow([opcode_hex, 1, "RLC HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "RLC HL M2", "HL", "REG_MEM", "REG_MEM", "RLC", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "RLC HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def rrc_r(registers, writer):
    for code, name in registers.items():
        opcode = 0x08 | code
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"RRC {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"RRC", "PC_INC", 1, 0, 1])

def rrc_hl(writer):
    opcode_hex = "0x0E"
    writer.writerow([opcode_hex, 1, "RRC HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "RRC HL M2", "HL", "REG_MEM", "REG_MEM", "RRC", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "RRC HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def rl_r(registers, writer):
    for code, name in registers.items():
        opcode = 0x10 | code
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"RL {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"RL", "PC_INC", 1, 0, 1])

def rl_hl(writer):
    opcode_hex = "0x16"
    writer.writerow([opcode_hex, 1, "RL HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "RL HL M2", "HL", "REG_MEM", "REG_MEM", "RL", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "RL HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def rr_r(registers, writer):
    for code, name in registers.items():
        opcode = 0x18 | code
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"RR {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"RR", "PC_INC", 1, 0, 1])

def rr_hl(writer):
    opcode_hex = "0x1E"
    writer.writerow([opcode_hex, 1, "RR HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "RR HL M2", "HL", "REG_MEM", "REG_MEM", "RR", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "RR HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def sla_r(registers, writer):
    for code, name in registers.items():
        opcode = 0x20 | code
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"SLA {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"SLA", "PC_INC", 1, 0, 1])

def sla_hl(writer):
    opcode_hex = "0x26"
    writer.writerow([opcode_hex, 1, "SLA HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "SLA HL M2", "HL", "REG_MEM", "REG_MEM", "SLA", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "SLA HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def sra_r(registers, writer):
    for code, name in registers.items():
        opcode = 0x28 | code
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"SRA {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"SRA", "PC_INC", 1, 0, 1])

def sra_hl(writer):
    opcode_hex = "0x2E"
    writer.writerow([opcode_hex, 1, "SRA HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "SRA HL M2", "HL", "REG_MEM", "REG_MEM", "SRA", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "SRA HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def swap_r(registers, writer):
    for code, name in registers.items():
        opcode = 0x30 | code
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"SWAP {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"SWAP", "PC_INC", 1, 0, 1])

def swap_hl(writer):
    opcode_hex = "0x36"
    writer.writerow([opcode_hex, 1, "SWAP HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "SWAP HL M2", "HL", "REG_MEM", "REG_MEM", "SWAP", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "SWAP HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def srl_r(registers, writer):
    for code, name in registers.items():
        opcode = 0x38 | code
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"SRL {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"SRL", "PC_INC", 1, 0, 1])

def srl_hl(writer):
    opcode_hex = "0x3E"
    writer.writerow([opcode_hex, 1, "SRL HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "SRL HL M2", "HL", "REG_MEM", "REG_MEM", "SRL", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "SRL HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def bit_b_r(registers, writer):
    for reg_code, reg_name in registers.items():
        for bit_idx in range(8):
            opcode = 0x40 | (bit_idx << 3) | reg_code
            opcode_hex = f"0x{opcode:02X}"
            writer.writerow([opcode_hex, 1, f"BIT {bit_idx}, {reg_name} M1", "PC", "NONE", f"REG_{reg_name}", "BIT", "PC_INC", 1, 0, 1])

def bit_b_hl(writer):
    for bit_idx in range(8):
        opcode = 0x40 | (bit_idx << 3) | 6
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"BIT {bit_idx}, HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"BIT {bit_idx}, HL M2", "HL", "NONE", "REG_MEM", "BIT", "NONE", 1, 0, 1])


def res_b_r(registers, writer):
    for reg_code, reg_name in registers.items():
        for bit_idx in range(8):
            opcode = 0x80 | (bit_idx << 3) | reg_code
            opcode_hex = f"0x{opcode:02X}"
            writer.writerow([opcode_hex, 1, f"RES {bit_idx}, {reg_name}", "PC", f"REG_{reg_name}", f"REG_{reg_name}", "RES", "PC_INC", 1, 0, 1])


def res_b_hl(writer):
    for bit_idx in range(8):
        opcode = 0x80 | (bit_idx << 3) | 6
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"RES {bit_idx}, HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"RES {bit_idx}, HL M2", "HL", "REG_MEM", "REG_MEM", "RES", "NONE", 1, 0, 0])
        writer.writerow([opcode_hex, 3, f"RES {bit_idx}, HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def set_b_r(registers, writer):
    for reg_code, reg_name in registers.items():
        for bit_idx in range(8):
            opcode = 0xC0 | (bit_idx << 3) | reg_code
            opcode_hex = f"0x{opcode:02X}"
            writer.writerow([opcode_hex, 1, f"SET {bit_idx}, {reg_name}", "PC", f"REG_{reg_name}", f"REG_{reg_name}", "SET", "PC_INC", 1, 0, 1])

def set_b_hl(writer):
    for bit_idx in range(8):
        opcode = 0xC0 | (bit_idx << 3) | 6
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"SET {bit_idx}, HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"SET {bit_idx}, HL M2", "HL", "REG_MEM", "REG_MEM", "SET", "NONE", 1, 0, 0])
        writer.writerow([opcode_hex, 3, f"SET {bit_idx}, HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])





