import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer, ClockCycles
import math

sample_width = 24
test_factor = 1
samples_ch1 = [[0x0, 0x0], [0x101010, 0x020202],[0xfffeff, 0xbecafe], [0x123456, 0xdeadbe], [0xf0f0f0, 0xf1f1f1], [0xfeefbe, 0xcafeca]]
samples_ch2 = [[0x0, 0x0], [0x030303, 0x404040],[0xfffeff, 0xbecafe], [0x123456, 0xdeadbe], [0xf0f0f0, 0xf1f1f1], [0xfeefbe, 0xcafeca]]
for gen in range(100*test_factor):
    sin_val = [round((math.sin(gen/(10*test_factor))+1)*0xffffff/2),round((math.sin(gen/(10*test_factor))+1)*0xffffff/2)]
    samples_ch1.append(sin_val)
    cos_val = [round((math.cos(gen/(10*test_factor))+1)*0xffffff/2),round((math.cos(gen/(10*test_factor))+1)*0xffffff/2)]
    samples_ch2.append(cos_val)
LEFT = 0
RIGHT = 1

#Theres a lot of boiler plate, dont judge me too much, its Sunday evening...

@cocotb.test()
async def test_i2s_add(dut):
    dut._log.debug("start")
    clock = Clock(dut.sck, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.debug("init")
    dut.ws.value = 1
    dut.sd_ch1.value = 0
    dut.sd_ch2.value = 0
    dut._log.debug("reset")
    dut.rst.value = 1
    dut.channel_sel.value = 3
    await ClockCycles(dut.sck, 5, rising=False)
    dut.rst.value = 0
    await ClockCycles(dut.sck, 5, rising=False)

    for sample_id in range(len(samples_ch1)):
        dut._log.debug("Shift data in with ws indicating new sample")
        dut._log.debug("ch1 left: {:X}".format(samples_ch1[sample_id][LEFT]))
        dut._log.debug("ch1 right {:X}".format(samples_ch1[sample_id][RIGHT]))
        dut._log.debug("ch2 left: {:X}".format(samples_ch2[sample_id][LEFT]))
        dut._log.debug("ch2 right {:X}".format(samples_ch2[sample_id][RIGHT]))

        dut.ws.value = LEFT
        dut.sd_ch1.value = (samples_ch1[sample_id][LEFT] >> 24) & 1
        dut.sd_ch2.value = (samples_ch2[sample_id][LEFT] >> 24) & 1
        await ClockCycles(dut.sck, 1, rising=False)
        out_val = 0
        for i in range(sample_width):
            dut.sd_ch1.value = (samples_ch1[sample_id][LEFT] >> (23-i)) & 1
            dut.sd_ch2.value = (samples_ch2[sample_id][LEFT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 1:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
            if i == sample_width-1:
                dut.ws.value = RIGHT
        await ClockCycles(dut.sck, 1, rising=False)
        
        if sample_id > 1:
            dut._log.debug("sd_out reconstructed left: {:X}".format(out_val))
            added_value = (samples_ch1[sample_id-1][LEFT] + samples_ch2[sample_id-1][LEFT]) >> 1;
            assert hex(added_value) == hex(out_val) 

        dut.sd_ch1.value = (samples_ch1[sample_id][RIGHT] >> 24) & 1
        dut.sd_ch2.value = (samples_ch2[sample_id][RIGHT] >> 24) & 1
        out_val = 0
        for i in range(sample_width):
            dut.sd_ch1.value = (samples_ch1[sample_id][RIGHT] >> (23-i)) & 1
            dut.sd_ch2.value = (samples_ch2[sample_id][RIGHT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 0:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
        await ClockCycles(dut.sck, 10, rising=False)
        
        if sample_id > 1:
            dut._log.debug("sd_out reconstructed right: {:X}".format(out_val))
            added_value = (samples_ch1[sample_id-1][RIGHT] + samples_ch2[sample_id-1][RIGHT]) >> 1;
            assert hex(added_value) == hex(out_val) 

        ref_xor_left = 0; 

@cocotb.test()
async def test_i2s_only_channel1(dut):
    dut._log.debug("start")
    clock = Clock(dut.sck, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.debug("init")
    dut.ws.value = 1
    dut.sd_ch1.value = 0
    dut.sd_ch2.value = 0
    dut._log.debug("reset")
    dut.rst.value = 1
    dut.channel_sel.value = 1
    await ClockCycles(dut.sck, 5, rising=False)
    dut.rst.value = 0
    await ClockCycles(dut.sck, 5, rising=False)

    for sample_id in range(len(samples_ch1)):
        dut._log.debug("Shift data in with ws indicating new sample")
        dut._log.debug("ch1 left: {:X}".format(samples_ch1[sample_id][LEFT]))
        dut._log.debug("ch1 right {:X}".format(samples_ch1[sample_id][RIGHT]))
        dut._log.debug("ch2 left: {:X}".format(samples_ch2[sample_id][LEFT]))
        dut._log.debug("ch2 right {:X}".format(samples_ch2[sample_id][RIGHT]))

        dut.ws.value = LEFT
        dut.sd_ch1.value = (samples_ch1[sample_id][LEFT] >> 24) & 1
        dut.sd_ch2.value = (samples_ch2[sample_id][LEFT] >> 24) & 1
        await ClockCycles(dut.sck, 1, rising=False)
        out_val = 0
        for i in range(sample_width):
            dut.sd_ch1.value = (samples_ch1[sample_id][LEFT] >> (23-i)) & 1
            dut.sd_ch2.value = (samples_ch2[sample_id][LEFT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 1:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
            if i == sample_width-1:
                dut.ws.value = RIGHT
        await ClockCycles(dut.sck, 1, rising=False)
        
        if sample_id > 1:
            dut._log.debug("sd_out reconstructed left: {:X}".format(out_val))
            added_value = (samples_ch1[sample_id-1][LEFT]) >> 1;
            assert hex(added_value) == hex(out_val) 

        dut.sd_ch1.value = (samples_ch1[sample_id][RIGHT] >> 24) & 1
        dut.sd_ch2.value = (samples_ch2[sample_id][RIGHT] >> 24) & 1
        out_val = 0
        for i in range(sample_width):
            dut.sd_ch1.value = (samples_ch1[sample_id][RIGHT] >> (23-i)) & 1
            dut.sd_ch2.value = (samples_ch2[sample_id][RIGHT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 0:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
        await ClockCycles(dut.sck, 10, rising=False)
        
        if sample_id > 1:
            dut._log.debug("sd_out reconstructed right: {:X}".format(out_val))
            added_value = (samples_ch1[sample_id-1][RIGHT]) >> 1;
            assert hex(added_value) == hex(out_val) 

@cocotb.test()
async def test_i2s_only_channel2(dut):
    dut._log.debug("start")
    clock = Clock(dut.sck, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.debug("init")
    dut.ws.value = 1
    dut.sd_ch1.value = 0
    dut.sd_ch2.value = 0
    dut._log.debug("reset")
    dut.rst.value = 1
    dut.channel_sel.value = 2
    await ClockCycles(dut.sck, 5, rising=False)
    dut.rst.value = 0
    await ClockCycles(dut.sck, 5, rising=False)

    for sample_id in range(len(samples_ch1)):
        dut._log.debug("Shift data in with ws indicating new sample")
        dut._log.debug("ch1 left: {:X}".format(samples_ch1[sample_id][LEFT]))
        dut._log.debug("ch1 right {:X}".format(samples_ch1[sample_id][RIGHT]))
        dut._log.debug("ch2 left: {:X}".format(samples_ch2[sample_id][LEFT]))
        dut._log.debug("ch2 right {:X}".format(samples_ch2[sample_id][RIGHT]))

        dut.ws.value = LEFT
        dut.sd_ch1.value = (samples_ch1[sample_id][LEFT] >> 24) & 1
        dut.sd_ch2.value = (samples_ch2[sample_id][LEFT] >> 24) & 1
        await ClockCycles(dut.sck, 1, rising=False)
        out_val = 0
        for i in range(sample_width):
            dut.sd_ch1.value = (samples_ch1[sample_id][LEFT] >> (23-i)) & 1
            dut.sd_ch2.value = (samples_ch2[sample_id][LEFT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 1:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
            if i == sample_width-1:
                dut.ws.value = RIGHT
        await ClockCycles(dut.sck, 1, rising=False)
        
        if sample_id > 1:
            dut._log.debug("sd_out reconstructed left: {:X}".format(out_val))
            added_value = (samples_ch2[sample_id-1][LEFT]) >> 1;
            assert hex(added_value) == hex(out_val) 

        dut.sd_ch1.value = (samples_ch1[sample_id][RIGHT] >> 24) & 1
        dut.sd_ch2.value = (samples_ch2[sample_id][RIGHT] >> 24) & 1
        out_val = 0
        for i in range(sample_width):
            dut.sd_ch1.value = (samples_ch1[sample_id][RIGHT] >> (23-i)) & 1
            dut.sd_ch2.value = (samples_ch2[sample_id][RIGHT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 0:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
        await ClockCycles(dut.sck, 10, rising=False)
        
        if sample_id > 1:
            dut._log.debug("sd_out reconstructed right: {:X}".format(out_val))
            added_value = (samples_ch2[sample_id-1][RIGHT]) >> 1;
            assert hex(added_value) == hex(out_val) 

@cocotb.test()
async def test_i2s_mute(dut):
    dut._log.debug("start")
    clock = Clock(dut.sck, 10, units="us")
    cocotb.start_soon(clock.start())

    dut._log.debug("init")
    dut.ws.value = 1
    dut.sd_ch1.value = 0
    dut.sd_ch2.value = 0
    dut._log.debug("reset")
    dut.rst.value = 1
    dut.channel_sel.value = 0
    await ClockCycles(dut.sck, 5, rising=False)
    dut.rst.value = 0
    await ClockCycles(dut.sck, 5, rising=False)

    for sample_id in range(len(samples_ch1)):
        dut._log.debug("Shift data in with ws indicating new sample")
        dut._log.debug("ch1 left: {:X}".format(samples_ch1[sample_id][LEFT]))
        dut._log.debug("ch1 right {:X}".format(samples_ch1[sample_id][RIGHT]))
        dut._log.debug("ch2 left: {:X}".format(samples_ch2[sample_id][LEFT]))
        dut._log.debug("ch2 right {:X}".format(samples_ch2[sample_id][RIGHT]))

        dut.ws.value = LEFT
        dut.sd_ch1.value = (samples_ch1[sample_id][LEFT] >> 24) & 1
        dut.sd_ch2.value = (samples_ch2[sample_id][LEFT] >> 24) & 1
        await ClockCycles(dut.sck, 1, rising=False)
        out_val = 0
        for i in range(sample_width):
            dut.sd_ch1.value = (samples_ch1[sample_id][LEFT] >> (23-i)) & 1
            dut.sd_ch2.value = (samples_ch2[sample_id][LEFT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 1:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
            if i == sample_width-1:
                dut.ws.value = RIGHT
        await ClockCycles(dut.sck, 1, rising=False)
        
        if sample_id > 1:
            dut._log.debug("sd_out reconstructed left: {:X}".format(out_val))
            added_value = 0;
            assert hex(added_value) == hex(out_val) 

        dut.sd_ch1.value = (samples_ch1[sample_id][RIGHT] >> 24) & 1
        dut.sd_ch2.value = (samples_ch2[sample_id][RIGHT] >> 24) & 1
        out_val = 0
        for i in range(sample_width):
            dut.sd_ch1.value = (samples_ch1[sample_id][RIGHT] >> (23-i)) & 1
            dut.sd_ch2.value = (samples_ch2[sample_id][RIGHT] >> (23-i)) & 1
            await ClockCycles(dut.sck, 1, rising=False)
            if sample_id > 0:
                out_val = out_val | dut.sd_out.value << sample_width-1-i
        await ClockCycles(dut.sck, 10, rising=False)
        
        if sample_id > 1:
            dut._log.debug("sd_out reconstructed right: {:X}".format(out_val))
            added_value = 0;
            assert hex(added_value) == hex(out_val) 
