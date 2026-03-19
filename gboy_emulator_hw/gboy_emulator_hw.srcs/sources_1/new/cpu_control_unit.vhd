library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;
use work.microcode_pkg.all;


entity cpu_control_unit is
    Port (
        clk         : in std_logic;
        rst         : in std_logic;
        mem_data_in   : in  std_logic_vector(7 downto 0);
        mem_data_out  : out std_logic_vector(7 downto 0);
        addr_bus    : out std_logic_vector(15 downto 0);
        mem_rd      : out std_logic;
        mem_wr      : out std_logic   
    );
end cpu_control_unit;

architecture rtl of cpu_control_unit is
    
    -- Execution State
    signal current_ir   : integer range 0 to 255 := 0;
    signal m_cycle      : integer range 1 to 5 := 1;
    signal t_cycle      : integer range 1 to 4 := 1;
    signal phase_executed  : integer range 1 to 4 := 1;

    -- Current Microcode Word from ROM
    signal mc           : microcode_row;
    
    -- Internal Data Bus
   signal internal_bus  : std_logic_vector(7 downto 0); 
   
    -- Internal Registers
    signal af, bc, de, hl, sp, pc, temp_wz: unsigned(15 downto 0) := (others => '0');

begin
    -- 1. Index the ROM using current IR and M-Cycle
    mc <= MICROCODE_ROM(current_ir, m_cycle);
    
    -- 2. Address Bus Multiplexer
    process(mc.addr_sel, bc, de, hl, sp, pc, temp_wz)
    begin
        case mc.addr_sel is
            when 0 => addr_bus <= std_logic_vector(pc);
            when 1 => addr_bus <= std_logic_vector(hl);
            when 2 => addr_bus <= std_logic_vector(bc);
            when 3 => addr_bus <= std_logic_vector(de);
            when 4 => addr_bus <= std_logic_vector(temp_wz);
            when 5 => addr_bus <= x"FF" & std_logic_vector(bc(7 downto 0));
            when 6 => addr_bus <= x"FF" & std_logic_vector(temp_wz(7 downto 0));
            when 7 => addr_bus <= std_logic_vector(sp);
            when others => addr_bus <= (others => '0');
        end case;    
    end process;
    
    -- 3. Internal Data Bus Mux
    process(mc.reg_src, af, bc, de, hl, temp_wz, sp, mem_data_in)
    begin
        case mc.reg_src is
            when 0 => internal_bus <= std_logic_vector(bc(15 downto 8));
            when 1 => internal_bus <= std_logic_vector(bc(7 downto 0));
            when 2 => internal_bus <= std_logic_vector(de(15 downto 8));
            when 3 => internal_bus <= std_logic_vector(de(7 downto 0));
            when 4 => internal_bus <= std_logic_vector(hl(15 downto 8));
            when 5 => internal_bus <= std_logic_vector(hl(7 downto 0));
            when 7 => internal_bus <= std_logic_vector(af(15 downto 8));
            when 8 => internal_bus <= std_logic_vector(af(7 downto 0));
            when 9 => internal_bus <= mem_data_in;
            when 10 => internal_bus <= std_logic_vector(temp_wz(7 downto 0));
            when 11 => internal_bus <= std_logic_vector(temp_wz(15 downto 8));
            when 12 => internal_bus <= std_logic_vector(sp(7 downto 0));
            when 13 => internal_bus <= std_logic_vector(sp(15 downto 8));
            when others => internal_bus <= (others => '0');
        end case;
    end process;

    -- 4. Rising edge
    process(clk, rst)
    begin
        if rst = '1' then
            current_ir <= 0;

            mem_data_out <= (others => '0');

            t_cycle <= 1;
            m_cycle <= 1;

            phase_executed <= 1;

            pc <= (others => '0');

            temp_wz <= (others => '0');

            -- rst registers
            af <= x"0A01";
            bc <= x"0203";
            de <= x"0405";
            hl <= x"0708";
            sp <= x"FFFB";

        elsif rising_edge(clk) then
            phase_executed <= t_cycle;

            case t_cycle is
                when 1 =>
                    -- Saample memory and start the M-cycle
                    if m_cycle = 1 then
                        if is_X(mem_data_in) then
                            current_ir <= 0;
                        else
                            current_ir <= to_integer(unsigned(mem_data_in));
                        end if;
                    end if;
                    t_cycle <= 2;

                when 2 =>
                -- Register writeback
                    case mc.reg_dest is
                        when 0 => bc(15 downto 8)  <= unsigned(internal_bus);
                        when 1 => bc(7 downto 0)  <= unsigned(internal_bus);
                        when 2 => de(15 downto 8)  <= unsigned(internal_bus);
                        when 3 => de(7 downto 0)  <= unsigned(internal_bus);
                        when 4 => hl(15 downto 8)  <= unsigned(internal_bus);
                        when 5 => hl(7 downto 0)  <= unsigned(internal_bus);
                        when 7 => af(15 downto 8)  <= unsigned(internal_bus);
                        when 8 => af(7 downto 0) <= unsigned(internal_bus and x"F0");
                        when 9 => mem_data_out <= internal_bus;
                        when 10 => temp_wz(7 downto 0) <= unsigned(internal_bus);
                        when 11 => temp_wz(15 downto 8) <= unsigned(internal_bus);
                        when 12 => sp(7 downto 0) <= unsigned(internal_bus);
                        when 13 => sp(15 downto 8) <= unsigned(internal_bus);
                        when others => null;
                    end case;
                    t_cycle <= 3;

                when 3 =>
                    -- Pointer math
                    case mc.idu_op is
                        when 1 => pc <= pc + 1;
                        when 2 => sp <= sp + 1;
                        when 3 => sp <= sp - 1;
                        when 4 => hl <= hl - 1;
                        when 5 => hl <= hl + 1;
                        when 6 => temp_wz <= temp_wz + 1;
                        when 7 => sp <= hl;
                        when others => null;
                    end case;
                    t_cycle <= 4;

                when 4 =>
                    -- Finish m_cycle
                    if mc.is_done = '1' then
                        m_cycle <= 1;
                    else
                        m_cycle <= m_cycle + 1;
                    end if;
                    t_cycle <= 1;

                when others =>
                    t_cycle <= 1;
            end case;
        end if;
    end process;

    -- 6. Memory Signals
    mem_rd <= mc.mem_read;
    mem_wr <= mc.mem_write;

end rtl;
