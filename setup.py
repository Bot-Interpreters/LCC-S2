import cx_Freeze

executables = [cx_Freeze.Executable('main.py')]

cx_Freeze.setup(name='Corona OutBreak',
                options={
                    'build_exe': {
                        'packages': ['pygame'],
                        'include_files': [
                                    'Comic Strips',
                                    'images',
                                    'sounds',
                                    'game.py',
                                    'settings.py',
                                    'sprites.py'
                        ]
                    }
                },
                executables=executables)
