"""Small helper to print code-cell outputs from an executed notebook.

This script uses a safe import for `nbformat` so it fails gracefully when run
outside the project virtual environment. If `nbformat` is not available it
prints a short message explaining how to install it into the project's
`.venv` and exits with a non-zero code.
"""

import json
import sys
import os

# Allow optional notebook path as first argument. If none provided, prefer an
# executed copy if it exists (experiment_demo.executed.ipynb), otherwise fall
# back to the original notebook file.
default_executed = 'notebooks/experiment_demo.executed.ipynb'
default_original = 'notebooks/experiment_demo.ipynb'
if len(sys.argv) > 1:
    nb_path = sys.argv[1]
elif os.path.exists(default_executed):
    nb_path = default_executed
else:
    nb_path = default_original

try:
    import nbformat
    # Prefer nbformat when available for robust parsing
    nb = nbformat.read(nb_path, as_version=4)
except ModuleNotFoundError:
    # Fallback: parse the notebook file as plain JSON. This allows the
    # script to run in environments without nbformat, though some rich
    # notebook semantics may be missing.
    print(
        "nbformat not found: falling back to plain json parsing (outputs may differ)."
    )
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)

# Print only textual outputs from code cells. This prints stream outputs
# (what print() writes) and text/plain from execute_result/display_data.
# nb may be an nbformat.NotebookNode (has .cells) or a plain dict (has 'cells').
cells = getattr(nb, 'cells', None) or nb.get('cells', [])
for idx, cell in enumerate(cells, start=1):
    if cell.get('cell_type') != 'code':
        continue
    texts = []
    for out in cell.get('outputs', []):
        otype = out.get('output_type')
        if otype == 'stream':
            texts.append(out.get('text', ''))
        elif otype in ('execute_result', 'display_data'):
            data = out.get('data', {})
            if 'text/plain' in data:
                texts.append(data['text/plain'])
    if texts:
        print(f'--- Cell {idx} outputs ---')
        for t in texts:
            # Normalize list outputs (some notebook JSON uses lists of strings)
            if isinstance(t, list):
                t = ''.join(t)
            # Convert non-string outputs to string
            if not isinstance(t, str):
                t = str(t)
            # Ensure output ends with a newline for readability
            if not t.endswith('\n'):
                t = t + '\n'
            sys.stdout.write(t)

