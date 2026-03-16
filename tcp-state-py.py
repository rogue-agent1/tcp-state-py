#!/usr/bin/env python3
"""TCP state machine simulation."""
import sys

TRANSITIONS={
    ('CLOSED','active_open'):'SYN_SENT',
    ('CLOSED','passive_open'):'LISTEN',
    ('LISTEN','syn'):'SYN_RCVD',
    ('LISTEN','close'):'CLOSED',
    ('SYN_SENT','syn_ack'):'ESTABLISHED',
    ('SYN_SENT','syn'):'SYN_RCVD',
    ('SYN_SENT','close'):'CLOSED',
    ('SYN_RCVD','ack'):'ESTABLISHED',
    ('SYN_RCVD','close'):'FIN_WAIT_1',
    ('ESTABLISHED','close'):'FIN_WAIT_1',
    ('ESTABLISHED','fin'):'CLOSE_WAIT',
    ('FIN_WAIT_1','ack'):'FIN_WAIT_2',
    ('FIN_WAIT_1','fin'):'CLOSING',
    ('FIN_WAIT_1','fin_ack'):'TIME_WAIT',
    ('FIN_WAIT_2','fin'):'TIME_WAIT',
    ('CLOSING','ack'):'TIME_WAIT',
    ('TIME_WAIT','timeout'):'CLOSED',
    ('CLOSE_WAIT','close'):'LAST_ACK',
    ('LAST_ACK','ack'):'CLOSED',
}

class TCPState:
    def __init__(self):self.state='CLOSED';self.history=['CLOSED']
    def event(self,evt):
        key=(self.state,evt)
        if key in TRANSITIONS:
            self.state=TRANSITIONS[key];self.history.append(self.state);return True
        return False

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        # Client: active open -> SYN_SENT -> syn_ack -> ESTABLISHED -> close -> FIN_WAIT_1
        c=TCPState()
        assert c.event('active_open') and c.state=='SYN_SENT'
        assert c.event('syn_ack') and c.state=='ESTABLISHED'
        assert c.event('close') and c.state=='FIN_WAIT_1'
        assert c.event('ack') and c.state=='FIN_WAIT_2'
        assert c.event('fin') and c.state=='TIME_WAIT'
        assert c.event('timeout') and c.state=='CLOSED'
        # Server: passive open -> LISTEN -> syn -> SYN_RCVD -> ack -> ESTABLISHED
        s=TCPState()
        assert s.event('passive_open') and s.state=='LISTEN'
        assert s.event('syn') and s.state=='SYN_RCVD'
        assert s.event('ack') and s.state=='ESTABLISHED'
        # Invalid transition
        assert not s.event('syn_ack')
        print("All tests passed!")
    else:
        t=TCPState()
        for e in['active_open','syn_ack','close','ack','fin','timeout']:
            t.event(e);print(f"  {e:15s} -> {t.state}")
if __name__=="__main__":main()
