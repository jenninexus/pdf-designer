"""Frozen entry point for the existing local PDF Designer Hub.

Electron invokes this executable with the ordinary ``pdf_tool.preview`` CLI
arguments. It intentionally owns no document rendering or UI of its own.
"""

from pdf_tool.preview import main


if __name__ == "__main__":
    main()
