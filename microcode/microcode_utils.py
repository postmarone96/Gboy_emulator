def remove_hl(registers):
    """
    Remove HL from the registers
    """
    if 6 in registers:
        registers.pop(6)
    
def generate_ld_r_r(registers, writer):
    """
    Load to the 8-bit register r, data from the 8-bit register r'.
    """
    remove_hl(registers)
    # Create the rows for all register combinations
    for d_code, d_name in registers.items():
        for s_code, s_name in registers.items():
            opcode_int = 0x40 | (d_code << 3) | s_code
            opcode_hex = f"0x{opcode_int:02X}"
            writer.writerow([
                opcode_hex,
                1,
                f"LD {d_name}, {s_name}",
                "PC",
                f"REG_{d_name}",
                f"REG_{s_name}",
                1, 0, 1, 1
            ])

def generate_ld_r_n(registers, writer):
    """
    Load to the 8-bit register r, the immediate data n.
    """
    remove_hl(registers)
    # Create the rows for all registers
    for d_code, d_name in registers.items():
        opcode_int = (d_code << 3) | 0x06
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([
            opcode_hex,
            1,
            f"LD {name}, n (M1)",
            "PC",
            "None",
            "None",
            1, 0, 1, 0
        ])
        writer.writerow([
            opcode_hex,
            2,
            f"LD {name}, n (M2)",
            "PC",
            f"REG_{d_name}",
            "MEM_DATA",
            1, 0, 1, 1
        ])