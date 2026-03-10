import csv
from microcode_utils import *

# The standard 3-bit register mapping for SM83
registers = {
    0: "B",
    1: "C",
    2: "D",
    3: "E",
    4: "H",
    5: "L",
    7: "A",
}

header_row = [
    "Opcode",     # e.g., 0xF0
    "M_Cycle",    # 1, 2, 3
    "Label",      # "LDH A, (n) (M3)"
    "Addr_Sel",   # Mux for Address Bus: PC, FF00_Z, SP, HL
    "Reg_Dest",   # Internal Latch Destination: REG_A, TEMP_Z, REG_MEM
    "Reg_Src",    # Internal Latch Source: REG_A, TEMP_Z, REG_MEM
    "ALU_Op",     # Math/Commit: NONE, A_FROM_Z, ADD, SUB
    "IDU_Op",     # Pointer Math: NONE, PC_INC, SP_DEC, SP_INC
    "Mem_Read",   # 1 or 0
    "Mem_Write",  # 1 or 0
    "Is_Done"     # 1 or 0
]

with open('microcode.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header_row)

    # LD r, r’: Load register
    generate_ld_r_r(registers, writer)

    # LD r, n: Load register (immediate)
    generate_ld_r_n(registers, writer)

    # LD r, (HL): Load register (indirect HL)
    generate_ld_r_hl(registers, writer)

    # LD (HL), r: Load from register (indirect HL)
    generate_ld_hl_r(registers, writer)

    # LD (HL), n: Load from immediate data (indirect HL)
    generate_ld_hl_n(registers, writer)

    # LD A, (BC): Load accumulator (indirect BC)
    generate_ld_a_bc(registers, writer)

    # LD A, (DE): Load accumulator (indirect DE)
    generate_ld_a_de(registers, writer)

    # LD (BC), A: Load from accumulator (indirect BC)
    generate_ld_bc_a(registers, writer)

    # LD (DE), A: Load from accumulator (indirect DE)
    generate_ld_de_a(registers, writer)

    # LD A, (nn): Load accumulator (direct)
    generate_ld_a_nn(registers, writer)

    # LD (nn), A: Load from accumulator (direct)
    generate_ld_nn_a(registers, writer)

    # LDH A, (C): Load accumulator (indirect 0xFF00+C)
    generate_ldh_a_c(registers, writer)

    # LDH (C), A: Load from accumulator (indirect 0xFF00+C)
    generate_ldh_c_a(registers, writer)

    # LDH A, (n): Load accumulator (direct 0xFF00+n)
    generate_ldh_a_n(registers, writer)

    # LDH (n), A: Load from accumulator (direct 0xFF00+n)
    generate_ldh_n_a(registers, writer)






