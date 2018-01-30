#!/usr/bin/env python

import os
import sys
import asyncio
import struct
from functools import reduce
from socket import socket, AF_BLUETOOTH, BTPROTO_L2CAP, SOCK_SEQPACKET, \
        BDADDR_ANY

import dbus
import dbus.service
import evdev


mod_table = dict(
        KEY_RIGHTMETA= 0b1000_0000,
        KEY_RIGHTALT=  0b0100_0000,
        KEY_RIGHTSHIFT=0b0010_0000,
        KEY_RIGHTCTRL= 0b0001_0000,
        KEY_LEFTMETA=  0b0000_1000,
        KEY_LEFTALT=   0b0000_0100,
        KEY_LEFTSHIFT= 0b0000_0010,
        KEY_LEFTCTRL=  0b0000_0001,
        )

mouse_button_table = {
    evdev.ecodes.BTN_LEFT:   0b0000_0001,
    evdev.ecodes.BTN_RIGHT:  0b0000_0010,
    evdev.ecodes.BTN_MIDDLE: 0b0000_0100,
}

keytable = {
    "KEY_RESERVED" : 0,
    "KEY_ESC" : 41,
    "KEY_1" : 30,
    "KEY_2" : 31,
    "KEY_3" : 32,
    "KEY_4" : 33,
    "KEY_5" : 34,
    "KEY_6" : 35,
    "KEY_7" : 36,
    "KEY_8" : 37,
    "KEY_9" : 38,
    "KEY_0" : 39,
    "KEY_MINUS" : 45,
    "KEY_EQUAL" : 46,
    "KEY_BACKSPACE" : 42,
    "KEY_TAB" : 43,
    "KEY_Q" : 20,
    "KEY_W" : 26,
    "KEY_E" : 8,
    "KEY_R" : 21,
    "KEY_T" : 23,
    "KEY_Y" : 28,
    "KEY_U" : 24,
    "KEY_I" : 12,
    "KEY_O" : 18,
    "KEY_P" : 19,
    "KEY_LEFTBRACE" : 47,
    "KEY_RIGHTBRACE" : 48,
    "KEY_ENTER" : 40,
    "KEY_LEFTCTRL" : 224,
    "KEY_A" : 4,
    "KEY_S" : 22,
    "KEY_D" : 7,
    "KEY_F" : 9,
    "KEY_G" : 10,
    "KEY_H" : 11,
    "KEY_J" : 13,
    "KEY_K" : 14,
    "KEY_L" : 15,
    "KEY_SEMICOLON" : 51,
    "KEY_APOSTROPHE" : 52,
    "KEY_GRAVE" : 53,
    "KEY_LEFTSHIFT" : 225,
    "KEY_BACKSLASH" : 50,
    "KEY_Z" : 29,
    "KEY_X" : 27,
    "KEY_C" : 6,
    "KEY_V" : 25,
    "KEY_B" : 5,
    "KEY_N" : 17,
    "KEY_M" : 16,
    "KEY_COMMA" : 54,
    "KEY_DOT" : 55,
    "KEY_SLASH" : 56,
    "KEY_RIGHTSHIFT" : 229,
    "KEY_KPASTERISK" : 85,
    "KEY_LEFTALT" : 226,
    "KEY_SPACE" : 44,
    "KEY_CAPSLOCK" : 57,
    "KEY_F1" : 58,
    "KEY_F2" : 59,
    "KEY_F3" : 60,
    "KEY_F4" : 61,
    "KEY_F5" : 62,
    "KEY_F6" : 63,
    "KEY_F7" : 64,
    "KEY_F8" : 65,
    "KEY_F9" : 66,
    "KEY_F10" : 67,
    "KEY_NUMLOCK" : 83,
    "KEY_SCROLLLOCK" : 71,
    "KEY_KP7" : 95,
    "KEY_KP8" : 96,
    "KEY_KP9" : 97,
    "KEY_KPMINUS" : 86,
    "KEY_KP4" : 92,
    "KEY_KP5" : 93,
    "KEY_KP6" : 94,
    "KEY_KPPLUS" : 87,
    "KEY_KP1" : 89,
    "KEY_KP2" : 90,
    "KEY_KP3" : 91,
    "KEY_KP0" : 98,
    "KEY_KPDOT" : 99,
    "KEY_ZENKAKUHANKAKU" : 148,
    "KEY_102ND" : 100,
    "KEY_F11" : 68,
    "KEY_F12" : 69,
    "KEY_RO" : 135,
    "KEY_KATAKANA" : 146,
    "KEY_HIRAGANA" : 147,
    "KEY_HENKAN" : 138,
    "KEY_KATAKANAHIRAGANA" : 136,
    "KEY_MUHENKAN" : 139,
    "KEY_KPJPCOMMA" : 140,
    "KEY_KPENTER" : 88,
    "KEY_RIGHTCTRL" : 228,
    "KEY_KPSLASH" : 84,
    "KEY_SYSRQ" : 70,
    "KEY_RIGHTALT" : 230,
    "KEY_HOME" : 74,
    "KEY_UP" : 82,
    "KEY_PAGEUP" : 75,
    "KEY_LEFT" : 80,
    "KEY_RIGHT" : 79,
    "KEY_END" : 77,
    "KEY_DOWN" : 81,
    "KEY_PAGEDOWN" : 78,
    "KEY_INSERT" : 73,
    "KEY_DELETE" : 76,
    "KEY_MUTE" : 239,
    "KEY_VOLUMEDOWN" : 238,
    "KEY_VOLUMEUP" : 237,
    "KEY_POWER" : 102,
    "KEY_KPEQUAL" : 103,
    "KEY_PAUSE" : 72,
    "KEY_KPCOMMA" : 133,
    "KEY_HANGEUL" : 144,
    "KEY_HANJA" : 145,
    "KEY_YEN" : 137,
    "KEY_LEFTMETA" : 227,
    "KEY_RIGHTMETA" : 231,
    "KEY_COMPOSE" : 101,
    "KEY_STOP" : 243,
    "KEY_AGAIN" : 121,
    "KEY_PROPS" : 118,
    "KEY_UNDO" : 122,
    "KEY_FRONT" : 119,
    "KEY_COPY" : 124,
    "KEY_OPEN" : 116,
    "KEY_PASTE" : 125,
    "KEY_FIND" : 244,
    "KEY_CUT" : 123,
    "KEY_HELP" : 117,
    "KEY_CALC" : 251,
    "KEY_SLEEP" : 248,
    "KEY_WWW" : 240,
    "KEY_COFFEE" : 249,
    "KEY_BACK" : 241,
    "KEY_FORWARD" : 242,
    "KEY_EJECTCD" : 236,
    "KEY_NEXTSONG" : 235,
    "KEY_PLAYPAUSE" : 232,
    "KEY_PREVIOUSSONG" : 234,
    "KEY_STOPCD" : 233,
    "KEY_REFRESH" : 250,
    "KEY_EDIT" : 247,
    "KEY_SCROLLUP" : 245,
    "KEY_SCROLLDOWN" : 246,
    "KEY_F13" : 104,
    "KEY_F14" : 105,
    "KEY_F15" : 106,
    "KEY_F16" : 107,
    "KEY_F17" : 108,
    "KEY_F18" : 109,
    "KEY_F19" : 110,
    "KEY_F20" : 111,
    "KEY_F21" : 112,
    "KEY_F22" : 113,
    "KEY_F23" : 114,
    "KEY_F24" : 115
}

class InputState(object):
    def __init__(self):
        self.mods = set()
        self.keys = set()
        self.buttons = set()

    async def handle_events(self, device, callback):
        async for event in device.async_read_loop():
            if event.type == evdev.ecodes.EV_KEY:
                event = evdev.events.KeyEvent(event)
                if event.event.code not in mouse_button_table:
                    self.handle_key_event(event, callback)
                else:
                    self.handle_button_event(event, callback)

            elif event.type == evdev.ecodes.EV_REL:
                event = evdev.events.RelEvent(event)
                self.handle_rel_event(event, callback)

            else:
                #print(event.type, event.value, evdev.categorize(event))
                pass

    def handle_key_event(self, event, callback):
        if event.keystate == event.key_down:
            if event.keycode in mod_table:
                self.mods.add(event.keycode)
            else:
                self.keys.add(event.keycode)
            callback(self.to_keyboard_report())

        elif event.keystate == event.key_up:
            if event.keycode in mod_table:
                self.mods.remove(event.keycode)
            else:
                self.keys.remove(event.keycode)
            callback(self.to_keyboard_report())

    def handle_button_event(self, event, callback):
        code = event.event.code
        if event.keystate == event.key_down:
            self.buttons.add(code)

        elif event.keystate == event.key_up:
            self.buttons.remove(code)

        callback(self.to_mouse_report(0, 0, 0))

    def handle_rel_event(self, event, callback):
        code = evdev.ecodes.REL[event.event.code]

        buttons = reduce(lambda v, e: v | mouse_button_table.get(e, 0), self.buttons, 0)
        val = event.event.value
        if code == 'REL_X':
            callback(self.to_mouse_report(val, 0, 0))
        elif code == 'REL_Y':
            callback(self.to_mouse_report(0, val, 0))
        elif code == 'REL_WHEEL':
            callback(self.to_mouse_report(0, 0, val))

    def to_keyboard_report(self):
        mod = reduce(lambda v, e: v | mod_table.get(e, 0), self.mods, 0)
        keys = (list(keytable[x] for x in self.keys) + ([0x00] * 6))[:6]
        return struct.pack('BBBBBBBBBB',
                0xA1,
                0x01,
                mod,
                0x00,
                *keys)

    def to_mouse_report(self, x, y, z):
        buttons = reduce(lambda v, e: v | mouse_button_table.get(e, 0), self.buttons, 0)
        data = (buttons, x & 0xFF, y & 0xFF, z & 0xFF)
        return struct.pack('BBBBBB',
                0xA1,
                0x02,
                *data)


def read_sdp_service_record():
    loc = os.path.join(os.path.dirname(__file__), 'sdp_record.xml')
    with open(loc) as fp:
        data = fp.read()
        return data

def setup_profile():
    opts = {
        'ServiceRecord': read_sdp_service_record(),
        'Role': 'server',
        'RequireAuthentication': False,
        'RequireAuthorization': False,
    }

    dbus_path = "/btk/profile"
    UUID="00001124-0000-1000-8000-00805f9b34fb"

    bus = dbus.SystemBus()
    manager = dbus.Interface(
            bus.get_object("org.bluez","/org/bluez"),
            "org.bluez.ProfileManager1")
    manager.RegisterProfile(dbus_path, UUID, opts)


async def listen(*, loop):
    scontrol = socket(AF_BLUETOOTH, SOCK_SEQPACKET, BTPROTO_L2CAP)
    sinterrupt = socket(AF_BLUETOOTH, SOCK_SEQPACKET, BTPROTO_L2CAP)

    scontrol.bind((BDADDR_ANY, 17))
    sinterrupt.bind((BDADDR_ANY, 19))

    scontrol.listen()
    sinterrupt.listen()

    scontrol.setblocking(False)
    sinterrupt.setblocking(False)

    while True:
        (ccontrol, _) = await loop.sock_accept(scontrol)
        (cinterrupt, _) = await loop.sock_accept(sinterrupt)
        yield (ccontrol, cinterrupt)


async def send_input(csock, isock, queues, *, loop):
    queue = asyncio.Queue(loop=loop)
    queues.add(queue)
    try:
        while True:
            data = await queue.get()
            try:
                await loop.sock_sendall(isock, data)
            except ConnectionResetError as e:
                print(e)
                break
    finally:
        queues.remove(queue)


async def read_sock(sock, *, loop):
    while True:
        data = await loop.sock_recv(sock, 16)
        if not data:
            break
        print(" ".join(f"{x:02x}" for x in data))


async def handle_client(csock, isock, queues, *, loop):
    with csock:
        with isock:
            input_future = asyncio.ensure_future(
                    send_input(csock, isock, queues, loop=loop),
                    loop=loop)
            c_read = asyncio.ensure_future(
                    read_sock(csock, loop=loop),
                    loop=loop)
            i_read = asyncio.ensure_future(
                    read_sock(isock, loop=loop),
                    loop=loop)
            def done(_):
                input_future.cancel()
                c_read.cancel()
                i_read.cancel()
            input_future.add_done_callback(done)
            c_read.add_done_callback(done)
            i_read.add_done_callback(done)

            await asyncio.gather(input_future, c_read, i_read, loop=loop)


async def run(sources, *, loop):
    setup_profile()

    queues = set()
    def callback(data):
        #print(" ".join(f"{x:02x}" for x in data))
        for queue in queues:
            queue.put_nowait(data)

    state = InputState()
    for source in sources:
        asyncio.ensure_future(
                state.handle_events(source, callback), loop=loop)

    async for (ccontrol, cinterrupt) in listen(loop=loop):
        asyncio.ensure_future(
                handle_client(ccontrol, cinterrupt, queues, loop=loop),
                loop=loop)


def main():
    inputs = sys.argv[1:]
    if not inputs:
        inputs = evdev.util.list_devices()
    sources = [evdev.InputDevice(x) for x in inputs]

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(sources, loop=loop))
    except KeyboardInterrupt:
        pass
    loop.close()


if __name__ == '__main__':
    main()
