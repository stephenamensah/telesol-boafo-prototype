# Merges output/pages/sp-*.pdf into output/Telesol-Boafo-Prototype-Screens.pdf
import glob, os
from pypdf import PdfWriter, PdfReader
out = os.path.join(os.path.dirname(__file__), '..', 'output')
w = PdfWriter()
for f in sorted(glob.glob(os.path.join(out, 'pages', 'sp-*.pdf'))):
    w.add_page(PdfReader(f).pages[0])
w.write(os.path.join(out, 'Telesol-Boafo-Prototype-Screens.pdf'))
print('Wrote output/Telesol-Boafo-Prototype-Screens.pdf')
