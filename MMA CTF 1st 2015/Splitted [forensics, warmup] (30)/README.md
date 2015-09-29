# Splitted

## Problem

[splitted.7z](splitted.7z)

## Solution

Credit: [@PeterMosmans](https://github.com/PeterMosmans)

You're given a .pcap file, which contains several HTTP partial downloads.

Analyzing the range, you can see the partials are out of order:

Stream 1 requests bytes 2345-2813.
Stream 2 requests bytes 0-468.
Stream 3 requests bytes 1407-1875.
Stream 4 requests bytes 2814-3282.
Stream 5 requests bytes 3283-3744.
Stream 6 requests bytes 469-937.
Stream 7 requests bytes 938-1406.
Stream 8 requests bytes 1876-2344.

Reassemble the stream, get a .PSD file. The flag is there.

@PeterMosmans wrote a reassembling script: [extract_file.py](extract_file.py).

And the flag is `MMA{sneak_spy_sisters}`.
