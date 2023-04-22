import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles

reg_width = 96
overhead_runs = 5

sample_width = 24
input_samples = [0xfffeff, 0xbecafe]


@cocotb.test()
async def test_shift_reg_perm_one(dut):
    dut._log.info("start")
    clock = Clock(dut.sck, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("init")
    dut.ws.value = 0
    dut.sd.value = 0
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.sck, 5)
    dut.rst.value = 0
    await ClockCycles(dut.sck, 5)

    dut._log.info("Put some data in and change word line")
    dut._log.info("{:X}".format(input_samples[0]))
    
    await ClockCycles(dut.sck, 1)
    dut.ws.value = 1
    value_out = 0x0
    dut.sd.value = (input_samples[0] >> 24) & 1
    await ClockCycles(dut.sck, 1)
    for i in range(sample_width):
        dut.sd.value = (input_samples[0] >> (23-i)) & 1
        await ClockCycles(dut.sck, 1)
        dut._log.info("i:{}, xor_data_left: 0b{}, xor_data_right: 0b{}".format(i, dut.xor_data_left.value, dut.xor_data_right.value))
        #value_out = (dut.sd.value << i) | value_out
        if i == sample_width-1:
            dut.ws.value = 0
    await ClockCycles(dut.sck, 1)
    dut.sd.value = (input_samples[1] >> 24) & 1
    for i in range(sample_width):
        dut.sd.value = (input_samples[1] >> (23-i)) & 1
        await ClockCycles(dut.sck, 1)
        dut._log.info("i:{}, xor_data_left: 0b{}, xor_data_right: 0b{}".format(i, dut.xor_data_left.value, dut.xor_data_right.value))
        #value_out = (dut.sd.value << i) | value_out
        if i == sample_width-1:
            dut.ws.value = 1
    await ClockCycles(dut.sck, 10)
    #assert hex(ref_val) == hex(value_out)
