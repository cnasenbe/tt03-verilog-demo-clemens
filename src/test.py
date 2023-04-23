import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
import math

sample_width = 24
samples_c1 = [[0x0, 0x0], [0x101010, 0x020202],[0xfffeff, 0xbecafe], [0x123456, 0xdeadbe], [0xf0f0f0, 0xf1f1f1], [0xfeefbe, 0xcafeca]]
samples_c2 = [[0x0, 0x0], [0x030303, 0x404040],[0xfffeff, 0xbecafe], [0x123456, 0xdeadbe], [0xf0f0f0, 0xf1f1f1], [0xfeefbe, 0xcafeca]]
for gen in range(100):
    sine_val = [round((math.sin(gen/10)+1)*0xffffff/2),round((math.sin(gen/10)+1)*0xffffff/2)]
    samples_c1.append(sine_val)
    samples_c2.append(sine_val)
LEFT = 0
RIGHT = 1

@cocotb.test()
async def test_i2s(dut):
    dut._log.info("start")
    clock = Clock(dut.sck, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.info("init")
    dut.ws.value = 1
    dut.sd_c1.value = 0
    dut.sd_c2.value = 0
    dut._log.info("reset")
    dut.rst.value = 1
    await ClockCycles(dut.sck, 5, rising=False)
    dut.rst.value = 0
    await ClockCycles(dut.sck, 5, rising=False)

    for sample_id in range(len(samples_c1)):
        dut._log.info("Shift data in with ws indicating new sample")
        dut._log.info("c1 left: {:X}".format(samples_c1[sample_id][LEFT]))
        dut._log.info("c1 right {:X}".format(samples_c1[sample_id][RIGHT]))
        dut._log.info("c2 left: {:X}".format(samples_c2[sample_id][LEFT]))
        dut._log.info("c2 right {:X}".format(samples_c2[sample_id][RIGHT]))

        dut.ws.value = LEFT
        dut.sd_c1.value = (samples_c1[sample_id][LEFT] >> 24) & 1
        dut.sd_c2.value = (samples_c2[sample_id][LEFT] >> 24) & 1
        await ClockCycles(dut.sck, 1, rising=False)
        out_val = 0
        for i in range(sample_width):
            dut.sd_c1.value = (samples_c1[sample_id][LEFT] >> (23-i)) & 1
            dut.sd_c2.value = (samples_c2[sample_id][LEFT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 1:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
            if i == sample_width-1:
                dut.ws.value = RIGHT
        await ClockCycles(dut.sck, 1, rising=False)
        
        if sample_id > 1:
            dut._log.info("sd_out reconstructed left: {:X}".format(out_val))
            added_value = (samples_c1[sample_id-1][LEFT] + samples_c2[sample_id-1][LEFT]) >> 1;
            assert hex(added_value) == hex(out_val) 

        #Can only check last sample once new sample has been started
        if sample_id > 0:
            ref_xor_right = 0; 
            for k in range(sample_width):
                ref_xor_right = ref_xor_right ^ ((samples_c1[sample_id-1][RIGHT] >> k) & 1)
            assert ref_xor_right == dut.xor_data_right.value
        
        dut.sd_c1.value = (samples_c1[sample_id][RIGHT] >> 24) & 1
        dut.sd_c2.value = (samples_c2[sample_id][RIGHT] >> 24) & 1
        out_val = 0
        for i in range(sample_width):
            dut.sd_c1.value = (samples_c1[sample_id][RIGHT] >> (23-i)) & 1
            dut.sd_c2.value = (samples_c2[sample_id][RIGHT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 0:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
        await ClockCycles(dut.sck, 10, rising=False)
        
        if sample_id > 1:
            dut._log.info("sd_out reconstructed right: {:X}".format(out_val))
            added_value = (samples_c1[sample_id-1][RIGHT] + samples_c2[sample_id-1][RIGHT]) >> 1;
            assert hex(added_value) == hex(out_val) 

        ref_xor_left = 0; 
        for k in range(sample_width):
            ref_xor_left = ref_xor_left ^ ((samples_c1[sample_id][LEFT] >> k) & 1)
        assert ref_xor_left == dut.xor_data_left.value
