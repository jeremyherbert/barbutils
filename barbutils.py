# SPDX-License-Identifier: MIT

import struct
import numpy as np

from typing import Union


def compute_barb_checksum(header: bytes) -> bytes:
    tmp = sum(struct.unpack("b" * 56, header[:56]))
    return struct.pack("<i", tmp)


def load_barb(payload: bytes):
    if len(payload) < 61:
        raise ValueError("payload is too short")

    header = payload[:56]
    checksum = payload[56:60]
    waveform_data = payload[60:]

    if compute_barb_checksum(header) != checksum:
        raise ValueError("incorrect checksum")

    sample_rate = struct.unpack("<d", header[0x08:0x08+8])[0]
    maximum_voltage = struct.unpack("<f", header[0x14:0x14+4])[0]
    minimum_voltage = struct.unpack("<f", header[0x18:0x18+4])[0]

    scale_voltage = np.max([np.abs(maximum_voltage), np.abs(minimum_voltage)])

    normalised_waveform_data = scale_voltage * np.array([x[0] for x in struct.iter_unpack("<h", waveform_data)]) / 2**15

    return sample_rate, normalised_waveform_data


def generate_barb(data: Union[np.array, list], sample_rate: float) -> bytes:
    if sample_rate < 10 or sample_rate > 1e9:
        raise ValueError("sample_rate must be between 10Hz and 1GHz")

    if np.max(data) > 10 or np.min(data) < -10:
        raise ValueError("all elements of data must be between -10 and 10")

    if len(data) == 0:
        raise ValueError("data is empty")

    header = b"\x01\x00\x00\x00"
    header += b"\x04\x00\x00\x00"
    header += struct.pack("<d", sample_rate)
    header += b"\xCD\xCC\x8C\x3F"
    header += struct.pack("<ff", np.max(data), np.min(data))
    header += b"\x00\x00\x00\x00"
    header += b"\x16\x00\x00\x00"
    header += b"\x00\x00\x00\x00"
    header += b"\x00\x00\x00\x00"
    header += b"\x00\x00\x00\x00"
    header += struct.pack("<I", len(data))
    header += b"\x00\x00\x00\x00"
    header += compute_barb_checksum(header)

    tmp_data = np.array(data, dtype=np.float64)
    tmp_data /= np.max(np.abs(tmp_data)*2)
    normalised_data = tmp_data
    scaled_data = np.array(normalised_data * (2**16 - 1), dtype=np.int16)

    payload = b""
    for i in scaled_data:
        payload += struct.pack("<h", i)

    return header + payload