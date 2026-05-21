# -*- coding: utf-8 -*-
import os, sys

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ANALISE-ESTUDO-CADASTRO-PROMOTORES-v2.html')

def main():
    with open(OUT, 'w', encoding='utf-8') as f:
        write_head(f)
        write_styles(f)
        write_body_start(f)
        write_sidebar(f)
        write_header(f)
        write_filters(f)
        write_pages(f)
        write_command_palette(f)
        write_scripts(f)
        f.write('</html>\n')
    sz = os.path.getsize(OUT)
    print(f'OK: {OUT} ({sz:,} bytes)')

if __name__ == '__main__':
    main()
