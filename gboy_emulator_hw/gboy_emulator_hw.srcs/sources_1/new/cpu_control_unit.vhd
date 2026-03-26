library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use ieee.numeric_std.all;
use work.microcode_pkg.all;


entity cpu_control_unit is
    generic (
        SIM_POST_BOOT : boolean := false
    );
    Port (
        clk             : in std_logic;
        rst             : in std_logic;

        mem_data_in     : in  std_logic_vector(7 downto 0);
        mem_data_out    : out std_logic_vector(7 downto 0);
        addr_bus        : out std_logic_vector(15 downto 0);
        mem_rd          : out std_logic;
        mem_wr          : out std_logic;

        vblank_irq    : in std_logic; -- Bit 0 (Priorität 1)
        lcd_stat_irq  : in std_logic; -- Bit 1 (Priorität 2)
        timer_irq     : in std_logic; -- Bit 2 (Priorität 3)
        serial_irq    : in std_logic; -- Bit 3 (Priorität 4)
        joypad_irq    : in std_logic  -- Bit 4 (Priorität 5)
    );
end cpu_control_unit;

architecture rtl of cpu_control_unit is
    -- Functions
    function get_sum_9bit(a, b : unsigned(7 downto 0); c : std_logic) return unsigned is
    begin
        return ("0" & a) + ("0" & b) + ("00000000" & c);
    end function;

    function get_sub_9bit(a, b : unsigned(7 downto 0); c : std_logic) return unsigned is
    begin
        return ("0" & a) - ("0" & b) - ("00000000" & c);
    end function;

    function get_hc_bit_sum(a, b : unsigned(3 downto 0); c : std_logic) return std_logic is
    begin
        if (("0" & a) + ("0" & b) + ("0000" & c) > 15) then return '1'; else return '0'; end if;
    end function;

    function get_hc_bit_sub(a, b : unsigned(3 downto 0); c : std_logic) return std_logic is
    begin
        if (("0" & a) < ("0" & b) + ("0000" & c)) then return '1'; else return '0'; end if;
    end function;

    -- Signals and Variables
    signal current_ir : integer range 0 to 256 := 0;
    signal cb_pending       : std_logic := '0';
    signal cb_exec          : std_logic := '0';
    signal m_cycle          : integer range 1 to 6 := 1;
    signal t_cycle          : integer range 1 to 4 := 1;
    signal phase_executed   : integer range 1 to 4 := 1;

    signal ime              : std_logic := '0';
    signal halted           : std_logic := '0';
    signal ei_pending       : std_logic := '0';


    signal mc               : microcode_row;
    signal dbg_mc_addr_sel  : integer range 0 to 8 := 0;
    signal dbg_mc_reg_dest  : integer range 0 to 16 := 16;
    signal dbg_mc_reg_src   : integer range 0 to 16 := 16;
    signal dbg_mc_alu_op    : integer range 0 to 35 := 0;
    signal dbg_mc_idu_op    : integer range 0 to 19 := 0;

    signal addr_bus_raw     : std_logic_vector(15 downto 0);
    signal mem_addr_hold    : std_logic_vector(15 downto 0) := (others => '0');
    signal internal_bus     : std_logic_vector(7 downto 0);
    signal internal_bus_16  : unsigned(15 downto 0);

    signal ie_reg : std_logic_vector(7 downto 0) := (others => '0');
    signal if_reg : std_logic_vector(7 downto 0) := (others => '0');


    -- Buffer Signals   
    signal sp_low_buffer : unsigned(7 downto 0) := (others => '0');

    -- Registers
    signal af, bc, de, hl, sp, pc, temp_wz: unsigned(15 downto 0) := (others => '0');

begin
    -- 1. Index the ROM using current IR and M-Cycle
    mc <= CB_MICROCODE_ROM(current_ir, m_cycle) when cb_exec = '1' else MICROCODE_ROM(current_ir, m_cycle);
    dbg_mc_addr_sel <= mc.addr_sel;
    dbg_mc_reg_dest <= mc.reg_dest;
    dbg_mc_reg_src  <= mc.reg_src;
    dbg_mc_alu_op   <= mc.alu_op;
    dbg_mc_idu_op   <= mc.idu_op;
    
    -- 2. Address Bus Multiplexer
    process(mc.addr_sel, bc, de, hl, sp, pc, temp_wz)
    begin
        case mc.addr_sel is
            when 0 => addr_bus_raw <= std_logic_vector(pc);
            when 1 => addr_bus_raw <= std_logic_vector(hl);
            when 2 => addr_bus_raw <= std_logic_vector(bc);
            when 3 => addr_bus_raw <= std_logic_vector(de);
            when 4 => addr_bus_raw <= std_logic_vector(temp_wz);
            when 5 => addr_bus_raw <= x"FF" & std_logic_vector(bc(7 downto 0));
            when 6 => addr_bus_raw <= x"FF" & std_logic_vector(temp_wz(7 downto 0));
            when 7 => addr_bus_raw <= std_logic_vector(sp);
            when others => addr_bus_raw <= (others => '0');
        end case;    
    end process;
    
    -- 3. Internal Data Bus Mux
    process(all)
    begin
        if mc.reg_src = 9 then
            if addr_bus = x"FFFF" then
                internal_bus <= ie_reg;
            elsif addr_bus = x"FF0F" then
                internal_bus <= if_reg;
            else
                internal_bus <= mem_data_in;
            end if;
        else
            case mc.reg_src is
                when 0  => internal_bus <= std_logic_vector(bc(15 downto 8));
                when 1  => internal_bus <= std_logic_vector(bc(7 downto 0));
                when 2  => internal_bus <= std_logic_vector(de(15 downto 8));
                when 3  => internal_bus <= std_logic_vector(de(7 downto 0));
                when 4  => internal_bus <= std_logic_vector(hl(15 downto 8));
                when 5  => internal_bus <= std_logic_vector(hl(7 downto 0));
                when 7  => internal_bus <= std_logic_vector(af(15 downto 8));
                when 8  => internal_bus <= std_logic_vector(af(7 downto 0));
                when 10 => internal_bus <= std_logic_vector(temp_wz(7 downto 0));
                when 11 => internal_bus <= std_logic_vector(temp_wz(15 downto 8));
                when 12 => internal_bus <= std_logic_vector(sp(7 downto 0));
                when 13 => internal_bus <= std_logic_vector(sp(15 downto 8));
                when 14 => internal_bus <= std_logic_vector(pc(15 downto 8));
                when 15 => internal_bus <= std_logic_vector(pc(7 downto 0));
                when others => internal_bus <= (others => '0');
            end case;
        end if;
    end process;

    addr_bus <= mem_addr_hold when (t_cycle = 3 or t_cycle = 4) else addr_bus_raw;
    
    -- 3.1 16 Bits Internal Data Bus Mux
    process(mc.reg_src, bc, de, hl, sp, af)
    begin
        case mc.reg_src is
            when 0 | 1   => internal_bus_16 <= bc;
            when 2 | 3   => internal_bus_16 <= de;
            when 4 | 5   => internal_bus_16 <= hl;
            when 12 | 13 => internal_bus_16 <= sp;
            when 7 | 8   => internal_bus_16 <= af;
            when others  => internal_bus_16 <= (others => '0');
        end case;
    end process;


    -- 4. Rising edge
    process(clk, rst)
        variable c_in, cc_true : std_logic;
        variable op_res, adjust, a8, src8, wb_data, ir_u: unsigned(7 downto 0) := (others => '0');
        variable adjust_16 : unsigned(15 downto 0):= (others => '0'); 
        variable addsub9 : unsigned(8 downto 0) := (others => '0');
        variable res17 : unsigned(16 downto 0) := (others => '0');
        variable bit_idx : integer range 0 to 7;
        variable wb_en   : std_logic := '0';
        variable wb_dest : integer range 0 to 15 := 15;
    begin
        if rst = '1' then
            halted <= '0';
            ime <= '0';
            ei_pending <= '0';
            cb_pending <= '0';
            cb_exec <= '0';

            current_ir <= 0;
            m_cycle <= 1;
            t_cycle <= 1;
            phase_executed <= 1;

            mem_data_out <= x"00";
            mem_addr_hold <= (others => '0');

            temp_wz <= x"0000";
            sp_low_buffer <= (others => '0');

            if SIM_POST_BOOT then
                pc <= x"0100";
                sp <= x"FFFE";
                af <= x"01B0";
                bc <= x"0013";
                de <= x"00D8";
                hl <= x"014D";
                ie_reg <= x"00";
                if_reg <= x"E1";
            else
                pc <= x"0000";
                sp <= x"FFFB";
                af <= x"FF10";
                bc <= x"0003";
                de <= x"0405";
                hl <= x"0708";
                ie_reg <= (others => '0');
                if_reg <= (others => '0');
            end if;

        elsif rising_edge(clk) then
            -- 1. Always querry Hardware Interrupts
            if vblank_irq   = '1' then if_reg(0) <= '1'; end if;
            if lcd_stat_irq = '1' then if_reg(1) <= '1'; end if;
            if timer_irq    = '1' then if_reg(2) <= '1'; end if;
            if serial_irq   = '1' then if_reg(3) <= '1'; end if;
            if joypad_irq   = '1' then if_reg(4) <= '1'; end if;
            
            if halted = '1' then
                if (ie_reg and if_reg) /= x"00" then
                    halted <= '0';
                    m_cycle <= 1;
                    t_cycle <= 1;
                end if;
            else
                phase_executed <= t_cycle;

                case t_cycle is
                    when 1 =>
                        if m_cycle = 1 then
                            if ei_pending = '1' then
                                ime <= '1';
                                ei_pending <= '0';
                            end if;

                            if ime = '1' and (unsigned(ie_reg) and unsigned(if_reg)) /= 0 then
                                current_ir <= 256; 
                                cb_exec    <= '0';
                            else
                                current_ir <= to_integer(unsigned(mem_data_in));
                                cb_exec    <= cb_pending;
                                cb_pending <= '0';
                                if cb_pending = '0' and unsigned(mem_data_in) = x"CB" then
                                    cb_pending <= '1';
                                end if;
                            end if;
                        end if;
                        t_cycle <= 2;

                    when 2 =>
                    mem_addr_hold <= addr_bus_raw;
                    -- Register writeback
                        case mc.reg_dest is
                            when 0  => bc(15 downto 8)      <= unsigned(internal_bus);
                            when 1  => bc(7 downto 0)       <= unsigned(internal_bus);
                            when 2  => de(15 downto 8)      <= unsigned(internal_bus);
                            when 3  => de(7 downto 0)       <= unsigned(internal_bus);
                            when 4  => hl(15 downto 8)      <= unsigned(internal_bus);
                            when 5  => hl(7 downto 0)       <= unsigned(internal_bus);
                            when 7  => af(15 downto 8)      <= unsigned(internal_bus);
                            when 8  => af(7 downto 0)       <= unsigned(internal_bus and x"F0");
                            when 9  => mem_data_out         <= internal_bus;
                            when 10 => temp_wz(7 downto 0)  <= unsigned(internal_bus);
                            when 11 => temp_wz(15 downto 8) <= unsigned(internal_bus);
                            when 12 => sp(7 downto 0)       <= unsigned(internal_bus);
                            when 13 => sp(15 downto 8)      <= unsigned(internal_bus);
                            when 14 => pc(15 downto 8)      <= unsigned(internal_bus);
                            when 15 => pc(7 downto 0)       <= unsigned(internal_bus);
                            when others => null;
                        end case;
                        
                        -- Internal I/O-Writeback for Interrupt-Register
                        if mc.mem_write = '1' then
                            if addr_bus = x"FFFF" then
                                ie_reg <= internal_bus;
                            elsif addr_bus = x"FF0F" then
                                if_reg <= "111" & internal_bus(4 downto 0); 
                            end if;
                        end if;

                        t_cycle <= 3;

                    when 3 =>
                        -- IDU operations
                        case mc.idu_op is
                            when 1  => pc <= pc + 1;
                            when 2  => sp <= sp + 1;
                            when 3  => sp <= sp - 1;
                            when 4  => hl <= hl + 1;
                            when 5  => hl <= hl - 1;
                            when 6  => de <= de + 1;
                            when 7  => de <= de - 1;
                            when 8  => bc <= bc + 1;
                            when 9  => bc <= bc - 1;
                            when 10 => temp_wz <= temp_wz + 1;
                            when 11 => sp <= hl;
                            when 12 => pc <= temp_wz;
                            when 13 => pc <= hl;
                            when 14 => 
                                pc <= temp_wz;
                                ime <= '1';
                            when 15 =>
                                ir_u := to_unsigned(current_ir, 8);
                                pc <= (others => '0');
                                pc(5 downto 3) <= ir_u(5 downto 3);
                            when 16 =>
                                if ime = '0' and (ie_reg and if_reg) /= x"00" then
                                    halted <= '0'; 
                                else
                                    halted <= '1';
                                end if;
                            when 17 =>
                                ime <= '0';
                                if (if_reg(0) = '1' and ie_reg(0) = '1') then
                                    temp_wz <= x"0040"; if_reg(0) <= '0'; -- V-Blank
                                elsif (if_reg(1) = '1' and ie_reg(1) = '1') then
                                    temp_wz <= x"0048"; if_reg(1) <= '0'; -- LCD STAT
                                elsif (if_reg(2) = '1' and ie_reg(2) = '1') then
                                    temp_wz <= x"0050"; if_reg(2) <= '0'; -- Timer
                                elsif (if_reg(3) = '1' and ie_reg(3) = '1') then
                                    temp_wz <= x"0058"; if_reg(3) <= '0'; -- Serial
                                elsif (if_reg(4) = '1' and ie_reg(4) = '1') then
                                    temp_wz <= x"0060"; if_reg(4) <= '0'; -- Joypad
                                end if;
                            when 18 =>
                                ime <= '0';
                                pc <= pc + 1;
                            when 19 =>
                                ei_pending <= '1';
                                pc <= pc + 1;
                            
                            when others => null;
                        end case;

                        -- ALU operations
                        wb_en := '0';
                        wb_dest := 15;
                        wb_data := (others => '0');
                        a8 := af(15 downto 8);
                        src8 := unsigned(internal_bus);

                        case mc.alu_op is
                            when 1 | 4 =>
                                c_in := '0' when mc.alu_op = 1 else af(4);
                                addsub9 := get_sum_9bit(a8, src8, c_in);

                                wb_en := '1';
                                wb_dest := 7;
                                wb_data := addsub9(7 downto 0);

                                af(7) <= '1' when addsub9(7 downto 0) = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= get_hc_bit_sum(a8(3 downto 0), src8(3 downto 0), c_in);
                                af(4) <= addsub9(8);

                            when 2 | 5 | 6 =>
                                c_in := af(4) when mc.alu_op = 5 else '0';
                                addsub9 := get_sub_9bit(a8, src8, c_in);

                                if mc.alu_op /= 6 then
                                    wb_en := '1';
                                    wb_dest := 7;
                                    wb_data := addsub9(7 downto 0);
                                end if;

                                af(7) <= '1' when addsub9(7 downto 0) = x"00" else '0';
                                af(6) <= '1';
                                af(5) <= get_hc_bit_sub(a8(3 downto 0), src8(3 downto 0), c_in);
                                af(4) <= addsub9(8);

                            when 3 =>
                                hl <= sp + unsigned(resize(signed(temp_wz(7 downto 0)), 16));
                                af(7) <= '0';
                                af(6) <= '0';
                                af(5) <= get_hc_bit_sum(sp(3 downto 0), unsigned(temp_wz(3 downto 0)), '0');
                                af(4) <= get_sum_9bit(sp(7 downto 0), unsigned(temp_wz(7 downto 0)), '0')(8);

                            when 7 | 8 =>
                            wb_en := '1';
                                wb_dest := mc.reg_dest;

                                if mc.alu_op = 7 then
                                    wb_data := src8 + 1;
                                    af(7) <= '1' when wb_data = x"00" else '0';
                                    af(6) <= '0';
                                    af(5) <= '1' when (("0" & src8(3 downto 0)) + 1 > 15) else '0';
                                else
                                    wb_data := src8 - 1;
                                    af(7) <= '1' when wb_data = x"00" else '0';
                                    af(6) <= '1';
                                    af(5) <= '1' when src8(3 downto 0) = x"0" else '0';
                                end if;

                            when 9 to 11 =>
                            case mc.alu_op is
                                    when 9 =>
                                        op_res := a8 and src8;
                                        af(5) <= '1';
                                    when 10 =>
                                        op_res := a8 or src8;
                                        af(5) <= '0';
                                    when 11 =>
                                        op_res := a8 xor src8;
                                        af(5) <= '0';
                                    when others =>
                                        op_res := a8;
                                end case;

                                wb_en := '1';
                                wb_dest := 7;
                                wb_data := op_res;

                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(4) <= '0';
                            
                            when 12 =>
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= not af(4);

                            when 13 =>
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= '1';
                            
                            when 14 =>
                                adjust := (others => '0');

                                if af(6) = '0' then
                                    if af(5) = '1' or a8(3 downto 0) > 9 then
                                        adjust := adjust or x"06";
                                    end if;
                                    if af(4) = '1' or a8 > x"99" then
                                        adjust := adjust or x"60";
                                        af(4) <= '1';
                                    end if;
                                    op_res := a8 + adjust;
                                else
                                    if af(5) = '1' then adjust := adjust or x"06"; end if;
                                    if af(4) = '1' then adjust := adjust or x"60"; end if;
                                    op_res := a8 - adjust;
                                end if;

                                wb_en := '1';
                                wb_dest := 7;
                                wb_data := op_res;

                                af(7) <= '1' when op_res = x"00" else '0';
                                af(5) <= '0';

                            when 15 =>
                                wb_en := '1';
                                wb_dest := 7;
                                wb_data := not a8;

                                af(6) <= '1';
                                af(5) <= '1';
                            
                            when 16 => 
                                res17 := ('0' & hl) + ('0' & internal_bus_16);
                                hl <= res17(15 downto 0);
                                af(6) <= '0';
                                af(5) <= '1' when (('0' & hl(11 downto 0)) + ('0' & internal_bus_16(11 downto 0)) > 4095) else '0';
                                af(4) <= res17(16);

                            when 17 =>
                                sp_low_buffer <= sp(7 downto 0) + src8;
                                af(7) <= '0';
                                af(6) <= '0';
                                af(5) <= '1' when (("0" & sp(3 downto 0)) + ("0" & src8(3 downto 0)) > 15) else '0';
                                af(4) <= '1' when (("0" & sp(7 downto 0)) + ("0" & src8) > 255) else '0';

                            when 18 => 
                                if src8(7) = '0' then
                                    sp <= sp(15 downto 8) + x"00" + ("0000000" & af(4)) & sp_low_buffer;
                                else
                                    sp <= sp(15 downto 8) + x"FF" + ("0000000" & af(4)) & sp_low_buffer;
                                end if;
                                
                            when 19 =>
                                op_res := af(14 downto 8) & af(15);
                                wb_en := '1';
                                wb_dest := 7;
                                wb_data := op_res;
                                af(4) <= af(15);
                                af(7) <= '0';
                                af(6) <= '0';
                                af(5) <= '0';
                            
                            when 20 =>
                                op_res := unsigned(af(8) & af(15 downto 9));
                                wb_en := '1';
                                wb_dest := 7;
                                wb_data := op_res;
                                af(4) <= af(8);
                                af(7) <= '0';
                                af(6) <= '0';
                                af(5) <= '0';

                            when 21 =>
                                op_res := unsigned(af(14 downto 8) & af(4));
                                wb_en := '1';
                                wb_dest := 7;
                                wb_data := op_res;
                                af(4) <= af(15);
                                af(7) <= '0';
                                af(6) <= '0';
                                af(5) <= '0';
                            
                            when 22 =>
                                op_res := unsigned(af(4) & af(15 downto 9));
                                wb_en := '1';
                                wb_dest := 7;
                                wb_data := op_res;
                                af(4) <= af(8);
                                af(7) <= '0';
                                af(6) <= '0';
                                af(5) <= '0';

                            when 23 =>
                            op_res := unsigned(internal_bus(6 downto 0) & internal_bus(7));
                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;
                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= internal_bus(7);

                            when 24 =>
                            op_res := unsigned(internal_bus(0) & internal_bus(7 downto 1));
                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;
                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= internal_bus(0);

                            when 25 =>
                                op_res := unsigned(internal_bus(6 downto 0) & af(4));
                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;
                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= internal_bus(7);
                            
                            when 26 =>
                                op_res := unsigned(af(4) & internal_bus(7 downto 1));
                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;
                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= internal_bus(0);
                            
                            when 27 =>
                                op_res := unsigned(internal_bus(6 downto 0) & '0');
                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;
                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= internal_bus(7);
                            
                            when 28 =>
                                op_res := unsigned(internal_bus(7) & internal_bus(7 downto 1));
                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;
                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= internal_bus(0);
                            
                            when 29 =>
                                op_res := unsigned(internal_bus(3 downto 0) & internal_bus(7 downto 4));
                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;
                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= '0';
                            
                            when 30 =>
                                op_res := unsigned('0' & internal_bus(7 downto 1));
                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;
                                af(7) <= '1' when op_res = x"00" else '0';
                                af(6) <= '0';
                                af(5) <= '0';
                                af(4) <= internal_bus(0);
                            
                            when 31 =>
                                ir_u := to_unsigned(current_ir, 8);
                                bit_idx := to_integer(ir_u(5 downto 3));
                                af(7) <= '1' when internal_bus(bit_idx) = '0' else '0';
                                af(6) <= '0';
                                af(5) <= '1';
                            
                            when 32 | 33 =>
                                ir_u := to_unsigned(current_ir, 8);
                                bit_idx := to_integer(ir_u(5 downto 3));
                                op_res := src8;

                                if mc.alu_op = 32 then
                                    op_res(bit_idx) := '0';
                                else
                                    op_res(bit_idx) := '1';
                                end if;

                                wb_en := '1';
                                wb_dest := mc.reg_dest;
                                wb_data := op_res;

                            when 34 =>
                                ir_u := to_unsigned(current_ir, 8);
                                case to_integer(ir_u(4 downto 3)) is
                                    when 0 => cc_true := '1' when af(7) = '0' else '0';
                                    when 1 => cc_true := '1' when af(7) = '1' else '0';
                                    when 2 => cc_true := '1' when af(4) = '0' else '0';
                                    when 3 => cc_true := '1' when af(4) = '1' else '0';
                                    when others => cc_true := '0';
                                end case;
                                                        
                            when 35 =>
                                if temp_wz(7) = '1' then 
                                    adjust_16 := x"FF" & temp_wz(7 downto 0);
                                else 
                                    adjust_16 := x"00" & temp_wz(7 downto 0);
                                end if;
                                pc <= pc + adjust_16;
                            
                            when others => null;
                        end case;

                        if wb_en = '1' then
                            case wb_dest is
                                when 0 => bc(15 downto 8) <= wb_data;
                                when 1 => bc(7 downto 0)  <= wb_data;
                                when 2 => de(15 downto 8) <= wb_data;
                                when 3 => de(7 downto 0)  <= wb_data;
                                when 4 => hl(15 downto 8) <= wb_data;
                                when 5 => hl(7 downto 0)  <= wb_data;
                                when 7 => af(15 downto 8) <= wb_data;
                                when 9 => mem_data_out    <= std_logic_vector(wb_data);
                                when others => null;
                            end case;
                        end if;

                        t_cycle <= 4;

                    when 4 =>
                        if mc.is_done = '1' then
                            m_cycle <= 1;
                        elsif mc.alu_op = 34 and cc_true = '0' then
                            m_cycle <= 1;
                        
                        else
                            m_cycle <= m_cycle + 1;
                        end if;
                        t_cycle <= 1;

                    when others =>
                        t_cycle <= 1;
                end case;

            end if;
        end if;
    end process;

    -- 6. Memory Signals
    mem_rd <= mc.mem_read;
    mem_wr <= mc.mem_write;

end rtl;
