def halt(writer):
    opcode_hex = "0x76"
    writer.writerow([opcode_hex, 1, "HALT M1", "PC", "NONE", "NONE", "NONE", "HALT_START", 1, 0, 1])

def interrupt_sequence(writer):
    opcode = "0x100"
    writer.writerow([opcode, 1, "INT M1", "NONE", "NONE", "NONE", "NONE", "GET_INT_VECTOR", 1, 0, 0])
    writer.writerow([opcode, 2, "INT M2", "NONE", "NONE", "NONE", "NONE", "SP_DEC", 0, 0, 0])
    writer.writerow([opcode, 3, "INT M3", "SP", "REG_MEM", "REG_PC_H", "NONE", "SP_DEC", 0, 1, 0])
    writer.writerow([opcode, 4, "INT M4", "SP", "REG_MEM", "REG_PC_L", "NONE", "WZ_TO_PC", 0, 1, 1])

def stop(writer):
    # Einfach 2 Bytes überspringen, damit der PC hinter dem STOP steht
    writer.writerow(["0x10", 1, "STOP M1", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 0])
    writer.writerow(["0x10", 2, "STOP M2", "PC", "NONE", "NONE", "NONE", "PC_INC", 1, 0, 1])

def di(writer):
    opcode_hex = "0xF3"
    writer.writerow([opcode_hex, 1, "DI M1", "PC", "NONE", "NONE", "NONE", "DI_OP", 1, 0, 1])

def ei(writer):
    opcode_hex = "0xFB"
    writer.writerow([opcode_hex, 1, "EI M1", "PC", "NONE", "NONE", "NONE", "EI_OP", 1, 0, 1])
