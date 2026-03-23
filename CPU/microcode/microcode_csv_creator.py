import csv
from load_8_bits_instr import *
from load_16_bits_instr import *
from arith_8_bits_instr import *
from arith_16_bits_instr import *
from rsb_instr import *
from control_flow_instr import *
from misc_instr import *

def csv_gen(path_to_csv_file, path_to_cb_csv_file):
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

    with open(path_to_csv_file, 'w', newline='') as f, open(path_to_cb_csv_file, 'w', newline='') as cbf:

        writer = csv.writer(f)
        cb_writer = csv.writer(cbf)

        writer.writerow(header_row)
        cb_writer.writerow(header_row)

        """8 Bit Load Instructions"""
        # NOP
        generate_nop(writer)

        # Done
        # LD r, r’: Load register
        generate_ld_r_r(b8_registers, writer)

        # Done
        # LD r, n: Load register (immediate)
        generate_ld_r_n(b8_registers, writer)

        # Done
        # LD r, (HL): Load register (indirect HL)
        generate_ld_r_hl(b8_registers, writer)

        # Done
        # LD (HL), r: Load from register (indirect HL)
        generate_ld_hl_r(b8_registers, writer)

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

        # Done
        # LD A, (HL-): Load accumulator (indirect HL, decrement)
        generate_ld_a_hl_minus(writer)

        # Done
        # LD (HL-), A: Load from accumulator (indirect HL, decrement)
        generate_ld_hl_minus_a(writer)

        # Done
        # LD A, (HL+): Load accumulator (indirect HL, increment)
        generate_ld_a_hl_plus(writer)

        # Done
        # LD (HL+), A: Load from accumulator (indirect HL, increment)
        generate_ld_hlplus_a(writer)

        """16 Bit Load Instructions"""
        # Done
        # LD rr, nn: Load 16-bit register / register pair
        generate_ld_rr_nn(writer, b16_registers)

        # # Done
        # Load to the absolute address specified by the 16-bit operand nn, data from the 16-bit SP register.
        generate_ld_nn_sp(writer)

        # # Done
        # LD SP, HL: Load stack pointer from HL
        generate_ld_sp_hl(writer)

        # # Done
        # PUSH rr: Push to stack
        generate_push_rr(writer, b16_registers_stack)

        # # Done
        # POP rr: Pop from stack
        generate_pop_rr(writer, b16_registers_stack)

        # Done
        # LD HL, SP+e: Load HL from adjusted stack pointer
        generate_ld_sp_plus_e(writer)

        """8-bit arithmetic and logical instructions"""
        # Done
        # ADD r: Add (register)
        add_r(b8_registers, writer)

        # ADD (HL): Add (indirect HL)
        add_hl(writer)

        # ADD n: Add (immediate)
        add_n(writer)

        # ADC r: Add with carry (register)
        adc_r(b8_registers, writer)

        # ADC n: Add with carry (register)
        adc_n(writer)

        # ADC (HL): Add with carry (indirect HL)
        adc_hl(writer)

        # SUB r: Subtract (register)
        sub_r(b8_registers, writer)

        # SUB (HL): Subtract (indirect HL)
        sub_hl(writer)

        # SUB n: Subtract (immediate)
        sub_n(writer)

        # SBC r: Subtract with carry (register)
        sbc_r(b8_registers, writer)

        # SBC (HL): Subtract with carry (indirect HL)
        sbc_hl(writer)

        # SBC n: Subtract with carry (immediate)
        sbc_n(writer)

        # CP r: Compare (register)
        cp_r(b8_registers, writer)

        # CP (HL): Compare (indirect HL)
        cp_hl(writer)

        # CP n: Compare (immediate)
        cp_n(writer)

        # INC r: Increment (register)
        inc_r(b8_registers, writer)

        # INC (HL): Increment (indirect HL)
        inc_hl(writer)

        # DEC r: Decrement (register)
        dec_r(b8_registers, writer)

        # DEC (HL): Decrement (indirect HL)
        dec_hl(writer)

        # AND r: Bitwise AND (register)
        and_r(b8_registers, writer)

        # AND (HL): Bitwise AND (indirect HL)
        and_hl(writer)

        # AND n: Bitwise AND (immediate)
        and_n(writer)

        # OR r: Bitwise OR (register)
        or_r(b8_registers, writer)

        # OR (HL): Bitwise OR (indirect HL)
        or_hl(writer)

        # OR n: Bitwise OR (immediate)
        or_n(writer)

        # XOR r: Bitwise XOR (register)
        xor_r(b8_registers, writer)

        # XOR (HL): Bitwise XOR (indirect HL)
        xor_hl(writer)

        # XOR n: Bitwise XOR (immediate)
        xor_n(writer)

        # CCF: Complement carry flag
        ccf(writer)

        # SCF: Set carry flag
        scf(writer)

        # DAA: Decimal adjust accumulator
        daa(writer)

        # CPL: Complement accumulator
        cpl(writer)

        """16-bit arithmetic instructions"""
        # Done
        # INC rr: Increment 16-bit register
        inc_rr(b16_registers, writer)

        # Done
        # DEC rr: Decrement 16-bit register
        dec_rr(b16_registers, writer)

        # Done
        # ADD HL, rr: Add (16-bit register)
        add_hl_rr(b16_registers, writer)

        # Done
        # ADD SP, e: Add to stack pointer (relative)
        add_sp_e(writer)

        """Rotate, shift, and bit operation instructions"""
        # RLCA: Rotate left circular (accumulator)
        rlca(writer)

        # RRCA: Rotate right circular (accumulator)
        rrca(writer)

        # RLA: Rotate left (accumulator)
        rla(writer)

        # RRA: Rotate right (accumulator)
        rra(writer)

        # CB Prefix
        cb_prefix(writer)

        # RLC r: Rotate left circular (register)
        rlc_r(b8_registers, cb_writer)

        # RLC (HL): Rotate left circular (indirect HL)
        rlc_hl(cb_writer)

        # RRC r: Rotate right circular (register)
        rrc_r(b8_registers, cb_writer)

        # RRC (HL): Rotate right circular (indirect HL)
        rrc_hl(cb_writer)

        # RL r: Rotate left (register)
        rl_r(b8_registers, cb_writer)

        # RL (HL): Rotate left (indirect HL)
        rl_hl(cb_writer)

        # RR r: Rotate right (register)
        rr_r(b8_registers, cb_writer)

        # RR (HL): Rotate right (indirect HL)
        rr_hl(cb_writer)

        # SLA r: Shift left arithmetic (register)
        sla_r(b8_registers, cb_writer)

        # SLA (HL): Shift left arithmetic (indirect HL)
        sla_hl(cb_writer)

        # SRA r: Shift right arithmetic (register)
        sra_r(b8_registers, cb_writer)

        # SRA (HL): Shift right arithmetic (indirect HL)
        sra_hl(cb_writer)

        # SWAP r: Swap nibbles (register)
        swap_r(b8_registers, cb_writer)

        # SWAP (HL): Swap nibbles (indirect HL)
        swap_hl(cb_writer)

        # SRL r: Shift right logical (register)
        srl_r(b8_registers, cb_writer)

        # SRL (HL): Shift right logical (indirect HL)
        srl_hl(cb_writer)

        # BIT b, r: Test bit (register)
        bit_b_r(b8_registers, cb_writer)

        # BIT b, (HL): Test bit (indirect HL)
        bit_b_hl(cb_writer)

        # RES b, r: Reset bit (register)
        res_b_r(b8_registers, cb_writer)

        # RES b, (HL): Reset bit (indirect HL)
        res_b_hl(cb_writer)

        # SET b, r: Set bit (register)
        set_b_r(b8_registers, cb_writer)

        # SET b, (HL): Set bit (indirect HL)
        set_b_hl(cb_writer)

        """Control flow instructions"""
        # JP nn: Jump
        jp_nn(writer)

        # JP HL: Jump to HL
        jp_hl(writer)

        # JP cc, nn: Jump (conditional)
        jp_cc_nn(writer)

        # JR e: Relative jump
        jr_e(writer)

        # JR cc, e: Relative jump (conditional)
        jr_cc_e(writer)

        # CALL nn: Call function
        call_nn(writer)

        # CALL cc, nn: Call function (conditional)
        call_cc_nn(writer)

        # RET: Return from function
        ret(writer)

        # RET cc: Return from function (conditional)
        ret_cc(writer)

        # RETI: Return from interrupt handler
        reti(writer)

        # RST n: Restart / Call function (implied)
        rst_n(writer)

        """Miscellaneous instructions"""
        # Interrupt entry sequence
        interrupt_sequence(writer)

        # HALT: Halt system clock
        halt(writer)

        # STOP: Stop system and main clocks
        stop(writer)

        # DI: Disable interrupts
        di(writer)

        # EI: Enable interrupts
        ei(writer)
