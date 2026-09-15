#!/usr/bin/env python3
"""Verify real repo-add preserves old entries during an incremental publish."""
import io
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
ROOT = Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory() as tmp:
    d=Path(tmp)
    def pkg(name):
        path=d/f'{name}-1-1-any.pkg.tar.gz'
        content=f'pkgname = {name}\npkgver = 1-1\npkgdesc = Test\nsize = 0\narch = any\n'.encode()
        with tarfile.open(path,'w:gz') as t:
            info=tarfile.TarInfo('.PKGINFO'); info.size=len(content); t.addfile(info,io.BytesIO(content))
        return path
    old=pkg('test-old')
    subprocess.run(['repo-add',str(d/'eratosthenes.db.tar.zst'),str(old)],check=True,capture_output=True)
    old.unlink()  # Old package isn't downloaded again during a partial CI build.
    pkg('test-new')
    subprocess.run(['bash',str(ROOT/'build/update-repo.sh')],env=dict(os.environ,OUTPUT_DIR=str(d),INCREMENTAL='true'),check=True,capture_output=True)
    names=subprocess.check_output(['tar','-tf',str(d/'eratosthenes.db.tar.zst')],text=True)
    assert 'test-old-1-1/desc' in names
    assert 'test-new-1-1/desc' in names
    print('Incremental database test passed: old and new entries retained')
