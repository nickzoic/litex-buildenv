from migen import *

from litex.soc.interconnect.csr import *


class PWM(Module, AutoCSR):
    def __init__(self, pwm, width=32):
        self._enable = CSRStorage()
        self._width = CSRStorage(width)
        self._period = CSRStorage(width)

        # # #

        cnt = Signal(width)

        enable = self._enable.storage
        width = self._width.storage
        period = self._period.storage

        self.sync += \
            If(enable,
                If(cnt < width,
                    pwm.eq(1)
                ).Else(
                    pwm.eq(0)
                ),
                If(cnt == period-1,
                    cnt.eq(0)
                ).Else(
                    cnt.eq(cnt+1)
                )
            ).Else(
                cnt.eq(0),
                pwm.eq(0)
            )


class MiniPWM(Module, AutoCSR):
    def __init__(self, pwm, width):
        self._duty = CSRStorage(width)

        cnt = Signal(width)
        duty = self._duty.storage

        self.sync += If(cnt < duty, pwm.eq(1)).Else(pwm.eq(0)), cnt.eq(cnt+1)

