import csv

from microcode_utils import *


def csv_gen(path_to_csv_file):
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
        "ALU_Op",     # Math/Commit: NONE, ADD, SUB
        "IDU_Op",     # Pointer Math: NONE, PC_INC, SP_DEC, SP_INC
        "Mem_Read",   # 1 or 0
        "Mem_Write",  # 1 or 0
        "Is_Done"     # 1 or 0
    ]

    with open(path_to_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header_row)

        # NOP
        generate_nop(writer)

        # Done
        # LD r, r’: Load register
        generate_ld_r_r(registers, writer)

        # Done
        # LD r, n: Load register (immediate)
        generate_ld_r_n(registers, writer)

        # Done
        # LD r, (HL): Load register (indirect HL)
        generate_ld_r_hl(registers, writer)

        # Done
        # LD (HL), r: Load from register (indirect HL)
        generate_ld_hl_r(registers, writer)

        # Done
        # LD (HL), n: Load from immediate data (indirect HL)
        generate_ld_hl_n(writer)

        # Done
        # LD A, (BC): Load accumulator (indirect BC)
        generate_ld_a_bc(writer)

        # Done
        # LD A, (DE): Load accumulator (indirect DE)
        generate_ld_a_de(writer)

        # Done
        # LD (BC), A: Load from accumulator (indirect BC)
        generate_ld_bc_a(writer)

        # Done
        # LD (DE), A: Load from accumulator (indirect DE)
        generate_ld_de_a(writer)

        # Done
        # LD A, (nn): Load accumulator (direct)
        generate_ld_a_nn(writer)

        # Done
        # LD (nn), A: Load from accumulator (direct)
        generate_ld_nn_a(writer)

        # Done
        # LDH A, (C): Load accumulator (indirect 0xFF00+C)
        generate_ldh_a_c(writer)

        # Done
        # LDH (C), A: Load from accumulator (indirect 0xFF00+C)
        generate_ldh_c_a(writer)

        # Done
        # LDH A, (n): Load accumulator (direct 0xFF00+n)
        generate_ldh_a_n(writer)

        # Done
        # LDH (n), A: Load from accumulator (direct 0xFF00+n)
        generate_ldh_n_a(writer)

        #



