# Pattern lock

## Problem

In android smartphone, you can use "pattern lock".

Pattern lock use 9 dots(3x3) on the screen in the figure below.

![](./image1.png?raw=true)

The following figures are examples of lock pattern.

![](./image2.png?raw=true) ![](./image3.png?raw=true)

Lock pattern must satisfy following three conditions.

- Use at most once each dot.
- Use at least 4 dots.
- Cannot skip the dot on the segment.

Flag is the number of lock patterns in decimal without MMA{...}.

## Solution

Credit: [@ecapuano](https://github.com/ecapuano)

It's a warmup challenge that's easily googleable, so you can just find the answer:
https://github.com/delight-im/AndroidPatternLock
http://stackoverflow.com/questions/12127833/patterns-possible-on-3x3-matrix-of-numbers

However, if you're curious about the math behind this, there's a good explanation with Python code in Quora:
https://www.quora.com/How-many-combinations-does-Android-9-point-unlock-have/answer/Yoyo-Zhou

The flag is `389112`.
