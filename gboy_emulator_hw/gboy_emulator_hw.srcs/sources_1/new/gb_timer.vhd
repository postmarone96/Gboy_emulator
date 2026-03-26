library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity gb_timer is
    Port(
        clk         : in std_logic;
        rst         : in std_logic;
        addr_bus    : in  std_logic_vector(15 downto 0);

        data_in     : in  std_logic_vector(7 downto 0);
        data_out     : out std_logic_vector(7 downto 0);

        rd_from_timer      : in  std_logic;
        wr_to_timer      : in  std_logic;

        timer_irq   : out std_logic
    );
end gb_timer;

architecture rtl of gb_timer is
    signal t_cycle      : unsigned(1 downto 0);
    signal div_counter  : unsigned(15 downto 0) := (others => '0');
    signal tima         : unsigned(7 downto 0)  := (others => '0');
    signal tma          : unsigned(7 downto 0)  := (others => '0');
    signal tac          : unsigned(7 downto 0)  := (others => '0');

    signal irq_pulse    : std_logic := '0';
    signal timer_bit    : std_logic;
    signal prev_bit     : std_logic := '0';
begin
    timer_irq <= irq_pulse;

    process (all)
    begin
        data_out <= (others => '0');

        if rd_from_timer = '1' then
            case addr_bus is
                when x"FF04" => data_out <= std_logic_vector(div_counter(15 downto 8)); -- DIV
                when x"FF05" => data_out <= std_logic_vector(tima);                      -- TIMA
                when x"FF06" => data_out <= std_logic_vector(tma);                       -- TMA
                when x"FF07" => data_out <= "11111" & std_logic_vector(tac(2 downto 0)); -- TAC
                when others  => null;
            end case;
        end if;
    end process;

    with tac(1 downto 0) select timer_bit <=
        div_counter(9)  when "00", -- 4096 Hz
        div_counter(3)  when "01", -- 262144 Hz
        div_counter(5)  when "10", -- 65536 Hz
        div_counter(7)  when others; -- 16384 Hz

    process(clk, rst)
    begin
        if rst then
            t_cycle     <= (others => '0');
            div_counter <= (others => '0');
            tima        <= (others => '0');
            tma         <= (others => '0');
            tac         <= (others => '0');
            prev_bit    <= '0';
            irq_pulse   <= '0';

        elsif rising_edge(clk) then
            irq_pulse <= '0';
            t_cycle <= t_cycle + 1;
            if t_cycle = "11" then 
                div_counter <= div_counter + 1;
            end if;

            if wr_to_timer = '1' then
                case addr_bus is
                    when x"FF04" => div_counter <= (others => '0'); -- DIV reset on write
                    when x"FF05" => tima <= unsigned(data_in);
                    when x"FF06" => tma  <= unsigned(data_in);
                    when x"FF07" => tac(2 downto 0) <= unsigned(data_in(2 downto 0));
                    when others  => null;
                end case;
            end if;

            if tac(2) = '1' then
                if prev_bit = '1' and timer_bit = '0' then
                    if tima = x"FF" then
                        tima <= tma;
                        irq_pulse <= '1';
                    else
                        tima <= tima + 1;
                    end if;
                end if;
            end if;

            prev_bit <= timer_bit;
        end if;
    end process;
end architecture;