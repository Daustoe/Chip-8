<snippet>
  <content>
# Chip-8

Python Chip 8 emulator for Python 3.4

This is my attempt to learn a bit more about emulation while using a language that I was comfortable with. Python doesn't have the largest community for Emulation as well, leaving quite a bit of room for optimization for what is currently out there.

This emulator was written using Pyglet, but was originally started with pygame. I may go back in the future and finish a version using pygame, but really we didn't utilize much from Pyglet. Transitioning would be as simple and replacing the window with pygames window and rewriting the draw function.

## Installation

TODO: 
  Want to implement setuptools sometime in the future.
  For now just run main.py from python.

## Usage

python main.py <rom filepath>
  Where the <rom filepath> is the filepath to the rom you wish to run on the emulator. Will not run without this arguement.
python main.py -h
  Displays help.

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## License

Copyright (c) 2014 Clayton Powell

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

</content>
</snippet>
