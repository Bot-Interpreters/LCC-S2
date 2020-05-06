import cx_Freeze

executables = [cx_Freeze.Executable(script='main.py',
                                    targetName='CoronaBreakout',
                                    shortcutName='Corona-Breakout',
                                    shortcutDir='DesktopFolder')]

cx_Freeze.setup(name='Corona Breakout',
                version='1.0',
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
                executables=executables,
                description={
                    'author': "Gautam J, Lokesh Kumar Bhansali, Sai Sidharth Sriram",
                    'disc': 'Platformer game based on COVID19'
                })
