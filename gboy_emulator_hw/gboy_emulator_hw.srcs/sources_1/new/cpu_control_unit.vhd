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
    signal m_cycle      : integer range 1 to 4 := 1;
    signal t_cycle      : integer range 1 to 4 := 1;
    signal phase_executed  : integer range 1 to 4 := 1;

    -- Current Microcode Word from ROM
    signal mc           : microcode_row;
    
    -- Internal Data Bus
   signal internal_bus  : std_logic_vector(7 downto 0); 
   
    -- Internal Registers
    signal reg_a, reg_b, reg_c, reg_d, reg_e, reg_h, reg_l: std_logic_vector(7 downto 0) := (others => '0');
    signal temp_z, temp_w: std_logic_vector(7 downto 0) := (others => '0');
    signal pc, sp: unsigned(15 downto 0) := (others => '0');

begin
    -- 1. Index the ROM using current IR and M-Cycle
    mc <= MICROCODE_ROM(current_ir, m_cycle);
    
    -- 2. Address Bus Multiplexer
    process(mc.addr_sel, pc, sp, reg_h, reg_l, reg_b, reg_c, reg_d, reg_e, temp_w, temp_z)
    begin
        case mc.addr_sel is
            when 0 => addr_bus <= std_logic_vector(pc);
            when 1 => addr_bus <= reg_h & reg_l;
            when 2 => addr_bus <= reg_b & reg_c;
            when 3 => addr_bus <= reg_d & reg_e;
            when 4 => addr_bus <= temp_w & temp_z;
            when 5 => addr_bus <= x"FF" & reg_c;
            when 6 => addr_bus <= x"FF" & temp_z;
            when 7 => addr_bus <= std_logic_vector(sp);
            when others => addr_bus <= (others => '0');
        end case;    
    end process;
    
    -- 3. Internal Data Bus Mux
    process(mc.reg_src, reg_a, reg_b, reg_c, reg_d, reg_e, reg_h, reg_l, temp_z, temp_w, mem_data_in)
    begin
        case mc.reg_src is
            when 0 => internal_bus <= reg_b;
            when 1 => internal_bus <= reg_c;
            when 2 => internal_bus <= reg_d;
            when 3 => internal_bus <= reg_e;
            when 4 => internal_bus <= reg_h;
            when 5 => internal_bus <= reg_l;
            when 7 => internal_bus <= reg_a;
            when 8 => internal_bus <= mem_data_in;
            when 9 => internal_bus <= temp_z;
            when 10=> internal_bus <= temp_w;
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
            sp <= (others => '0');

            temp_z <= (others => '0');
            temp_w <= (others => '0');

            -- rst registers
            reg_a <= x"01";
            reg_b <= x"02";
            reg_c <= x"03";
            reg_d <= x"04";
            reg_e <= x"05";
            reg_h <= x"07";
            reg_l <= x"08";

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
                        when 0 => reg_b  <= internal_bus;
                        when 1 => reg_c  <= internal_bus;
                        when 2 => reg_d  <= internal_bus;
                        when 3 => reg_e  <= internal_bus;
                        when 4 => reg_h  <= internal_bus;
                        when 5 => reg_l  <= internal_bus;
                        when 7 => reg_a  <= internal_bus;
                        when 8 => mem_data_out <= internal_bus;
                        when 9 => temp_z <= internal_bus;
                        when 10=> temp_w <= internal_bus;
                        when others => null;
                    end case;
                    t_cycle <= 3;

                when 3 =>
                    -- Pointer math
                    case mc.idu_op is
                        when 1 => pc <= pc + 1;
                        when 2 => sp <= sp + 1;
                        when 3 => sp <= sp - 1;
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
