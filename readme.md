#pyMASreceipt - python module for parsing the contents of _MASReceipt/receipt file inside a Mac App Store .app

pyMASreceipt is a python module for parsing the receipt contents of a Mac App Store app (located within the application bundle: Contents/Resources/_MASReceipt/receipt).

It is a best guess at contents, following the documentation provided by Apple at: http://developer.apple.com/library/mac/#releasenotes/General/ValidateAppStoreReceipt/_index.html

This module depends on the module 'python-asn1' by Geert Jansen (geertj@github), available here: https://github.com/geertj/python-asn1

##Credits

- pyMASreceipt is written by pudquick@github 
- python-asn1 is written by geertj@github 

##License

pyMASreceipt is released under a standard MIT license.

	Permission is hereby granted, free of charge, to any person
	obtaining a copy of this software and associated documentation files
	(the "Software"), to deal in the Software without restriction,
	including without limitation the rights to use, copy, modify, merge,
	publish, distribute, sublicense, and/or sell copies of the Software,
	and to permit persons to whom the Software is furnished to do so,
	subject to the following conditions:

	The above copyright notice and this permission notice shall be
	included in all copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
	EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
	MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
	NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
	BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
	ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
	CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
