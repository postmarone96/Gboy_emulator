import csv

from microcode_8_bits_utils import *
from microcode_16_bits_utils import *

def csv_gen(path_to_csv_file):
    # The standard 3-bit register mapping for SM83
    b8_registers = {
        0: "B",
        1: "C",
        2: "D",
        3: "E",
        4: "H",
        5: "L",
        7: "A",
    }

    b16_registers = {
        "00": "BC",
        "01": "DE",
        "10": "HL",
        "11": "SP"
    }

    b16_registers_stack = {
        "00": "BC",
        "01": "DE",
        "10": "HL",
        "11": "AF"
    }



    header_row = [
        "Opcode",     # e.g., 0xF0
        "M_Cycle",    # 1, 2, 3
        "Label",      # "LDH A, (n) (M3)"
        "Addr_Sel",   # Mux for Address Bus: PC, FF00_Z, SP, HL
        "Reg_Dest",   # Internal Latch Destination: REG_A, TEMP_Z, REG_MEM
        "Reg_Src",    # Internal Latch Source: REG_A, TEMP_Z, REG_MEM
        "ALU_Op",     # Math/Commit: NONE, ADD, SUB
        "IDU_Op",     # Pointer Math: NONE, PC_INC, HL_INC, HL_DEC, WZ_DEC, WZ_INC
        "Mem_Read",   # 1 or 0
        "Mem_Write",  # 1 or 0
        "Is_Done"     # 1 or 0
    ]

    with open(path_to_csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header_row)

        """8 Bit Load Instructions"""
        # NOP
        generate_nop(writer)
        #
        # # Done
        # # LD r, r’: Load register
        # generate_ld_r_r(b8_registers, writer)
        #
        # # Done
        # # LD r, n: Load register (immediate)
        # generate_ld_r_n(b8_registers, writer)
        #
        # # Done
        # # LD r, (HL): Load register (indirect HL)
        # generate_ld_r_hl(b8_registers, writer)
        #
        # # Done
        # # LD (HL), r: Load from register (indirect HL)
        # generate_ld_hl_r(b8_registers, writer)
        #
        # # Done
        # # LD (HL), n: Load from immediate data (indirect HL)
        # generate_ld_hl_n(writer)
        #
        # # Done
        # # LD A, (BC): Load accumulator (indirect BC)
        # generate_ld_a_bc(writer)
        #
        # # Done
        # # LD A, (DE): Load accumulator (indirect DE)
        # generate_ld_a_de(writer)
        #
        # # Done
        # # LD (BC), A: Load from accumulator (indirect BC)
        # generate_ld_bc_a(writer)
        #
        # # Done
        # # LD (DE), A: Load from accumulator (indirect DE)
        # generate_ld_de_a(writer)
        #
        # # Done
        # # LD A, (nn): Load accumulator (direct)
        # generate_ld_a_nn(writer)
        #
        # # Done
        # # LD (nn), A: Load from accumulator (direct)
        # generate_ld_nn_a(writer)
        #
        # # Done
        # # LDH A, (C): Load accumulator (indirect 0xFF00+C)
        # generate_ldh_a_c(writer)
        #
        # # Done
        # # LDH (C), A: Load from accumulator (indirect 0xFF00+C)
        # generate_ldh_c_a(writer)
        #
        # # Done
        # # LDH A, (n): Load accumulator (direct 0xFF00+n)
        # generate_ldh_a_n(writer)
        #
        # # Done
        # # LDH (n), A: Load from accumulator (direct 0xFF00+n)
        # generate_ldh_n_a(writer)

        # # Done
        # LD A, (HL-): Load accumulator (indirect HL, decrement)
        # generate_ld_a_hl_minus(writer)

        # # Done
        # LD (HL-), A: Load from accumulator (indirect HL, decrement)
        # generate_ld_hl_minus_a(writer)

        # # Done
        # LD A, (HL+): Load accumulator (indirect HL, increment)
        # generate_ld_a_hl_plus(writer)

        # # Done
        # LD (HL+), A: Load from accumulator (indirect HL, increment)
        # generate_ld_hlplus_a(writer)

        """16 Bit Load Instructions"""
        # # Done
        # # LD rr, nn: Load 16-bit register / register pair
        # generate_ld_rr_nn(writer, b16_registers)
        #
        # # # Done
        # # Load to the absolute address specified by the 16-bit operand nn, data from the 16-bit SP register.
        # generate_ld_nn_sp(writer)
        #
        # # # Done
        # # LD SP, HL: Load stack pointer from HL
        # generate_ld_sp_hl(writer)
        #
        # # # Done
        # # PUSH rr: Push to stack
        # generate_push_rr(writer, b16_registers_stack)
        #
        # # # Done
        # # POP rr: Pop from stack
        # generate_pop_rr(writer, b16_registers_stack)

        # Done
        # LD HL, SP+e: Load HL from adjusted stack pointer
        generate_ld_sp_plus_e(writer)



