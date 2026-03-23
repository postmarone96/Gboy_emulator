def add_r(registers, writer):
    """
    Adds to the 8-bit A register, the 8-bit register r, and stores the result back into the A register.
    """
    for code, name in registers.items():
        opcode_int = 128 + code
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([opcode_hex, 1, f"ADD {name} M1", "PC", "NONE", f"REG_{name}", "ADD", "PC_INC", 1, 0, 1])

def add_hl(writer):
    opcode_hex = "0x86"
    writer.writerow([opcode_hex, 1, "ADD HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "ADD HL M2", "HL", "NONE", "REG_MEM", "ADD", "NONE", 1, 0, 1])

def add_n(writer):
    opcode_hex = "0xC6"
    writer.writerow([opcode_hex, 1, "ADD HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "ADD HL M2", "PC", "NONE", "REG_MEM", "ADD", "PC_INC", 1, 0, 1])

def adc_r(registers, writer):
    for code, name in registers.items():
        opcode_int = 136 + code
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([opcode_hex, 1, f"ADC {name} M1", "PC", "NONE", f"REG_{name}", "ADC", "PC_INC", 1, 0, 1])

def adc_hl(writer):
    opcode_hex = "0x8E"
    writer.writerow([opcode_hex, 1, "ADC HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "ADC HL M2", "HL", "NONE", "REG_MEM", "ADC", "NONE", 1, 0, 1])

def adc_n(writer):
    opcode_hex = "0xCE"
    writer.writerow([opcode_hex, 1, "ADC n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "ADC n M2", "PC", "NONE", "REG_MEM", "ADC", "PC_INC", 1, 0, 1])

def sub_r(registers, writer):
    for code, name in registers.items():
        opcode_int = 144 + code
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([opcode_hex, 1, f"SUB {name} M1", "PC", "NONE", f"REG_{name}", "SUB", "PC_INC", 1, 0, 1])

def sub_hl(writer):
    opcode_hex = "0x96"
    writer.writerow([opcode_hex, 1, "SUB HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "SUB HL M2", "HL", "NONE", "REG_MEM", "SUB", "NONE", 1, 0, 1])

def sub_n(writer):
    opcode_hex = "0xD6"
    writer.writerow([opcode_hex, 1, "SUB n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "SUB n M2", "PC", "NONE", "REG_MEM", "SUB", "PC_INC", 1, 0, 1])

def sbc_r(registers, writer):
    for code, name in registers.items():
        opcode_int = 152 + code
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([opcode_hex, 1, f"SBC {name} M1", "PC", "NONE", f"REG_{name}", "SBC", "PC_INC", 1, 0, 1])

def sbc_hl(writer):
    opcode_hex = "0x9E"
    writer.writerow([opcode_hex, 1, "SBC HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "SBC HL M2", "HL", "NONE", "REG_MEM", "SBC", "NONE", 1, 0, 1])

def sbc_n(writer):
    opcode_hex = "0xDE"
    writer.writerow([opcode_hex, 1, "SBC n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "SBC n M2", "PC", "NONE", "REG_MEM", "SBC", "PC_INC", 1, 0, 1])

def cp_r(registers, writer):
    for code, name in registers.items():
        opcode_int = 184 + code
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([opcode_hex, 1, f"CP {name} M1", "PC", "NONE", f"REG_{name}", "CP", "PC_INC", 1, 0, 1])

def cp_hl(writer):
    opcode_hex = "0xBE"
    writer.writerow([opcode_hex, 1, "CP HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "CP HL M2", "HL", "NONE", "REG_MEM", "CP", "NONE", 1, 0, 1])

def cp_n(writer):
    opcode_hex = "0xFE"
    writer.writerow([opcode_hex, 1, "CP n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "CP n M2", "PC", "NONE", "REG_MEM", "CP", "PC_INC", 1, 0, 1])

def inc_r(registers, writer):
    for code, name in registers.items():
        opcode_int = (code << 3) | 0b100
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([opcode_hex, 1, f"INC {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"INC", "PC_INC", 1, 0, 1])

def inc_hl(writer):
    opcode_hex = "0x34"
    writer.writerow([opcode_hex, 1, "INC HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "INC HL M2", "HL", "REG_MEM", "REG_MEM", "INC", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "INC HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def dec_r(registers, writer):
    for code, name in registers.items():
        opcode_int = 0x00 | (code << 3) | 5
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([opcode_hex, 1, f"DEC {name} M1", "PC", f"REG_{name}", f"REG_{name}", f"DEC", "PC_INC", 1, 0, 1])

def dec_hl(writer):
    opcode_hex = "0x35"
    writer.writerow([opcode_hex, 1, "DEC HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "DEC HL M2", "HL", "REG_MEM", "REG_MEM", "DEC", "NONE", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "DEC HL M3", "HL", "NONE", "NONE", "NONE", "NONE", 0, 1, 1])

def and_r(registers, writer):
    for code, name in registers.items():
        opcode_int = 0xA0 + code
        writer.writerow([f"0x{opcode_int:02X}", 1, f"AND {name} M1", "PC", "NONE", f"REG_{name}", "AND", "PC_INC", 1, 0, 1])

def and_hl(writer):
    opcode_hex = "0xA6"
    writer.writerow([opcode_hex, 1, "AND HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "AND HL M2", "HL", "NONE", "REG_MEM", "AND", "NONE", 1, 0, 1])

def and_n(writer):
    opcode_hex = "0xE6"
    writer.writerow([opcode_hex, 1, "AND n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "AND n M2", "PC", "NONE", "REG_MEM", "AND", "PC_INC", 1, 0, 1])

def or_r(registers, writer):
    for code, name in registers.items():
        opcode_int = 0xB0 + code
        writer.writerow([f"0x{opcode_int:02X}", 1, f"OR {name} M1", "PC", "NONE", f"REG_{name}", "OR", "PC_INC", 1, 0, 1])

def or_hl(writer):
    opcode_hex = "0xB6"
    writer.writerow([opcode_hex, 1, "OR HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "OR HL M2", "HL", "NONE", "REG_MEM", "OR", "NONE", 1, 0, 1])

def or_n(writer):
    opcode_hex = "0xF6"
    writer.writerow([opcode_hex, 1, "OR n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "OR n M2", "PC", "NONE", "REG_MEM", "OR", "PC_INC", 1, 0, 1])

def xor_r(registers, writer):
    for code, name in registers.items():
        opcode_int = 0xA8 + code
        writer.writerow([f"0x{opcode_int:02X}", 1, f"XOR {name} M1", "PC", "NONE", f"REG_{name}", "XOR", "PC_INC", 1, 0, 1])

def xor_hl(writer):
    opcode_hex = "0xAE"
    writer.writerow([opcode_hex, 1, "XOR HL M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "XOR HL M2", "HL", "NONE", "REG_MEM", "XOR", "NONE", 1, 0, 1])

def xor_n(writer):
    opcode_hex = "0xEE"
    writer.writerow([opcode_hex, 1, "XOR n M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "XOR n M2", "PC", "NONE", "REG_MEM", "XOR", "PC_INC", 1, 0, 1])

def ccf(writer):
    opcode_hex = "0x3F"
    writer.writerow([opcode_hex, 1, "CCF M1", "PC", "NONE", "NONE", "CCF", "PC_INC", 1, 0, 1])

def scf(writer):
    opcode_hex = "0x37"
    writer.writerow([opcode_hex, 1, "SCF M1", "PC", "NONE", "NONE", "SCF", "PC_INC", 1, 0, 1])

def daa(writer):
    opcode_hex = "0x27"
    writer.writerow([opcode_hex, 1, "DAA M1", "PC", "NONE", "NONE", "DAA", "PC_INC", 1, 0, 1])

def cpl(writer):
    opcode_hex = "0x2F"
    writer.writerow([opcode_hex, 1, "CPL M1", "PC", "NONE", "NONE", "CPL", "PC_INC", 1, 0, 1])

