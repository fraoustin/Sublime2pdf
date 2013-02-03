## Summary

2pdf to generate a pdf file.

pdf file can be printed

2pdf use:

* rst2pdf https://code.google.com/p/rst2pdf/
* pil http://www.pythonware.com/products/pil/
* pygments http://pygments.org/
* reportlab http://www.reportlab.com/software/opensource/rl-toolkit/
* docutils http://docutils.sourceforge.net/

## How to install

1. Clone or [download] git repo into your packages folder (in ST2, find Browse Packages... menu item to open this folder)
2. Restart ST2 editor (if required)

Or with [Package Control](http://wbond.net/sublime_packages/package_control):

1. Run "Package Control: Add repository" and add https://github.com/fraoustin/Sublime2pdf
2. Run "Package Control: Install Package" command, find and install `2pdf` plugin.
3. Restart ST2 editor (if required)


## How to Use

click menu Selection -> ToPdf


### Configure key binding

add the following line to keymap settings

	{ "keys": ["ctrl+p"], "command": "to_pdf" }


### Configure

stylesheet-code is stylesheet use by rst2pdf for all syntax except for the restructured syntax

stylesheet-rst is stylesheet use by rst2pdf for the restructured syntax

	{
    "stylesheet-code": "print.style",
    "stylesheet-rst": "",
    "breaklevel": 0,
    "compressed": false
	}




## License

view license of

rst2.pdf