# barbutils

BARB files are binary arbitrary waveform files used by Agilent/Keysight waveform generators (also known as "function generators"). Files generated with this python script have been tested on a 33600-series generator. Script requires python 3.6+ and numpy.

Warning: You likely can generate files which will be outside of the usable range of your device (for example, a sample rate too high). Use at your own risk.

---

### File structure

All multi-byte numbers are little-endian (LSB first).

Offset | Length (bytes) | Type | Description
--- | --- | --- | ---
0x00 | 8 | ? | 01 00 00 00 <br> 04 00 00 00
0x08 | 8 | IEEE754 double precision float | Sample rate in samples/sec
0x10 | 4 | ? | CD CC 8C 3F
0x14 | 4 | IEEE754 single precision float | Maximum voltage
0x18 | 4 | IEEE754 single precision float | Minimum voltage
0x1C | 24 | ? | 00 00 00 00 <br> 16 00 00 00 <br> 00 00 00 00 <br> 00 00 00 00 <br> 00 00 00 00
0x30 | 4 | uint32 | Number of points in the waveform
0x34 | 4 | ? | 00 00 00 00
0x38 | 4 | int32 | For each byte in the first 56 bytes of the header, convert it to int8_t, then convert to int32_t, then add them all together 
0x3C | Number of waveform points * 2 | Array of int16 | Waveform points. All points are scaled relative to max(abs(maximum voltage), abs(minimum voltage))
