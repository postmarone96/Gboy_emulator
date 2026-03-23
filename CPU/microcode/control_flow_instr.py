def jp_nn(writer):
    opcode_hex = "0xC3"
    writer.writerow([opcode_hex, 1, "JP nn M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "JP nn M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "JP nn M3", "PC", "TEMP_W", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 4, "JP nn M4", "WZ", "NONE", "NONE", "NONE", "WZ_TO_PC", 0, 0, 1])

def jp_hl(writer):
    opcode_hex = "0xE9"
    writer.writerow([opcode_hex, 1, "JP HL M1", "PC", "NONE", "NONE", "NONE", "HL_TO_PC", 1, 0, 0])

def jp_cc_nn(writer):
    # Mapping: NZ=00, Z=01, NC=10, C=11 (Bits 4-3)
    conditions = {0: "NZ", 1: "Z", 2: "NC", 3: "C"}
    for code, name in conditions.items():
        opcode = 0xC2 | (code << 3)
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"JP {name},nn M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"JP {name},nn M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 3, f"JP {name},nn M3", "PC", "TEMP_W", "REG_MEM", "CHECK_CC", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 4, f"JP {name},nn M4", "NONE", "NONE", "NONE", "NONE", "WZ_TO_PC", 0, 0, 1])

def jr_e(writer):
    opcode_hex = "0x18"
    writer.writerow([opcode_hex, 1, "JR e M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "JR e M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "JR e M3", "NONE", "NONE", "NONE", "JR_ADD", "NONE", 0, 0, 1])


def jr_cc_e(writer):
    conditions = {0: "NZ", 1: "Z", 2: "NC", 3: "C"}
    for code, name in conditions.items():
        opcode = 0x20 | (code << 3)
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"JR {name},e M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"JR {name},e M2", "PC", "TEMP_Z", "REG_MEM", "CHECK_CC", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 3, f"JR {name},e M3", "NONE", "NONE", "NONE", "JR_ADD", "NONE", 0, 0, 1])

def call_nn(writer):
    opcode_hex = "0xCD"
    writer.writerow([opcode_hex, 1, "CALL nn M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "CALL nn M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "CALL nn M3", "PC", "TEMP_W", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 4, "CALL nn M4", "NONE", "NONE", "NONE", "NONE", "SP_DEC", 0, 0, 0])
    writer.writerow([opcode_hex, 5, "CALL nn M5", "SP", "REG_MEM", "REG_PC_H", "NONE", "SP_DEC", 0, 1, 0])
    writer.writerow([opcode_hex, 6, "CALL nn M6", "SP", "REG_MEM", "REG_PC_L", "NONE", "WZ_TO_PC", 0, 1, 1])


def call_cc_nn(writer):
    # Opcodes: 0xC4 (NZ), 0xCC (Z), 0xD4 (NC), 0xDC (C)
    conditions = {0: "NZ", 1: "Z", 2: "NC", 3: "C"}
    for code, name in conditions.items():
        opcode = 0xC4 | (code << 3)
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"CALL {name},nn M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"CALL {name},nn M2", "PC", "TEMP_Z", "REG_MEM", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 3, f"CALL {name},nn M3", "PC", "TEMP_W", "REG_MEM", "CHECK_CC", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 4, f"CALL {name},nn M4", "NONE", "NONE", "NONE", "NONE", "SP_DEC", 0, 0, 0])
        writer.writerow([opcode_hex, 5, f"CALL {name},nn M5", "SP", "REG_MEM", "REG_PC_H", "NONE", "SP_DEC", 0, 1, 0])
        writer.writerow([opcode_hex, 6, f"CALL {name},nn M6", "SP", "REG_MEM", "REG_PC_L", "NONE", "WZ_TO_PC", 0, 1, 1])

def ret(writer):
    opcode_hex = "0xC9"
    writer.writerow([opcode_hex, 1, "RET M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "RET M2", "SP", "TEMP_Z", "REG_MEM", "NONE", "SP_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "RET M3", "SP", "TEMP_W", "REG_MEM", "NONE", "SP_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 4, "RET M4", "NONE", "NONE", "NONE", "NONE", "WZ_TO_PC", 0, 0, 1])


def ret_cc(writer):
    # Opcodes: 0xC0 (NZ), 0xC8 (Z), 0xD0 (NC), 0xD8 (C)
    conditions = {0: "NZ", 1: "Z", 2: "NC", 3: "C"}
    for code, name in conditions.items():
        opcode = 0xC0 | (code << 3)
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"RET {name} M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"RET {name} M2", "NONE", "NONE", "NONE", "CHECK_CC", "NONE", 0, 0, 0])
        writer.writerow([opcode_hex, 3, f"RET {name} M3", "SP", "TEMP_Z", "REG_MEM", "NONE", "SP_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 4, f"RET {name} M4", "SP", "TEMP_W", "REG_MEM", "NONE", "SP_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 5, f"RET {name} M5", "NONE", "NONE", "NONE", "NONE", "WZ_TO_PC", 0, 0, 1])

def reti(writer):
    opcode_hex = "0xD9"
    writer.writerow([opcode_hex, 1, "RETI M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 2, "RETI M2", "SP", "TEMP_Z", "REG_MEM", "NONE", "SP_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 3, "RETI M3", "SP", "TEMP_W", "REG_MEM", "NONE", "SP_INC", 1, 0, 0])
    writer.writerow([opcode_hex, 4, "RETI M4", "NONE", "NONE", "NONE", "NONE", "RETI_DONE", 0, 0, 1])

def rst_n(writer):
    # RST Adressen: 00h, 08h, 10h, 18h, 20h, 28h, 30h, 38h
    for i in range(8):
        n = i * 8
        opcode = 0xC7 | (i << 3)
        opcode_hex = f"0x{opcode:02X}"
        writer.writerow([opcode_hex, 1, f"RST {n:02X}h M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
        writer.writerow([opcode_hex, 2, f"RST {n:02X}h M2", "NONE", "NONE", "NONE", "NONE", "SP_DEC", 0, 0, 0])
        writer.writerow([opcode_hex, 3, f"RST {n:02X}h M3", "SP", "REG_MEM", "REG_PC_H", "NONE", "SP_DEC", 0, 1, 0])
        writer.writerow([opcode_hex, 4, f"RST {n:02X}h M4", "SP", "REG_MEM", "REG_PC_L", "NONE", "RST_PC", 0, 1, 1])
