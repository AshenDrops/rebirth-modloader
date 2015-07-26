# -*- mode: python -*-
a = Analysis(['rebirth_modloader/main.py'],
             pathex=['/home/ashlynn/git/rebirth-modloader'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts + [('O','','OPTION')],
          a.binaries,
          a.zipfiles,
          a.datas,
          name='rebirth_modloader.app',
          debug=False,
          strip=None,
          upx=True,
          console=True )
