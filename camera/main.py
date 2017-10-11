#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = 0.1

from os import path
import argparse
import errno
import sys
import time

# Read the arguments early so we can prevent Kivy from detecting them
if __name__ == '__main__':
    argv = sys.argv[1:]
    sys.argv = sys.argv[:1]
    if "--" in argv:
        index = argv.index("--")
        kivy_args = argv[index+1:]
        argv = argv[:index]

        sys.argv.extend(kivy_args)

    parser = argparse.ArgumentParser(description="Kivy Camera, a simple camera app based on Kivy.")
    parser.add_argument("-o", "--one-shot", action='store_true', dest="one_shot", default=False, required=False, help="Take only one picture and exit. When this option is used, the \"--output\" option is mandatory and must be a file name.")
    parser.add_argument("-O", "--output", default="~/Pictures/Kivy Camera", required=False, help="Output directory, defaults to ~/Pictures/Kivy Camera. When --one-shoot is used, this is mandatory and a file name must be specified.")
    parser.add_argument("-p", "--prefix", default="IMG_%Y%m%d_%H%M%S", help="File name prefix. It can be formatted in order to add timestamps (see https://docs.python.org/2/library/time.html#time.strftime ). Default is IMG_%Y%m%d_%H%M%S")
    parser.add_argument("-V", '--version', action='version', help="Displays the current version and exits", version=__version__)
    parser.add_argument('--', dest="args", help="Kivy arguments. All arguments after this are interpreted by Kivy. Pass \"-- --help\" to get Kivy's usage.")
    args = parser.parse_args(argv)
    args.output = path.abspath(path.expanduser(args.output))

    # if not args.one_shot and path.exists(args.output) and not path.isdir(args.output):
    #     raise OSError(errno.ENOTDIR, "Not a directory", args.output)
    # if not args.one_shot and not path.exists(args.output):
    #     raise OSError(errno.ENOENT, "No such file or directory", args.output)
    # if args.one_shot and path.isdir(args.output):
    #     raise OSError(errno.EISDIR, "Is a directory", args.output)
    # if args.one_shot and not path.isdir(path.dirname(args.output)):
    #     raise OSError(errno.ENOENT, "No such file or directory", args.output)
    # if args.one_shot and not (args.output.lower().endswith(".png") or args.output.lower().endswith(".jpg")):
    #     raise OSError(errno.EPERM, "File format not supported (only jpg and png are supported)", args.output)

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image

class Root(FloatLayout):
    camera = ObjectProperty(None)

class ShutterButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ShutterButton, self).__init__(**kwargs)
        self.bind(on_press=self.set_color)
        self.bind(on_release=self.unset_color)

    def set_color(self, *args):
        self.color = (.6, .6, .6, 1)

    def unset_color(self, *args):
        self.color = (1, 1, 1, 1)

class CameraApp(App):
    output = StringProperty("")
    one_shot = BooleanProperty(False)
    prefix = StringProperty("IMG_%Y%m%d_%H%M%S")

    def build(self):
        self.root = Root()
        return self.root

    def shoot(self, *args):
        name = self.output
        if not self.one_shot:
            name = path.join(self.output, time.strftime(self.prefix) + ".png")

        self.root.camera.texture.save(name, flipped=False)

        if self.one_shot:
            self.stop()


if __name__ == '__main__':
    CameraApp(one_shot=args.one_shot, prefix=args.prefix, output=args.output).run()
