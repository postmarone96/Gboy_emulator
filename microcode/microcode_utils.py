def generate_ld_r_r(registers, writer):
    """
    Load to the 8-bit register r, data from the 8-bit register r'.
    """
    # Remove HL from the registers
    if 6 in registers:
        registers.pop(6)

    # Create the rows for all register combinations
    for d_code, d_name in registers.items():
        for s_code, s_name in registers.items():
            opcode_int = 0x40 | (d_code << 3) | s_code
            opcode_hex = f"0x{opcode_int:02X}"
            writer.writerow([
                opcode_hex,
                1,
                f"LD {d_name}, {s_name}",
                f"REG_{d_name}",
                f"REG_{s_name}",
                1, 0, 1, 1
            ])