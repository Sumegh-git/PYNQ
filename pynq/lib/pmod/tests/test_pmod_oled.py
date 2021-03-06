#   Copyright (c) 2016, Xilinx, Inc.
#   All rights reserved.
# 
#   Redistribution and use in source and binary forms, with or without 
#   modification, are permitted provided that the following conditions are met:
#
#   1.  Redistributions of source code must retain the above copyright notice, 
#       this list of conditions and the following disclaimer.
#
#   2.  Redistributions in binary form must reproduce the above copyright 
#       notice, this list of conditions and the following disclaimer in the 
#       documentation and/or other materials provided with the distribution.
#
#   3.  Neither the name of the copyright holder nor the names of its 
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
#   AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, 
#   THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR 
#   PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR 
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, 
#   PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#   OR BUSINESS INTERRUPTION). HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
#   WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR 
#   OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


import pytest
from pynq import Overlay
from pynq.lib.pmod import Pmod_OLED
from pynq.lib.pmod import PMODA
from pynq.lib.pmod import PMODB
from pynq.tests.util import user_answer_yes
from pynq.tests.util import get_interface_id


__author__ = "Giuseppe Natale, Yun Rock Qu"
__copyright__ = "Copyright 2016, Xilinx"
__email__ = "pynq_support@xilinx.com"


try:
    _ = Overlay('base.bit', download=False)
    flag0 = True
except IOError:
    flag0 = False
flag1 = user_answer_yes("\nPmod OLED attached to the board?")
if flag1:
    oled_id = eval(get_interface_id('Pmod OLED', options=['PMODA', 'PMODB']))
flag = flag0 and flag1


@pytest.mark.skipif(not flag, 
                    reason="need OLED attached to the base overlay")
def test_write_string():
    """Test for the OLED Pmod.
    
    Writes on the OLED the string 'Welcome to PYNQ.' and asks the user to 
    confirm if it is shown on the OLED. After that, it clears the screen. 
    This test can be skipped.
    
    """
    Overlay('base.bit').download()
    oled = Pmod_OLED(oled_id)

    oled.draw_line(0, 0, 255, 0)
    oled.draw_line(0, 2, 255, 2)
    oled.write('Welcome to PYNQ.', 0, 1)
    oled.draw_line(0, 20, 255, 20)
    oled.draw_line(0, 22, 255, 22)

    assert user_answer_yes("\nWelcome message shown on the OLED?")
    oled.clear()
    assert user_answer_yes("OLED screen clear now?")

    del oled
