def generate_ld_r_r(registers, writer):
    """
    Load to the 8-bit register r, data from the 8-bit register r'.
    """
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
    # Create the rows for all registers
    for code, name in registers.items():
        opcode_int = (code << 3) | 0x06
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([
            opcode_hex,
            1,
            f"LD {name}, n (M1)",
            "PC",
            "NONE",
            "NONE",
            1, 0, 1, 0
        ])
        writer.writerow([
            opcode_hex,
            2,
            f"LD {name}, n (M2)",
            "PC",
            f"REG_{name}",
            "MEM_DATA",
            1, 0, 1, 1
        ])

def generate_ld_r_hl(registers, writer):
    """
    Load to the 8-bit register r, data from the absolute address specified by the 16-bit register HL.
    """
    # Create the rows for all registers
    for code, name in registers.items():
        opcode_int = 0x40 | (code << 3) | 0x06
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([
            opcode_hex,
            1,
            f"LD {name}, (HL) (M1)",
            "PC",
            "NONE",
            "NONE",
            1, 0, 1, 0
        ])
        writer.writerow([
            opcode_hex,
            2,
            f"LD {name}, (HL) (M2)",
            "HL",
            f"REG_{name}",
            "MEM_DATA",
            1, 0, 0, 1
        ])

def generate_ld_hl_r(registers, writer):
    """
    Load to the absolute address specified by the 16-bit register HL, data from the 8-bit register r.
    """
    # Create the rows for all registers
    for code, name in registers.items():
        opcode_int = 0x70 | code
        opcode_hex = f"0x{opcode_int:02X}"
        writer.writerow([
            opcode_hex,
            1,
            f"LD (HL), {name} (M1)",
            "PC",
            "NONE",
            "NONE",
            1, 0, 1, 0  # Read, Write, PC_Inc, Done
        ])
        writer.writerow([
            opcode_hex,
            2,
            f"LD (HL), {name} (M2)",
            "HL",
            "MEM_DATA",
            f"REG_{name}",
            0, 1, 0, 1  # Read, Write, PC_Inc, Done
        ])

def generate_ld_hl_n(registers, writer):
    """
    Load to the absolute address specified by the 16-bit register HL, the immediate data n.
    """
    opcode_int = 0x36
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LD (HL), n (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LD (HL), n (M2)",
        "PC",
        "TEMP_Z",
        "MEM_DATA",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        3,
        "LD (HL), n (M3)",
        "HL",
        "MEM_DATA",
        "TEMP_Z",
        0, 1, 0, 1  # Read, Write, PC_Inc, Done
    ])

def generate_ld_a_bc(registers, writer):
    """
    Load to the 8-bit A register, data from the absolute address specified by the 16-bit register BC.
    """
    opcode_int = 0x0A
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LD A, (BC) (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LD A, (BC) (M2)",
        "BC",
        "REG_A",
        "MEM_DATA",
        1, 0, 0, 1  # Read, Write, PC_Inc, Done
    ])

def generate_ld_a_de(registers, writer):
    """
    Load to the 8-bit A register, data from the absolute address specified by the 16-bit register DE.
    """
    opcode_int = 0x1A
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LD A, (DE) (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LD A, (DE) (M2)",
        "DE",
        "REG_A",
        "MEM_DATA",
        1, 0, 0, 1  # Read, Write, PC_Inc, Done
    ])

def generate_ld_bc_a(registers, writer):
    """
    Load to the absolute address specified by the 16-bit register BC, data from the 8-bit A register.    
    """
    opcode_int = 0x02
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LD (BC), A (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LD (BC), A (M2)",
        "BC",
        "MEM_DATA",
        "REG_A",
        0, 1, 0, 1  # Read, Write, PC_Inc, Done
    ])

def generate_ld_de_a(registers, writer):
    """
    Load to the absolute address specified by the 16-bit register DE, data from the 8-bit A register.
    """
    opcode_int = 0x12
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LD (DE), A (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LD (DE), A (M2)",
        "DE",
        "MEM_DATA",
        "REG_A",
        0, 1, 0, 1  # Read, Write, PC_Inc, Done
    ])

def generate_ld_a_nn(registers, writer):
    """
    Load to the 8-bit A register, data from the absolute address specified by the 16-bit operand nn.    
    """
    opcode_int = 0xFA
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LD A, (nn) (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LD A, (nn) (M2)",
        "PC",
        "TEMP_Z",
        "MEM_DATA",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
        writer.writerow([
        opcode_hex,
        3,
        "LD A, (nn) (M3)",
        "PC",
        "TEMP_W",
        "MEM_DATA",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        4,
        "LD A, (nn) (M4)",
        "WZ",
        "REG_A",
        "MEM_DATA",
        1, 0, 0, 1  # Read, Write, PC_Inc, Done
    ])

def generate_ld_nn_a(registers, writer):
    """
    Load to the absolute address specified by the 16-bit operand nn, data from the 8-bit A register.
    """
    opcode_int = 0xEA
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LD (nn), A (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LD (nn), A (M2)",
        "PC",
        "TEMP_Z",
        "MEM_DATA",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
        writer.writerow([
        opcode_hex,
        3,
        "LD (nn), A (M3)",
        "PC",
        "TEMP_W",
        "MEM_DATA",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        4,
        "LD (nn), A (M4)",
        "WZ",
        "MEM_DATA",
        "REG_A",
        0, 1, 0, 1  # Read, Write, PC_Inc, Done
    ])

def generate_ldh_a_c(registers, writer):
    """
    Load to the 8-bit A register, data from the address specified by the 8-bit C register. The full
    16-bit absolute address is obtained by setting the most significant byte to 0xFF and the least
    significant byte to the value of C, so the possible range is 0xFF00-0xFFFF.
    """
    opcode_int = 0xF2
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LDH A, (C) (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LDH A, (C) (M2)",
        "FF00_C",
        "REG_A",
        f"MEM_DATA",
        1, 0, 0, 1  # Read, Write, PC_Inc, Done
    ])

def generate_ldh_c_a(registers, writer):
    """
    Load to the address specified by the 8-bit C register, data from the 8-bit A register. The full
    16-bit absolute address is obtained by setting the most significant byte to 0xFF and the least
    significant byte to the value of C, so the possible range is 0xFF00-0xFFFF.
    """
    opcode_int = 0xE2
    opcode_hex = f"0x{opcode_int:02X}"
    writer.writerow([
        opcode_hex,
        1,
        "LDH (C), A (M1)",
        "PC",
        "NONE",
        "NONE",
        1, 0, 1, 0  # Read, Write, PC_Inc, Done
    ])
    writer.writerow([
        opcode_hex,
        2,
        "LDH (C), A (M2)",
        "FF00_C",
        "MEM_DATA",
        "REG_A",
        0, 1, 0, 1  # Read, Write, PC_Inc, Done
    ])   
