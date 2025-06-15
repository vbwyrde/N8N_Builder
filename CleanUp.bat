REM Create archive directory if it doesn't exist
if not exist "Archive" mkdir Archive
if not exist "Archive\Duplicates" mkdir Archive\Duplicates
if not exist "Archive\Obsolete" mkdir Archive\Obsolete
REM Move duplicate files to archive (keeping the recommended version)

REM Duplicate group: ef991552...
REM Keeping: n8n_builder\agents\integration\message_broker.py
move "agents\integration\message_broker.py" "Archive\Duplicates\message_broker.py"
move "n8n_builder\agents\agents\integration\message_broker.py" "Archive\Duplicates\message_broker.py"

REM Duplicate group: 5f022c3b...
REM Keeping: n8n_builder\agents\integration\message_protocol.py
move "agents\integration\message_protocol.py" "Archive\Duplicates\message_protocol.py"
move "n8n_builder\agents\agents\integration\message_protocol.py" "Archive\Duplicates\message_protocol.py"

REM Duplicate group: c09d7fe6...
REM Keeping: n8n_builder\agents\integration\state_manager.py
move "agents\integration\state_manager.py" "Archive\Duplicates\state_manager.py"
move "n8n_builder\agents\agents\integration\state_manager.py" "Archive\Duplicates\state_manager.py"

REM Duplicate group: b9a838fc...
REM Keeping: n8n_builder\agents\integration\__init__.py
move "agents\integration\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 18d27e19...
REM Keeping: n8n_builder\venv\Lib\site-packages\distutils-precedence.pth
move "venv\Lib\site-packages\distutils-precedence.pth" "Archive\Duplicates\distutils-precedence.pth"

REM Duplicate group: 18d7a22c...
REM Keeping: n8n_builder\venv\Lib\site-packages\py.py
move "venv\Lib\site-packages\py.py" "Archive\Duplicates\py.py"

REM Duplicate group: f781d594...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\ansi.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\ansi.py" "Archive\Duplicates\ansi.py"
move "venv\Lib\site-packages\colorama\ansi.py" "Archive\Duplicates\ansi.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\ansi.py" "Archive\Duplicates\ansi.py"

REM Duplicate group: 0ca18c79...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\ansitowin32.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\ansitowin32.py" "Archive\Duplicates\ansitowin32.py"
move "venv\Lib\site-packages\colorama\ansitowin32.py" "Archive\Duplicates\ansitowin32.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\ansitowin32.py" "Archive\Duplicates\ansitowin32.py"

REM Duplicate group: 1a15620a...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\initialise.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\initialise.py" "Archive\Duplicates\initialise.py"
move "venv\Lib\site-packages\colorama\initialise.py" "Archive\Duplicates\initialise.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\initialise.py" "Archive\Duplicates\initialise.py"

REM Duplicate group: 0af1249c...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\win32.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\win32.py" "Archive\Duplicates\win32.py"
move "venv\Lib\site-packages\colorama\win32.py" "Archive\Duplicates\win32.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\win32.py" "Archive\Duplicates\win32.py"

REM Duplicate group: a52a65ae...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\winterm.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\winterm.py" "Archive\Duplicates\winterm.py"
move "venv\Lib\site-packages\colorama\winterm.py" "Archive\Duplicates\winterm.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\winterm.py" "Archive\Duplicates\winterm.py"

REM Duplicate group: c2daa3df...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\__init__.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\colorama\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: ffd5754e...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\tests\ansitowin32_test.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\ansitowin32_test.py" "Archive\Duplicates\ansitowin32_test.py"
move "venv\Lib\site-packages\colorama\tests\ansitowin32_test.py" "Archive\Duplicates\ansitowin32_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\ansitowin32_test.py" "Archive\Duplicates\ansitowin32_test.py"

REM Duplicate group: 5986a968...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\tests\ansi_test.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\ansi_test.py" "Archive\Duplicates\ansi_test.py"
move "venv\Lib\site-packages\colorama\tests\ansi_test.py" "Archive\Duplicates\ansi_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\ansi_test.py" "Archive\Duplicates\ansi_test.py"

REM Duplicate group: 711f7c7a...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\tests\initialise_test.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\initialise_test.py" "Archive\Duplicates\initialise_test.py"
move "venv\Lib\site-packages\colorama\tests\initialise_test.py" "Archive\Duplicates\initialise_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\initialise_test.py" "Archive\Duplicates\initialise_test.py"

REM Duplicate group: 7634e030...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\tests\isatty_test.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\isatty_test.py" "Archive\Duplicates\isatty_test.py"
move "venv\Lib\site-packages\colorama\tests\isatty_test.py" "Archive\Duplicates\isatty_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\isatty_test.py" "Archive\Duplicates\isatty_test.py"

REM Duplicate group: 31142629...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\tests\utils.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\utils.py" "Archive\Duplicates\utils.py"
move "venv\Lib\site-packages\colorama\tests\utils.py" "Archive\Duplicates\utils.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\utils.py" "Archive\Duplicates\utils.py"

REM Duplicate group: 3322cabd...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\tests\winterm_test.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\winterm_test.py" "Archive\Duplicates\winterm_test.py"
move "venv\Lib\site-packages\colorama\tests\winterm_test.py" "Archive\Duplicates\winterm_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\winterm_test.py" "Archive\Duplicates\winterm_test.py"

REM Duplicate group: b1fda43e...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama\tests\__init__.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\colorama\tests\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 365c9bfe...
REM Keeping: venv\Lib\site-packages\PyJWT-2.10.1.dist-info\INSTALLER
move "n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\top_level.txt" "Archive\Duplicates\top_level.txt"
move "n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\aiohappyeyeballs-2.6.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\aiosignal-1.3.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\annotated_types-0.7.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\anyio-4.9.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\attrs-25.3.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\certifi-2025.4.26.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\cffi-1.17.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\charset_normalizer-3.4.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\click-8.2.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\coverage-7.8.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\ecdsa-0.19.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\frozenlist-1.6.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\h11-0.16.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\httpcore-1.0.9.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\idna-3.10.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\mdurl-0.1.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\multidict-6.4.4.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\packaging-25.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\top_level.txt" "Archive\Duplicates\top_level.txt"
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pycares-4.8.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pycparser-2.22.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pydantic_core-2.33.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\python_multipart-0.0.6.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\rich-14.0.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\rsa-4.9.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\six-1.17.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\starlette-0.46.2.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\typing_inspection-0.4.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\urllib3-2.4.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\uuid-1.30.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"
move "venv\Lib\site-packages\yarl-1.20.0.dist-info\INSTALLER" "Archive\Duplicates\INSTALLER"

REM Duplicate group: 40a32558...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\METADATA
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\METADATA" "Archive\Duplicates\METADATA"

REM Duplicate group: 510fedd8...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\RECORD
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\RECORD" "Archive\Duplicates\RECORD"

REM Duplicate group: 292bc427...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\WHEEL
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: b4936429...
REM Keeping: n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\licenses\LICENSE.txt
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\licenses\LICENSE.txt" "Archive\Duplicates\LICENSE.txt"

REM Duplicate group: ec76a439...
REM Keeping: n8n_builder\venv\Lib\site-packages\iniconfig\exceptions.py
move "venv\Lib\site-packages\iniconfig\exceptions.py" "Archive\Duplicates\exceptions.py"

REM Duplicate group: d41d8cd9...
REM Keeping: Scripts\logs\errors.log
move "n8n_builder\venv\Lib\site-packages\iniconfig\py.typed" "Archive\Duplicates\py.typed"
move "n8n_builder\venv\Lib\site-packages\packaging\py.typed" "Archive\Duplicates\py.typed"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\legacy\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\cli\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\metadata\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\compat\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\packages\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\packages\backports\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\jaraco\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\py.typed" "Archive\Duplicates\py.typed"
move "n8n_builder\venv\Lib\site-packages\pytest\py.typed" "Archive\Duplicates\py.typed"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\jaraco\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "n8n_builder\venv\Lib\site-packages\_pytest\py.typed" "Archive\Duplicates\py.typed"
move "n8n_builder\venv\Lib\site-packages\_pytest\_py\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\aiodns\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\aiohappyeyeballs\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\aiosignal\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\annotated_types\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\anyio\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\anyio\streams\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\anyio\_backends\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\anyio\_core\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\attr\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\attrs\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\bcrypt\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\certifi\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\charset_normalizer\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\click\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\click-8.2.1.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\cryptography\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\fastapi\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\fastapi\dependencies\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\fastapi\openapi\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\httpcore\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\httpcore\_backends\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\httpx\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\httpx\_transports\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\idna\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\iniconfig\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\jwt\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\markdown_it\cli\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\markdown_it\common\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\multipart\tests\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\packaging\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\pip\_internal\operations\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_internal\resolution\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_internal\resolution\legacy\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_internal\utils\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\cli\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\metadata\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\resolvelib\compat\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\packages\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\packages\backports\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\pkg_resources\_vendor\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\jaraco\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pluggy\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\pycares\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\pydantic\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\pydantic\deprecated\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pydantic\v1\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\pydantic\_internal\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\pydantic_core\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\pytest\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\pytest_asyncio\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\pytest_mock\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\python_multipart-0.0.6.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\rich\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\rich-14.0.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\setuptools\_vendor\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\jaraco\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\sniffio\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\sniffio\_tests\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\starlette\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\typing_inspection\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\typing_inspection\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\urllib3\contrib\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\uuid-1.30.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\uvicorn\lifespan\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\uvicorn\loops\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\uvicorn\middleware\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\uvicorn\protocols\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\uvicorn\protocols\http\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\uvicorn\protocols\websockets\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\websockets\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\websockets\asyncio\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\websockets\sync\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\REQUESTED" "Archive\Duplicates\REQUESTED"
move "venv\Lib\site-packages\_pytest\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\_pytest\_py\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: f0700c12...
REM Keeping: n8n_builder\venv\Lib\site-packages\iniconfig\_parse.py
move "venv\Lib\site-packages\iniconfig\_parse.py" "Archive\Duplicates\_parse.py"

REM Duplicate group: ad5a2a8e...
REM Keeping: n8n_builder\venv\Lib\site-packages\iniconfig\_version.py
move "venv\Lib\site-packages\iniconfig\_version.py" "Archive\Duplicates\_version.py"

REM Duplicate group: 5cddc994...
REM Keeping: n8n_builder\venv\Lib\site-packages\iniconfig\__init__.py
move "venv\Lib\site-packages\iniconfig\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 8bcff2db...
REM Keeping: n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\METADATA
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\METADATA" "Archive\Duplicates\METADATA"

REM Duplicate group: 9872de9b...
REM Keeping: n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\RECORD
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\RECORD" "Archive\Duplicates\RECORD"

REM Duplicate group: e2fcb0ad...
REM Keeping: n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\WHEEL
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\attrs-25.3.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\httpcore-1.0.9.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\starlette-0.46.2.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\typing_inspection-0.4.1.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\urllib3-2.4.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: 4a73af4b...
REM Keeping: n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\licenses\LICENSE
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\licenses\LICENSE" "Archive\Duplicates\LICENSE"

REM Duplicate group: 1be7f129...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\markers.py
move "venv\Lib\site-packages\packaging\markers.py" "Archive\Duplicates\markers.py"

REM Duplicate group: 7cfeeeeb...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\metadata.py
move "venv\Lib\site-packages\packaging\metadata.py" "Archive\Duplicates\metadata.py"

REM Duplicate group: 2fc711cf...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\requirements.py
move "venv\Lib\site-packages\packaging\requirements.py" "Archive\Duplicates\requirements.py"

REM Duplicate group: 5e70fd47...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\specifiers.py
move "venv\Lib\site-packages\packaging\specifiers.py" "Archive\Duplicates\specifiers.py"

REM Duplicate group: 343d0677...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\tags.py
move "venv\Lib\site-packages\packaging\tags.py" "Archive\Duplicates\tags.py"

REM Duplicate group: f6d73a16...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\utils.py
move "venv\Lib\site-packages\packaging\utils.py" "Archive\Duplicates\utils.py"

REM Duplicate group: fa56706c...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\version.py
move "venv\Lib\site-packages\packaging\version.py" "Archive\Duplicates\version.py"

REM Duplicate group: e83ac3c8...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\_elffile.py
move "venv\Lib\site-packages\packaging\_elffile.py" "Archive\Duplicates\_elffile.py"

REM Duplicate group: 46426bd4...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\_manylinux.py
move "venv\Lib\site-packages\packaging\_manylinux.py" "Archive\Duplicates\_manylinux.py"

REM Duplicate group: d0d487bb...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\_musllinux.py
move "venv\Lib\site-packages\packaging\_musllinux.py" "Archive\Duplicates\_musllinux.py"

REM Duplicate group: b8877d07...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\_parser.py
move "venv\Lib\site-packages\packaging\_parser.py" "Archive\Duplicates\_parser.py"

REM Duplicate group: de664fed...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\_structures.py
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\_structures.py" "Archive\Duplicates\_structures.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\_structures.py" "Archive\Duplicates\_structures.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\_structures.py" "Archive\Duplicates\_structures.py"
move "venv\Lib\site-packages\packaging\_structures.py" "Archive\Duplicates\_structures.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\_structures.py" "Archive\Duplicates\_structures.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\_structures.py" "Archive\Duplicates\_structures.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\_structures.py" "Archive\Duplicates\_structures.py"

REM Duplicate group: 58bff3ae...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\_tokenizer.py
move "venv\Lib\site-packages\packaging\_tokenizer.py" "Archive\Duplicates\_tokenizer.py"

REM Duplicate group: bb0d0797...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\__init__.py
move "venv\Lib\site-packages\packaging\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 313a72cf...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\licenses\_spdx.py
move "venv\Lib\site-packages\packaging\licenses\_spdx.py" "Archive\Duplicates\_spdx.py"

REM Duplicate group: 846baef4...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging\licenses\__init__.py
move "venv\Lib\site-packages\packaging\licenses\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: ee4c1c51...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\METADATA
move "venv\Lib\site-packages\packaging-25.0.dist-info\METADATA" "Archive\Duplicates\METADATA"

REM Duplicate group: b37e0a0b...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\RECORD
move "venv\Lib\site-packages\packaging-25.0.dist-info\RECORD" "Archive\Duplicates\RECORD"

REM Duplicate group: eca1d2e3...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\WHEEL
move "venv\Lib\site-packages\click-8.2.1.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\packaging-25.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: faadaedc...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE
move "venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE" "Archive\Duplicates\LICENSE"

REM Duplicate group: 2ee41112...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE.APACHE
move "venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE.APACHE" "Archive\Duplicates\LICENSE.APACHE"

REM Duplicate group: 7bef9bf4...
REM Keeping: n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE.BSD
move "venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE.BSD" "Archive\Duplicates\LICENSE.BSD"

REM Duplicate group: c1d1d04b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\py.typed
move "venv\Lib\site-packages\pip\py.typed" "Archive\Duplicates\py.typed"

REM Duplicate group: 6a135100...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\__init__.py
move "venv\Lib\site-packages\pip\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 0bf2ccce...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\__main__.py
move "venv\Lib\site-packages\pip\__main__.py" "Archive\Duplicates\__main__.py"

REM Duplicate group: 6db12aa0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\__pip-runner__.py
move "venv\Lib\site-packages\pip\__pip-runner__.py" "Archive\Duplicates\__pip-runner__.py"

REM Duplicate group: cc659ae8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\build_env.py
move "venv\Lib\site-packages\pip\_internal\build_env.py" "Archive\Duplicates\build_env.py"

REM Duplicate group: f1bc83ed...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cache.py
move "venv\Lib\site-packages\pip\_internal\cache.py" "Archive\Duplicates\cache.py"

REM Duplicate group: 8582b590...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\configuration.py
move "venv\Lib\site-packages\pip\_internal\configuration.py" "Archive\Duplicates\configuration.py"

REM Duplicate group: e3d846bb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\exceptions.py
move "venv\Lib\site-packages\pip\_internal\exceptions.py" "Archive\Duplicates\exceptions.py"

REM Duplicate group: 0bb4fe23...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\main.py
move "venv\Lib\site-packages\pip\_internal\main.py" "Archive\Duplicates\main.py"

REM Duplicate group: add5decf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\pyproject.py
move "venv\Lib\site-packages\pip\_internal\pyproject.py" "Archive\Duplicates\pyproject.py"

REM Duplicate group: 844a56a6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\self_outdated_check.py
move "venv\Lib\site-packages\pip\_internal\self_outdated_check.py" "Archive\Duplicates\self_outdated_check.py"

REM Duplicate group: 5b77ff30...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\wheel_builder.py
move "venv\Lib\site-packages\pip\_internal\wheel_builder.py" "Archive\Duplicates\wheel_builder.py"

REM Duplicate group: 8d88eefa...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\__init__.py
move "venv\Lib\site-packages\pip\_internal\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: ffff66dd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\autocompletion.py
move "venv\Lib\site-packages\pip\_internal\cli\autocompletion.py" "Archive\Duplicates\autocompletion.py"

REM Duplicate group: 9a615dbc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\base_command.py
move "venv\Lib\site-packages\pip\_internal\cli\base_command.py" "Archive\Duplicates\base_command.py"

REM Duplicate group: 2ee6423a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\cmdoptions.py
move "venv\Lib\site-packages\pip\_internal\cli\cmdoptions.py" "Archive\Duplicates\cmdoptions.py"

REM Duplicate group: fd633c05...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\command_context.py
move "venv\Lib\site-packages\pip\_internal\cli\command_context.py" "Archive\Duplicates\command_context.py"

REM Duplicate group: f13c5729...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\main.py
move "venv\Lib\site-packages\pip\_internal\cli\main.py" "Archive\Duplicates\main.py"

REM Duplicate group: 325f7776...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\main_parser.py
move "venv\Lib\site-packages\pip\_internal\cli\main_parser.py" "Archive\Duplicates\main_parser.py"

REM Duplicate group: 07bbbc82...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\parser.py
move "venv\Lib\site-packages\pip\_internal\cli\parser.py" "Archive\Duplicates\parser.py"

REM Duplicate group: e4a507bf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\progress_bars.py
move "venv\Lib\site-packages\pip\_internal\cli\progress_bars.py" "Archive\Duplicates\progress_bars.py"

REM Duplicate group: d96783e2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\req_command.py
move "venv\Lib\site-packages\pip\_internal\cli\req_command.py" "Archive\Duplicates\req_command.py"

REM Duplicate group: aedc7e09...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\spinners.py
move "venv\Lib\site-packages\pip\_internal\cli\spinners.py" "Archive\Duplicates\spinners.py"

REM Duplicate group: c28210e3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\status_codes.py
move "venv\Lib\site-packages\pip\_internal\cli\status_codes.py" "Archive\Duplicates\status_codes.py"

REM Duplicate group: f0ac37f2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\cli\__init__.py
move "venv\Lib\site-packages\pip\_internal\cli\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 682e9e3d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\cache.py
move "venv\Lib\site-packages\pip\_internal\commands\cache.py" "Archive\Duplicates\cache.py"

REM Duplicate group: 8d3705d0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\check.py
move "venv\Lib\site-packages\pip\_internal\commands\check.py" "Archive\Duplicates\check.py"

REM Duplicate group: 0503fd9b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\completion.py
move "venv\Lib\site-packages\pip\_internal\commands\completion.py" "Archive\Duplicates\completion.py"

REM Duplicate group: 4af1a525...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\configuration.py
move "venv\Lib\site-packages\pip\_internal\commands\configuration.py" "Archive\Duplicates\configuration.py"

REM Duplicate group: 03a80cc4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\debug.py
move "venv\Lib\site-packages\pip\_internal\commands\debug.py" "Archive\Duplicates\debug.py"

REM Duplicate group: 851dad10...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\download.py
move "venv\Lib\site-packages\pip\_internal\commands\download.py" "Archive\Duplicates\download.py"

REM Duplicate group: e641266c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\freeze.py
move "venv\Lib\site-packages\pip\_internal\commands\freeze.py" "Archive\Duplicates\freeze.py"

REM Duplicate group: 0c3c6e30...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\hash.py
move "venv\Lib\site-packages\pip\_internal\commands\hash.py" "Archive\Duplicates\hash.py"

REM Duplicate group: c2be5ef0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\help.py
move "venv\Lib\site-packages\pip\_internal\commands\help.py" "Archive\Duplicates\help.py"

REM Duplicate group: 1f6b9cab...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\index.py
move "venv\Lib\site-packages\pip\_internal\commands\index.py" "Archive\Duplicates\index.py"

REM Duplicate group: 60ad2255...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\inspect.py
move "venv\Lib\site-packages\pip\_internal\commands\inspect.py" "Archive\Duplicates\inspect.py"

REM Duplicate group: 256d4392...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\install.py
move "venv\Lib\site-packages\pip\_internal\commands\install.py" "Archive\Duplicates\install.py"

REM Duplicate group: 38829d72...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\list.py
move "venv\Lib\site-packages\pip\_internal\commands\list.py" "Archive\Duplicates\list.py"

REM Duplicate group: f013ff9e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\search.py
move "venv\Lib\site-packages\pip\_internal\commands\search.py" "Archive\Duplicates\search.py"

REM Duplicate group: a06a1835...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\show.py
move "venv\Lib\site-packages\pip\_internal\commands\show.py" "Archive\Duplicates\show.py"

REM Duplicate group: 59b79280...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\uninstall.py
move "venv\Lib\site-packages\pip\_internal\commands\uninstall.py" "Archive\Duplicates\uninstall.py"

REM Duplicate group: 59988dc9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\wheel.py
move "venv\Lib\site-packages\pip\_internal\commands\wheel.py" "Archive\Duplicates\wheel.py"

REM Duplicate group: 11dfacd3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\commands\__init__.py
move "venv\Lib\site-packages\pip\_internal\commands\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: a39e2142...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\base.py
move "venv\Lib\site-packages\pip\_internal\distributions\base.py" "Archive\Duplicates\base.py"

REM Duplicate group: 320a5e9d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\installed.py
move "venv\Lib\site-packages\pip\_internal\distributions\installed.py" "Archive\Duplicates\installed.py"

REM Duplicate group: 78195c23...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\sdist.py
move "venv\Lib\site-packages\pip\_internal\distributions\sdist.py" "Archive\Duplicates\sdist.py"

REM Duplicate group: afbe768a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\wheel.py
move "venv\Lib\site-packages\pip\_internal\distributions\wheel.py" "Archive\Duplicates\wheel.py"

REM Duplicate group: 8fbfe6a4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\__init__.py
move "venv\Lib\site-packages\pip\_internal\distributions\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 5a01fb62...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\index\collector.py
move "venv\Lib\site-packages\pip\_internal\index\collector.py" "Archive\Duplicates\collector.py"

REM Duplicate group: 25d0de70...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\index\package_finder.py
move "venv\Lib\site-packages\pip\_internal\index\package_finder.py" "Archive\Duplicates\package_finder.py"

REM Duplicate group: 126de081...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\index\sources.py
move "venv\Lib\site-packages\pip\_internal\index\sources.py" "Archive\Duplicates\sources.py"

REM Duplicate group: 8b1d3a4a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\index\__init__.py
move "venv\Lib\site-packages\pip\_internal\index\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: df3959ad...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\locations\base.py
move "venv\Lib\site-packages\pip\_internal\locations\base.py" "Archive\Duplicates\base.py"

REM Duplicate group: dbb42571...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\locations\_distutils.py
move "venv\Lib\site-packages\pip\_internal\locations\_distutils.py" "Archive\Duplicates\_distutils.py"

REM Duplicate group: 7bb5b794...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\locations\_sysconfig.py
move "venv\Lib\site-packages\pip\_internal\locations\_sysconfig.py" "Archive\Duplicates\_sysconfig.py"

REM Duplicate group: 42097813...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\locations\__init__.py
move "venv\Lib\site-packages\pip\_internal\locations\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 326b1527...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\base.py
move "venv\Lib\site-packages\pip\_internal\metadata\base.py" "Archive\Duplicates\base.py"

REM Duplicate group: 1ca1e323...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\pkg_resources.py
move "venv\Lib\site-packages\pip\_internal\metadata\pkg_resources.py" "Archive\Duplicates\pkg_resources.py"

REM Duplicate group: a7945fc4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\_json.py
move "venv\Lib\site-packages\pip\_internal\metadata\_json.py" "Archive\Duplicates\_json.py"

REM Duplicate group: 21a91c36...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\__init__.py
move "venv\Lib\site-packages\pip\_internal\metadata\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 868e0cb1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\importlib\_compat.py
move "venv\Lib\site-packages\pip\_internal\metadata\importlib\_compat.py" "Archive\Duplicates\_compat.py"

REM Duplicate group: 3f43a05c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\importlib\_dists.py
move "venv\Lib\site-packages\pip\_internal\metadata\importlib\_dists.py" "Archive\Duplicates\_dists.py"

REM Duplicate group: 65eca748...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\importlib\_envs.py
move "venv\Lib\site-packages\pip\_internal\metadata\importlib\_envs.py" "Archive\Duplicates\_envs.py"

REM Duplicate group: 2e7acd4a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\importlib\__init__.py
move "venv\Lib\site-packages\pip\_internal\metadata\importlib\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: ba64cbfb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\candidate.py
move "venv\Lib\site-packages\pip\_internal\models\candidate.py" "Archive\Duplicates\candidate.py"

REM Duplicate group: f46c4276...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\direct_url.py
move "venv\Lib\site-packages\pip\_internal\models\direct_url.py" "Archive\Duplicates\direct_url.py"

REM Duplicate group: d5b6f19f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\format_control.py
move "venv\Lib\site-packages\pip\_internal\models\format_control.py" "Archive\Duplicates\format_control.py"

REM Duplicate group: f67480db...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\index.py
move "venv\Lib\site-packages\pip\_internal\models\index.py" "Archive\Duplicates\index.py"

REM Duplicate group: 805b24bd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\installation_report.py
move "venv\Lib\site-packages\pip\_internal\models\installation_report.py" "Archive\Duplicates\installation_report.py"

REM Duplicate group: 09b2bee2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\link.py
move "venv\Lib\site-packages\pip\_internal\models\link.py" "Archive\Duplicates\link.py"

REM Duplicate group: 77b8766c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\scheme.py
move "venv\Lib\site-packages\pip\_internal\models\scheme.py" "Archive\Duplicates\scheme.py"

REM Duplicate group: 3bc5a1b3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\search_scope.py
move "venv\Lib\site-packages\pip\_internal\models\search_scope.py" "Archive\Duplicates\search_scope.py"

REM Duplicate group: a9fa37ff...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\selection_prefs.py
move "venv\Lib\site-packages\pip\_internal\models\selection_prefs.py" "Archive\Duplicates\selection_prefs.py"

REM Duplicate group: 0e0c276e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\target_python.py
move "venv\Lib\site-packages\pip\_internal\models\target_python.py" "Archive\Duplicates\target_python.py"

REM Duplicate group: a6e4de72...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\wheel.py
move "venv\Lib\site-packages\pip\_internal\models\wheel.py" "Archive\Duplicates\wheel.py"

REM Duplicate group: f4122df1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\models\__init__.py
move "venv\Lib\site-packages\pip\_internal\models\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: eab28efb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\network\auth.py
move "venv\Lib\site-packages\pip\_internal\network\auth.py" "Archive\Duplicates\auth.py"

REM Duplicate group: 5978bc48...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\network\cache.py
move "venv\Lib\site-packages\pip\_internal\network\cache.py" "Archive\Duplicates\cache.py"

REM Duplicate group: 67c8374c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\network\download.py
move "venv\Lib\site-packages\pip\_internal\network\download.py" "Archive\Duplicates\download.py"

REM Duplicate group: 4c80d4fd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\network\lazy_wheel.py
move "venv\Lib\site-packages\pip\_internal\network\lazy_wheel.py" "Archive\Duplicates\lazy_wheel.py"

REM Duplicate group: c6d17e0d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\network\session.py
move "venv\Lib\site-packages\pip\_internal\network\session.py" "Archive\Duplicates\session.py"

REM Duplicate group: 75363245...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\network\utils.py
move "venv\Lib\site-packages\pip\_internal\network\utils.py" "Archive\Duplicates\utils.py"

REM Duplicate group: 0ff15b3f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\network\xmlrpc.py
move "venv\Lib\site-packages\pip\_internal\network\xmlrpc.py" "Archive\Duplicates\xmlrpc.py"

REM Duplicate group: 3893f116...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\network\__init__.py
move "venv\Lib\site-packages\pip\_internal\network\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: f53e5714...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\check.py
move "venv\Lib\site-packages\pip\_internal\operations\check.py" "Archive\Duplicates\check.py"

REM Duplicate group: 7dd939a4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\freeze.py
move "venv\Lib\site-packages\pip\_internal\operations\freeze.py" "Archive\Duplicates\freeze.py"

REM Duplicate group: 4f8c0d5e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\prepare.py
move "venv\Lib\site-packages\pip\_internal\operations\prepare.py" "Archive\Duplicates\prepare.py"

REM Duplicate group: fdd1a9b1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\build_tracker.py
move "venv\Lib\site-packages\pip\_internal\operations\build\build_tracker.py" "Archive\Duplicates\build_tracker.py"

REM Duplicate group: 39771cd0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\metadata.py
move "venv\Lib\site-packages\pip\_internal\operations\build\metadata.py" "Archive\Duplicates\metadata.py"

REM Duplicate group: e46da46f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\metadata_editable.py
move "venv\Lib\site-packages\pip\_internal\operations\build\metadata_editable.py" "Archive\Duplicates\metadata_editable.py"

REM Duplicate group: 8d1b8a2e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\metadata_legacy.py
move "venv\Lib\site-packages\pip\_internal\operations\build\metadata_legacy.py" "Archive\Duplicates\metadata_legacy.py"

REM Duplicate group: bfd26e6b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\wheel.py
move "venv\Lib\site-packages\pip\_internal\operations\build\wheel.py" "Archive\Duplicates\wheel.py"

REM Duplicate group: d481fb9c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\wheel_editable.py
move "venv\Lib\site-packages\pip\_internal\operations\build\wheel_editable.py" "Archive\Duplicates\wheel_editable.py"

REM Duplicate group: 3a5b3604...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\wheel_legacy.py
move "venv\Lib\site-packages\pip\_internal\operations\build\wheel_legacy.py" "Archive\Duplicates\wheel_legacy.py"

REM Duplicate group: dcb76a8a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\install\editable_legacy.py
move "venv\Lib\site-packages\pip\_internal\operations\install\editable_legacy.py" "Archive\Duplicates\editable_legacy.py"

REM Duplicate group: d12804f3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\install\wheel.py
move "venv\Lib\site-packages\pip\_internal\operations\install\wheel.py" "Archive\Duplicates\wheel.py"

REM Duplicate group: c6f771f7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\operations\install\__init__.py
move "venv\Lib\site-packages\pip\_internal\operations\install\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 506c18a0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\req\constructors.py
move "venv\Lib\site-packages\pip\_internal\req\constructors.py" "Archive\Duplicates\constructors.py"

REM Duplicate group: cc2ec3d4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\req\req_file.py
move "venv\Lib\site-packages\pip\_internal\req\req_file.py" "Archive\Duplicates\req_file.py"

REM Duplicate group: d00cfec3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\req\req_install.py
move "venv\Lib\site-packages\pip\_internal\req\req_install.py" "Archive\Duplicates\req_install.py"

REM Duplicate group: 5e5ce95b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\req\req_set.py
move "venv\Lib\site-packages\pip\_internal\req\req_set.py" "Archive\Duplicates\req_set.py"

REM Duplicate group: 315a9bab...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\req\req_uninstall.py
move "venv\Lib\site-packages\pip\_internal\req\req_uninstall.py" "Archive\Duplicates\req_uninstall.py"

REM Duplicate group: 90f64157...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\req\__init__.py
move "venv\Lib\site-packages\pip\_internal\req\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: bbfa436b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\base.py
move "venv\Lib\site-packages\pip\_internal\resolution\base.py" "Archive\Duplicates\base.py"

REM Duplicate group: ba2ce05d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\legacy\resolver.py
move "venv\Lib\site-packages\pip\_internal\resolution\legacy\resolver.py" "Archive\Duplicates\resolver.py"

REM Duplicate group: f7d21a49...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\base.py
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\base.py" "Archive\Duplicates\base.py"

REM Duplicate group: 6ce9b45f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\candidates.py
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\candidates.py" "Archive\Duplicates\candidates.py"

REM Duplicate group: 04d7693d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py" "Archive\Duplicates\factory.py"

REM Duplicate group: d849f61f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\found_candidates.py
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\found_candidates.py" "Archive\Duplicates\found_candidates.py"

REM Duplicate group: 273efd24...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\provider.py
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\provider.py" "Archive\Duplicates\provider.py"

REM Duplicate group: e87077fb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\reporter.py
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\reporter.py" "Archive\Duplicates\reporter.py"

REM Duplicate group: 48bbbdfd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\requirements.py
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\requirements.py" "Archive\Duplicates\requirements.py"

REM Duplicate group: cc46af0e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py" "Archive\Duplicates\resolver.py"

REM Duplicate group: c165a574...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\appdirs.py
move "venv\Lib\site-packages\pip\_internal\utils\appdirs.py" "Archive\Duplicates\appdirs.py"

REM Duplicate group: af88d940...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\compat.py
move "venv\Lib\site-packages\pip\_internal\utils\compat.py" "Archive\Duplicates\compat.py"

REM Duplicate group: 964ca22d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\compatibility_tags.py
move "venv\Lib\site-packages\pip\_internal\utils\compatibility_tags.py" "Archive\Duplicates\compatibility_tags.py"

REM Duplicate group: 913ab688...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\datetime.py
move "venv\Lib\site-packages\pip\_internal\utils\datetime.py" "Archive\Duplicates\datetime.py"

REM Duplicate group: 816175bf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\deprecation.py
move "venv\Lib\site-packages\pip\_internal\utils\deprecation.py" "Archive\Duplicates\deprecation.py"

REM Duplicate group: 3d5e258e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\direct_url_helpers.py
move "venv\Lib\site-packages\pip\_internal\utils\direct_url_helpers.py" "Archive\Duplicates\direct_url_helpers.py"

REM Duplicate group: d96e0242...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\egg_link.py
move "venv\Lib\site-packages\pip\_internal\utils\egg_link.py" "Archive\Duplicates\egg_link.py"

REM Duplicate group: 71781af6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\encoding.py
move "venv\Lib\site-packages\pip\_internal\utils\encoding.py" "Archive\Duplicates\encoding.py"

REM Duplicate group: 68249091...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\entrypoints.py
move "venv\Lib\site-packages\pip\_internal\utils\entrypoints.py" "Archive\Duplicates\entrypoints.py"

REM Duplicate group: deee0a94...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\filesystem.py
move "venv\Lib\site-packages\pip\_internal\utils\filesystem.py" "Archive\Duplicates\filesystem.py"

REM Duplicate group: daae55f8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\filetypes.py
move "venv\Lib\site-packages\pip\_internal\utils\filetypes.py" "Archive\Duplicates\filetypes.py"

REM Duplicate group: bd495c93...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\glibc.py
move "venv\Lib\site-packages\pip\_internal\utils\glibc.py" "Archive\Duplicates\glibc.py"

REM Duplicate group: ea92f129...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\hashes.py
move "venv\Lib\site-packages\pip\_internal\utils\hashes.py" "Archive\Duplicates\hashes.py"

REM Duplicate group: 3f31f9f9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\inject_securetransport.py
move "venv\Lib\site-packages\pip\_internal\utils\inject_securetransport.py" "Archive\Duplicates\inject_securetransport.py"

REM Duplicate group: c3a7e62d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\logging.py
move "venv\Lib\site-packages\pip\_internal\utils\logging.py" "Archive\Duplicates\logging.py"

REM Duplicate group: 8ce480f4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\misc.py
move "venv\Lib\site-packages\pip\_internal\utils\misc.py" "Archive\Duplicates\misc.py"

REM Duplicate group: 2cec2380...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\models.py
move "venv\Lib\site-packages\pip\_internal\utils\models.py" "Archive\Duplicates\models.py"

REM Duplicate group: 44be67ad...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\packaging.py
move "venv\Lib\site-packages\pip\_internal\utils\packaging.py" "Archive\Duplicates\packaging.py"

REM Duplicate group: 9ae597ef...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\setuptools_build.py
move "venv\Lib\site-packages\pip\_internal\utils\setuptools_build.py" "Archive\Duplicates\setuptools_build.py"

REM Duplicate group: e9eb376c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\subprocess.py
move "venv\Lib\site-packages\pip\_internal\utils\subprocess.py" "Archive\Duplicates\subprocess.py"

REM Duplicate group: ea5a1ece...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\temp_dir.py
move "venv\Lib\site-packages\pip\_internal\utils\temp_dir.py" "Archive\Duplicates\temp_dir.py"

REM Duplicate group: 1f709c05...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\unpacking.py
move "venv\Lib\site-packages\pip\_internal\utils\unpacking.py" "Archive\Duplicates\unpacking.py"

REM Duplicate group: 918837f1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\urls.py
move "venv\Lib\site-packages\pip\_internal\utils\urls.py" "Archive\Duplicates\urls.py"

REM Duplicate group: 15111b45...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\virtualenv.py
move "venv\Lib\site-packages\pip\_internal\utils\virtualenv.py" "Archive\Duplicates\virtualenv.py"

REM Duplicate group: c8484c27...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\wheel.py
move "venv\Lib\site-packages\pip\_internal\utils\wheel.py" "Archive\Duplicates\wheel.py"

REM Duplicate group: ae014f7c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\_jaraco_text.py
move "venv\Lib\site-packages\pip\_internal\utils\_jaraco_text.py" "Archive\Duplicates\_jaraco_text.py"

REM Duplicate group: d525aebd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\utils\_log.py
move "venv\Lib\site-packages\pip\_internal\utils\_log.py" "Archive\Duplicates\_log.py"

REM Duplicate group: 6979f5f3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\bazaar.py
move "venv\Lib\site-packages\pip\_internal\vcs\bazaar.py" "Archive\Duplicates\bazaar.py"

REM Duplicate group: 564812e8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\git.py
move "venv\Lib\site-packages\pip\_internal\vcs\git.py" "Archive\Duplicates\git.py"

REM Duplicate group: 33139730...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\mercurial.py
move "venv\Lib\site-packages\pip\_internal\vcs\mercurial.py" "Archive\Duplicates\mercurial.py"

REM Duplicate group: 8e172102...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\subversion.py
move "venv\Lib\site-packages\pip\_internal\vcs\subversion.py" "Archive\Duplicates\subversion.py"

REM Duplicate group: bd929711...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py
move "venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py" "Archive\Duplicates\versioncontrol.py"

REM Duplicate group: eba6bd4a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\__init__.py
move "venv\Lib\site-packages\pip\_internal\vcs\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 9379cf68...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\six.py
move "venv\Lib\site-packages\pip\_vendor\six.py" "Archive\Duplicates\six.py"

REM Duplicate group: 894ccca4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\typing_extensions.py
move "venv\Lib\site-packages\pip\_vendor\typing_extensions.py" "Archive\Duplicates\typing_extensions.py"

REM Duplicate group: 1956f899...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\vendor.txt
move "venv\Lib\site-packages\pip\_vendor\vendor.txt" "Archive\Duplicates\vendor.txt"

REM Duplicate group: ff960210...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\__init__.py
move "venv\Lib\site-packages\pip\_vendor\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: a6a352c3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\adapter.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\adapter.py" "Archive\Duplicates\adapter.py"

REM Duplicate group: f5b45637...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\cache.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\cache.py" "Archive\Duplicates\cache.py"

REM Duplicate group: ac86eb36...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\compat.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\compat.py" "Archive\Duplicates\compat.py"

REM Duplicate group: 938d4a5e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py" "Archive\Duplicates\controller.py"

REM Duplicate group: a5b34487...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py" "Archive\Duplicates\filewrapper.py"

REM Duplicate group: 0ffe6dec...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py" "Archive\Duplicates\heuristics.py"

REM Duplicate group: 9253bd42...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\serialize.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\serialize.py" "Archive\Duplicates\serialize.py"

REM Duplicate group: 36005e57...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py" "Archive\Duplicates\wrapper.py"

REM Duplicate group: 38d8427c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\_cmd.py" "Archive\Duplicates\_cmd.py"

REM Duplicate group: 049c2d43...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\__init__.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 7ac1cf7b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py" "Archive\Duplicates\file_cache.py"

REM Duplicate group: 9bb77121...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\redis_cache.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\redis_cache.py" "Archive\Duplicates\redis_cache.py"

REM Duplicate group: d42a315b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__init__.py
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 59a15f9a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\certifi\cacert.pem
move "venv\Lib\site-packages\pip\_vendor\certifi\cacert.pem" "Archive\Duplicates\cacert.pem"

REM Duplicate group: be7f0b9c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\certifi\core.py
move "venv\Lib\site-packages\pip\_vendor\certifi\core.py" "Archive\Duplicates\core.py"

REM Duplicate group: 8975b791...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\certifi\__init__.py
move "venv\Lib\site-packages\pip\_vendor\certifi\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 49689cf4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\certifi\__main__.py
move "venv\Lib\site-packages\pip\_vendor\certifi\__main__.py" "Archive\Duplicates\__main__.py"

REM Duplicate group: 7a347287...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\big5freq.py
move "venv\Lib\site-packages\pip\_vendor\chardet\big5freq.py" "Archive\Duplicates\big5freq.py"

REM Duplicate group: 26ae8ad2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\big5prober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\big5prober.py" "Archive\Duplicates\big5prober.py"

REM Duplicate group: 6e27e858...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\chardistribution.py
move "venv\Lib\site-packages\pip\_vendor\chardet\chardistribution.py" "Archive\Duplicates\chardistribution.py"

REM Duplicate group: afd85e30...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\charsetgroupprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\charsetgroupprober.py" "Archive\Duplicates\charsetgroupprober.py"

REM Duplicate group: 075b00a4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\charsetprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\charsetprober.py" "Archive\Duplicates\charsetprober.py"

REM Duplicate group: 875d1512...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\codingstatemachine.py
move "venv\Lib\site-packages\pip\_vendor\chardet\codingstatemachine.py" "Archive\Duplicates\codingstatemachine.py"

REM Duplicate group: 9167badf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\codingstatemachinedict.py
move "venv\Lib\site-packages\pip\_vendor\chardet\codingstatemachinedict.py" "Archive\Duplicates\codingstatemachinedict.py"

REM Duplicate group: 08ba79a1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\cp949prober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\cp949prober.py" "Archive\Duplicates\cp949prober.py"

REM Duplicate group: 95ef7a9d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\enums.py
move "venv\Lib\site-packages\pip\_vendor\chardet\enums.py" "Archive\Duplicates\enums.py"

REM Duplicate group: fc0026dd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\escprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\escprober.py" "Archive\Duplicates\escprober.py"

REM Duplicate group: 695aacd8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\escsm.py
move "venv\Lib\site-packages\pip\_vendor\chardet\escsm.py" "Archive\Duplicates\escsm.py"

REM Duplicate group: d3202d07...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\eucjpprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\eucjpprober.py" "Archive\Duplicates\eucjpprober.py"

REM Duplicate group: ca57adf0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\euckrfreq.py
move "venv\Lib\site-packages\pip\_vendor\chardet\euckrfreq.py" "Archive\Duplicates\euckrfreq.py"

REM Duplicate group: d0884702...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\euckrprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\euckrprober.py" "Archive\Duplicates\euckrprober.py"

REM Duplicate group: 9547e6b9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\euctwfreq.py
move "venv\Lib\site-packages\pip\_vendor\chardet\euctwfreq.py" "Archive\Duplicates\euctwfreq.py"

REM Duplicate group: 544cffdf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\euctwprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\euctwprober.py" "Archive\Duplicates\euctwprober.py"

REM Duplicate group: 415a69cb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\gb2312freq.py
move "venv\Lib\site-packages\pip\_vendor\chardet\gb2312freq.py" "Archive\Duplicates\gb2312freq.py"

REM Duplicate group: cc03fe03...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\gb2312prober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\gb2312prober.py" "Archive\Duplicates\gb2312prober.py"

REM Duplicate group: 6bcd08ed...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\hebrewprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\hebrewprober.py" "Archive\Duplicates\hebrewprober.py"

REM Duplicate group: c2788319...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\jisfreq.py
move "venv\Lib\site-packages\pip\_vendor\chardet\jisfreq.py" "Archive\Duplicates\jisfreq.py"

REM Duplicate group: dcdaef14...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\johabfreq.py
move "venv\Lib\site-packages\pip\_vendor\chardet\johabfreq.py" "Archive\Duplicates\johabfreq.py"

REM Duplicate group: b75c1935...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\johabprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\johabprober.py" "Archive\Duplicates\johabprober.py"

REM Duplicate group: 6de3572a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\jpcntx.py
move "venv\Lib\site-packages\pip\_vendor\chardet\jpcntx.py" "Archive\Duplicates\jpcntx.py"

REM Duplicate group: de325c59...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langbulgarianmodel.py
move "venv\Lib\site-packages\pip\_vendor\chardet\langbulgarianmodel.py" "Archive\Duplicates\langbulgarianmodel.py"

REM Duplicate group: 99499edf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langgreekmodel.py
move "venv\Lib\site-packages\pip\_vendor\chardet\langgreekmodel.py" "Archive\Duplicates\langgreekmodel.py"

REM Duplicate group: 8091a0c9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langhebrewmodel.py
move "venv\Lib\site-packages\pip\_vendor\chardet\langhebrewmodel.py" "Archive\Duplicates\langhebrewmodel.py"

REM Duplicate group: 712b7a91...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langhungarianmodel.py
move "venv\Lib\site-packages\pip\_vendor\chardet\langhungarianmodel.py" "Archive\Duplicates\langhungarianmodel.py"

REM Duplicate group: f1dc1162...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langrussianmodel.py
move "venv\Lib\site-packages\pip\_vendor\chardet\langrussianmodel.py" "Archive\Duplicates\langrussianmodel.py"

REM Duplicate group: 7ddb0814...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langthaimodel.py
move "venv\Lib\site-packages\pip\_vendor\chardet\langthaimodel.py" "Archive\Duplicates\langthaimodel.py"

REM Duplicate group: 47ef8726...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langturkishmodel.py
move "venv\Lib\site-packages\pip\_vendor\chardet\langturkishmodel.py" "Archive\Duplicates\langturkishmodel.py"

REM Duplicate group: 9612208d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\latin1prober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\latin1prober.py" "Archive\Duplicates\latin1prober.py"

REM Duplicate group: 3c23bc2f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\macromanprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\macromanprober.py" "Archive\Duplicates\macromanprober.py"

REM Duplicate group: 704ee40b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\mbcharsetprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\mbcharsetprober.py" "Archive\Duplicates\mbcharsetprober.py"

REM Duplicate group: e553887a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\mbcsgroupprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\mbcsgroupprober.py" "Archive\Duplicates\mbcsgroupprober.py"

REM Duplicate group: c3fb17a5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\mbcssm.py
move "venv\Lib\site-packages\pip\_vendor\chardet\mbcssm.py" "Archive\Duplicates\mbcssm.py"

REM Duplicate group: 78bb0657...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\resultdict.py
move "venv\Lib\site-packages\pip\_vendor\chardet\resultdict.py" "Archive\Duplicates\resultdict.py"

REM Duplicate group: adda0d0c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\sbcharsetprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\sbcharsetprober.py" "Archive\Duplicates\sbcharsetprober.py"

REM Duplicate group: beaf119d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\sbcsgroupprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\sbcsgroupprober.py" "Archive\Duplicates\sbcsgroupprober.py"

REM Duplicate group: 0fe9125a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\sjisprober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\sjisprober.py" "Archive\Duplicates\sjisprober.py"

REM Duplicate group: be007f9a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\universaldetector.py
move "venv\Lib\site-packages\pip\_vendor\chardet\universaldetector.py" "Archive\Duplicates\universaldetector.py"

REM Duplicate group: 4d340602...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\utf1632prober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\utf1632prober.py" "Archive\Duplicates\utf1632prober.py"

REM Duplicate group: 6e9466a0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\utf8prober.py
move "venv\Lib\site-packages\pip\_vendor\chardet\utf8prober.py" "Archive\Duplicates\utf8prober.py"

REM Duplicate group: f1253f0b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\version.py
move "venv\Lib\site-packages\pip\_vendor\chardet\version.py" "Archive\Duplicates\version.py"

REM Duplicate group: 94ea57e8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\__init__.py
move "venv\Lib\site-packages\pip\_vendor\chardet\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 7fd01b5b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\cli\chardetect.py
move "venv\Lib\site-packages\pip\_vendor\chardet\cli\chardetect.py" "Archive\Duplicates\chardetect.py"

REM Duplicate group: 39c3f5bc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\metadata\languages.py
move "venv\Lib\site-packages\pip\_vendor\chardet\metadata\languages.py" "Archive\Duplicates\languages.py"

REM Duplicate group: 352a89fc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\compat.py
move "venv\Lib\site-packages\pip\_vendor\distlib\compat.py" "Archive\Duplicates\compat.py"

REM Duplicate group: eb27a633...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\database.py
move "venv\Lib\site-packages\pip\_vendor\distlib\database.py" "Archive\Duplicates\database.py"

REM Duplicate group: b409a76e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\index.py
move "venv\Lib\site-packages\pip\_vendor\distlib\index.py" "Archive\Duplicates\index.py"

REM Duplicate group: 6364d230...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\locators.py
move "venv\Lib\site-packages\pip\_vendor\distlib\locators.py" "Archive\Duplicates\locators.py"

REM Duplicate group: 8fd3bf94...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\manifest.py
move "venv\Lib\site-packages\pip\_vendor\distlib\manifest.py" "Archive\Duplicates\manifest.py"

REM Duplicate group: 3c45ca46...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\markers.py
move "venv\Lib\site-packages\pip\_vendor\distlib\markers.py" "Archive\Duplicates\markers.py"

REM Duplicate group: 06646e79...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\metadata.py
move "venv\Lib\site-packages\pip\_vendor\distlib\metadata.py" "Archive\Duplicates\metadata.py"

REM Duplicate group: 669a6548...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\resources.py
move "venv\Lib\site-packages\pip\_vendor\distlib\resources.py" "Archive\Duplicates\resources.py"

REM Duplicate group: 330056e1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\scripts.py
move "venv\Lib\site-packages\pip\_vendor\distlib\scripts.py" "Archive\Duplicates\scripts.py"

REM Duplicate group: 07894acc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\t32.exe
move "venv\Lib\site-packages\pip\_vendor\distlib\t32.exe" "Archive\Duplicates\t32.exe"

REM Duplicate group: f4935e39...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\t64-arm.exe
move "venv\Lib\site-packages\pip\_vendor\distlib\t64-arm.exe" "Archive\Duplicates\t64-arm.exe"

REM Duplicate group: 19d621a4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\t64.exe
move "venv\Lib\site-packages\pip\_vendor\distlib\t64.exe" "Archive\Duplicates\t64.exe"

REM Duplicate group: adb1ea8a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\util.py
move "venv\Lib\site-packages\pip\_vendor\distlib\util.py" "Archive\Duplicates\util.py"

REM Duplicate group: 5b21e9bc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\version.py
move "venv\Lib\site-packages\pip\_vendor\distlib\version.py" "Archive\Duplicates\version.py"

REM Duplicate group: 2e91e902...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\w32.exe
move "venv\Lib\site-packages\pip\_vendor\distlib\w32.exe" "Archive\Duplicates\w32.exe"

REM Duplicate group: 79ef49f5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\w64-arm.exe
move "venv\Lib\site-packages\pip\_vendor\distlib\w64-arm.exe" "Archive\Duplicates\w64-arm.exe"

REM Duplicate group: d65d7ad7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\w64.exe
move "venv\Lib\site-packages\pip\_vendor\distlib\w64.exe" "Archive\Duplicates\w64.exe"

REM Duplicate group: c5f3304e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\wheel.py
move "venv\Lib\site-packages\pip\_vendor\distlib\wheel.py" "Archive\Duplicates\wheel.py"

REM Duplicate group: eb05f9ac...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\__init__.py
move "venv\Lib\site-packages\pip\_vendor\distlib\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 32070f03...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distro\distro.py
move "venv\Lib\site-packages\pip\_vendor\distro\distro.py" "Archive\Duplicates\distro.py"

REM Duplicate group: 5b9b7efb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distro\__init__.py
move "venv\Lib\site-packages\pip\_vendor\distro\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 9ba2b2b4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\distro\__main__.py
move "venv\Lib\site-packages\pip\_vendor\distro\__main__.py" "Archive\Duplicates\__main__.py"

REM Duplicate group: 5c337705...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\codec.py
move "venv\Lib\site-packages\pip\_vendor\idna\codec.py" "Archive\Duplicates\codec.py"

REM Duplicate group: f1fb109a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\compat.py
move "venv\Lib\site-packages\pip\_vendor\idna\compat.py" "Archive\Duplicates\compat.py"

REM Duplicate group: 437556ef...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\core.py
move "venv\Lib\site-packages\pip\_vendor\idna\core.py" "Archive\Duplicates\core.py"

REM Duplicate group: 4c7d5f44...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\idnadata.py
move "venv\Lib\site-packages\pip\_vendor\idna\idnadata.py" "Archive\Duplicates\idnadata.py"

REM Duplicate group: f67c377c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\intranges.py
move "venv\Lib\site-packages\pip\_vendor\idna\intranges.py" "Archive\Duplicates\intranges.py"

REM Duplicate group: ea29a1cf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\package_data.py
move "venv\Lib\site-packages\pip\_vendor\idna\package_data.py" "Archive\Duplicates\package_data.py"

REM Duplicate group: 54f2b594...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\uts46data.py
move "venv\Lib\site-packages\pip\_vendor\idna\uts46data.py" "Archive\Duplicates\uts46data.py"

REM Duplicate group: 3159dcdf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\__init__.py
move "venv\Lib\site-packages\pip\_vendor\idna\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 741a3304...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\msgpack\exceptions.py
move "venv\Lib\site-packages\pip\_vendor\msgpack\exceptions.py" "Archive\Duplicates\exceptions.py"

REM Duplicate group: 5b76079b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\msgpack\ext.py
move "venv\Lib\site-packages\pip\_vendor\msgpack\ext.py" "Archive\Duplicates\ext.py"

REM Duplicate group: 3a2ed7c2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\msgpack\fallback.py
move "venv\Lib\site-packages\pip\_vendor\msgpack\fallback.py" "Archive\Duplicates\fallback.py"

REM Duplicate group: ad506184...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\msgpack\__init__.py
move "venv\Lib\site-packages\pip\_vendor\msgpack\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 54536dff...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\markers.py
move "venv\Lib\site-packages\pip\_vendor\packaging\markers.py" "Archive\Duplicates\markers.py"

REM Duplicate group: 04b21f77...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\requirements.py
move "venv\Lib\site-packages\pip\_vendor\packaging\requirements.py" "Archive\Duplicates\requirements.py"

REM Duplicate group: 7acafe40...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\specifiers.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\specifiers.py" "Archive\Duplicates\specifiers.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\specifiers.py" "Archive\Duplicates\specifiers.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\specifiers.py" "Archive\Duplicates\specifiers.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\specifiers.py" "Archive\Duplicates\specifiers.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\specifiers.py" "Archive\Duplicates\specifiers.py"

REM Duplicate group: e38b0468...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\tags.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\tags.py" "Archive\Duplicates\tags.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\tags.py" "Archive\Duplicates\tags.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\tags.py" "Archive\Duplicates\tags.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\tags.py" "Archive\Duplicates\tags.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\tags.py" "Archive\Duplicates\tags.py"

REM Duplicate group: 35929626...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\utils.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\utils.py" "Archive\Duplicates\utils.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\utils.py" "Archive\Duplicates\utils.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\utils.py" "Archive\Duplicates\utils.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\utils.py" "Archive\Duplicates\utils.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\utils.py" "Archive\Duplicates\utils.py"

REM Duplicate group: 8fb00e72...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\version.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\version.py" "Archive\Duplicates\version.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\version.py" "Archive\Duplicates\version.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\version.py" "Archive\Duplicates\version.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\version.py" "Archive\Duplicates\version.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\version.py" "Archive\Duplicates\version.py"

REM Duplicate group: 80df840e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\_manylinux.py" "Archive\Duplicates\_manylinux.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\_manylinux.py" "Archive\Duplicates\_manylinux.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py" "Archive\Duplicates\_manylinux.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\_manylinux.py" "Archive\Duplicates\_manylinux.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\_manylinux.py" "Archive\Duplicates\_manylinux.py"

REM Duplicate group: 0210636e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\_musllinux.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\_musllinux.py" "Archive\Duplicates\_musllinux.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\_musllinux.py" "Archive\Duplicates\_musllinux.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\_musllinux.py" "Archive\Duplicates\_musllinux.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\_musllinux.py" "Archive\Duplicates\_musllinux.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\_musllinux.py" "Archive\Duplicates\_musllinux.py"

REM Duplicate group: 68d5fc8a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\__about__.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\__about__.py" "Archive\Duplicates\__about__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\__about__.py" "Archive\Duplicates\__about__.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\__about__.py" "Archive\Duplicates\__about__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\__about__.py" "Archive\Duplicates\__about__.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\__about__.py" "Archive\Duplicates\__about__.py"

REM Duplicate group: b85796f8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\__init__.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\__init__.py" "Archive\Duplicates\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: b46dafde...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 8996cc44...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\android.py
move "venv\Lib\site-packages\pip\_vendor\platformdirs\android.py" "Archive\Duplicates\android.py"

REM Duplicate group: e7023d06...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\api.py
move "venv\Lib\site-packages\pip\_vendor\platformdirs\api.py" "Archive\Duplicates\api.py"

REM Duplicate group: f5ad7696...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py
move "venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py" "Archive\Duplicates\macos.py"

REM Duplicate group: e38f8d17...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\unix.py
move "venv\Lib\site-packages\pip\_vendor\platformdirs\unix.py" "Archive\Duplicates\unix.py"

REM Duplicate group: b766c417...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\version.py
move "venv\Lib\site-packages\pip\_vendor\platformdirs\version.py" "Archive\Duplicates\version.py"

REM Duplicate group: ed0fa0da...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\windows.py
move "venv\Lib\site-packages\pip\_vendor\platformdirs\windows.py" "Archive\Duplicates\windows.py"

REM Duplicate group: 31053c71...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py
move "venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 07b8ba17...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\__main__.py
move "venv\Lib\site-packages\pip\_vendor\platformdirs\__main__.py" "Archive\Duplicates\__main__.py"

REM Duplicate group: f2bca974...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\cmdline.py
move "venv\Lib\site-packages\pip\_vendor\pygments\cmdline.py" "Archive\Duplicates\cmdline.py"

REM Duplicate group: 90add264...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\console.py
move "venv\Lib\site-packages\pip\_vendor\pygments\console.py" "Archive\Duplicates\console.py"

REM Duplicate group: fcfaa131...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\filter.py
move "venv\Lib\site-packages\pip\_vendor\pygments\filter.py" "Archive\Duplicates\filter.py"

REM Duplicate group: 54f253fd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatter.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatter.py" "Archive\Duplicates\formatter.py"

REM Duplicate group: 72d9cd1a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\lexer.py
move "venv\Lib\site-packages\pip\_vendor\pygments\lexer.py" "Archive\Duplicates\lexer.py"

REM Duplicate group: da1ec0a8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\modeline.py
move "venv\Lib\site-packages\pip\_vendor\pygments\modeline.py" "Archive\Duplicates\modeline.py"

REM Duplicate group: 0f021950...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\plugin.py
move "venv\Lib\site-packages\pip\_vendor\pygments\plugin.py" "Archive\Duplicates\plugin.py"

REM Duplicate group: da7fa8a5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\regexopt.py
move "venv\Lib\site-packages\pip\_vendor\pygments\regexopt.py" "Archive\Duplicates\regexopt.py"

REM Duplicate group: 04bec5b0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\scanner.py
move "venv\Lib\site-packages\pip\_vendor\pygments\scanner.py" "Archive\Duplicates\scanner.py"

REM Duplicate group: 7380596c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\sphinxext.py
move "venv\Lib\site-packages\pip\_vendor\pygments\sphinxext.py" "Archive\Duplicates\sphinxext.py"

REM Duplicate group: d9392569...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\style.py
move "venv\Lib\site-packages\pip\_vendor\pygments\style.py" "Archive\Duplicates\style.py"

REM Duplicate group: b64ad1ec...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\token.py
move "venv\Lib\site-packages\pip\_vendor\pygments\token.py" "Archive\Duplicates\token.py"

REM Duplicate group: 1e93f2c6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\unistring.py
move "venv\Lib\site-packages\pip\_vendor\pygments\unistring.py" "Archive\Duplicates\unistring.py"

REM Duplicate group: c038afec...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\util.py
move "venv\Lib\site-packages\pip\_vendor\pygments\util.py" "Archive\Duplicates\util.py"

REM Duplicate group: 0c50ad35...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pygments\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: a0c094e4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\__main__.py
move "venv\Lib\site-packages\pip\_vendor\pygments\__main__.py" "Archive\Duplicates\__main__.py"

REM Duplicate group: bf85a1a3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 80063ae7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\bbcode.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\bbcode.py" "Archive\Duplicates\bbcode.py"

REM Duplicate group: 94583bcf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\groff.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\groff.py" "Archive\Duplicates\groff.py"

REM Duplicate group: 2ae51866...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\html.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\html.py" "Archive\Duplicates\html.py"

REM Duplicate group: 274c5490...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\img.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\img.py" "Archive\Duplicates\img.py"

REM Duplicate group: c2108247...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\irc.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\irc.py" "Archive\Duplicates\irc.py"

REM Duplicate group: 4b9ae57b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\latex.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\latex.py" "Archive\Duplicates\latex.py"

REM Duplicate group: 0173e1f8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\other.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\other.py" "Archive\Duplicates\other.py"

REM Duplicate group: ac3be3bb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\pangomarkup.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\pangomarkup.py" "Archive\Duplicates\pangomarkup.py"

REM Duplicate group: 688ccb93...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\rtf.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\rtf.py" "Archive\Duplicates\rtf.py"

REM Duplicate group: 5eb511ce...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\svg.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\svg.py" "Archive\Duplicates\svg.py"

REM Duplicate group: 69320fd9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\terminal.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\terminal.py" "Archive\Duplicates\terminal.py"

REM Duplicate group: 35b6d850...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\terminal256.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\terminal256.py" "Archive\Duplicates\terminal256.py"

REM Duplicate group: 678f14d9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\_mapping.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\_mapping.py" "Archive\Duplicates\_mapping.py"

REM Duplicate group: 1db7a639...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 5e567c17...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py
move "venv\Lib\site-packages\pip\_vendor\pygments\lexers\python.py" "Archive\Duplicates\python.py"

REM Duplicate group: 6cbdc6b4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\lexers\_mapping.py
move "venv\Lib\site-packages\pip\_vendor\pygments\lexers\_mapping.py" "Archive\Duplicates\_mapping.py"

REM Duplicate group: ef80b7f9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\lexers\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pygments\lexers\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: a99e5813...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 146786b5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\actions.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\actions.py" "Archive\Duplicates\actions.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\actions.py" "Archive\Duplicates\actions.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\actions.py" "Archive\Duplicates\actions.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\actions.py" "Archive\Duplicates\actions.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\actions.py" "Archive\Duplicates\actions.py"

REM Duplicate group: 01204205...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\common.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\common.py" "Archive\Duplicates\common.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\common.py" "Archive\Duplicates\common.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\common.py" "Archive\Duplicates\common.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\common.py" "Archive\Duplicates\common.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\common.py" "Archive\Duplicates\common.py"

REM Duplicate group: 9a7cad2c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\core.py
move "venv\Lib\site-packages\pip\_vendor\pyparsing\core.py" "Archive\Duplicates\core.py"

REM Duplicate group: f1f31bb0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\exceptions.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\exceptions.py" "Archive\Duplicates\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\exceptions.py" "Archive\Duplicates\exceptions.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\exceptions.py" "Archive\Duplicates\exceptions.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\exceptions.py" "Archive\Duplicates\exceptions.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\exceptions.py" "Archive\Duplicates\exceptions.py"

REM Duplicate group: 74ecbf6f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\helpers.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\helpers.py" "Archive\Duplicates\helpers.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\helpers.py" "Archive\Duplicates\helpers.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\helpers.py" "Archive\Duplicates\helpers.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\helpers.py" "Archive\Duplicates\helpers.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\helpers.py" "Archive\Duplicates\helpers.py"

REM Duplicate group: 96e34a81...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\results.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\results.py" "Archive\Duplicates\results.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\results.py" "Archive\Duplicates\results.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\results.py" "Archive\Duplicates\results.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\results.py" "Archive\Duplicates\results.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\results.py" "Archive\Duplicates\results.py"

REM Duplicate group: 5e9b66d2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\testing.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\testing.py" "Archive\Duplicates\testing.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\testing.py" "Archive\Duplicates\testing.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\testing.py" "Archive\Duplicates\testing.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\testing.py" "Archive\Duplicates\testing.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\testing.py" "Archive\Duplicates\testing.py"

REM Duplicate group: c9b7c7bb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\unicode.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\unicode.py" "Archive\Duplicates\unicode.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\unicode.py" "Archive\Duplicates\unicode.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\unicode.py" "Archive\Duplicates\unicode.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\unicode.py" "Archive\Duplicates\unicode.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\unicode.py" "Archive\Duplicates\unicode.py"

REM Duplicate group: e2b2a337...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\util.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\util.py" "Archive\Duplicates\util.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\util.py" "Archive\Duplicates\util.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\util.py" "Archive\Duplicates\util.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\util.py" "Archive\Duplicates\util.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\util.py" "Archive\Duplicates\util.py"

REM Duplicate group: d9b69962...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pyparsing\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: e3c2c212...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\diagram\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pyparsing\diagram\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 6d627346...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_compat.py
move "venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_compat.py" "Archive\Duplicates\_compat.py"

REM Duplicate group: 7006214c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py
move "venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_impl.py" "Archive\Duplicates\_impl.py"

REM Duplicate group: 80c06109...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyproject_hooks\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pyproject_hooks\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 4d0d470c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py
move "venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\_in_process.py" "Archive\Duplicates\_in_process.py"

REM Duplicate group: 44ae0a51...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\__init__.py
move "venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: f03a9cf5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\adapters.py
move "venv\Lib\site-packages\pip\_vendor\requests\adapters.py" "Archive\Duplicates\adapters.py"

REM Duplicate group: 85eefa4b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\api.py
move "venv\Lib\site-packages\pip\_vendor\requests\api.py" "Archive\Duplicates\api.py"

REM Duplicate group: f9967d6b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\auth.py
move "venv\Lib\site-packages\pip\_vendor\requests\auth.py" "Archive\Duplicates\auth.py"

REM Duplicate group: 9479d3b9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\certs.py
move "venv\Lib\site-packages\pip\_vendor\requests\certs.py" "Archive\Duplicates\certs.py"

REM Duplicate group: 48ec2c85...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\compat.py
move "venv\Lib\site-packages\pip\_vendor\requests\compat.py" "Archive\Duplicates\compat.py"

REM Duplicate group: 91b27fbf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\cookies.py
move "venv\Lib\site-packages\pip\_vendor\requests\cookies.py" "Archive\Duplicates\cookies.py"

REM Duplicate group: 312e2f64...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\exceptions.py
move "venv\Lib\site-packages\pip\_vendor\requests\exceptions.py" "Archive\Duplicates\exceptions.py"

REM Duplicate group: 225866fa...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\help.py
move "venv\Lib\site-packages\pip\_vendor\requests\help.py" "Archive\Duplicates\help.py"

REM Duplicate group: 94eb2900...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\hooks.py
move "venv\Lib\site-packages\pip\_vendor\requests\hooks.py" "Archive\Duplicates\hooks.py"
move "venv\Lib\site-packages\requests\hooks.py" "Archive\Duplicates\hooks.py"

REM Duplicate group: ecc41965...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\models.py
move "venv\Lib\site-packages\pip\_vendor\requests\models.py" "Archive\Duplicates\models.py"

REM Duplicate group: 4f61660b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\packages.py
move "venv\Lib\site-packages\pip\_vendor\requests\packages.py" "Archive\Duplicates\packages.py"

REM Duplicate group: b687828a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\sessions.py
move "venv\Lib\site-packages\pip\_vendor\requests\sessions.py" "Archive\Duplicates\sessions.py"

REM Duplicate group: 663dd9e4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\status_codes.py
move "venv\Lib\site-packages\pip\_vendor\requests\status_codes.py" "Archive\Duplicates\status_codes.py"

REM Duplicate group: 07794891...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\structures.py
move "venv\Lib\site-packages\pip\_vendor\requests\structures.py" "Archive\Duplicates\structures.py"
move "venv\Lib\site-packages\requests\structures.py" "Archive\Duplicates\structures.py"

REM Duplicate group: 82ba0c7e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\utils.py
move "venv\Lib\site-packages\pip\_vendor\requests\utils.py" "Archive\Duplicates\utils.py"

REM Duplicate group: 7772cb60...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\_internal_utils.py
move "venv\Lib\site-packages\pip\_vendor\requests\_internal_utils.py" "Archive\Duplicates\_internal_utils.py"

REM Duplicate group: 6d78dc47...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\__init__.py
move "venv\Lib\site-packages\pip\_vendor\requests\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 99217e33...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\__version__.py
move "venv\Lib\site-packages\pip\_vendor\requests\__version__.py" "Archive\Duplicates\__version__.py"

REM Duplicate group: 665e6250...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\providers.py
move "venv\Lib\site-packages\pip\_vendor\resolvelib\providers.py" "Archive\Duplicates\providers.py"

REM Duplicate group: 5bf3f0bf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\reporters.py
move "venv\Lib\site-packages\pip\_vendor\resolvelib\reporters.py" "Archive\Duplicates\reporters.py"

REM Duplicate group: 63876928...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers.py
move "venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers.py" "Archive\Duplicates\resolvers.py"

REM Duplicate group: 1de4b6ff...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\structs.py
move "venv\Lib\site-packages\pip\_vendor\resolvelib\structs.py" "Archive\Duplicates\structs.py"

REM Duplicate group: 8b67527e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\__init__.py
move "venv\Lib\site-packages\pip\_vendor\resolvelib\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 8ccca912...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\compat\collections_abc.py
move "venv\Lib\site-packages\pip\_vendor\resolvelib\compat\collections_abc.py" "Archive\Duplicates\collections_abc.py"

REM Duplicate group: 39d8c0ac...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\abc.py
move "venv\Lib\site-packages\pip\_vendor\rich\abc.py" "Archive\Duplicates\abc.py"

REM Duplicate group: e68e4dcd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\align.py
move "venv\Lib\site-packages\pip\_vendor\rich\align.py" "Archive\Duplicates\align.py"

REM Duplicate group: 90cf20a4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\ansi.py
move "venv\Lib\site-packages\pip\_vendor\rich\ansi.py" "Archive\Duplicates\ansi.py"

REM Duplicate group: 48b51f3a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\bar.py
move "venv\Lib\site-packages\pip\_vendor\rich\bar.py" "Archive\Duplicates\bar.py"

REM Duplicate group: 30023d8c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\box.py
move "venv\Lib\site-packages\pip\_vendor\rich\box.py" "Archive\Duplicates\box.py"

REM Duplicate group: a36f45d4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\cells.py
move "venv\Lib\site-packages\pip\_vendor\rich\cells.py" "Archive\Duplicates\cells.py"

REM Duplicate group: 47ab433f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\color.py
move "venv\Lib\site-packages\pip\_vendor\rich\color.py" "Archive\Duplicates\color.py"

REM Duplicate group: 9f03fdec...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\color_triplet.py
move "venv\Lib\site-packages\pip\_vendor\rich\color_triplet.py" "Archive\Duplicates\color_triplet.py"
move "venv\Lib\site-packages\rich\color_triplet.py" "Archive\Duplicates\color_triplet.py"

REM Duplicate group: d32c7ef4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\columns.py
move "venv\Lib\site-packages\pip\_vendor\rich\columns.py" "Archive\Duplicates\columns.py"
move "venv\Lib\site-packages\rich\columns.py" "Archive\Duplicates\columns.py"

REM Duplicate group: 9c564450...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\console.py
move "venv\Lib\site-packages\pip\_vendor\rich\console.py" "Archive\Duplicates\console.py"

REM Duplicate group: cef54cef...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\constrain.py
move "venv\Lib\site-packages\pip\_vendor\rich\constrain.py" "Archive\Duplicates\constrain.py"
move "venv\Lib\site-packages\rich\constrain.py" "Archive\Duplicates\constrain.py"

REM Duplicate group: 9c40b402...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\containers.py
move "venv\Lib\site-packages\pip\_vendor\rich\containers.py" "Archive\Duplicates\containers.py"

REM Duplicate group: 7433e137...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\control.py
move "venv\Lib\site-packages\pip\_vendor\rich\control.py" "Archive\Duplicates\control.py"

REM Duplicate group: 7042e55f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\default_styles.py
move "venv\Lib\site-packages\pip\_vendor\rich\default_styles.py" "Archive\Duplicates\default_styles.py"

REM Duplicate group: 406e905b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\diagnose.py
move "venv\Lib\site-packages\pip\_vendor\rich\diagnose.py" "Archive\Duplicates\diagnose.py"

REM Duplicate group: e82e259f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\emoji.py
move "venv\Lib\site-packages\pip\_vendor\rich\emoji.py" "Archive\Duplicates\emoji.py"

REM Duplicate group: b7ed3594...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\errors.py
move "venv\Lib\site-packages\pip\_vendor\rich\errors.py" "Archive\Duplicates\errors.py"
move "venv\Lib\site-packages\rich\errors.py" "Archive\Duplicates\errors.py"

REM Duplicate group: afa45bb4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\filesize.py
move "venv\Lib\site-packages\pip\_vendor\rich\filesize.py" "Archive\Duplicates\filesize.py"

REM Duplicate group: eedd79e9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\file_proxy.py
move "venv\Lib\site-packages\pip\_vendor\rich\file_proxy.py" "Archive\Duplicates\file_proxy.py"
move "venv\Lib\site-packages\rich\file_proxy.py" "Archive\Duplicates\file_proxy.py"

REM Duplicate group: 15b3201b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\highlighter.py
move "venv\Lib\site-packages\pip\_vendor\rich\highlighter.py" "Archive\Duplicates\highlighter.py"

REM Duplicate group: 7fba872a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\json.py
move "venv\Lib\site-packages\pip\_vendor\rich\json.py" "Archive\Duplicates\json.py"

REM Duplicate group: cce8f456...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\jupyter.py
move "venv\Lib\site-packages\pip\_vendor\rich\jupyter.py" "Archive\Duplicates\jupyter.py"

REM Duplicate group: fed3d43a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\layout.py
move "venv\Lib\site-packages\pip\_vendor\rich\layout.py" "Archive\Duplicates\layout.py"

REM Duplicate group: e1a37b96...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\live.py
move "venv\Lib\site-packages\pip\_vendor\rich\live.py" "Archive\Duplicates\live.py"

REM Duplicate group: f0037cf6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\live_render.py
move "venv\Lib\site-packages\pip\_vendor\rich\live_render.py" "Archive\Duplicates\live_render.py"

REM Duplicate group: 0c56aec2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\logging.py
move "venv\Lib\site-packages\pip\_vendor\rich\logging.py" "Archive\Duplicates\logging.py"

REM Duplicate group: 76b015db...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\markup.py
move "venv\Lib\site-packages\pip\_vendor\rich\markup.py" "Archive\Duplicates\markup.py"

REM Duplicate group: 9a85d7d3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\measure.py
move "venv\Lib\site-packages\pip\_vendor\rich\measure.py" "Archive\Duplicates\measure.py"
move "venv\Lib\site-packages\rich\measure.py" "Archive\Duplicates\measure.py"

REM Duplicate group: a5009662...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\padding.py
move "venv\Lib\site-packages\pip\_vendor\rich\padding.py" "Archive\Duplicates\padding.py"

REM Duplicate group: d2f3f5a5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\pager.py
move "venv\Lib\site-packages\pip\_vendor\rich\pager.py" "Archive\Duplicates\pager.py"
move "venv\Lib\site-packages\rich\pager.py" "Archive\Duplicates\pager.py"

REM Duplicate group: d604e236...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\palette.py
move "venv\Lib\site-packages\pip\_vendor\rich\palette.py" "Archive\Duplicates\palette.py"

REM Duplicate group: 2f4c4176...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\panel.py
move "venv\Lib\site-packages\pip\_vendor\rich\panel.py" "Archive\Duplicates\panel.py"

REM Duplicate group: da8356fd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\pretty.py
move "venv\Lib\site-packages\pip\_vendor\rich\pretty.py" "Archive\Duplicates\pretty.py"

REM Duplicate group: 45d63a8c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\progress.py
move "venv\Lib\site-packages\pip\_vendor\rich\progress.py" "Archive\Duplicates\progress.py"

REM Duplicate group: 33f2e24b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\progress_bar.py
move "venv\Lib\site-packages\pip\_vendor\rich\progress_bar.py" "Archive\Duplicates\progress_bar.py"

REM Duplicate group: e0281226...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\prompt.py
move "venv\Lib\site-packages\pip\_vendor\rich\prompt.py" "Archive\Duplicates\prompt.py"

REM Duplicate group: eccf6e36...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\protocol.py
move "venv\Lib\site-packages\pip\_vendor\rich\protocol.py" "Archive\Duplicates\protocol.py"

REM Duplicate group: 2b7a3fc1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\region.py
move "venv\Lib\site-packages\pip\_vendor\rich\region.py" "Archive\Duplicates\region.py"
move "venv\Lib\site-packages\rich\region.py" "Archive\Duplicates\region.py"

REM Duplicate group: e06a7dd7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\repr.py
move "venv\Lib\site-packages\pip\_vendor\rich\repr.py" "Archive\Duplicates\repr.py"

REM Duplicate group: 790460de...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\rule.py
move "venv\Lib\site-packages\pip\_vendor\rich\rule.py" "Archive\Duplicates\rule.py"

REM Duplicate group: e079470d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\scope.py
move "venv\Lib\site-packages\pip\_vendor\rich\scope.py" "Archive\Duplicates\scope.py"

REM Duplicate group: 0c196d1d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\screen.py
move "venv\Lib\site-packages\pip\_vendor\rich\screen.py" "Archive\Duplicates\screen.py"

REM Duplicate group: 7daf763b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\segment.py
move "venv\Lib\site-packages\pip\_vendor\rich\segment.py" "Archive\Duplicates\segment.py"

REM Duplicate group: 1709acb3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\spinner.py
move "venv\Lib\site-packages\pip\_vendor\rich\spinner.py" "Archive\Duplicates\spinner.py"

REM Duplicate group: 3d1772b4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\status.py
move "venv\Lib\site-packages\pip\_vendor\rich\status.py" "Archive\Duplicates\status.py"

REM Duplicate group: 7c60a5c7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\style.py
move "venv\Lib\site-packages\pip\_vendor\rich\style.py" "Archive\Duplicates\style.py"

REM Duplicate group: 9525ec56...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\styled.py
move "venv\Lib\site-packages\pip\_vendor\rich\styled.py" "Archive\Duplicates\styled.py"

REM Duplicate group: 4be167b7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\syntax.py
move "venv\Lib\site-packages\pip\_vendor\rich\syntax.py" "Archive\Duplicates\syntax.py"

REM Duplicate group: 7aaf0f31...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\table.py
move "venv\Lib\site-packages\pip\_vendor\rich\table.py" "Archive\Duplicates\table.py"

REM Duplicate group: 26697a91...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\terminal_theme.py
move "venv\Lib\site-packages\pip\_vendor\rich\terminal_theme.py" "Archive\Duplicates\terminal_theme.py"
move "venv\Lib\site-packages\rich\terminal_theme.py" "Archive\Duplicates\terminal_theme.py"

REM Duplicate group: fb2f51fd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\text.py
move "venv\Lib\site-packages\pip\_vendor\rich\text.py" "Archive\Duplicates\text.py"

REM Duplicate group: 2c48cef3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\theme.py
move "venv\Lib\site-packages\pip\_vendor\rich\theme.py" "Archive\Duplicates\theme.py"

REM Duplicate group: 579b6ab8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\themes.py
move "venv\Lib\site-packages\pip\_vendor\rich\themes.py" "Archive\Duplicates\themes.py"
move "venv\Lib\site-packages\rich\themes.py" "Archive\Duplicates\themes.py"

REM Duplicate group: 97cab9ce...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\traceback.py
move "venv\Lib\site-packages\pip\_vendor\rich\traceback.py" "Archive\Duplicates\traceback.py"

REM Duplicate group: 04b17aaf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\tree.py
move "venv\Lib\site-packages\pip\_vendor\rich\tree.py" "Archive\Duplicates\tree.py"

REM Duplicate group: 291ed6df...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_cell_widths.py
move "venv\Lib\site-packages\pip\_vendor\rich\_cell_widths.py" "Archive\Duplicates\_cell_widths.py"

REM Duplicate group: ee5b0bcd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_emoji_codes.py
move "venv\Lib\site-packages\pip\_vendor\rich\_emoji_codes.py" "Archive\Duplicates\_emoji_codes.py"
move "venv\Lib\site-packages\rich\_emoji_codes.py" "Archive\Duplicates\_emoji_codes.py"

REM Duplicate group: aa906731...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_emoji_replace.py
move "venv\Lib\site-packages\pip\_vendor\rich\_emoji_replace.py" "Archive\Duplicates\_emoji_replace.py"
move "venv\Lib\site-packages\rich\_emoji_replace.py" "Archive\Duplicates\_emoji_replace.py"

REM Duplicate group: c8bb53a3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_export_format.py
move "venv\Lib\site-packages\pip\_vendor\rich\_export_format.py" "Archive\Duplicates\_export_format.py"

REM Duplicate group: 7977cd94...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_extension.py
move "venv\Lib\site-packages\pip\_vendor\rich\_extension.py" "Archive\Duplicates\_extension.py"

REM Duplicate group: fa1ea276...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_fileno.py
move "venv\Lib\site-packages\pip\_vendor\rich\_fileno.py" "Archive\Duplicates\_fileno.py"
move "venv\Lib\site-packages\rich\_fileno.py" "Archive\Duplicates\_fileno.py"

REM Duplicate group: 22804d52...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_inspect.py
move "venv\Lib\site-packages\pip\_vendor\rich\_inspect.py" "Archive\Duplicates\_inspect.py"

REM Duplicate group: fa18d80f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_log_render.py
move "venv\Lib\site-packages\pip\_vendor\rich\_log_render.py" "Archive\Duplicates\_log_render.py"

REM Duplicate group: cb02e73e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_loop.py
move "venv\Lib\site-packages\pip\_vendor\rich\_loop.py" "Archive\Duplicates\_loop.py"
move "venv\Lib\site-packages\rich\_loop.py" "Archive\Duplicates\_loop.py"

REM Duplicate group: 7275da3b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_null_file.py
move "venv\Lib\site-packages\pip\_vendor\rich\_null_file.py" "Archive\Duplicates\_null_file.py"

REM Duplicate group: e16fbfbe...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_palettes.py
move "venv\Lib\site-packages\pip\_vendor\rich\_palettes.py" "Archive\Duplicates\_palettes.py"
move "venv\Lib\site-packages\rich\_palettes.py" "Archive\Duplicates\_palettes.py"

REM Duplicate group: 285ad4f0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_pick.py
move "venv\Lib\site-packages\pip\_vendor\rich\_pick.py" "Archive\Duplicates\_pick.py"
move "venv\Lib\site-packages\rich\_pick.py" "Archive\Duplicates\_pick.py"

REM Duplicate group: 6cbb7e0a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_ratio.py
move "venv\Lib\site-packages\pip\_vendor\rich\_ratio.py" "Archive\Duplicates\_ratio.py"

REM Duplicate group: 5dbf3829...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_spinners.py
move "venv\Lib\site-packages\pip\_vendor\rich\_spinners.py" "Archive\Duplicates\_spinners.py"
move "venv\Lib\site-packages\rich\_spinners.py" "Archive\Duplicates\_spinners.py"

REM Duplicate group: dc38e75c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_stack.py
move "venv\Lib\site-packages\pip\_vendor\rich\_stack.py" "Archive\Duplicates\_stack.py"
move "venv\Lib\site-packages\rich\_stack.py" "Archive\Duplicates\_stack.py"

REM Duplicate group: ae430575...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_timer.py
move "venv\Lib\site-packages\pip\_vendor\rich\_timer.py" "Archive\Duplicates\_timer.py"
move "venv\Lib\site-packages\rich\_timer.py" "Archive\Duplicates\_timer.py"

REM Duplicate group: 5c80e352...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py
move "venv\Lib\site-packages\pip\_vendor\rich\_win32_console.py" "Archive\Duplicates\_win32_console.py"

REM Duplicate group: ab18c7f0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_windows.py
move "venv\Lib\site-packages\pip\_vendor\rich\_windows.py" "Archive\Duplicates\_windows.py"

REM Duplicate group: 0f359f6a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_windows_renderer.py
move "venv\Lib\site-packages\pip\_vendor\rich\_windows_renderer.py" "Archive\Duplicates\_windows_renderer.py"

REM Duplicate group: 875c3bdf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_wrap.py
move "venv\Lib\site-packages\pip\_vendor\rich\_wrap.py" "Archive\Duplicates\_wrap.py"

REM Duplicate group: f434655d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\__init__.py
move "venv\Lib\site-packages\pip\_vendor\rich\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 743f8bb0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\__main__.py
move "venv\Lib\site-packages\pip\_vendor\rich\__main__.py" "Archive\Duplicates\__main__.py"

REM Duplicate group: 9cf0ef9a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\after.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\after.py" "Archive\Duplicates\after.py"

REM Duplicate group: 73c6edc1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\before.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\before.py" "Archive\Duplicates\before.py"

REM Duplicate group: e63ae282...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\before_sleep.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\before_sleep.py" "Archive\Duplicates\before_sleep.py"

REM Duplicate group: 9d250e25...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\nap.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\nap.py" "Archive\Duplicates\nap.py"

REM Duplicate group: f33cf9d9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\retry.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\retry.py" "Archive\Duplicates\retry.py"

REM Duplicate group: ddc0766d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\stop.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\stop.py" "Archive\Duplicates\stop.py"

REM Duplicate group: cdafc1a6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\tornadoweb.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\tornadoweb.py" "Archive\Duplicates\tornadoweb.py"

REM Duplicate group: b6fbc9d1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\wait.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\wait.py" "Archive\Duplicates\wait.py"

REM Duplicate group: 77463013...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\_asyncio.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\_asyncio.py" "Archive\Duplicates\_asyncio.py"

REM Duplicate group: 9537ab9e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\_utils.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\_utils.py" "Archive\Duplicates\_utils.py"

REM Duplicate group: 1c17a415...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\__init__.py
move "venv\Lib\site-packages\pip\_vendor\tenacity\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: f67cd21b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tomli\_parser.py
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\tomli\_parser.py" "Archive\Duplicates\_parser.py"
move "venv\Lib\site-packages\pip\_vendor\tomli\_parser.py" "Archive\Duplicates\_parser.py"
move "venv\Lib\site-packages\setuptools\_vendor\tomli\_parser.py" "Archive\Duplicates\_parser.py"

REM Duplicate group: 0111df35...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tomli\_re.py
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\tomli\_re.py" "Archive\Duplicates\_re.py"
move "venv\Lib\site-packages\pip\_vendor\tomli\_re.py" "Archive\Duplicates\_re.py"
move "venv\Lib\site-packages\setuptools\_vendor\tomli\_re.py" "Archive\Duplicates\_re.py"

REM Duplicate group: 19a32b71...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tomli\_types.py
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\tomli\_types.py" "Archive\Duplicates\_types.py"
move "venv\Lib\site-packages\pip\_vendor\tomli\_types.py" "Archive\Duplicates\_types.py"
move "venv\Lib\site-packages\setuptools\_vendor\tomli\_types.py" "Archive\Duplicates\_types.py"

REM Duplicate group: eb1b063b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\tomli\__init__.py
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\tomli\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\tomli\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\tomli\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 7f3d2e4e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\connection.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\connection.py" "Archive\Duplicates\connection.py"

REM Duplicate group: fa321357...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\connectionpool.py" "Archive\Duplicates\connectionpool.py"

REM Duplicate group: 8e282c0b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\exceptions.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\exceptions.py" "Archive\Duplicates\exceptions.py"

REM Duplicate group: 93a2dc05...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\fields.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\fields.py" "Archive\Duplicates\fields.py"

REM Duplicate group: 2ea9f2fe...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\filepost.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\filepost.py" "Archive\Duplicates\filepost.py"

REM Duplicate group: f54cacfc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py" "Archive\Duplicates\poolmanager.py"

REM Duplicate group: 79224141...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\request.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\request.py" "Archive\Duplicates\request.py"

REM Duplicate group: d15dab20...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\response.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\response.py" "Archive\Duplicates\response.py"

REM Duplicate group: c00034ca...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\_collections.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\_collections.py" "Archive\Duplicates\_collections.py"

REM Duplicate group: f6c1dff2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\_version.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\_version.py" "Archive\Duplicates\_version.py"

REM Duplicate group: aa0aaf78...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 00396289...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\appengine.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\appengine.py" "Archive\Duplicates\appengine.py"

REM Duplicate group: 0d256433...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\ntlmpool.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\ntlmpool.py" "Archive\Duplicates\ntlmpool.py"

REM Duplicate group: 395256c6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py" "Archive\Duplicates\pyopenssl.py"

REM Duplicate group: 273b0e5f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\securetransport.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\securetransport.py" "Archive\Duplicates\securetransport.py"

REM Duplicate group: 1cc7d6ae...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py" "Archive\Duplicates\socks.py"

REM Duplicate group: acc1a179...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_appengine_environ.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_appengine_environ.py" "Archive\Duplicates\_appengine_environ.py"

REM Duplicate group: 6661de51...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\bindings.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\bindings.py" "Archive\Duplicates\bindings.py"

REM Duplicate group: c4cf8188...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\low_level.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\low_level.py" "Archive\Duplicates\low_level.py"

REM Duplicate group: 6a3d2d8f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\packages\six.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\packages\six.py" "Archive\Duplicates\six.py"

REM Duplicate group: d26b39c4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\packages\backports\makefile.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\packages\backports\makefile.py" "Archive\Duplicates\makefile.py"

REM Duplicate group: 3530b010...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\connection.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\connection.py" "Archive\Duplicates\connection.py"

REM Duplicate group: 6823df66...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\proxy.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\proxy.py" "Archive\Duplicates\proxy.py"

REM Duplicate group: 71642693...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\queue.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\queue.py" "Archive\Duplicates\queue.py"

REM Duplicate group: aa68da75...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\request.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\request.py" "Archive\Duplicates\request.py"

REM Duplicate group: 6eb83504...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\response.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\response.py" "Archive\Duplicates\response.py"

REM Duplicate group: 237e2f6d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py" "Archive\Duplicates\retry.py"

REM Duplicate group: 33c5c43f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\ssltransport.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\ssltransport.py" "Archive\Duplicates\ssltransport.py"

REM Duplicate group: b9cf4ed1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_.py" "Archive\Duplicates\ssl_.py"

REM Duplicate group: b0db7b08...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py" "Archive\Duplicates\ssl_match_hostname.py"

REM Duplicate group: 88856538...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py" "Archive\Duplicates\timeout.py"

REM Duplicate group: 3b0f140e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py" "Archive\Duplicates\url.py"

REM Duplicate group: cf3f9090...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\wait.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\wait.py" "Archive\Duplicates\wait.py"

REM Duplicate group: f951fb18...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\__init__.py
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: f60643fb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\labels.py
move "venv\Lib\site-packages\pip\_vendor\webencodings\labels.py" "Archive\Duplicates\labels.py"

REM Duplicate group: 16b377e2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\mklabels.py
move "venv\Lib\site-packages\pip\_vendor\webencodings\mklabels.py" "Archive\Duplicates\mklabels.py"

REM Duplicate group: f576e857...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\tests.py
move "venv\Lib\site-packages\pip\_vendor\webencodings\tests.py" "Archive\Duplicates\tests.py"

REM Duplicate group: 74a6bdc1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\x_user_defined.py
move "venv\Lib\site-packages\pip\_vendor\webencodings\x_user_defined.py" "Archive\Duplicates\x_user_defined.py"

REM Duplicate group: 55d9055c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\__init__.py
move "venv\Lib\site-packages\pip\_vendor\webencodings\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 5dd87bf7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\AUTHORS.txt
move "venv\Lib\site-packages\pip-23.1.2.dist-info\AUTHORS.txt" "Archive\Duplicates\AUTHORS.txt"

REM Duplicate group: 055d3859...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\entry_points.txt
move "venv\Lib\site-packages\pip-23.1.2.dist-info\entry_points.txt" "Archive\Duplicates\entry_points.txt"

REM Duplicate group: 63ec52ba...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\LICENSE.txt
move "venv\Lib\site-packages\pip-23.1.2.dist-info\LICENSE.txt" "Archive\Duplicates\LICENSE.txt"

REM Duplicate group: 82f9e2c8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\METADATA
move "venv\Lib\site-packages\pip-23.1.2.dist-info\METADATA" "Archive\Duplicates\METADATA"

REM Duplicate group: 4d570301...
REM Keeping: n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\WHEEL
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\pycparser-2.22.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: 3d574bbe...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\__init__.py
move "venv\Lib\site-packages\pkg_resources\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 46dbb33b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\extern\__init__.py
move "venv\Lib\site-packages\pkg_resources\extern\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 845b81ec...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\appdirs.py
move "venv\Lib\site-packages\pkg_resources\_vendor\appdirs.py" "Archive\Duplicates\appdirs.py"

REM Duplicate group: 873640dc...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\zipp.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\zipp.py" "Archive\Duplicates\zipp.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\zipp.py" "Archive\Duplicates\zipp.py"
move "venv\Lib\site-packages\setuptools\_vendor\zipp.py" "Archive\Duplicates\zipp.py"

REM Duplicate group: 7a25905a...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\abc.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\abc.py" "Archive\Duplicates\abc.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\abc.py" "Archive\Duplicates\abc.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\abc.py" "Archive\Duplicates\abc.py"

REM Duplicate group: 5ecff1f9...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\readers.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\readers.py" "Archive\Duplicates\readers.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\readers.py" "Archive\Duplicates\readers.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\readers.py" "Archive\Duplicates\readers.py"

REM Duplicate group: cf67edb2...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\simple.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\simple.py" "Archive\Duplicates\simple.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\simple.py" "Archive\Duplicates\simple.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\simple.py" "Archive\Duplicates\simple.py"

REM Duplicate group: aa3c6d5d...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_adapters.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_adapters.py" "Archive\Duplicates\_adapters.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_adapters.py" "Archive\Duplicates\_adapters.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_adapters.py" "Archive\Duplicates\_adapters.py"

REM Duplicate group: 4586d6fd...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_common.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_common.py" "Archive\Duplicates\_common.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_common.py" "Archive\Duplicates\_common.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_common.py" "Archive\Duplicates\_common.py"

REM Duplicate group: 3dde5bf9...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_compat.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_compat.py" "Archive\Duplicates\_compat.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_compat.py" "Archive\Duplicates\_compat.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_compat.py" "Archive\Duplicates\_compat.py"

REM Duplicate group: 19609edd...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_itertools.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_itertools.py" "Archive\Duplicates\_itertools.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_itertools.py" "Archive\Duplicates\_itertools.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_itertools.py" "Archive\Duplicates\_itertools.py"

REM Duplicate group: 2d6e64dd...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_legacy.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_legacy.py" "Archive\Duplicates\_legacy.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_legacy.py" "Archive\Duplicates\_legacy.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_legacy.py" "Archive\Duplicates\_legacy.py"

REM Duplicate group: 548187b8...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\__init__.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 75e722bf...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\jaraco\context.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\jaraco\context.py" "Archive\Duplicates\context.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\jaraco\context.py" "Archive\Duplicates\context.py"
move "venv\Lib\site-packages\setuptools\_vendor\jaraco\context.py" "Archive\Duplicates\context.py"

REM Duplicate group: 7dac0f72...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\jaraco\functools.py
move "venv\Lib\site-packages\pkg_resources\_vendor\jaraco\functools.py" "Archive\Duplicates\functools.py"

REM Duplicate group: d120c417...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\jaraco\text\__init__.py
move "venv\Lib\site-packages\pkg_resources\_vendor\jaraco\text\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 9c3397ea...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\more.py
move "venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\more.py" "Archive\Duplicates\more.py"

REM Duplicate group: af669c41...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\recipes.py
move "venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\recipes.py" "Archive\Duplicates\recipes.py"

REM Duplicate group: cca04c36...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\__init__.py
move "venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 0c7c9505...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\markers.py
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\markers.py" "Archive\Duplicates\markers.py"

REM Duplicate group: c804db66...
REM Keeping: n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\requirements.py
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\requirements.py" "Archive\Duplicates\requirements.py"

REM Duplicate group: 4d5ead9e...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\core.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\core.py" "Archive\Duplicates\core.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\core.py" "Archive\Duplicates\core.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\core.py" "Archive\Duplicates\core.py"

REM Duplicate group: 1fe62ca1...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\__init__.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: e59c7a12...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\diagram\__init__.py
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\diagram\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\diagram\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\diagram\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 52014cde...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy\_callers.py
move "venv\Lib\site-packages\pluggy\_callers.py" "Archive\Duplicates\_callers.py"

REM Duplicate group: aaca6569...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy\_hooks.py
move "venv\Lib\site-packages\pluggy\_hooks.py" "Archive\Duplicates\_hooks.py"

REM Duplicate group: 47c75386...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy\_manager.py
move "venv\Lib\site-packages\pluggy\_manager.py" "Archive\Duplicates\_manager.py"

REM Duplicate group: f67e22f8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy\_result.py
move "venv\Lib\site-packages\pluggy\_result.py" "Archive\Duplicates\_result.py"

REM Duplicate group: 8e1768c6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy\_tracing.py
move "venv\Lib\site-packages\pluggy\_tracing.py" "Archive\Duplicates\_tracing.py"

REM Duplicate group: 2797a180...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy\_version.py
move "venv\Lib\site-packages\pluggy\_version.py" "Archive\Duplicates\_version.py"

REM Duplicate group: df385a93...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy\_warnings.py
move "venv\Lib\site-packages\pluggy\_warnings.py" "Archive\Duplicates\_warnings.py"

REM Duplicate group: a0512b65...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy\__init__.py
move "venv\Lib\site-packages\pluggy\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 14b83885...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\METADATA
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\METADATA" "Archive\Duplicates\METADATA"

REM Duplicate group: d65c5246...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\RECORD
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\RECORD" "Archive\Duplicates\RECORD"

REM Duplicate group: b8111315...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\top_level.txt
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\top_level.txt" "Archive\Duplicates\top_level.txt"

REM Duplicate group: a302392b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\WHEEL
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: 1c8206d1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\licenses\LICENSE
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\licenses\LICENSE" "Archive\Duplicates\LICENSE"

REM Duplicate group: f0185c24...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\cmdline.py
move "venv\Lib\site-packages\pygments\cmdline.py" "Archive\Duplicates\cmdline.py"

REM Duplicate group: bc6640c4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\console.py
move "venv\Lib\site-packages\pygments\console.py" "Archive\Duplicates\console.py"

REM Duplicate group: 073f7123...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\filter.py
move "venv\Lib\site-packages\pygments\filter.py" "Archive\Duplicates\filter.py"

REM Duplicate group: 47ffee51...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatter.py
move "venv\Lib\site-packages\pygments\formatter.py" "Archive\Duplicates\formatter.py"

REM Duplicate group: cfba39ea...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexer.py
move "venv\Lib\site-packages\pygments\lexer.py" "Archive\Duplicates\lexer.py"

REM Duplicate group: dbd9abab...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\modeline.py
move "venv\Lib\site-packages\pygments\modeline.py" "Archive\Duplicates\modeline.py"

REM Duplicate group: cd3980f1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\plugin.py
move "venv\Lib\site-packages\pygments\plugin.py" "Archive\Duplicates\plugin.py"

REM Duplicate group: 7c870b80...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\regexopt.py
move "venv\Lib\site-packages\pygments\regexopt.py" "Archive\Duplicates\regexopt.py"

REM Duplicate group: f8d00a39...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\scanner.py
move "venv\Lib\site-packages\pygments\scanner.py" "Archive\Duplicates\scanner.py"

REM Duplicate group: e3a1b1bd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\sphinxext.py
move "venv\Lib\site-packages\pygments\sphinxext.py" "Archive\Duplicates\sphinxext.py"

REM Duplicate group: 048b0e5b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\style.py
move "venv\Lib\site-packages\pygments\style.py" "Archive\Duplicates\style.py"

REM Duplicate group: ec3709fd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\token.py
move "venv\Lib\site-packages\pygments\token.py" "Archive\Duplicates\token.py"

REM Duplicate group: de812a0a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\unistring.py
move "venv\Lib\site-packages\pygments\unistring.py" "Archive\Duplicates\unistring.py"

REM Duplicate group: 8137604e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\util.py
move "venv\Lib\site-packages\pygments\util.py" "Archive\Duplicates\util.py"

REM Duplicate group: 4fd8faf3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\__init__.py
move "venv\Lib\site-packages\pygments\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 52f22819...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\__main__.py
move "venv\Lib\site-packages\pygments\__main__.py" "Archive\Duplicates\__main__.py"

REM Duplicate group: cf574ae0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\filters\__init__.py
move "venv\Lib\site-packages\pygments\filters\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: b484113a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\bbcode.py
move "venv\Lib\site-packages\pygments\formatters\bbcode.py" "Archive\Duplicates\bbcode.py"

REM Duplicate group: e871e830...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\groff.py
move "venv\Lib\site-packages\pygments\formatters\groff.py" "Archive\Duplicates\groff.py"

REM Duplicate group: 1ed2268a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\html.py
move "venv\Lib\site-packages\pygments\formatters\html.py" "Archive\Duplicates\html.py"

REM Duplicate group: fa8548f9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\img.py
move "venv\Lib\site-packages\pygments\formatters\img.py" "Archive\Duplicates\img.py"

REM Duplicate group: f31a346f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\irc.py
move "venv\Lib\site-packages\pygments\formatters\irc.py" "Archive\Duplicates\irc.py"

REM Duplicate group: e3de66b1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\latex.py
move "venv\Lib\site-packages\pygments\formatters\latex.py" "Archive\Duplicates\latex.py"

REM Duplicate group: 8005b339...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\other.py
move "venv\Lib\site-packages\pygments\formatters\other.py" "Archive\Duplicates\other.py"

REM Duplicate group: c50be0dc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\pangomarkup.py
move "venv\Lib\site-packages\pygments\formatters\pangomarkup.py" "Archive\Duplicates\pangomarkup.py"

REM Duplicate group: 4b2fe6f5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\rtf.py
move "venv\Lib\site-packages\pygments\formatters\rtf.py" "Archive\Duplicates\rtf.py"

REM Duplicate group: 0d4faa23...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\svg.py
move "venv\Lib\site-packages\pygments\formatters\svg.py" "Archive\Duplicates\svg.py"

REM Duplicate group: d1dc9f65...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\terminal.py
move "venv\Lib\site-packages\pygments\formatters\terminal.py" "Archive\Duplicates\terminal.py"

REM Duplicate group: 506f4b00...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\terminal256.py
move "venv\Lib\site-packages\pygments\formatters\terminal256.py" "Archive\Duplicates\terminal256.py"

REM Duplicate group: 75b034b7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\_mapping.py
move "venv\Lib\site-packages\pygments\formatters\_mapping.py" "Archive\Duplicates\_mapping.py"

REM Duplicate group: 6611597d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\formatters\__init__.py
move "venv\Lib\site-packages\pygments\formatters\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 2f60eb01...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\actionscript.py
move "venv\Lib\site-packages\pygments\lexers\actionscript.py" "Archive\Duplicates\actionscript.py"

REM Duplicate group: 38f17dac...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ada.py
move "venv\Lib\site-packages\pygments\lexers\ada.py" "Archive\Duplicates\ada.py"

REM Duplicate group: 4cccbc67...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\agile.py
move "venv\Lib\site-packages\pygments\lexers\agile.py" "Archive\Duplicates\agile.py"

REM Duplicate group: f6dc5f70...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\algebra.py
move "venv\Lib\site-packages\pygments\lexers\algebra.py" "Archive\Duplicates\algebra.py"

REM Duplicate group: 0fe51840...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ambient.py
move "venv\Lib\site-packages\pygments\lexers\ambient.py" "Archive\Duplicates\ambient.py"

REM Duplicate group: a9ac5749...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\amdgpu.py
move "venv\Lib\site-packages\pygments\lexers\amdgpu.py" "Archive\Duplicates\amdgpu.py"

REM Duplicate group: e9adb536...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ampl.py
move "venv\Lib\site-packages\pygments\lexers\ampl.py" "Archive\Duplicates\ampl.py"

REM Duplicate group: 3b47b08f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\apdlexer.py
move "venv\Lib\site-packages\pygments\lexers\apdlexer.py" "Archive\Duplicates\apdlexer.py"

REM Duplicate group: d1272fd9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\apl.py
move "venv\Lib\site-packages\pygments\lexers\apl.py" "Archive\Duplicates\apl.py"

REM Duplicate group: fe8f4d3d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\archetype.py
move "venv\Lib\site-packages\pygments\lexers\archetype.py" "Archive\Duplicates\archetype.py"

REM Duplicate group: 51c722f1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\arrow.py
move "venv\Lib\site-packages\pygments\lexers\arrow.py" "Archive\Duplicates\arrow.py"

REM Duplicate group: e2e8f810...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\arturo.py
move "venv\Lib\site-packages\pygments\lexers\arturo.py" "Archive\Duplicates\arturo.py"

REM Duplicate group: e5e0257e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\asc.py
move "venv\Lib\site-packages\pygments\lexers\asc.py" "Archive\Duplicates\asc.py"

REM Duplicate group: 80de5de3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\asm.py
move "venv\Lib\site-packages\pygments\lexers\asm.py" "Archive\Duplicates\asm.py"

REM Duplicate group: 5ac45faa...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\asn1.py
move "venv\Lib\site-packages\pygments\lexers\asn1.py" "Archive\Duplicates\asn1.py"

REM Duplicate group: e246eaed...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\automation.py
move "venv\Lib\site-packages\pygments\lexers\automation.py" "Archive\Duplicates\automation.py"

REM Duplicate group: 73d885dd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\bare.py
move "venv\Lib\site-packages\pygments\lexers\bare.py" "Archive\Duplicates\bare.py"

REM Duplicate group: 6a45f257...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\basic.py
move "venv\Lib\site-packages\pygments\lexers\basic.py" "Archive\Duplicates\basic.py"

REM Duplicate group: ec0be69f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\bdd.py
move "venv\Lib\site-packages\pygments\lexers\bdd.py" "Archive\Duplicates\bdd.py"

REM Duplicate group: 29c7a2fc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\berry.py
move "venv\Lib\site-packages\pygments\lexers\berry.py" "Archive\Duplicates\berry.py"

REM Duplicate group: 0eeae770...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\bibtex.py
move "venv\Lib\site-packages\pygments\lexers\bibtex.py" "Archive\Duplicates\bibtex.py"

REM Duplicate group: c8850a8c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\blueprint.py
move "venv\Lib\site-packages\pygments\lexers\blueprint.py" "Archive\Duplicates\blueprint.py"

REM Duplicate group: ce4da971...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\boa.py
move "venv\Lib\site-packages\pygments\lexers\boa.py" "Archive\Duplicates\boa.py"

REM Duplicate group: 5c63ded6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\bqn.py
move "venv\Lib\site-packages\pygments\lexers\bqn.py" "Archive\Duplicates\bqn.py"

REM Duplicate group: 3e1f9096...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\business.py
move "venv\Lib\site-packages\pygments\lexers\business.py" "Archive\Duplicates\business.py"

REM Duplicate group: 61afa91d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\capnproto.py
move "venv\Lib\site-packages\pygments\lexers\capnproto.py" "Archive\Duplicates\capnproto.py"

REM Duplicate group: f36a524a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\carbon.py
move "venv\Lib\site-packages\pygments\lexers\carbon.py" "Archive\Duplicates\carbon.py"

REM Duplicate group: e0e0d73d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\cddl.py
move "venv\Lib\site-packages\pygments\lexers\cddl.py" "Archive\Duplicates\cddl.py"

REM Duplicate group: 55487ff1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\chapel.py
move "venv\Lib\site-packages\pygments\lexers\chapel.py" "Archive\Duplicates\chapel.py"

REM Duplicate group: a7c53240...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\clean.py
move "venv\Lib\site-packages\pygments\lexers\clean.py" "Archive\Duplicates\clean.py"

REM Duplicate group: e04645eb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\codeql.py
move "venv\Lib\site-packages\pygments\lexers\codeql.py" "Archive\Duplicates\codeql.py"

REM Duplicate group: 0592c895...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\comal.py
move "venv\Lib\site-packages\pygments\lexers\comal.py" "Archive\Duplicates\comal.py"

REM Duplicate group: 3c46e7b0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\compiled.py
move "venv\Lib\site-packages\pygments\lexers\compiled.py" "Archive\Duplicates\compiled.py"

REM Duplicate group: eefa3927...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\configs.py
move "venv\Lib\site-packages\pygments\lexers\configs.py" "Archive\Duplicates\configs.py"

REM Duplicate group: 8f8afc1c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\console.py
move "venv\Lib\site-packages\pygments\lexers\console.py" "Archive\Duplicates\console.py"

REM Duplicate group: 058c8139...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\cplint.py
move "venv\Lib\site-packages\pygments\lexers\cplint.py" "Archive\Duplicates\cplint.py"

REM Duplicate group: a7ef032b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\crystal.py
move "venv\Lib\site-packages\pygments\lexers\crystal.py" "Archive\Duplicates\crystal.py"

REM Duplicate group: 65fb39ca...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\csound.py
move "venv\Lib\site-packages\pygments\lexers\csound.py" "Archive\Duplicates\csound.py"

REM Duplicate group: b7102ee4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\css.py
move "venv\Lib\site-packages\pygments\lexers\css.py" "Archive\Duplicates\css.py"

REM Duplicate group: 15f09377...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\c_cpp.py
move "venv\Lib\site-packages\pygments\lexers\c_cpp.py" "Archive\Duplicates\c_cpp.py"

REM Duplicate group: 6ebcd8e1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\c_like.py
move "venv\Lib\site-packages\pygments\lexers\c_like.py" "Archive\Duplicates\c_like.py"

REM Duplicate group: 2c3e7b7e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\d.py
move "venv\Lib\site-packages\pygments\lexers\d.py" "Archive\Duplicates\d.py"

REM Duplicate group: ca7795eb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\dalvik.py
move "venv\Lib\site-packages\pygments\lexers\dalvik.py" "Archive\Duplicates\dalvik.py"

REM Duplicate group: ef25a533...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\data.py
move "venv\Lib\site-packages\pygments\lexers\data.py" "Archive\Duplicates\data.py"

REM Duplicate group: 96eedccf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\dax.py
move "venv\Lib\site-packages\pygments\lexers\dax.py" "Archive\Duplicates\dax.py"

REM Duplicate group: ff98f26e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\devicetree.py
move "venv\Lib\site-packages\pygments\lexers\devicetree.py" "Archive\Duplicates\devicetree.py"

REM Duplicate group: 4a4de21a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\diff.py
move "venv\Lib\site-packages\pygments\lexers\diff.py" "Archive\Duplicates\diff.py"

REM Duplicate group: 26e44de6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\dns.py
move "venv\Lib\site-packages\pygments\lexers\dns.py" "Archive\Duplicates\dns.py"

REM Duplicate group: b4fa9fd0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\dotnet.py
move "venv\Lib\site-packages\pygments\lexers\dotnet.py" "Archive\Duplicates\dotnet.py"

REM Duplicate group: c18e9b89...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\dsls.py
move "venv\Lib\site-packages\pygments\lexers\dsls.py" "Archive\Duplicates\dsls.py"

REM Duplicate group: 1835dd8e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\dylan.py
move "venv\Lib\site-packages\pygments\lexers\dylan.py" "Archive\Duplicates\dylan.py"

REM Duplicate group: 94754141...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ecl.py
move "venv\Lib\site-packages\pygments\lexers\ecl.py" "Archive\Duplicates\ecl.py"

REM Duplicate group: 68d1d80b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\eiffel.py
move "venv\Lib\site-packages\pygments\lexers\eiffel.py" "Archive\Duplicates\eiffel.py"

REM Duplicate group: 8b66f4bd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\elm.py
move "venv\Lib\site-packages\pygments\lexers\elm.py" "Archive\Duplicates\elm.py"

REM Duplicate group: 7b50f7d2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\elpi.py
move "venv\Lib\site-packages\pygments\lexers\elpi.py" "Archive\Duplicates\elpi.py"

REM Duplicate group: c9c9173f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\email.py
move "venv\Lib\site-packages\pygments\lexers\email.py" "Archive\Duplicates\email.py"

REM Duplicate group: 048ea5a8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\erlang.py
move "venv\Lib\site-packages\pygments\lexers\erlang.py" "Archive\Duplicates\erlang.py"

REM Duplicate group: 65e26265...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\esoteric.py
move "venv\Lib\site-packages\pygments\lexers\esoteric.py" "Archive\Duplicates\esoteric.py"

REM Duplicate group: 725bb089...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ezhil.py
move "venv\Lib\site-packages\pygments\lexers\ezhil.py" "Archive\Duplicates\ezhil.py"

REM Duplicate group: dfcf25c4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\factor.py
move "venv\Lib\site-packages\pygments\lexers\factor.py" "Archive\Duplicates\factor.py"

REM Duplicate group: 52516dc0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\fantom.py
move "venv\Lib\site-packages\pygments\lexers\fantom.py" "Archive\Duplicates\fantom.py"

REM Duplicate group: ddeff058...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\felix.py
move "venv\Lib\site-packages\pygments\lexers\felix.py" "Archive\Duplicates\felix.py"

REM Duplicate group: 750f9087...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\fift.py
move "venv\Lib\site-packages\pygments\lexers\fift.py" "Archive\Duplicates\fift.py"

REM Duplicate group: f200e00f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\floscript.py
move "venv\Lib\site-packages\pygments\lexers\floscript.py" "Archive\Duplicates\floscript.py"

REM Duplicate group: 83ddeb02...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\forth.py
move "venv\Lib\site-packages\pygments\lexers\forth.py" "Archive\Duplicates\forth.py"

REM Duplicate group: 72da45ec...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\fortran.py
move "venv\Lib\site-packages\pygments\lexers\fortran.py" "Archive\Duplicates\fortran.py"

REM Duplicate group: de699ef4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\foxpro.py
move "venv\Lib\site-packages\pygments\lexers\foxpro.py" "Archive\Duplicates\foxpro.py"

REM Duplicate group: 0340e243...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\freefem.py
move "venv\Lib\site-packages\pygments\lexers\freefem.py" "Archive\Duplicates\freefem.py"

REM Duplicate group: 8fee9cb6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\func.py
move "venv\Lib\site-packages\pygments\lexers\func.py" "Archive\Duplicates\func.py"

REM Duplicate group: 7fb3736d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\functional.py
move "venv\Lib\site-packages\pygments\lexers\functional.py" "Archive\Duplicates\functional.py"

REM Duplicate group: b30bde41...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\futhark.py
move "venv\Lib\site-packages\pygments\lexers\futhark.py" "Archive\Duplicates\futhark.py"

REM Duplicate group: 9839c395...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\gcodelexer.py
move "venv\Lib\site-packages\pygments\lexers\gcodelexer.py" "Archive\Duplicates\gcodelexer.py"

REM Duplicate group: 97395060...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\gdscript.py
move "venv\Lib\site-packages\pygments\lexers\gdscript.py" "Archive\Duplicates\gdscript.py"

REM Duplicate group: 1450bfe9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\gleam.py
move "venv\Lib\site-packages\pygments\lexers\gleam.py" "Archive\Duplicates\gleam.py"

REM Duplicate group: 987ba418...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\go.py
move "venv\Lib\site-packages\pygments\lexers\go.py" "Archive\Duplicates\go.py"

REM Duplicate group: 734b55d3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\grammar_notation.py
move "venv\Lib\site-packages\pygments\lexers\grammar_notation.py" "Archive\Duplicates\grammar_notation.py"

REM Duplicate group: 778669e6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\graph.py
move "venv\Lib\site-packages\pygments\lexers\graph.py" "Archive\Duplicates\graph.py"

REM Duplicate group: 46163754...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\graphics.py
move "venv\Lib\site-packages\pygments\lexers\graphics.py" "Archive\Duplicates\graphics.py"

REM Duplicate group: fe58230e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\graphql.py
move "venv\Lib\site-packages\pygments\lexers\graphql.py" "Archive\Duplicates\graphql.py"

REM Duplicate group: 7d57fb1a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\graphviz.py
move "venv\Lib\site-packages\pygments\lexers\graphviz.py" "Archive\Duplicates\graphviz.py"

REM Duplicate group: 56c7cc09...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\gsql.py
move "venv\Lib\site-packages\pygments\lexers\gsql.py" "Archive\Duplicates\gsql.py"

REM Duplicate group: c41e4aac...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\hare.py
move "venv\Lib\site-packages\pygments\lexers\hare.py" "Archive\Duplicates\hare.py"

REM Duplicate group: b6e46658...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\haskell.py
move "venv\Lib\site-packages\pygments\lexers\haskell.py" "Archive\Duplicates\haskell.py"

REM Duplicate group: c072e6ea...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\haxe.py
move "venv\Lib\site-packages\pygments\lexers\haxe.py" "Archive\Duplicates\haxe.py"

REM Duplicate group: 5208bde1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\hdl.py
move "venv\Lib\site-packages\pygments\lexers\hdl.py" "Archive\Duplicates\hdl.py"

REM Duplicate group: ffd661f7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\hexdump.py
move "venv\Lib\site-packages\pygments\lexers\hexdump.py" "Archive\Duplicates\hexdump.py"

REM Duplicate group: 257b75bc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\html.py
move "venv\Lib\site-packages\pygments\lexers\html.py" "Archive\Duplicates\html.py"

REM Duplicate group: a80c628b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\idl.py
move "venv\Lib\site-packages\pygments\lexers\idl.py" "Archive\Duplicates\idl.py"

REM Duplicate group: 4446ee23...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\igor.py
move "venv\Lib\site-packages\pygments\lexers\igor.py" "Archive\Duplicates\igor.py"

REM Duplicate group: 3bb6f6e2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\inferno.py
move "venv\Lib\site-packages\pygments\lexers\inferno.py" "Archive\Duplicates\inferno.py"

REM Duplicate group: 7c123256...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\installers.py
move "venv\Lib\site-packages\pygments\lexers\installers.py" "Archive\Duplicates\installers.py"

REM Duplicate group: ca69ba1a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\int_fiction.py
move "venv\Lib\site-packages\pygments\lexers\int_fiction.py" "Archive\Duplicates\int_fiction.py"

REM Duplicate group: b05b8e64...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\iolang.py
move "venv\Lib\site-packages\pygments\lexers\iolang.py" "Archive\Duplicates\iolang.py"

REM Duplicate group: 7dfe5e01...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\j.py
move "venv\Lib\site-packages\pygments\lexers\j.py" "Archive\Duplicates\j.py"

REM Duplicate group: 2ef95e5d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\javascript.py
move "venv\Lib\site-packages\pygments\lexers\javascript.py" "Archive\Duplicates\javascript.py"

REM Duplicate group: 26f2a1eb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\jmespath.py
move "venv\Lib\site-packages\pygments\lexers\jmespath.py" "Archive\Duplicates\jmespath.py"

REM Duplicate group: f1ad787f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\jslt.py
move "venv\Lib\site-packages\pygments\lexers\jslt.py" "Archive\Duplicates\jslt.py"

REM Duplicate group: 06193539...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\json5.py
move "venv\Lib\site-packages\pygments\lexers\json5.py" "Archive\Duplicates\json5.py"

REM Duplicate group: 5d585b7e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\jsonnet.py
move "venv\Lib\site-packages\pygments\lexers\jsonnet.py" "Archive\Duplicates\jsonnet.py"

REM Duplicate group: 01dd644d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\jsx.py
move "venv\Lib\site-packages\pygments\lexers\jsx.py" "Archive\Duplicates\jsx.py"

REM Duplicate group: b750c14e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\julia.py
move "venv\Lib\site-packages\pygments\lexers\julia.py" "Archive\Duplicates\julia.py"

REM Duplicate group: 183983d5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\jvm.py
move "venv\Lib\site-packages\pygments\lexers\jvm.py" "Archive\Duplicates\jvm.py"

REM Duplicate group: cfcd3370...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\kuin.py
move "venv\Lib\site-packages\pygments\lexers\kuin.py" "Archive\Duplicates\kuin.py"

REM Duplicate group: 82caeda6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\kusto.py
move "venv\Lib\site-packages\pygments\lexers\kusto.py" "Archive\Duplicates\kusto.py"

REM Duplicate group: cea009ed...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ldap.py
move "venv\Lib\site-packages\pygments\lexers\ldap.py" "Archive\Duplicates\ldap.py"

REM Duplicate group: 5568c297...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\lean.py
move "venv\Lib\site-packages\pygments\lexers\lean.py" "Archive\Duplicates\lean.py"

REM Duplicate group: 36500f4e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\lilypond.py
move "venv\Lib\site-packages\pygments\lexers\lilypond.py" "Archive\Duplicates\lilypond.py"

REM Duplicate group: e9e16ccb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\lisp.py
move "venv\Lib\site-packages\pygments\lexers\lisp.py" "Archive\Duplicates\lisp.py"

REM Duplicate group: 3c587969...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\macaulay2.py
move "venv\Lib\site-packages\pygments\lexers\macaulay2.py" "Archive\Duplicates\macaulay2.py"

REM Duplicate group: 6094234a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\make.py
move "venv\Lib\site-packages\pygments\lexers\make.py" "Archive\Duplicates\make.py"

REM Duplicate group: 57c4f3a8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\maple.py
move "venv\Lib\site-packages\pygments\lexers\maple.py" "Archive\Duplicates\maple.py"

REM Duplicate group: 0a18f68f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\markup.py
move "venv\Lib\site-packages\pygments\lexers\markup.py" "Archive\Duplicates\markup.py"

REM Duplicate group: be7d86c1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\math.py
move "venv\Lib\site-packages\pygments\lexers\math.py" "Archive\Duplicates\math.py"

REM Duplicate group: fcee3272...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\matlab.py
move "venv\Lib\site-packages\pygments\lexers\matlab.py" "Archive\Duplicates\matlab.py"

REM Duplicate group: 585ec4e4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\maxima.py
move "venv\Lib\site-packages\pygments\lexers\maxima.py" "Archive\Duplicates\maxima.py"

REM Duplicate group: 109653fc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\meson.py
move "venv\Lib\site-packages\pygments\lexers\meson.py" "Archive\Duplicates\meson.py"

REM Duplicate group: e1030cd0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\mime.py
move "venv\Lib\site-packages\pygments\lexers\mime.py" "Archive\Duplicates\mime.py"

REM Duplicate group: 7de2b5a6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\minecraft.py
move "venv\Lib\site-packages\pygments\lexers\minecraft.py" "Archive\Duplicates\minecraft.py"

REM Duplicate group: 09a756db...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\mips.py
move "venv\Lib\site-packages\pygments\lexers\mips.py" "Archive\Duplicates\mips.py"

REM Duplicate group: 14fe082b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ml.py
move "venv\Lib\site-packages\pygments\lexers\ml.py" "Archive\Duplicates\ml.py"

REM Duplicate group: bb78aab1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\modeling.py
move "venv\Lib\site-packages\pygments\lexers\modeling.py" "Archive\Duplicates\modeling.py"

REM Duplicate group: 44212e4d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\modula2.py
move "venv\Lib\site-packages\pygments\lexers\modula2.py" "Archive\Duplicates\modula2.py"

REM Duplicate group: e9844c7f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\mojo.py
move "venv\Lib\site-packages\pygments\lexers\mojo.py" "Archive\Duplicates\mojo.py"

REM Duplicate group: 9164de23...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\monte.py
move "venv\Lib\site-packages\pygments\lexers\monte.py" "Archive\Duplicates\monte.py"

REM Duplicate group: 92e14d41...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\mosel.py
move "venv\Lib\site-packages\pygments\lexers\mosel.py" "Archive\Duplicates\mosel.py"

REM Duplicate group: 27c2196e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ncl.py
move "venv\Lib\site-packages\pygments\lexers\ncl.py" "Archive\Duplicates\ncl.py"

REM Duplicate group: 0f2db212...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\nimrod.py
move "venv\Lib\site-packages\pygments\lexers\nimrod.py" "Archive\Duplicates\nimrod.py"

REM Duplicate group: 267839fe...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\nit.py
move "venv\Lib\site-packages\pygments\lexers\nit.py" "Archive\Duplicates\nit.py"

REM Duplicate group: 9255b3f6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\nix.py
move "venv\Lib\site-packages\pygments\lexers\nix.py" "Archive\Duplicates\nix.py"

REM Duplicate group: 51f9ea73...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\numbair.py
move "venv\Lib\site-packages\pygments\lexers\numbair.py" "Archive\Duplicates\numbair.py"

REM Duplicate group: b24cf306...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\oberon.py
move "venv\Lib\site-packages\pygments\lexers\oberon.py" "Archive\Duplicates\oberon.py"

REM Duplicate group: 06257273...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\objective.py
move "venv\Lib\site-packages\pygments\lexers\objective.py" "Archive\Duplicates\objective.py"

REM Duplicate group: 1426251b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ooc.py
move "venv\Lib\site-packages\pygments\lexers\ooc.py" "Archive\Duplicates\ooc.py"

REM Duplicate group: 6df4a2bf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\openscad.py
move "venv\Lib\site-packages\pygments\lexers\openscad.py" "Archive\Duplicates\openscad.py"

REM Duplicate group: 21e9c2f6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\other.py
move "venv\Lib\site-packages\pygments\lexers\other.py" "Archive\Duplicates\other.py"

REM Duplicate group: fc7ca046...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\parasail.py
move "venv\Lib\site-packages\pygments\lexers\parasail.py" "Archive\Duplicates\parasail.py"

REM Duplicate group: 408418a3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\parsers.py
move "venv\Lib\site-packages\pygments\lexers\parsers.py" "Archive\Duplicates\parsers.py"

REM Duplicate group: 85f4c34a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\pascal.py
move "venv\Lib\site-packages\pygments\lexers\pascal.py" "Archive\Duplicates\pascal.py"

REM Duplicate group: d331c975...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\pawn.py
move "venv\Lib\site-packages\pygments\lexers\pawn.py" "Archive\Duplicates\pawn.py"

REM Duplicate group: 4ee74085...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\pddl.py
move "venv\Lib\site-packages\pygments\lexers\pddl.py" "Archive\Duplicates\pddl.py"

REM Duplicate group: 82edd7d9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\perl.py
move "venv\Lib\site-packages\pygments\lexers\perl.py" "Archive\Duplicates\perl.py"

REM Duplicate group: b3c211d9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\phix.py
move "venv\Lib\site-packages\pygments\lexers\phix.py" "Archive\Duplicates\phix.py"

REM Duplicate group: 88e487c8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\php.py
move "venv\Lib\site-packages\pygments\lexers\php.py" "Archive\Duplicates\php.py"

REM Duplicate group: 67c7326f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\pointless.py
move "venv\Lib\site-packages\pygments\lexers\pointless.py" "Archive\Duplicates\pointless.py"

REM Duplicate group: 39e87a4c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\pony.py
move "venv\Lib\site-packages\pygments\lexers\pony.py" "Archive\Duplicates\pony.py"

REM Duplicate group: bec7ad24...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\praat.py
move "venv\Lib\site-packages\pygments\lexers\praat.py" "Archive\Duplicates\praat.py"

REM Duplicate group: a08c97ad...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\procfile.py
move "venv\Lib\site-packages\pygments\lexers\procfile.py" "Archive\Duplicates\procfile.py"

REM Duplicate group: cbb6180a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\prolog.py
move "venv\Lib\site-packages\pygments\lexers\prolog.py" "Archive\Duplicates\prolog.py"

REM Duplicate group: 9ca29b39...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\promql.py
move "venv\Lib\site-packages\pygments\lexers\promql.py" "Archive\Duplicates\promql.py"

REM Duplicate group: 0a858dbf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\prql.py
move "venv\Lib\site-packages\pygments\lexers\prql.py" "Archive\Duplicates\prql.py"

REM Duplicate group: 698f4d43...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ptx.py
move "venv\Lib\site-packages\pygments\lexers\ptx.py" "Archive\Duplicates\ptx.py"

REM Duplicate group: dc6fac52...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\python.py
move "venv\Lib\site-packages\pygments\lexers\python.py" "Archive\Duplicates\python.py"

REM Duplicate group: a59b6e85...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\q.py
move "venv\Lib\site-packages\pygments\lexers\q.py" "Archive\Duplicates\q.py"

REM Duplicate group: 7acd1c5e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\qlik.py
move "venv\Lib\site-packages\pygments\lexers\qlik.py" "Archive\Duplicates\qlik.py"

REM Duplicate group: 01e8dd31...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\qvt.py
move "venv\Lib\site-packages\pygments\lexers\qvt.py" "Archive\Duplicates\qvt.py"

REM Duplicate group: c8743068...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\r.py
move "venv\Lib\site-packages\pygments\lexers\r.py" "Archive\Duplicates\r.py"

REM Duplicate group: 564a137a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\rdf.py
move "venv\Lib\site-packages\pygments\lexers\rdf.py" "Archive\Duplicates\rdf.py"

REM Duplicate group: b3e34d37...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\rebol.py
move "venv\Lib\site-packages\pygments\lexers\rebol.py" "Archive\Duplicates\rebol.py"

REM Duplicate group: 30d73389...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\rego.py
move "venv\Lib\site-packages\pygments\lexers\rego.py" "Archive\Duplicates\rego.py"

REM Duplicate group: 45d34aa8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\resource.py
move "venv\Lib\site-packages\pygments\lexers\resource.py" "Archive\Duplicates\resource.py"

REM Duplicate group: f4cc3ef8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ride.py
move "venv\Lib\site-packages\pygments\lexers\ride.py" "Archive\Duplicates\ride.py"

REM Duplicate group: e783b15d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\rita.py
move "venv\Lib\site-packages\pygments\lexers\rita.py" "Archive\Duplicates\rita.py"

REM Duplicate group: 548e7390...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\rnc.py
move "venv\Lib\site-packages\pygments\lexers\rnc.py" "Archive\Duplicates\rnc.py"

REM Duplicate group: 1aa68bd3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\roboconf.py
move "venv\Lib\site-packages\pygments\lexers\roboconf.py" "Archive\Duplicates\roboconf.py"

REM Duplicate group: afefed99...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\robotframework.py
move "venv\Lib\site-packages\pygments\lexers\robotframework.py" "Archive\Duplicates\robotframework.py"

REM Duplicate group: 80dc7c62...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ruby.py
move "venv\Lib\site-packages\pygments\lexers\ruby.py" "Archive\Duplicates\ruby.py"

REM Duplicate group: 398ad59e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\rust.py
move "venv\Lib\site-packages\pygments\lexers\rust.py" "Archive\Duplicates\rust.py"

REM Duplicate group: fdd0fe30...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\sas.py
move "venv\Lib\site-packages\pygments\lexers\sas.py" "Archive\Duplicates\sas.py"

REM Duplicate group: 7b654463...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\savi.py
move "venv\Lib\site-packages\pygments\lexers\savi.py" "Archive\Duplicates\savi.py"

REM Duplicate group: 48ed6ff0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\scdoc.py
move "venv\Lib\site-packages\pygments\lexers\scdoc.py" "Archive\Duplicates\scdoc.py"

REM Duplicate group: 5834df24...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\scripting.py
move "venv\Lib\site-packages\pygments\lexers\scripting.py" "Archive\Duplicates\scripting.py"

REM Duplicate group: 6aa13bad...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\sgf.py
move "venv\Lib\site-packages\pygments\lexers\sgf.py" "Archive\Duplicates\sgf.py"

REM Duplicate group: 9e71097f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\shell.py
move "venv\Lib\site-packages\pygments\lexers\shell.py" "Archive\Duplicates\shell.py"

REM Duplicate group: d90ebdde...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\sieve.py
move "venv\Lib\site-packages\pygments\lexers\sieve.py" "Archive\Duplicates\sieve.py"

REM Duplicate group: 525fedd5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\slash.py
move "venv\Lib\site-packages\pygments\lexers\slash.py" "Archive\Duplicates\slash.py"

REM Duplicate group: 30933fa2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\smalltalk.py
move "venv\Lib\site-packages\pygments\lexers\smalltalk.py" "Archive\Duplicates\smalltalk.py"

REM Duplicate group: deca076e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\smithy.py
move "venv\Lib\site-packages\pygments\lexers\smithy.py" "Archive\Duplicates\smithy.py"

REM Duplicate group: b1d9c432...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\smv.py
move "venv\Lib\site-packages\pygments\lexers\smv.py" "Archive\Duplicates\smv.py"

REM Duplicate group: 363345ce...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\snobol.py
move "venv\Lib\site-packages\pygments\lexers\snobol.py" "Archive\Duplicates\snobol.py"

REM Duplicate group: d4442fe4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\solidity.py
move "venv\Lib\site-packages\pygments\lexers\solidity.py" "Archive\Duplicates\solidity.py"

REM Duplicate group: fa2502d3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\soong.py
move "venv\Lib\site-packages\pygments\lexers\soong.py" "Archive\Duplicates\soong.py"

REM Duplicate group: 23481bf5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\sophia.py
move "venv\Lib\site-packages\pygments\lexers\sophia.py" "Archive\Duplicates\sophia.py"

REM Duplicate group: 5aabab60...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\special.py
move "venv\Lib\site-packages\pygments\lexers\special.py" "Archive\Duplicates\special.py"

REM Duplicate group: f4cb4cb9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\spice.py
move "venv\Lib\site-packages\pygments\lexers\spice.py" "Archive\Duplicates\spice.py"

REM Duplicate group: af2d14d7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\sql.py
move "venv\Lib\site-packages\pygments\lexers\sql.py" "Archive\Duplicates\sql.py"

REM Duplicate group: fc7d4d8a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\srcinfo.py
move "venv\Lib\site-packages\pygments\lexers\srcinfo.py" "Archive\Duplicates\srcinfo.py"

REM Duplicate group: 79bd4cd3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\stata.py
move "venv\Lib\site-packages\pygments\lexers\stata.py" "Archive\Duplicates\stata.py"

REM Duplicate group: 33f2f45b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\supercollider.py
move "venv\Lib\site-packages\pygments\lexers\supercollider.py" "Archive\Duplicates\supercollider.py"

REM Duplicate group: 112e669f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\tablegen.py
move "venv\Lib\site-packages\pygments\lexers\tablegen.py" "Archive\Duplicates\tablegen.py"

REM Duplicate group: 90237b53...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\tact.py
move "venv\Lib\site-packages\pygments\lexers\tact.py" "Archive\Duplicates\tact.py"

REM Duplicate group: 57a686d9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\tal.py
move "venv\Lib\site-packages\pygments\lexers\tal.py" "Archive\Duplicates\tal.py"

REM Duplicate group: b60d0ff7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\tcl.py
move "venv\Lib\site-packages\pygments\lexers\tcl.py" "Archive\Duplicates\tcl.py"

REM Duplicate group: ade61c7f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\teal.py
move "venv\Lib\site-packages\pygments\lexers\teal.py" "Archive\Duplicates\teal.py"

REM Duplicate group: a9bb04f0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\templates.py
move "venv\Lib\site-packages\pygments\lexers\templates.py" "Archive\Duplicates\templates.py"

REM Duplicate group: 5d3d9b8b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\teraterm.py
move "venv\Lib\site-packages\pygments\lexers\teraterm.py" "Archive\Duplicates\teraterm.py"

REM Duplicate group: 1c6df74d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\testing.py
move "venv\Lib\site-packages\pygments\lexers\testing.py" "Archive\Duplicates\testing.py"

REM Duplicate group: 7b07c473...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\text.py
move "venv\Lib\site-packages\pygments\lexers\text.py" "Archive\Duplicates\text.py"

REM Duplicate group: 0845e058...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\textedit.py
move "venv\Lib\site-packages\pygments\lexers\textedit.py" "Archive\Duplicates\textedit.py"

REM Duplicate group: dcb8cad3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\textfmts.py
move "venv\Lib\site-packages\pygments\lexers\textfmts.py" "Archive\Duplicates\textfmts.py"

REM Duplicate group: 1cefcfc5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\theorem.py
move "venv\Lib\site-packages\pygments\lexers\theorem.py" "Archive\Duplicates\theorem.py"

REM Duplicate group: 7808046b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\thingsdb.py
move "venv\Lib\site-packages\pygments\lexers\thingsdb.py" "Archive\Duplicates\thingsdb.py"

REM Duplicate group: fd69b92a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\tlb.py
move "venv\Lib\site-packages\pygments\lexers\tlb.py" "Archive\Duplicates\tlb.py"

REM Duplicate group: 834ac562...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\tls.py
move "venv\Lib\site-packages\pygments\lexers\tls.py" "Archive\Duplicates\tls.py"

REM Duplicate group: 5f32d9c0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\tnt.py
move "venv\Lib\site-packages\pygments\lexers\tnt.py" "Archive\Duplicates\tnt.py"

REM Duplicate group: a0177797...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\trafficscript.py
move "venv\Lib\site-packages\pygments\lexers\trafficscript.py" "Archive\Duplicates\trafficscript.py"

REM Duplicate group: e20d885e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\typoscript.py
move "venv\Lib\site-packages\pygments\lexers\typoscript.py" "Archive\Duplicates\typoscript.py"

REM Duplicate group: 79d48feb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\typst.py
move "venv\Lib\site-packages\pygments\lexers\typst.py" "Archive\Duplicates\typst.py"

REM Duplicate group: fb800b54...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\ul4.py
move "venv\Lib\site-packages\pygments\lexers\ul4.py" "Archive\Duplicates\ul4.py"

REM Duplicate group: 5f7a53dc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\unicon.py
move "venv\Lib\site-packages\pygments\lexers\unicon.py" "Archive\Duplicates\unicon.py"

REM Duplicate group: c88a0e16...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\urbi.py
move "venv\Lib\site-packages\pygments\lexers\urbi.py" "Archive\Duplicates\urbi.py"

REM Duplicate group: 471e57bd...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\usd.py
move "venv\Lib\site-packages\pygments\lexers\usd.py" "Archive\Duplicates\usd.py"

REM Duplicate group: 17feb73b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\varnish.py
move "venv\Lib\site-packages\pygments\lexers\varnish.py" "Archive\Duplicates\varnish.py"

REM Duplicate group: 4325531c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\verification.py
move "venv\Lib\site-packages\pygments\lexers\verification.py" "Archive\Duplicates\verification.py"

REM Duplicate group: 6887657d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\verifpal.py
move "venv\Lib\site-packages\pygments\lexers\verifpal.py" "Archive\Duplicates\verifpal.py"

REM Duplicate group: ad5b42c6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\vip.py
move "venv\Lib\site-packages\pygments\lexers\vip.py" "Archive\Duplicates\vip.py"

REM Duplicate group: c1f23dca...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\vyper.py
move "venv\Lib\site-packages\pygments\lexers\vyper.py" "Archive\Duplicates\vyper.py"

REM Duplicate group: bfcc265b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\web.py
move "venv\Lib\site-packages\pygments\lexers\web.py" "Archive\Duplicates\web.py"

REM Duplicate group: 633229c9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\webassembly.py
move "venv\Lib\site-packages\pygments\lexers\webassembly.py" "Archive\Duplicates\webassembly.py"

REM Duplicate group: a22371b2...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\webidl.py
move "venv\Lib\site-packages\pygments\lexers\webidl.py" "Archive\Duplicates\webidl.py"

REM Duplicate group: 87cb154d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\webmisc.py
move "venv\Lib\site-packages\pygments\lexers\webmisc.py" "Archive\Duplicates\webmisc.py"

REM Duplicate group: 45694354...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\wgsl.py
move "venv\Lib\site-packages\pygments\lexers\wgsl.py" "Archive\Duplicates\wgsl.py"

REM Duplicate group: 0c1228ec...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\whiley.py
move "venv\Lib\site-packages\pygments\lexers\whiley.py" "Archive\Duplicates\whiley.py"

REM Duplicate group: 948c48b7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\wowtoc.py
move "venv\Lib\site-packages\pygments\lexers\wowtoc.py" "Archive\Duplicates\wowtoc.py"

REM Duplicate group: 5fc3162c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\wren.py
move "venv\Lib\site-packages\pygments\lexers\wren.py" "Archive\Duplicates\wren.py"

REM Duplicate group: bc44e163...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\x10.py
move "venv\Lib\site-packages\pygments\lexers\x10.py" "Archive\Duplicates\x10.py"

REM Duplicate group: 3d1972ef...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\xorg.py
move "venv\Lib\site-packages\pygments\lexers\xorg.py" "Archive\Duplicates\xorg.py"

REM Duplicate group: a6fac96b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\yang.py
move "venv\Lib\site-packages\pygments\lexers\yang.py" "Archive\Duplicates\yang.py"

REM Duplicate group: 630da832...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\yara.py
move "venv\Lib\site-packages\pygments\lexers\yara.py" "Archive\Duplicates\yara.py"

REM Duplicate group: 4fd93791...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\zig.py
move "venv\Lib\site-packages\pygments\lexers\zig.py" "Archive\Duplicates\zig.py"

REM Duplicate group: ac939c71...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_ada_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_ada_builtins.py" "Archive\Duplicates\_ada_builtins.py"

REM Duplicate group: 064d16f9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_asy_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_asy_builtins.py" "Archive\Duplicates\_asy_builtins.py"

REM Duplicate group: 70272745...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_cl_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_cl_builtins.py" "Archive\Duplicates\_cl_builtins.py"

REM Duplicate group: 5adb81dc...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_cocoa_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_cocoa_builtins.py" "Archive\Duplicates\_cocoa_builtins.py"

REM Duplicate group: 03ed1ac8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_csound_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_csound_builtins.py" "Archive\Duplicates\_csound_builtins.py"

REM Duplicate group: 90c24bde...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_css_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_css_builtins.py" "Archive\Duplicates\_css_builtins.py"

REM Duplicate group: 20b0aa9e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_googlesql_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_googlesql_builtins.py" "Archive\Duplicates\_googlesql_builtins.py"

REM Duplicate group: 983555e8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_julia_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_julia_builtins.py" "Archive\Duplicates\_julia_builtins.py"

REM Duplicate group: 1467cf93...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_lasso_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_lasso_builtins.py" "Archive\Duplicates\_lasso_builtins.py"

REM Duplicate group: 7962c3ac...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_lilypond_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_lilypond_builtins.py" "Archive\Duplicates\_lilypond_builtins.py"

REM Duplicate group: ed6ed997...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_luau_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_luau_builtins.py" "Archive\Duplicates\_luau_builtins.py"

REM Duplicate group: fe6857f8...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_lua_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_lua_builtins.py" "Archive\Duplicates\_lua_builtins.py"

REM Duplicate group: 421ad012...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_mapping.py
move "venv\Lib\site-packages\pygments\lexers\_mapping.py" "Archive\Duplicates\_mapping.py"

REM Duplicate group: 6c48a302...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_mql_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_mql_builtins.py" "Archive\Duplicates\_mql_builtins.py"

REM Duplicate group: d5319526...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_mysql_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_mysql_builtins.py" "Archive\Duplicates\_mysql_builtins.py"

REM Duplicate group: 4420eb4e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_openedge_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_openedge_builtins.py" "Archive\Duplicates\_openedge_builtins.py"

REM Duplicate group: aa8dc2c1...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_php_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_php_builtins.py" "Archive\Duplicates\_php_builtins.py"

REM Duplicate group: 74d14d26...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_postgres_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_postgres_builtins.py" "Archive\Duplicates\_postgres_builtins.py"

REM Duplicate group: 1fec4853...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_qlik_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_qlik_builtins.py" "Archive\Duplicates\_qlik_builtins.py"

REM Duplicate group: 8cf8c6c9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_scheme_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_scheme_builtins.py" "Archive\Duplicates\_scheme_builtins.py"

REM Duplicate group: 79888aa9...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_scilab_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_scilab_builtins.py" "Archive\Duplicates\_scilab_builtins.py"

REM Duplicate group: def87ff5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_sourcemod_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_sourcemod_builtins.py" "Archive\Duplicates\_sourcemod_builtins.py"

REM Duplicate group: 37ced189...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_stan_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_stan_builtins.py" "Archive\Duplicates\_stan_builtins.py"

REM Duplicate group: 28be5586...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_stata_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_stata_builtins.py" "Archive\Duplicates\_stata_builtins.py"

REM Duplicate group: a9bfb9df...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_tsql_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_tsql_builtins.py" "Archive\Duplicates\_tsql_builtins.py"

REM Duplicate group: 55109f92...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_usd_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_usd_builtins.py" "Archive\Duplicates\_usd_builtins.py"

REM Duplicate group: 4004c7ad...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_vbscript_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_vbscript_builtins.py" "Archive\Duplicates\_vbscript_builtins.py"

REM Duplicate group: 8754d621...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\_vim_builtins.py
move "venv\Lib\site-packages\pygments\lexers\_vim_builtins.py" "Archive\Duplicates\_vim_builtins.py"

REM Duplicate group: 08b599f7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\lexers\__init__.py
move "venv\Lib\site-packages\pygments\lexers\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 78a7e80c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\abap.py
move "venv\Lib\site-packages\pygments\styles\abap.py" "Archive\Duplicates\abap.py"

REM Duplicate group: 9b963c4b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\algol.py
move "venv\Lib\site-packages\pygments\styles\algol.py" "Archive\Duplicates\algol.py"

REM Duplicate group: 778c2616...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\algol_nu.py
move "venv\Lib\site-packages\pygments\styles\algol_nu.py" "Archive\Duplicates\algol_nu.py"

REM Duplicate group: fd77937b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\arduino.py
move "venv\Lib\site-packages\pygments\styles\arduino.py" "Archive\Duplicates\arduino.py"

REM Duplicate group: d425ccfe...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\autumn.py
move "venv\Lib\site-packages\pygments\styles\autumn.py" "Archive\Duplicates\autumn.py"

REM Duplicate group: b72c8aeb...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\borland.py
move "venv\Lib\site-packages\pygments\styles\borland.py" "Archive\Duplicates\borland.py"

REM Duplicate group: fb9a3869...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\bw.py
move "venv\Lib\site-packages\pygments\styles\bw.py" "Archive\Duplicates\bw.py"

REM Duplicate group: d8067ca5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\coffee.py
move "venv\Lib\site-packages\pygments\styles\coffee.py" "Archive\Duplicates\coffee.py"

REM Duplicate group: 3631e880...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\colorful.py
move "venv\Lib\site-packages\pygments\styles\colorful.py" "Archive\Duplicates\colorful.py"

REM Duplicate group: bb91d3b6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\default.py
move "venv\Lib\site-packages\pygments\styles\default.py" "Archive\Duplicates\default.py"

REM Duplicate group: 25eb66fa...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\dracula.py
move "venv\Lib\site-packages\pygments\styles\dracula.py" "Archive\Duplicates\dracula.py"

REM Duplicate group: 0d1b9e1f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\emacs.py
move "venv\Lib\site-packages\pygments\styles\emacs.py" "Archive\Duplicates\emacs.py"

REM Duplicate group: 39835c34...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\friendly.py
move "venv\Lib\site-packages\pygments\styles\friendly.py" "Archive\Duplicates\friendly.py"

REM Duplicate group: 0e48500c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\friendly_grayscale.py
move "venv\Lib\site-packages\pygments\styles\friendly_grayscale.py" "Archive\Duplicates\friendly_grayscale.py"

REM Duplicate group: 25f7ed91...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\fruity.py
move "venv\Lib\site-packages\pygments\styles\fruity.py" "Archive\Duplicates\fruity.py"

REM Duplicate group: 09cda579...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\gh_dark.py
move "venv\Lib\site-packages\pygments\styles\gh_dark.py" "Archive\Duplicates\gh_dark.py"

REM Duplicate group: a2c47ced...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\gruvbox.py
move "venv\Lib\site-packages\pygments\styles\gruvbox.py" "Archive\Duplicates\gruvbox.py"

REM Duplicate group: 9df67191...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\igor.py
move "venv\Lib\site-packages\pygments\styles\igor.py" "Archive\Duplicates\igor.py"

REM Duplicate group: 357a8f1a...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\inkpot.py
move "venv\Lib\site-packages\pygments\styles\inkpot.py" "Archive\Duplicates\inkpot.py"

REM Duplicate group: a2a39550...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\lightbulb.py
move "venv\Lib\site-packages\pygments\styles\lightbulb.py" "Archive\Duplicates\lightbulb.py"

REM Duplicate group: 02e26a53...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\lilypond.py
move "venv\Lib\site-packages\pygments\styles\lilypond.py" "Archive\Duplicates\lilypond.py"

REM Duplicate group: 3bb3f20e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\lovelace.py
move "venv\Lib\site-packages\pygments\styles\lovelace.py" "Archive\Duplicates\lovelace.py"

REM Duplicate group: 8401713c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\manni.py
move "venv\Lib\site-packages\pygments\styles\manni.py" "Archive\Duplicates\manni.py"

REM Duplicate group: c16bbca3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\material.py
move "venv\Lib\site-packages\pygments\styles\material.py" "Archive\Duplicates\material.py"

REM Duplicate group: 7e76f2be...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\monokai.py
move "venv\Lib\site-packages\pygments\styles\monokai.py" "Archive\Duplicates\monokai.py"

REM Duplicate group: 16039de6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\murphy.py
move "venv\Lib\site-packages\pygments\styles\murphy.py" "Archive\Duplicates\murphy.py"

REM Duplicate group: 2c985c3e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\native.py
move "venv\Lib\site-packages\pygments\styles\native.py" "Archive\Duplicates\native.py"

REM Duplicate group: fb44cae7...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\nord.py
move "venv\Lib\site-packages\pygments\styles\nord.py" "Archive\Duplicates\nord.py"

REM Duplicate group: 552bacfe...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\onedark.py
move "venv\Lib\site-packages\pygments\styles\onedark.py" "Archive\Duplicates\onedark.py"

REM Duplicate group: 7d0e495e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\paraiso_dark.py
move "venv\Lib\site-packages\pygments\styles\paraiso_dark.py" "Archive\Duplicates\paraiso_dark.py"

REM Duplicate group: 4ca5754f...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\paraiso_light.py
move "venv\Lib\site-packages\pygments\styles\paraiso_light.py" "Archive\Duplicates\paraiso_light.py"

REM Duplicate group: ee5f50a3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\pastie.py
move "venv\Lib\site-packages\pygments\styles\pastie.py" "Archive\Duplicates\pastie.py"

REM Duplicate group: 604ef62c...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\perldoc.py
move "venv\Lib\site-packages\pygments\styles\perldoc.py" "Archive\Duplicates\perldoc.py"

REM Duplicate group: cbea5eda...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\rainbow_dash.py
move "venv\Lib\site-packages\pygments\styles\rainbow_dash.py" "Archive\Duplicates\rainbow_dash.py"

REM Duplicate group: 3f9d9ab3...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\rrt.py
move "venv\Lib\site-packages\pygments\styles\rrt.py" "Archive\Duplicates\rrt.py"

REM Duplicate group: ee2de6cf...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\sas.py
move "venv\Lib\site-packages\pygments\styles\sas.py" "Archive\Duplicates\sas.py"

REM Duplicate group: e2c18c5b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\solarized.py
move "venv\Lib\site-packages\pygments\styles\solarized.py" "Archive\Duplicates\solarized.py"

REM Duplicate group: 776023f0...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\staroffice.py
move "venv\Lib\site-packages\pygments\styles\staroffice.py" "Archive\Duplicates\staroffice.py"

REM Duplicate group: 40f70691...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\stata_dark.py
move "venv\Lib\site-packages\pygments\styles\stata_dark.py" "Archive\Duplicates\stata_dark.py"

REM Duplicate group: 5ec8ae98...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\stata_light.py
move "venv\Lib\site-packages\pygments\styles\stata_light.py" "Archive\Duplicates\stata_light.py"

REM Duplicate group: 8b94ed55...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\tango.py
move "venv\Lib\site-packages\pygments\styles\tango.py" "Archive\Duplicates\tango.py"

REM Duplicate group: a8517769...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\trac.py
move "venv\Lib\site-packages\pygments\styles\trac.py" "Archive\Duplicates\trac.py"

REM Duplicate group: 9f85d4ec...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\vim.py
move "venv\Lib\site-packages\pygments\styles\vim.py" "Archive\Duplicates\vim.py"

REM Duplicate group: 86832e8d...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\vs.py
move "venv\Lib\site-packages\pygments\styles\vs.py" "Archive\Duplicates\vs.py"

REM Duplicate group: 3b32d5c6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\xcode.py
move "venv\Lib\site-packages\pygments\styles\xcode.py" "Archive\Duplicates\xcode.py"

REM Duplicate group: c6f7a245...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\zenburn.py
move "venv\Lib\site-packages\pygments\styles\zenburn.py" "Archive\Duplicates\zenburn.py"

REM Duplicate group: a279da65...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\_mapping.py
move "venv\Lib\site-packages\pygments\styles\_mapping.py" "Archive\Duplicates\_mapping.py"

REM Duplicate group: eb7363a6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments\styles\__init__.py
move "venv\Lib\site-packages\pygments\styles\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: e3efb166...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\entry_points.txt
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\entry_points.txt" "Archive\Duplicates\entry_points.txt"

REM Duplicate group: 49fbc1b4...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\METADATA
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\METADATA" "Archive\Duplicates\METADATA"

REM Duplicate group: 078de1df...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\licenses\AUTHORS
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\licenses\AUTHORS" "Archive\Duplicates\AUTHORS"

REM Duplicate group: 36a13c90...
REM Keeping: n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\licenses\LICENSE
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\licenses\LICENSE" "Archive\Duplicates\LICENSE"

REM Duplicate group: 22843d9e...
REM Keeping: n8n_builder\venv\Lib\site-packages\pytest\__init__.py
move "venv\Lib\site-packages\pytest\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 0d4b4572...
REM Keeping: n8n_builder\venv\Lib\site-packages\pytest\__main__.py
move "venv\Lib\site-packages\pytest\__main__.py" "Archive\Duplicates\__main__.py"

REM Duplicate group: e773ebd6...
REM Keeping: n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\entry_points.txt
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\entry_points.txt" "Archive\Duplicates\entry_points.txt"

REM Duplicate group: 85f19f10...
REM Keeping: n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\METADATA
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\METADATA" "Archive\Duplicates\METADATA"

REM Duplicate group: fd1734d5...
REM Keeping: n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\top_level.txt
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\top_level.txt" "Archive\Duplicates\top_level.txt"

REM Duplicate group: 08dd01ac...
REM Keeping: n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\WHEEL
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: e5100a41...
REM Keeping: n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\licenses\AUTHORS
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\licenses\AUTHORS" "Archive\Duplicates\AUTHORS"

REM Duplicate group: bd27e41b...
REM Keeping: n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\licenses\LICENSE
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\licenses\LICENSE" "Archive\Duplicates\LICENSE"

REM Duplicate group: bd2fe8a2...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\archive_util.py
move "venv\Lib\site-packages\setuptools\archive_util.py" "Archive\Duplicates\archive_util.py"

REM Duplicate group: e946c7d0...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\build_meta.py
move "venv\Lib\site-packages\setuptools\build_meta.py" "Archive\Duplicates\build_meta.py"

REM Duplicate group: a32a382b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\cli.exe
move "n8n_builder\venv\Lib\site-packages\setuptools\cli-32.exe" "Archive\Duplicates\cli-32.exe"
move "venv\Lib\site-packages\setuptools\cli-32.exe" "Archive\Duplicates\cli-32.exe"
move "venv\Lib\site-packages\setuptools\cli.exe" "Archive\Duplicates\cli.exe"

REM Duplicate group: d2778164...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\cli-64.exe
move "venv\Lib\site-packages\setuptools\cli-64.exe" "Archive\Duplicates\cli-64.exe"

REM Duplicate group: 305ab0a5...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\cli-arm64.exe
move "venv\Lib\site-packages\setuptools\cli-arm64.exe" "Archive\Duplicates\cli-arm64.exe"

REM Duplicate group: 94491d75...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\depends.py
move "venv\Lib\site-packages\setuptools\depends.py" "Archive\Duplicates\depends.py"

REM Duplicate group: 5213c4de...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\dep_util.py
move "venv\Lib\site-packages\setuptools\dep_util.py" "Archive\Duplicates\dep_util.py"

REM Duplicate group: 29b8e3bf...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\discovery.py
move "venv\Lib\site-packages\setuptools\discovery.py" "Archive\Duplicates\discovery.py"

REM Duplicate group: f82f18af...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\dist.py
move "venv\Lib\site-packages\setuptools\dist.py" "Archive\Duplicates\dist.py"

REM Duplicate group: 773528bb...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\errors.py
move "venv\Lib\site-packages\setuptools\errors.py" "Archive\Duplicates\errors.py"

REM Duplicate group: cb98c1d5...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\extension.py
move "venv\Lib\site-packages\setuptools\extension.py" "Archive\Duplicates\extension.py"

REM Duplicate group: 9e7c3495...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\glob.py
move "venv\Lib\site-packages\setuptools\glob.py" "Archive\Duplicates\glob.py"

REM Duplicate group: e97c622b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\gui.exe
move "n8n_builder\venv\Lib\site-packages\setuptools\gui-32.exe" "Archive\Duplicates\gui-32.exe"
move "venv\Lib\site-packages\setuptools\gui-32.exe" "Archive\Duplicates\gui-32.exe"
move "venv\Lib\site-packages\setuptools\gui.exe" "Archive\Duplicates\gui.exe"

REM Duplicate group: 2ffc9a24...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\gui-64.exe
move "venv\Lib\site-packages\setuptools\gui-64.exe" "Archive\Duplicates\gui-64.exe"

REM Duplicate group: fccf856a...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\gui-arm64.exe
move "venv\Lib\site-packages\setuptools\gui-arm64.exe" "Archive\Duplicates\gui-arm64.exe"

REM Duplicate group: 34c4d5bc...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\installer.py
move "venv\Lib\site-packages\setuptools\installer.py" "Archive\Duplicates\installer.py"

REM Duplicate group: d1765679...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\launch.py
move "venv\Lib\site-packages\setuptools\launch.py" "Archive\Duplicates\launch.py"

REM Duplicate group: aca44136...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\logging.py
move "venv\Lib\site-packages\setuptools\logging.py" "Archive\Duplicates\logging.py"

REM Duplicate group: b38f6c1c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\monkey.py
move "venv\Lib\site-packages\setuptools\monkey.py" "Archive\Duplicates\monkey.py"

REM Duplicate group: adb4e371...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\msvc.py
move "venv\Lib\site-packages\setuptools\msvc.py" "Archive\Duplicates\msvc.py"

REM Duplicate group: c6aa890d...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\namespaces.py
move "venv\Lib\site-packages\setuptools\namespaces.py" "Archive\Duplicates\namespaces.py"

REM Duplicate group: 54555192...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\package_index.py
move "venv\Lib\site-packages\setuptools\package_index.py" "Archive\Duplicates\package_index.py"

REM Duplicate group: cc3dfaa6...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\py34compat.py
move "venv\Lib\site-packages\setuptools\py34compat.py" "Archive\Duplicates\py34compat.py"

REM Duplicate group: c8f96cb4...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\sandbox.py
move "venv\Lib\site-packages\setuptools\sandbox.py" "Archive\Duplicates\sandbox.py"

REM Duplicate group: 762d226e...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\script (dev).tmpl
move "venv\Lib\site-packages\setuptools\script (dev).tmpl" "Archive\Duplicates\script (dev).tmpl"

REM Duplicate group: c7c13d61...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\script.tmpl
move "venv\Lib\site-packages\setuptools\script.tmpl" "Archive\Duplicates\script.tmpl"

REM Duplicate group: 01778f86...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\unicode_utils.py
move "venv\Lib\site-packages\setuptools\unicode_utils.py" "Archive\Duplicates\unicode_utils.py"

REM Duplicate group: e862a919...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\version.py
move "venv\Lib\site-packages\setuptools\version.py" "Archive\Duplicates\version.py"

REM Duplicate group: 1e62169f...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\wheel.py
move "venv\Lib\site-packages\setuptools\wheel.py" "Archive\Duplicates\wheel.py"

REM Duplicate group: f2cab2a0...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\windows_support.py
move "venv\Lib\site-packages\setuptools\windows_support.py" "Archive\Duplicates\windows_support.py"

REM Duplicate group: 00eb5ca8...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_deprecation_warning.py
move "venv\Lib\site-packages\setuptools\_deprecation_warning.py" "Archive\Duplicates\_deprecation_warning.py"

REM Duplicate group: 06143d69...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_entry_points.py
move "venv\Lib\site-packages\setuptools\_entry_points.py" "Archive\Duplicates\_entry_points.py"

REM Duplicate group: c79f492b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_imp.py
move "venv\Lib\site-packages\setuptools\_imp.py" "Archive\Duplicates\_imp.py"

REM Duplicate group: 34e9c62c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_importlib.py
move "venv\Lib\site-packages\setuptools\_importlib.py" "Archive\Duplicates\_importlib.py"

REM Duplicate group: 1cea9ea2...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_itertools.py
move "venv\Lib\site-packages\setuptools\_itertools.py" "Archive\Duplicates\_itertools.py"

REM Duplicate group: 6c60d27a...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_path.py
move "venv\Lib\site-packages\setuptools\_path.py" "Archive\Duplicates\_path.py"

REM Duplicate group: ef9f2f90...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_reqs.py
move "venv\Lib\site-packages\setuptools\_reqs.py" "Archive\Duplicates\_reqs.py"

REM Duplicate group: 5623c289...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\__init__.py
move "venv\Lib\site-packages\setuptools\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 6b8a4071...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\alias.py
move "venv\Lib\site-packages\setuptools\command\alias.py" "Archive\Duplicates\alias.py"

REM Duplicate group: 956c9d44...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\bdist_egg.py
move "venv\Lib\site-packages\setuptools\command\bdist_egg.py" "Archive\Duplicates\bdist_egg.py"

REM Duplicate group: 952dba26...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\bdist_rpm.py
move "venv\Lib\site-packages\setuptools\command\bdist_rpm.py" "Archive\Duplicates\bdist_rpm.py"

REM Duplicate group: d4bc6606...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\build.py
move "venv\Lib\site-packages\setuptools\command\build.py" "Archive\Duplicates\build.py"

REM Duplicate group: 2d4bff77...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\build_clib.py
move "venv\Lib\site-packages\setuptools\command\build_clib.py" "Archive\Duplicates\build_clib.py"

REM Duplicate group: 1ba005d5...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\build_ext.py
move "venv\Lib\site-packages\setuptools\command\build_ext.py" "Archive\Duplicates\build_ext.py"

REM Duplicate group: 4724b684...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\build_py.py
move "venv\Lib\site-packages\setuptools\command\build_py.py" "Archive\Duplicates\build_py.py"

REM Duplicate group: 485d0c7e...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\develop.py
move "venv\Lib\site-packages\setuptools\command\develop.py" "Archive\Duplicates\develop.py"

REM Duplicate group: bf0f0266...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\dist_info.py
move "venv\Lib\site-packages\setuptools\command\dist_info.py" "Archive\Duplicates\dist_info.py"

REM Duplicate group: ca291c26...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\easy_install.py
move "venv\Lib\site-packages\setuptools\command\easy_install.py" "Archive\Duplicates\easy_install.py"

REM Duplicate group: 5b7867e1...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\editable_wheel.py
move "venv\Lib\site-packages\setuptools\command\editable_wheel.py" "Archive\Duplicates\editable_wheel.py"

REM Duplicate group: fda66863...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\egg_info.py
move "venv\Lib\site-packages\setuptools\command\egg_info.py" "Archive\Duplicates\egg_info.py"

REM Duplicate group: 845b54b9...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\install.py
move "venv\Lib\site-packages\setuptools\command\install.py" "Archive\Duplicates\install.py"

REM Duplicate group: b3e5662b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\install_egg_info.py
move "venv\Lib\site-packages\setuptools\command\install_egg_info.py" "Archive\Duplicates\install_egg_info.py"

REM Duplicate group: 214d8644...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\install_lib.py
move "venv\Lib\site-packages\setuptools\command\install_lib.py" "Archive\Duplicates\install_lib.py"

REM Duplicate group: 7458b238...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\install_scripts.py
move "venv\Lib\site-packages\setuptools\command\install_scripts.py" "Archive\Duplicates\install_scripts.py"

REM Duplicate group: 0b558625...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\launcher manifest.xml
move "venv\Lib\site-packages\setuptools\command\launcher manifest.xml" "Archive\Duplicates\launcher manifest.xml"

REM Duplicate group: 4630e987...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\py36compat.py
move "venv\Lib\site-packages\setuptools\command\py36compat.py" "Archive\Duplicates\py36compat.py"

REM Duplicate group: 58e7138e...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\register.py
move "venv\Lib\site-packages\setuptools\command\register.py" "Archive\Duplicates\register.py"

REM Duplicate group: 3ebd81d3...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\rotate.py
move "venv\Lib\site-packages\setuptools\command\rotate.py" "Archive\Duplicates\rotate.py"

REM Duplicate group: c71d737d...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\saveopts.py
move "venv\Lib\site-packages\setuptools\command\saveopts.py" "Archive\Duplicates\saveopts.py"

REM Duplicate group: c04c8525...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\sdist.py
move "venv\Lib\site-packages\setuptools\command\sdist.py" "Archive\Duplicates\sdist.py"

REM Duplicate group: 6bfb403b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\setopt.py
move "venv\Lib\site-packages\setuptools\command\setopt.py" "Archive\Duplicates\setopt.py"

REM Duplicate group: 31458eaa...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\test.py
move "venv\Lib\site-packages\setuptools\command\test.py" "Archive\Duplicates\test.py"

REM Duplicate group: dcb51ba6...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\upload.py
move "venv\Lib\site-packages\setuptools\command\upload.py" "Archive\Duplicates\upload.py"

REM Duplicate group: ca61d508...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\upload_docs.py
move "venv\Lib\site-packages\setuptools\command\upload_docs.py" "Archive\Duplicates\upload_docs.py"

REM Duplicate group: adf722bc...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\command\__init__.py
move "venv\Lib\site-packages\setuptools\command\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: f3619c72...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\expand.py
move "venv\Lib\site-packages\setuptools\config\expand.py" "Archive\Duplicates\expand.py"

REM Duplicate group: f23d20ea...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\pyprojecttoml.py
move "venv\Lib\site-packages\setuptools\config\pyprojecttoml.py" "Archive\Duplicates\pyprojecttoml.py"

REM Duplicate group: 899329a3...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\setupcfg.py
move "venv\Lib\site-packages\setuptools\config\setupcfg.py" "Archive\Duplicates\setupcfg.py"

REM Duplicate group: 47bec85c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\_apply_pyprojecttoml.py
move "venv\Lib\site-packages\setuptools\config\_apply_pyprojecttoml.py" "Archive\Duplicates\_apply_pyprojecttoml.py"

REM Duplicate group: 18326477...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\__init__.py
move "venv\Lib\site-packages\setuptools\config\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 9d6fb658...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\error_reporting.py
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\error_reporting.py" "Archive\Duplicates\error_reporting.py"

REM Duplicate group: ab17441b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\extra_validations.py
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\extra_validations.py" "Archive\Duplicates\extra_validations.py"

REM Duplicate group: d3e20b6b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_exceptions.py
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_exceptions.py" "Archive\Duplicates\fastjsonschema_exceptions.py"

REM Duplicate group: 7d8e59f5...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_validations.py
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_validations.py" "Archive\Duplicates\fastjsonschema_validations.py"

REM Duplicate group: d54ca134...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\formats.py
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\formats.py" "Archive\Duplicates\formats.py"

REM Duplicate group: fbd22e53...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\__init__.py
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 95e3912f...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\extern\__init__.py
move "venv\Lib\site-packages\setuptools\extern\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 9d4248d2...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\archive_util.py
move "venv\Lib\site-packages\setuptools\_distutils\archive_util.py" "Archive\Duplicates\archive_util.py"

REM Duplicate group: 0bc90003...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\bcppcompiler.py
move "venv\Lib\site-packages\setuptools\_distutils\bcppcompiler.py" "Archive\Duplicates\bcppcompiler.py"

REM Duplicate group: efd651cd...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\ccompiler.py
move "venv\Lib\site-packages\setuptools\_distutils\ccompiler.py" "Archive\Duplicates\ccompiler.py"

REM Duplicate group: aadbbf53...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\cmd.py
move "venv\Lib\site-packages\setuptools\_distutils\cmd.py" "Archive\Duplicates\cmd.py"

REM Duplicate group: 0e3982bd...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\config.py
move "venv\Lib\site-packages\setuptools\_distutils\config.py" "Archive\Duplicates\config.py"

REM Duplicate group: c64b0e5c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\core.py
move "venv\Lib\site-packages\setuptools\_distutils\core.py" "Archive\Duplicates\core.py"

REM Duplicate group: ba2636ac...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\cygwinccompiler.py
move "venv\Lib\site-packages\setuptools\_distutils\cygwinccompiler.py" "Archive\Duplicates\cygwinccompiler.py"

REM Duplicate group: bc1e4c71...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\debug.py
move "venv\Lib\site-packages\setuptools\_distutils\debug.py" "Archive\Duplicates\debug.py"

REM Duplicate group: baed01b0...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\dep_util.py
move "venv\Lib\site-packages\setuptools\_distutils\dep_util.py" "Archive\Duplicates\dep_util.py"

REM Duplicate group: 34549b8f...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\dir_util.py
move "venv\Lib\site-packages\setuptools\_distutils\dir_util.py" "Archive\Duplicates\dir_util.py"

REM Duplicate group: 99f07c52...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\dist.py
move "venv\Lib\site-packages\setuptools\_distutils\dist.py" "Archive\Duplicates\dist.py"

REM Duplicate group: 111c454a...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\errors.py
move "venv\Lib\site-packages\setuptools\_distutils\errors.py" "Archive\Duplicates\errors.py"

REM Duplicate group: 68941c98...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\extension.py
move "venv\Lib\site-packages\setuptools\_distutils\extension.py" "Archive\Duplicates\extension.py"

REM Duplicate group: 1ccb8a82...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\fancy_getopt.py
move "venv\Lib\site-packages\setuptools\_distutils\fancy_getopt.py" "Archive\Duplicates\fancy_getopt.py"

REM Duplicate group: 9347530e...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\filelist.py
move "venv\Lib\site-packages\setuptools\_distutils\filelist.py" "Archive\Duplicates\filelist.py"

REM Duplicate group: 7fe98ee6...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\file_util.py
move "venv\Lib\site-packages\setuptools\_distutils\file_util.py" "Archive\Duplicates\file_util.py"

REM Duplicate group: 9bb6d133...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\log.py
move "venv\Lib\site-packages\setuptools\_distutils\log.py" "Archive\Duplicates\log.py"

REM Duplicate group: 1761f856...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\msvc9compiler.py
move "venv\Lib\site-packages\setuptools\_distutils\msvc9compiler.py" "Archive\Duplicates\msvc9compiler.py"

REM Duplicate group: 85cccd8c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\msvccompiler.py
move "venv\Lib\site-packages\setuptools\_distutils\msvccompiler.py" "Archive\Duplicates\msvccompiler.py"

REM Duplicate group: d8ec2dd4...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\py38compat.py
move "venv\Lib\site-packages\setuptools\_distutils\py38compat.py" "Archive\Duplicates\py38compat.py"

REM Duplicate group: 87aafd66...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\py39compat.py
move "venv\Lib\site-packages\setuptools\_distutils\py39compat.py" "Archive\Duplicates\py39compat.py"

REM Duplicate group: 1337738b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\spawn.py
move "venv\Lib\site-packages\setuptools\_distutils\spawn.py" "Archive\Duplicates\spawn.py"

REM Duplicate group: da3a1497...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\sysconfig.py
move "venv\Lib\site-packages\setuptools\_distutils\sysconfig.py" "Archive\Duplicates\sysconfig.py"

REM Duplicate group: 486ab4e7...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\text_file.py
move "venv\Lib\site-packages\setuptools\_distutils\text_file.py" "Archive\Duplicates\text_file.py"

REM Duplicate group: 50ecbf04...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\unixccompiler.py
move "venv\Lib\site-packages\setuptools\_distutils\unixccompiler.py" "Archive\Duplicates\unixccompiler.py"

REM Duplicate group: 19690d43...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\util.py
move "venv\Lib\site-packages\setuptools\_distutils\util.py" "Archive\Duplicates\util.py"

REM Duplicate group: f7b9c826...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\version.py
move "venv\Lib\site-packages\setuptools\_distutils\version.py" "Archive\Duplicates\version.py"

REM Duplicate group: d62d3724...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\versionpredicate.py
move "venv\Lib\site-packages\setuptools\_distutils\versionpredicate.py" "Archive\Duplicates\versionpredicate.py"

REM Duplicate group: b9fb9a52...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\_collections.py
move "venv\Lib\site-packages\setuptools\_distutils\_collections.py" "Archive\Duplicates\_collections.py"

REM Duplicate group: 9c9dec5c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\_functools.py
move "venv\Lib\site-packages\setuptools\_distutils\_functools.py" "Archive\Duplicates\_functools.py"

REM Duplicate group: e533f53d...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\_macos_compat.py
move "venv\Lib\site-packages\setuptools\_distutils\_macos_compat.py" "Archive\Duplicates\_macos_compat.py"

REM Duplicate group: b4876c95...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\_msvccompiler.py
move "venv\Lib\site-packages\setuptools\_distutils\_msvccompiler.py" "Archive\Duplicates\_msvccompiler.py"

REM Duplicate group: 247f9ecb...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\__init__.py
move "venv\Lib\site-packages\setuptools\_distutils\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 7e9a61e2...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\bdist.py
move "venv\Lib\site-packages\setuptools\_distutils\command\bdist.py" "Archive\Duplicates\bdist.py"

REM Duplicate group: 25e05968...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\bdist_dumb.py
move "venv\Lib\site-packages\setuptools\_distutils\command\bdist_dumb.py" "Archive\Duplicates\bdist_dumb.py"

REM Duplicate group: 1cf82eb2...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\bdist_rpm.py
move "venv\Lib\site-packages\setuptools\_distutils\command\bdist_rpm.py" "Archive\Duplicates\bdist_rpm.py"

REM Duplicate group: 65313396...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build.py
move "venv\Lib\site-packages\setuptools\_distutils\command\build.py" "Archive\Duplicates\build.py"

REM Duplicate group: 6aa9bde5...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build_clib.py
move "venv\Lib\site-packages\setuptools\_distutils\command\build_clib.py" "Archive\Duplicates\build_clib.py"

REM Duplicate group: 0db6376c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build_ext.py
move "venv\Lib\site-packages\setuptools\_distutils\command\build_ext.py" "Archive\Duplicates\build_ext.py"

REM Duplicate group: 40e19079...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build_py.py
move "venv\Lib\site-packages\setuptools\_distutils\command\build_py.py" "Archive\Duplicates\build_py.py"

REM Duplicate group: 6a62cd29...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build_scripts.py
move "venv\Lib\site-packages\setuptools\_distutils\command\build_scripts.py" "Archive\Duplicates\build_scripts.py"

REM Duplicate group: cef3dc96...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\check.py
move "venv\Lib\site-packages\setuptools\_distutils\command\check.py" "Archive\Duplicates\check.py"

REM Duplicate group: 2d8e3f2b...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\clean.py
move "venv\Lib\site-packages\setuptools\_distutils\command\clean.py" "Archive\Duplicates\clean.py"

REM Duplicate group: 0cb64d61...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\config.py
move "venv\Lib\site-packages\setuptools\_distutils\command\config.py" "Archive\Duplicates\config.py"

REM Duplicate group: 9a254bac...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install.py
move "venv\Lib\site-packages\setuptools\_distutils\command\install.py" "Archive\Duplicates\install.py"

REM Duplicate group: 46b54f5d...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_data.py
move "venv\Lib\site-packages\setuptools\_distutils\command\install_data.py" "Archive\Duplicates\install_data.py"

REM Duplicate group: cedf3ebc...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_egg_info.py
move "venv\Lib\site-packages\setuptools\_distutils\command\install_egg_info.py" "Archive\Duplicates\install_egg_info.py"

REM Duplicate group: bbff011a...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_headers.py
move "venv\Lib\site-packages\setuptools\_distutils\command\install_headers.py" "Archive\Duplicates\install_headers.py"

REM Duplicate group: bb1803b4...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_lib.py
move "venv\Lib\site-packages\setuptools\_distutils\command\install_lib.py" "Archive\Duplicates\install_lib.py"

REM Duplicate group: d131c77c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_scripts.py
move "venv\Lib\site-packages\setuptools\_distutils\command\install_scripts.py" "Archive\Duplicates\install_scripts.py"

REM Duplicate group: 282f467f...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\py37compat.py
move "venv\Lib\site-packages\setuptools\_distutils\command\py37compat.py" "Archive\Duplicates\py37compat.py"

REM Duplicate group: f33c3218...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\register.py
move "venv\Lib\site-packages\setuptools\_distutils\command\register.py" "Archive\Duplicates\register.py"

REM Duplicate group: f4e6342d...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\sdist.py
move "venv\Lib\site-packages\setuptools\_distutils\command\sdist.py" "Archive\Duplicates\sdist.py"

REM Duplicate group: 7cfef463...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\upload.py
move "venv\Lib\site-packages\setuptools\_distutils\command\upload.py" "Archive\Duplicates\upload.py"

REM Duplicate group: 9abfe95c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\_framework_compat.py
move "venv\Lib\site-packages\setuptools\_distutils\command\_framework_compat.py" "Archive\Duplicates\_framework_compat.py"

REM Duplicate group: 1b9abceb...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\__init__.py
move "venv\Lib\site-packages\setuptools\_distutils\command\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: f3186384...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\ordered_set.py
move "venv\Lib\site-packages\setuptools\_vendor\ordered_set.py" "Archive\Duplicates\ordered_set.py"

REM Duplicate group: 7bbf1f21...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\typing_extensions.py
move "venv\Lib\site-packages\setuptools\_vendor\typing_extensions.py" "Archive\Duplicates\typing_extensions.py"

REM Duplicate group: 910b70e4...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_adapters.py
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_adapters.py" "Archive\Duplicates\_adapters.py"

REM Duplicate group: 353c8330...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_collections.py
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_collections.py" "Archive\Duplicates\_collections.py"

REM Duplicate group: 9a8dbb92...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_compat.py
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_compat.py" "Archive\Duplicates\_compat.py"

REM Duplicate group: 0cff4df9...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_functools.py
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_functools.py" "Archive\Duplicates\_functools.py"

REM Duplicate group: e8b2ec15...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_itertools.py
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_itertools.py" "Archive\Duplicates\_itertools.py"

REM Duplicate group: 9c2789e4...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_meta.py
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_meta.py" "Archive\Duplicates\_meta.py"

REM Duplicate group: 8ff71463...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_text.py
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_text.py" "Archive\Duplicates\_text.py"

REM Duplicate group: d99add70...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\__init__.py
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 1192ca38...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\jaraco\functools.py
move "venv\Lib\site-packages\setuptools\_vendor\jaraco\functools.py" "Archive\Duplicates\functools.py"

REM Duplicate group: 2ef9196f...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\jaraco\text\__init__.py
move "venv\Lib\site-packages\setuptools\_vendor\jaraco\text\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 864c5ef9...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\more_itertools\more.py
move "venv\Lib\site-packages\setuptools\_vendor\more_itertools\more.py" "Archive\Duplicates\more.py"

REM Duplicate group: c8a83456...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\more_itertools\recipes.py
move "venv\Lib\site-packages\setuptools\_vendor\more_itertools\recipes.py" "Archive\Duplicates\recipes.py"

REM Duplicate group: d4b166b1...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\more_itertools\__init__.py
move "venv\Lib\site-packages\setuptools\_vendor\more_itertools\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 88753faf...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\markers.py
move "venv\Lib\site-packages\setuptools\_vendor\packaging\markers.py" "Archive\Duplicates\markers.py"

REM Duplicate group: a8303b07...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\requirements.py
move "venv\Lib\site-packages\setuptools\_vendor\packaging\requirements.py" "Archive\Duplicates\requirements.py"

REM Duplicate group: d3262b65...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\entry_points.txt
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\entry_points.txt" "Archive\Duplicates\entry_points.txt"

REM Duplicate group: 7a7126e0...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\LICENSE
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\LICENSE" "Archive\Duplicates\LICENSE"

REM Duplicate group: 9e59bd13...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\METADATA
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\METADATA" "Archive\Duplicates\METADATA"

REM Duplicate group: 087f72a0...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\RECORD
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\RECORD" "Archive\Duplicates\RECORD"

REM Duplicate group: 789a691c...
REM Keeping: n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\top_level.txt
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\top_level.txt" "Archive\Duplicates\top_level.txt"

REM Duplicate group: 012a3e19...
REM Keeping: n8n_builder\venv\Lib\site-packages\_distutils_hack\override.py
move "venv\Lib\site-packages\_distutils_hack\override.py" "Archive\Duplicates\override.py"

REM Duplicate group: 128079c8...
REM Keeping: n8n_builder\venv\Lib\site-packages\_distutils_hack\__init__.py
move "venv\Lib\site-packages\_distutils_hack\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 7f5ca55c...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\cacheprovider.py
move "venv\Lib\site-packages\_pytest\cacheprovider.py" "Archive\Duplicates\cacheprovider.py"

REM Duplicate group: b7c367bf...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\capture.py
move "venv\Lib\site-packages\_pytest\capture.py" "Archive\Duplicates\capture.py"

REM Duplicate group: 09999b1d...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\compat.py
move "venv\Lib\site-packages\_pytest\compat.py" "Archive\Duplicates\compat.py"

REM Duplicate group: 9517e5bb...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\debugging.py
move "venv\Lib\site-packages\_pytest\debugging.py" "Archive\Duplicates\debugging.py"

REM Duplicate group: 42c51201...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\deprecated.py
move "venv\Lib\site-packages\_pytest\deprecated.py" "Archive\Duplicates\deprecated.py"

REM Duplicate group: ab3b0c92...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\doctest.py
move "venv\Lib\site-packages\_pytest\doctest.py" "Archive\Duplicates\doctest.py"

REM Duplicate group: 16201224...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\faulthandler.py
move "venv\Lib\site-packages\_pytest\faulthandler.py" "Archive\Duplicates\faulthandler.py"

REM Duplicate group: b755fe9e...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\fixtures.py
move "venv\Lib\site-packages\_pytest\fixtures.py" "Archive\Duplicates\fixtures.py"

REM Duplicate group: b56c4274...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\freeze_support.py
move "venv\Lib\site-packages\_pytest\freeze_support.py" "Archive\Duplicates\freeze_support.py"

REM Duplicate group: abd383a5...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\helpconfig.py
move "venv\Lib\site-packages\_pytest\helpconfig.py" "Archive\Duplicates\helpconfig.py"

REM Duplicate group: 8e18e05a...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\hookspec.py
move "venv\Lib\site-packages\_pytest\hookspec.py" "Archive\Duplicates\hookspec.py"

REM Duplicate group: ce03a319...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\junitxml.py
move "venv\Lib\site-packages\_pytest\junitxml.py" "Archive\Duplicates\junitxml.py"

REM Duplicate group: fdae2c7e...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\legacypath.py
move "venv\Lib\site-packages\_pytest\legacypath.py" "Archive\Duplicates\legacypath.py"

REM Duplicate group: 05e3b87b...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\logging.py
move "venv\Lib\site-packages\_pytest\logging.py" "Archive\Duplicates\logging.py"

REM Duplicate group: e774c8f1...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\main.py
move "venv\Lib\site-packages\_pytest\main.py" "Archive\Duplicates\main.py"

REM Duplicate group: 23ea5d2d...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\monkeypatch.py
move "venv\Lib\site-packages\_pytest\monkeypatch.py" "Archive\Duplicates\monkeypatch.py"

REM Duplicate group: 6633cb4d...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\nodes.py
move "venv\Lib\site-packages\_pytest\nodes.py" "Archive\Duplicates\nodes.py"

REM Duplicate group: f0cbaa33...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\outcomes.py
move "venv\Lib\site-packages\_pytest\outcomes.py" "Archive\Duplicates\outcomes.py"

REM Duplicate group: fa3e6534...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\pastebin.py
move "venv\Lib\site-packages\_pytest\pastebin.py" "Archive\Duplicates\pastebin.py"

REM Duplicate group: 3d8592e5...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\pathlib.py
move "venv\Lib\site-packages\_pytest\pathlib.py" "Archive\Duplicates\pathlib.py"

REM Duplicate group: 9423c405...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\pytester.py
move "venv\Lib\site-packages\_pytest\pytester.py" "Archive\Duplicates\pytester.py"

REM Duplicate group: abd21426...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\pytester_assertions.py
move "venv\Lib\site-packages\_pytest\pytester_assertions.py" "Archive\Duplicates\pytester_assertions.py"

REM Duplicate group: b99511e7...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\python.py
move "venv\Lib\site-packages\_pytest\python.py" "Archive\Duplicates\python.py"

REM Duplicate group: a66f2499...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\python_api.py
move "venv\Lib\site-packages\_pytest\python_api.py" "Archive\Duplicates\python_api.py"

REM Duplicate group: 67e4c5b0...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\raises.py
move "venv\Lib\site-packages\_pytest\raises.py" "Archive\Duplicates\raises.py"

REM Duplicate group: e59c3e85...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\recwarn.py
move "venv\Lib\site-packages\_pytest\recwarn.py" "Archive\Duplicates\recwarn.py"

REM Duplicate group: fff8ec1a...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\reports.py
move "venv\Lib\site-packages\_pytest\reports.py" "Archive\Duplicates\reports.py"

REM Duplicate group: 52cf2876...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\runner.py
move "venv\Lib\site-packages\_pytest\runner.py" "Archive\Duplicates\runner.py"

REM Duplicate group: 076480b3...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\scope.py
move "venv\Lib\site-packages\_pytest\scope.py" "Archive\Duplicates\scope.py"

REM Duplicate group: 79c8ff0a...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\setuponly.py
move "venv\Lib\site-packages\_pytest\setuponly.py" "Archive\Duplicates\setuponly.py"

REM Duplicate group: fe8857c1...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\setupplan.py
move "venv\Lib\site-packages\_pytest\setupplan.py" "Archive\Duplicates\setupplan.py"

REM Duplicate group: 5f62ebed...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\skipping.py
move "venv\Lib\site-packages\_pytest\skipping.py" "Archive\Duplicates\skipping.py"

REM Duplicate group: ec38c307...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\stash.py
move "venv\Lib\site-packages\_pytest\stash.py" "Archive\Duplicates\stash.py"

REM Duplicate group: e935d255...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\stepwise.py
move "venv\Lib\site-packages\_pytest\stepwise.py" "Archive\Duplicates\stepwise.py"

REM Duplicate group: c3849db2...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\terminal.py
move "venv\Lib\site-packages\_pytest\terminal.py" "Archive\Duplicates\terminal.py"

REM Duplicate group: 41b99cfc...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\threadexception.py
move "venv\Lib\site-packages\_pytest\threadexception.py" "Archive\Duplicates\threadexception.py"

REM Duplicate group: a1dbfeb3...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\timing.py
move "venv\Lib\site-packages\_pytest\timing.py" "Archive\Duplicates\timing.py"

REM Duplicate group: 713ce87a...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\tmpdir.py
move "venv\Lib\site-packages\_pytest\tmpdir.py" "Archive\Duplicates\tmpdir.py"

REM Duplicate group: 5e6f798b...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\tracemalloc.py
move "venv\Lib\site-packages\_pytest\tracemalloc.py" "Archive\Duplicates\tracemalloc.py"

REM Duplicate group: 4ca5f05d...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\unittest.py
move "venv\Lib\site-packages\_pytest\unittest.py" "Archive\Duplicates\unittest.py"

REM Duplicate group: 58faf05c...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\unraisableexception.py
move "venv\Lib\site-packages\_pytest\unraisableexception.py" "Archive\Duplicates\unraisableexception.py"

REM Duplicate group: a798e89c...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\warnings.py
move "venv\Lib\site-packages\_pytest\warnings.py" "Archive\Duplicates\warnings.py"

REM Duplicate group: c53145ed...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\warning_types.py
move "venv\Lib\site-packages\_pytest\warning_types.py" "Archive\Duplicates\warning_types.py"

REM Duplicate group: 01552af0...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_argcomplete.py
move "venv\Lib\site-packages\_pytest\_argcomplete.py" "Archive\Duplicates\_argcomplete.py"

REM Duplicate group: 89ec4332...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_version.py
move "venv\Lib\site-packages\_pytest\_version.py" "Archive\Duplicates\_version.py"

REM Duplicate group: c7c2ce8f...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\__init__.py
move "venv\Lib\site-packages\_pytest\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 24dcfead...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\assertion\rewrite.py
move "venv\Lib\site-packages\_pytest\assertion\rewrite.py" "Archive\Duplicates\rewrite.py"

REM Duplicate group: a5e45edf...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\assertion\truncate.py
move "venv\Lib\site-packages\_pytest\assertion\truncate.py" "Archive\Duplicates\truncate.py"

REM Duplicate group: b9936029...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\assertion\util.py
move "venv\Lib\site-packages\_pytest\assertion\util.py" "Archive\Duplicates\util.py"

REM Duplicate group: e342d89f...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\assertion\__init__.py
move "venv\Lib\site-packages\_pytest\assertion\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 928d6ebc...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\config\argparsing.py
move "venv\Lib\site-packages\_pytest\config\argparsing.py" "Archive\Duplicates\argparsing.py"

REM Duplicate group: ac209f93...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\config\compat.py
move "venv\Lib\site-packages\_pytest\config\compat.py" "Archive\Duplicates\compat.py"

REM Duplicate group: cd491bda...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\config\exceptions.py
move "venv\Lib\site-packages\_pytest\config\exceptions.py" "Archive\Duplicates\exceptions.py"

REM Duplicate group: 5a50358d...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\config\findpaths.py
move "venv\Lib\site-packages\_pytest\config\findpaths.py" "Archive\Duplicates\findpaths.py"

REM Duplicate group: 0beb76af...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\config\__init__.py
move "venv\Lib\site-packages\_pytest\config\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: c964b527...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\mark\expression.py
move "venv\Lib\site-packages\_pytest\mark\expression.py" "Archive\Duplicates\expression.py"

REM Duplicate group: 790fe8fe...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\mark\structures.py
move "venv\Lib\site-packages\_pytest\mark\structures.py" "Archive\Duplicates\structures.py"

REM Duplicate group: 45d80baf...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\mark\__init__.py
move "venv\Lib\site-packages\_pytest\mark\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 3241f730...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_code\code.py
move "venv\Lib\site-packages\_pytest\_code\code.py" "Archive\Duplicates\code.py"

REM Duplicate group: 08cf254e...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_code\source.py
move "venv\Lib\site-packages\_pytest\_code\source.py" "Archive\Duplicates\source.py"

REM Duplicate group: bfffda80...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_code\__init__.py
move "venv\Lib\site-packages\_pytest\_code\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: e8a69b08...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_io\pprint.py
move "venv\Lib\site-packages\_pytest\_io\pprint.py" "Archive\Duplicates\pprint.py"

REM Duplicate group: e3b45ee8...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_io\saferepr.py
move "venv\Lib\site-packages\_pytest\_io\saferepr.py" "Archive\Duplicates\saferepr.py"

REM Duplicate group: 047f3059...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_io\terminalwriter.py
move "venv\Lib\site-packages\_pytest\_io\terminalwriter.py" "Archive\Duplicates\terminalwriter.py"

REM Duplicate group: af6c0a06...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_io\wcwidth.py
move "venv\Lib\site-packages\_pytest\_io\wcwidth.py" "Archive\Duplicates\wcwidth.py"

REM Duplicate group: fb3d4ec3...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_io\__init__.py
move "venv\Lib\site-packages\_pytest\_io\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 83f4e2e4...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_py\error.py
move "venv\Lib\site-packages\_pytest\_py\error.py" "Archive\Duplicates\error.py"

REM Duplicate group: 507dc1e6...
REM Keeping: n8n_builder\venv\Lib\site-packages\_pytest\_py\path.py
move "venv\Lib\site-packages\_pytest\_py\path.py" "Archive\Duplicates\path.py"

REM Duplicate group: ffb074b8...
REM Keeping: n8n_builder\venv\Scripts\Activate.ps1
move "venv\Scripts\Activate.ps1" "Archive\Duplicates\Activate.ps1"

REM Duplicate group: cd761ddd...
REM Keeping: n8n_builder\venv\Scripts\deactivate.bat
move "venv\Scripts\deactivate.bat" "Archive\Duplicates\deactivate.bat"

REM Duplicate group: 0e42358f...
REM Keeping: n8n_builder\venv\Scripts\pip3.11.exe
move "n8n_builder\venv\Scripts\pip.exe" "Archive\Duplicates\pip.exe"
move "n8n_builder\venv\Scripts\pip3.exe" "Archive\Duplicates\pip3.exe"

REM Duplicate group: 113e6522...
REM Keeping: n8n_builder\venv\Scripts\pytest.exe
move "n8n_builder\venv\Scripts\py.test.exe" "Archive\Duplicates\py.test.exe"

REM Duplicate group: 90b6768b...
REM Keeping: n8n_builder\venv\Scripts\python.exe
move "venv\Scripts\python.exe" "Archive\Duplicates\python.exe"

REM Duplicate group: 3e0fc321...
REM Keeping: n8n_builder\venv\Scripts\pythonw.exe
move "venv\Scripts\pythonw.exe" "Archive\Duplicates\pythonw.exe"

REM Duplicate group: 68b329da...
REM Keeping: n8n_builder.egg-info\dependency_links.txt
move "venv\Lib\site-packages\passlib\ext\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\zip-safe" "Archive\Duplicates\zip-safe"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\zip-safe" "Archive\Duplicates\zip-safe"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\zip-safe" "Archive\Duplicates\zip-safe"
move "venv\Lib\site-packages\uvicorn\py.typed" "Archive\Duplicates\py.typed"

REM Duplicate group: 5bbc1e6b...
REM Keeping: projects\test-1\Test1 Workflow A.json
move "projects\test-1\create-a-workflow-that-sends-an-email-to-markeltho.json" "Archive\Duplicates\create-a-workflow-that-sends-an-email-to-markeltho.json"

REM Duplicate group: 3ff0b453...
REM Keeping: projects\test-1\test-workflow.json
move "projects\test-1\test-workflow_2025-06-14_10-23-56.json" "Archive\Duplicates\test-workflow_2025-06-14_10-23-56.json"

REM Duplicate group: fcf6b249...
REM Keeping: venv\Lib\site-packages\aiohappyeyeballs-2.6.1.dist-info\LICENSE
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\licenses\LICENSE" "Archive\Duplicates\LICENSE"

REM Duplicate group: cf056e8e...
REM Keeping: venv\Lib\site-packages\aiosignal-1.3.2.dist-info\LICENSE
move "venv\Lib\site-packages\frozenlist-1.6.2.dist-info\licenses\LICENSE" "Archive\Duplicates\LICENSE"

REM Duplicate group: 9f892250...
REM Keeping: venv\Lib\site-packages\six-1.17.0.dist-info\WHEEL
move "venv\Lib\site-packages\aiosignal-1.3.2.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: fce95ff4...
REM Keeping: venv\Lib\site-packages\cryptography\hazmat\primitives\__init__.py
move "venv\Lib\site-packages\cryptography\hazmat\bindings\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\openssl\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 9125eda3...
REM Keeping: venv\Lib\site-packages\cryptography\hazmat\decrepit\__init__.py
move "venv\Lib\site-packages\cryptography\hazmat\decrepit\ciphers\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: bd2fa011...
REM Keeping: venv\Lib\site-packages\markdown_it\py.typed
move "venv\Lib\site-packages\dotenv\py.typed" "Archive\Duplicates\py.typed"
move "venv\Lib\site-packages\mdurl\py.typed" "Archive\Duplicates\py.typed"

REM Duplicate group: 3522f1a6...
REM Keeping: venv\Lib\site-packages\frozenlist\py.typed
move "venv\Lib\site-packages\h11\py.typed" "Archive\Duplicates\py.typed"

REM Duplicate group: 9c3ef233...
REM Keeping: venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\WHEEL
move "venv\Lib\site-packages\h11-0.16.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: c3c172be...
REM Keeping: venv\Lib\site-packages\httpx-0.25.1.dist-info\WHEEL
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: 76e90429...
REM Keeping: venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\WHEEL
move "venv\Lib\site-packages\mdurl-0.1.2.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: b54ac1a1...
REM Keeping: venv\Lib\site-packages\multipart\tests\test_data\http\single_field_with_leading_newlines.yaml
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field.yaml" "Archive\Duplicates\single_field.yaml"

REM Duplicate group: 82b5ec96...
REM Keeping: venv\Lib\site-packages\yarl\py.typed
move "venv\Lib\site-packages\propcache\py.typed" "Archive\Duplicates\py.typed"

REM Duplicate group: 8d4be910...
REM Keeping: venv\Lib\site-packages\yarl-1.20.0.dist-info\WHEEL
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: 3b83ef96...
REM Keeping: venv\Lib\site-packages\yarl-1.20.0.dist-info\licenses\LICENSE
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\licenses\LICENSE" "Archive\Duplicates\LICENSE"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\LICENSE.APACHE2" "Archive\Duplicates\LICENSE.APACHE2"

REM Duplicate group: e581798a...
REM Keeping: venv\Lib\site-packages\yarl-1.20.0.dist-info\licenses\NOTICE
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\licenses\NOTICE" "Archive\Duplicates\NOTICE"

REM Duplicate group: 0fc1b4d3...
REM Keeping: venv\Lib\site-packages\pyasn1\type\__init__.py
move "venv\Lib\site-packages\pyasn1\codec\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\ber\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\cer\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\der\__init__.py" "Archive\Duplicates\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\native\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: c7d2f152...
REM Keeping: venv\Lib\site-packages\pydantic_core\_pydantic_core.cp311-win_amd64.pyd
move "venv\Lib\site-packages\~ydantic_core\_pydantic_core.cp311-win_amd64.pyd" "Archive\Duplicates\_pydantic_core.cp311-win_amd64.pyd"

REM Duplicate group: 6f7cfaed...
REM Keeping: venv\Lib\site-packages\pydantic_core\_pydantic_core.pyi
move "venv\Lib\site-packages\~ydantic_core\_pydantic_core.pyi" "Archive\Duplicates\_pydantic_core.pyi"

REM Duplicate group: 80509a1c...
REM Keeping: venv\Lib\site-packages\pydantic_core\__init__.py
move "venv\Lib\site-packages\~ydantic_core\__init__.py" "Archive\Duplicates\__init__.py"

REM Duplicate group: 680a7f5d...
REM Keeping: venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\WHEEL
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\WHEEL" "Archive\Duplicates\WHEEL"

REM Duplicate group: e8554ae9...
REM Keeping: venv\Scripts\coverage3.exe
move "venv\Scripts\coverage-3.11.exe" "Archive\Duplicates\coverage-3.11.exe"
move "venv\Scripts\coverage.exe" "Archive\Duplicates\coverage.exe"

REM Duplicate group: 35637f9a...
REM Keeping: venv\Scripts\pip3.11.exe
move "venv\Scripts\pip.exe" "Archive\Duplicates\pip.exe"
move "venv\Scripts\pip3.exe" "Archive\Duplicates\pip3.exe"

REM Duplicate group: e07ef301...
REM Keeping: venv\Scripts\pytest.exe
move "venv\Scripts\py.test.exe" "Archive\Duplicates\py.test.exe"
Move Obsolete Files to Archive
REM Move potentially obsolete files to archive
move "Documentation\API_DOCUMENTATION.md" "Archive\Obsolete\API_DOCUMENTATION.md"
move "Documentation\API_QUICK_REFERENCE.md" "Archive\Obsolete\API_QUICK_REFERENCE.md"
move "Documentation\DOCUMENTATION.MD" "Archive\Obsolete\DOCUMENTATION.MD"
move "Documentation\NN_Builder.MD" "Archive\Obsolete\NN_Builder.MD"
move "Documentation\PRD.MD" "Archive\Obsolete\PRD.MD"
move "Documentation\ProcessFlow.MD" "Archive\Obsolete\ProcessFlow.MD"
move "Documentation\UI_Enhancements.md" "Archive\Obsolete\UI_Enhancements.md"
move "Documentation\VERSION_1.0_COMPLETION_SUMMARY.md" "Archive\Obsolete\VERSION_1.0_COMPLETION_SUMMARY.md"
move "Documentation\ValidationPRD.MD" "Archive\Obsolete\ValidationPRD.MD"
move "Scripts\logs\errors.log" "Archive\Obsolete\errors.log"
move "Scripts\logs\n8n_builder.log" "Archive\Obsolete\n8n_builder.log"
move "agents\integration\__init__.py" "Archive\Obsolete\__init__.py"
move "agents\integration\message_broker.py" "Archive\Obsolete\message_broker.py"
move "agents\integration\message_protocol.py" "Archive\Obsolete\message_protocol.py"
move "agents\integration\state_manager.py" "Archive\Obsolete\state_manager.py"
move "agents\workflow_iteration_agent.py" "Archive\Obsolete\workflow_iteration_agent.py"
move "config\error_recovery_config.json" "Archive\Obsolete\error_recovery_config.json"
move "config\monitoring_config.json" "Archive\Obsolete\monitoring_config.json"
move "config\security_config.json" "Archive\Obsolete\security_config.json"
move "logs\errors.log" "Archive\Obsolete\errors.log"
move "logs\n8n_builder.log" "Archive\Obsolete\n8n_builder.log"
move "n8n_builder.egg-info\PKG-INFO" "Archive\Obsolete\PKG-INFO"
move "n8n_builder.egg-info\SOURCES.txt" "Archive\Obsolete\SOURCES.txt"
move "n8n_builder.egg-info\dependency_links.txt" "Archive\Obsolete\dependency_links.txt"
move "n8n_builder.egg-info\requires.txt" "Archive\Obsolete\requires.txt"
move "n8n_builder.egg-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "n8n_builder\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\agents\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\agents\agents\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\agents\agents\base_agent.py" "Archive\Obsolete\base_agent.py"
move "n8n_builder\agents\agents\config_manager.py" "Archive\Obsolete\config_manager.py"
move "n8n_builder\agents\agents\error_recovery_agent.py" "Archive\Obsolete\error_recovery_agent.py"
move "n8n_builder\agents\agents\integration\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\agents\agents\integration\agent_integration_manager.py" "Archive\Obsolete\agent_integration_manager.py"
move "n8n_builder\agents\agents\integration\error_recovery.py" "Archive\Obsolete\error_recovery.py"
move "n8n_builder\agents\agents\integration\event_stream_manager.py" "Archive\Obsolete\event_stream_manager.py"
move "n8n_builder\agents\agents\integration\event_types.py" "Archive\Obsolete\event_types.py"
move "n8n_builder\agents\agents\integration\message_broker.py" "Archive\Obsolete\message_broker.py"
move "n8n_builder\agents\agents\integration\message_protocol.py" "Archive\Obsolete\message_protocol.py"
move "n8n_builder\agents\agents\integration\monitoring.py" "Archive\Obsolete\monitoring.py"
move "n8n_builder\agents\agents\integration\security.py" "Archive\Obsolete\security.py"
move "n8n_builder\agents\agents\integration\state_manager.py" "Archive\Obsolete\state_manager.py"
move "n8n_builder\agents\agents\integration\ui_controller.py" "Archive\Obsolete\ui_controller.py"
move "n8n_builder\agents\agents\json_extractor_agent.py" "Archive\Obsolete\json_extractor_agent.py"
move "n8n_builder\agents\agents\llm_client.py" "Archive\Obsolete\llm_client.py"
move "n8n_builder\agents\agents\orchestrator_agent.py" "Archive\Obsolete\orchestrator_agent.py"
move "n8n_builder\agents\agents\validation_agent.py" "Archive\Obsolete\validation_agent.py"
move "n8n_builder\agents\agents\workflow_documentation_agent.py" "Archive\Obsolete\workflow_documentation_agent.py"
move "n8n_builder\agents\agents\workflow_executor_agent.py" "Archive\Obsolete\workflow_executor_agent.py"
move "n8n_builder\agents\agents\workflow_generator_agent.py" "Archive\Obsolete\workflow_generator_agent.py"
move "n8n_builder\agents\agents\workflow_optimizer_agent.py" "Archive\Obsolete\workflow_optimizer_agent.py"
move "n8n_builder\agents\agents\workflow_testing_agent.py" "Archive\Obsolete\workflow_testing_agent.py"
move "n8n_builder\agents\base_agent.py" "Archive\Obsolete\base_agent.py"
move "n8n_builder\agents\error_recovery_agent.py" "Archive\Obsolete\error_recovery_agent.py"
move "n8n_builder\agents\integration\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\agents\integration\agent_integration_manager.py" "Archive\Obsolete\agent_integration_manager.py"
move "n8n_builder\agents\integration\error_recovery.py" "Archive\Obsolete\error_recovery.py"
move "n8n_builder\agents\integration\event_stream_manager.py" "Archive\Obsolete\event_stream_manager.py"
move "n8n_builder\agents\integration\event_types.py" "Archive\Obsolete\event_types.py"
move "n8n_builder\agents\integration\message_broker.py" "Archive\Obsolete\message_broker.py"
move "n8n_builder\agents\integration\message_protocol.py" "Archive\Obsolete\message_protocol.py"
move "n8n_builder\agents\integration\monitoring.py" "Archive\Obsolete\monitoring.py"
move "n8n_builder\agents\integration\security.py" "Archive\Obsolete\security.py"
move "n8n_builder\agents\integration\state_manager.py" "Archive\Obsolete\state_manager.py"
move "n8n_builder\agents\integration\ui_controller.py" "Archive\Obsolete\ui_controller.py"
move "n8n_builder\agents\orchestrator_agent.py" "Archive\Obsolete\orchestrator_agent.py"
move "n8n_builder\agents\validation_agent.py" "Archive\Obsolete\validation_agent.py"
move "n8n_builder\agents\workflow_documentation_agent.py" "Archive\Obsolete\workflow_documentation_agent.py"
move "n8n_builder\agents\workflow_executor_agent.py" "Archive\Obsolete\workflow_executor_agent.py"
move "n8n_builder\agents\workflow_generator_agent.py" "Archive\Obsolete\workflow_generator_agent.py"
move "n8n_builder\agents\workflow_optimizer_agent.py" "Archive\Obsolete\workflow_optimizer_agent.py"
move "n8n_builder\agents\workflow_testing_agent.py" "Archive\Obsolete\workflow_testing_agent.py"
move "n8n_builder\cli.py" "Archive\Obsolete\cli.py"
move "n8n_builder\code_generation_patterns.py" "Archive\Obsolete\code_generation_patterns.py"
move "n8n_builder\config.py" "Archive\Obsolete\config.py"
move "n8n_builder\logging_config.py" "Archive\Obsolete\logging_config.py"
move "n8n_builder\performance_optimizer.py" "Archive\Obsolete\performance_optimizer.py"
move "n8n_builder\retry_manager.py" "Archive\Obsolete\retry_manager.py"
move "n8n_builder\validation\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\validation\config.py" "Archive\Obsolete\config.py"
move "n8n_builder\validation\error_codes.py" "Archive\Obsolete\error_codes.py"
move "n8n_builder\validation\validation_service.py" "Archive\Obsolete\validation_service.py"
move "n8n_builder\validation\validators\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\validation\validators\connection.py" "Archive\Obsolete\connection.py"
move "n8n_builder\validation\validators\node.py" "Archive\Obsolete\node.py"
move "n8n_builder\validation\validators\workflow_logic.py" "Archive\Obsolete\workflow_logic.py"
move "n8n_builder\validation\validators\workflow_structure.py" "Archive\Obsolete\workflow_structure.py"
move "n8n_builder\validators.py" "Archive\Obsolete\validators.py"
move "n8n_builder\venv\Lib\site-packages\_distutils_hack\override.py" "Archive\Obsolete\override.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_argcomplete.py" "Archive\Obsolete\_argcomplete.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_code\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_code\source.py" "Archive\Obsolete\source.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_io\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_io\pprint.py" "Archive\Obsolete\pprint.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_io\saferepr.py" "Archive\Obsolete\saferepr.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_io\terminalwriter.py" "Archive\Obsolete\terminalwriter.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_io\wcwidth.py" "Archive\Obsolete\wcwidth.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_py\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_py\error.py" "Archive\Obsolete\error.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\_version.py" "Archive\Obsolete\_version.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\assertion\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\assertion\truncate.py" "Archive\Obsolete\truncate.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\assertion\util.py" "Archive\Obsolete\util.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\cacheprovider.py" "Archive\Obsolete\cacheprovider.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\capture.py" "Archive\Obsolete\capture.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\compat.py" "Archive\Obsolete\compat.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\config\argparsing.py" "Archive\Obsolete\argparsing.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\config\compat.py" "Archive\Obsolete\compat.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\config\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\debugging.py" "Archive\Obsolete\debugging.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\faulthandler.py" "Archive\Obsolete\faulthandler.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\freeze_support.py" "Archive\Obsolete\freeze_support.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\helpconfig.py" "Archive\Obsolete\helpconfig.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\hookspec.py" "Archive\Obsolete\hookspec.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\junitxml.py" "Archive\Obsolete\junitxml.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\legacypath.py" "Archive\Obsolete\legacypath.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\logging.py" "Archive\Obsolete\logging.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\mark\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\mark\expression.py" "Archive\Obsolete\expression.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\monkeypatch.py" "Archive\Obsolete\monkeypatch.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\outcomes.py" "Archive\Obsolete\outcomes.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\pastebin.py" "Archive\Obsolete\pastebin.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\py.typed" "Archive\Obsolete\py.typed"
move "n8n_builder\venv\Lib\site-packages\_pytest\pytester_assertions.py" "Archive\Obsolete\pytester_assertions.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\python_api.py" "Archive\Obsolete\python_api.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\raises.py" "Archive\Obsolete\raises.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\recwarn.py" "Archive\Obsolete\recwarn.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\reports.py" "Archive\Obsolete\reports.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\runner.py" "Archive\Obsolete\runner.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\scope.py" "Archive\Obsolete\scope.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\setuponly.py" "Archive\Obsolete\setuponly.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\setupplan.py" "Archive\Obsolete\setupplan.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\skipping.py" "Archive\Obsolete\skipping.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\stash.py" "Archive\Obsolete\stash.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\stepwise.py" "Archive\Obsolete\stepwise.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\threadexception.py" "Archive\Obsolete\threadexception.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\timing.py" "Archive\Obsolete\timing.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\tmpdir.py" "Archive\Obsolete\tmpdir.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\tracemalloc.py" "Archive\Obsolete\tracemalloc.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\unittest.py" "Archive\Obsolete\unittest.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\unraisableexception.py" "Archive\Obsolete\unraisableexception.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\warning_types.py" "Archive\Obsolete\warning_types.py"
move "n8n_builder\venv\Lib\site-packages\_pytest\warnings.py" "Archive\Obsolete\warnings.py"
move "n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "n8n_builder\venv\Lib\site-packages\colorama-0.4.6.dist-info\licenses\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "n8n_builder\venv\Lib\site-packages\colorama\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\colorama\ansi.py" "Archive\Obsolete\ansi.py"
move "n8n_builder\venv\Lib\site-packages\colorama\ansitowin32.py" "Archive\Obsolete\ansitowin32.py"
move "n8n_builder\venv\Lib\site-packages\colorama\initialise.py" "Archive\Obsolete\initialise.py"
move "n8n_builder\venv\Lib\site-packages\colorama\tests\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\colorama\tests\ansi_test.py" "Archive\Obsolete\ansi_test.py"
move "n8n_builder\venv\Lib\site-packages\colorama\tests\ansitowin32_test.py" "Archive\Obsolete\ansitowin32_test.py"
move "n8n_builder\venv\Lib\site-packages\colorama\tests\initialise_test.py" "Archive\Obsolete\initialise_test.py"
move "n8n_builder\venv\Lib\site-packages\colorama\tests\isatty_test.py" "Archive\Obsolete\isatty_test.py"
move "n8n_builder\venv\Lib\site-packages\colorama\tests\utils.py" "Archive\Obsolete\utils.py"
move "n8n_builder\venv\Lib\site-packages\colorama\tests\winterm_test.py" "Archive\Obsolete\winterm_test.py"
move "n8n_builder\venv\Lib\site-packages\colorama\win32.py" "Archive\Obsolete\win32.py"
move "n8n_builder\venv\Lib\site-packages\colorama\winterm.py" "Archive\Obsolete\winterm.py"
move "n8n_builder\venv\Lib\site-packages\distutils-precedence.pth" "Archive\Obsolete\distutils-precedence.pth"
move "n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "n8n_builder\venv\Lib\site-packages\iniconfig-2.1.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "n8n_builder\venv\Lib\site-packages\iniconfig\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\iniconfig\_parse.py" "Archive\Obsolete\_parse.py"
move "n8n_builder\venv\Lib\site-packages\iniconfig\_version.py" "Archive\Obsolete\_version.py"
move "n8n_builder\venv\Lib\site-packages\iniconfig\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\iniconfig\py.typed" "Archive\Obsolete\py.typed"
move "n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE.APACHE" "Archive\Obsolete\LICENSE.APACHE"
move "n8n_builder\venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE.BSD" "Archive\Obsolete\LICENSE.BSD"
move "n8n_builder\venv\Lib\site-packages\packaging\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\packaging\_elffile.py" "Archive\Obsolete\_elffile.py"
move "n8n_builder\venv\Lib\site-packages\packaging\_manylinux.py" "Archive\Obsolete\_manylinux.py"
move "n8n_builder\venv\Lib\site-packages\packaging\_parser.py" "Archive\Obsolete\_parser.py"
move "n8n_builder\venv\Lib\site-packages\packaging\_structures.py" "Archive\Obsolete\_structures.py"
move "n8n_builder\venv\Lib\site-packages\packaging\_tokenizer.py" "Archive\Obsolete\_tokenizer.py"
move "n8n_builder\venv\Lib\site-packages\packaging\licenses\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\packaging\licenses\_spdx.py" "Archive\Obsolete\_spdx.py"
move "n8n_builder\venv\Lib\site-packages\packaging\markers.py" "Archive\Obsolete\markers.py"
move "n8n_builder\venv\Lib\site-packages\packaging\metadata.py" "Archive\Obsolete\metadata.py"
move "n8n_builder\venv\Lib\site-packages\packaging\py.typed" "Archive\Obsolete\py.typed"
move "n8n_builder\venv\Lib\site-packages\packaging\requirements.py" "Archive\Obsolete\requirements.py"
move "n8n_builder\venv\Lib\site-packages\packaging\specifiers.py" "Archive\Obsolete\specifiers.py"
move "n8n_builder\venv\Lib\site-packages\packaging\tags.py" "Archive\Obsolete\tags.py"
move "n8n_builder\venv\Lib\site-packages\packaging\utils.py" "Archive\Obsolete\utils.py"
move "n8n_builder\venv\Lib\site-packages\packaging\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\AUTHORS.txt" "Archive\Obsolete\AUTHORS.txt"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "n8n_builder\venv\Lib\site-packages\pip-23.1.2.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "n8n_builder\venv\Lib\site-packages\pip\__pip-runner__.py" "Archive\Obsolete\__pip-runner__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\autocompletion.py" "Archive\Obsolete\autocompletion.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\cmdoptions.py" "Archive\Obsolete\cmdoptions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\command_context.py" "Archive\Obsolete\command_context.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\main_parser.py" "Archive\Obsolete\main_parser.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\parser.py" "Archive\Obsolete\parser.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\progress_bars.py" "Archive\Obsolete\progress_bars.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\req_command.py" "Archive\Obsolete\req_command.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\spinners.py" "Archive\Obsolete\spinners.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\cli\status_codes.py" "Archive\Obsolete\status_codes.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\cache.py" "Archive\Obsolete\cache.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\check.py" "Archive\Obsolete\check.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\completion.py" "Archive\Obsolete\completion.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\configuration.py" "Archive\Obsolete\configuration.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\debug.py" "Archive\Obsolete\debug.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\download.py" "Archive\Obsolete\download.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\freeze.py" "Archive\Obsolete\freeze.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\hash.py" "Archive\Obsolete\hash.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\help.py" "Archive\Obsolete\help.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\index.py" "Archive\Obsolete\index.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\inspect.py" "Archive\Obsolete\inspect.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\install.py" "Archive\Obsolete\install.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\list.py" "Archive\Obsolete\list.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\search.py" "Archive\Obsolete\search.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\show.py" "Archive\Obsolete\show.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\uninstall.py" "Archive\Obsolete\uninstall.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\commands\wheel.py" "Archive\Obsolete\wheel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\configuration.py" "Archive\Obsolete\configuration.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\base.py" "Archive\Obsolete\base.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\installed.py" "Archive\Obsolete\installed.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\sdist.py" "Archive\Obsolete\sdist.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\distributions\wheel.py" "Archive\Obsolete\wheel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\index\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\index\package_finder.py" "Archive\Obsolete\package_finder.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\index\sources.py" "Archive\Obsolete\sources.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\locations\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\locations\_distutils.py" "Archive\Obsolete\_distutils.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\locations\_sysconfig.py" "Archive\Obsolete\_sysconfig.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\locations\base.py" "Archive\Obsolete\base.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\_json.py" "Archive\Obsolete\_json.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\base.py" "Archive\Obsolete\base.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\importlib\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\importlib\_compat.py" "Archive\Obsolete\_compat.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\importlib\_dists.py" "Archive\Obsolete\_dists.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\importlib\_envs.py" "Archive\Obsolete\_envs.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\metadata\pkg_resources.py" "Archive\Obsolete\pkg_resources.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\candidate.py" "Archive\Obsolete\candidate.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\format_control.py" "Archive\Obsolete\format_control.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\index.py" "Archive\Obsolete\index.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\installation_report.py" "Archive\Obsolete\installation_report.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\link.py" "Archive\Obsolete\link.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\scheme.py" "Archive\Obsolete\scheme.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\search_scope.py" "Archive\Obsolete\search_scope.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\selection_prefs.py" "Archive\Obsolete\selection_prefs.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\models\wheel.py" "Archive\Obsolete\wheel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\network\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\network\auth.py" "Archive\Obsolete\auth.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\network\cache.py" "Archive\Obsolete\cache.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\network\download.py" "Archive\Obsolete\download.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\network\lazy_wheel.py" "Archive\Obsolete\lazy_wheel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\network\session.py" "Archive\Obsolete\session.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\network\utils.py" "Archive\Obsolete\utils.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\network\xmlrpc.py" "Archive\Obsolete\xmlrpc.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\build_tracker.py" "Archive\Obsolete\build_tracker.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\metadata.py" "Archive\Obsolete\metadata.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\metadata_editable.py" "Archive\Obsolete\metadata_editable.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\metadata_legacy.py" "Archive\Obsolete\metadata_legacy.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\wheel.py" "Archive\Obsolete\wheel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\wheel_editable.py" "Archive\Obsolete\wheel_editable.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\build\wheel_legacy.py" "Archive\Obsolete\wheel_legacy.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\check.py" "Archive\Obsolete\check.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\freeze.py" "Archive\Obsolete\freeze.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\install\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\install\editable_legacy.py" "Archive\Obsolete\editable_legacy.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\operations\prepare.py" "Archive\Obsolete\prepare.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\req\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\req\req_file.py" "Archive\Obsolete\req_file.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\req\req_set.py" "Archive\Obsolete\req_set.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\base.py" "Archive\Obsolete\base.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\legacy\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\legacy\resolver.py" "Archive\Obsolete\resolver.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\base.py" "Archive\Obsolete\base.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\candidates.py" "Archive\Obsolete\candidates.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py" "Archive\Obsolete\factory.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\found_candidates.py" "Archive\Obsolete\found_candidates.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\provider.py" "Archive\Obsolete\provider.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\reporter.py" "Archive\Obsolete\reporter.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\requirements.py" "Archive\Obsolete\requirements.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py" "Archive\Obsolete\resolver.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\self_outdated_check.py" "Archive\Obsolete\self_outdated_check.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\_jaraco_text.py" "Archive\Obsolete\_jaraco_text.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\_log.py" "Archive\Obsolete\_log.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\appdirs.py" "Archive\Obsolete\appdirs.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\compat.py" "Archive\Obsolete\compat.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\compatibility_tags.py" "Archive\Obsolete\compatibility_tags.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\datetime.py" "Archive\Obsolete\datetime.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\deprecation.py" "Archive\Obsolete\deprecation.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\direct_url_helpers.py" "Archive\Obsolete\direct_url_helpers.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\egg_link.py" "Archive\Obsolete\egg_link.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\encoding.py" "Archive\Obsolete\encoding.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\entrypoints.py" "Archive\Obsolete\entrypoints.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\filesystem.py" "Archive\Obsolete\filesystem.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\filetypes.py" "Archive\Obsolete\filetypes.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\glibc.py" "Archive\Obsolete\glibc.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\hashes.py" "Archive\Obsolete\hashes.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\inject_securetransport.py" "Archive\Obsolete\inject_securetransport.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\logging.py" "Archive\Obsolete\logging.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\models.py" "Archive\Obsolete\models.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\packaging.py" "Archive\Obsolete\packaging.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\setuptools_build.py" "Archive\Obsolete\setuptools_build.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\subprocess.py" "Archive\Obsolete\subprocess.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\temp_dir.py" "Archive\Obsolete\temp_dir.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\unpacking.py" "Archive\Obsolete\unpacking.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\urls.py" "Archive\Obsolete\urls.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\virtualenv.py" "Archive\Obsolete\virtualenv.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\utils\wheel.py" "Archive\Obsolete\wheel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\bazaar.py" "Archive\Obsolete\bazaar.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\git.py" "Archive\Obsolete\git.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\mercurial.py" "Archive\Obsolete\mercurial.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\subversion.py" "Archive\Obsolete\subversion.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py" "Archive\Obsolete\versioncontrol.py"
move "n8n_builder\venv\Lib\site-packages\pip\_internal\wheel_builder.py" "Archive\Obsolete\wheel_builder.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\adapter.py" "Archive\Obsolete\adapter.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\cache.py" "Archive\Obsolete\cache.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py" "Archive\Obsolete\file_cache.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\redis_cache.py" "Archive\Obsolete\redis_cache.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\compat.py" "Archive\Obsolete\compat.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py" "Archive\Obsolete\controller.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py" "Archive\Obsolete\filewrapper.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py" "Archive\Obsolete\heuristics.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\serialize.py" "Archive\Obsolete\serialize.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py" "Archive\Obsolete\wrapper.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\certifi\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\certifi\__main__.py" "Archive\Obsolete\__main__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\certifi\cacert.pem" "Archive\Obsolete\cacert.pem"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\certifi\core.py" "Archive\Obsolete\core.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\big5freq.py" "Archive\Obsolete\big5freq.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\big5prober.py" "Archive\Obsolete\big5prober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\chardistribution.py" "Archive\Obsolete\chardistribution.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\charsetgroupprober.py" "Archive\Obsolete\charsetgroupprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\charsetprober.py" "Archive\Obsolete\charsetprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\cli\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\codingstatemachine.py" "Archive\Obsolete\codingstatemachine.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\codingstatemachinedict.py" "Archive\Obsolete\codingstatemachinedict.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\cp949prober.py" "Archive\Obsolete\cp949prober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\enums.py" "Archive\Obsolete\enums.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\escprober.py" "Archive\Obsolete\escprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\escsm.py" "Archive\Obsolete\escsm.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\eucjpprober.py" "Archive\Obsolete\eucjpprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\euckrfreq.py" "Archive\Obsolete\euckrfreq.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\euckrprober.py" "Archive\Obsolete\euckrprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\euctwfreq.py" "Archive\Obsolete\euctwfreq.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\euctwprober.py" "Archive\Obsolete\euctwprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\gb2312freq.py" "Archive\Obsolete\gb2312freq.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\gb2312prober.py" "Archive\Obsolete\gb2312prober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\hebrewprober.py" "Archive\Obsolete\hebrewprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\jisfreq.py" "Archive\Obsolete\jisfreq.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\johabfreq.py" "Archive\Obsolete\johabfreq.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\johabprober.py" "Archive\Obsolete\johabprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\jpcntx.py" "Archive\Obsolete\jpcntx.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langbulgarianmodel.py" "Archive\Obsolete\langbulgarianmodel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langgreekmodel.py" "Archive\Obsolete\langgreekmodel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langhebrewmodel.py" "Archive\Obsolete\langhebrewmodel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langhungarianmodel.py" "Archive\Obsolete\langhungarianmodel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langrussianmodel.py" "Archive\Obsolete\langrussianmodel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langthaimodel.py" "Archive\Obsolete\langthaimodel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\langturkishmodel.py" "Archive\Obsolete\langturkishmodel.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\latin1prober.py" "Archive\Obsolete\latin1prober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\macromanprober.py" "Archive\Obsolete\macromanprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\mbcharsetprober.py" "Archive\Obsolete\mbcharsetprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\mbcsgroupprober.py" "Archive\Obsolete\mbcsgroupprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\mbcssm.py" "Archive\Obsolete\mbcssm.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\metadata\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\metadata\languages.py" "Archive\Obsolete\languages.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\resultdict.py" "Archive\Obsolete\resultdict.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\sbcharsetprober.py" "Archive\Obsolete\sbcharsetprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\sbcsgroupprober.py" "Archive\Obsolete\sbcsgroupprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\sjisprober.py" "Archive\Obsolete\sjisprober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\universaldetector.py" "Archive\Obsolete\universaldetector.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\utf1632prober.py" "Archive\Obsolete\utf1632prober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\utf8prober.py" "Archive\Obsolete\utf8prober.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\chardet\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\ansi.py" "Archive\Obsolete\ansi.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\ansitowin32.py" "Archive\Obsolete\ansitowin32.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\initialise.py" "Archive\Obsolete\initialise.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\ansi_test.py" "Archive\Obsolete\ansi_test.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\ansitowin32_test.py" "Archive\Obsolete\ansitowin32_test.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\initialise_test.py" "Archive\Obsolete\initialise_test.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\isatty_test.py" "Archive\Obsolete\isatty_test.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\utils.py" "Archive\Obsolete\utils.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\tests\winterm_test.py" "Archive\Obsolete\winterm_test.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\win32.py" "Archive\Obsolete\win32.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\colorama\winterm.py" "Archive\Obsolete\winterm.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\markers.py" "Archive\Obsolete\markers.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\resources.py" "Archive\Obsolete\resources.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\t32.exe" "Archive\Obsolete\t32.exe"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\t64-arm.exe" "Archive\Obsolete\t64-arm.exe"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\t64.exe" "Archive\Obsolete\t64.exe"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\w32.exe" "Archive\Obsolete\w32.exe"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\w64-arm.exe" "Archive\Obsolete\w64-arm.exe"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distlib\w64.exe" "Archive\Obsolete\w64.exe"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\distro\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\codec.py" "Archive\Obsolete\codec.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\compat.py" "Archive\Obsolete\compat.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\core.py" "Archive\Obsolete\core.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\idnadata.py" "Archive\Obsolete\idnadata.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\intranges.py" "Archive\Obsolete\intranges.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\package_data.py" "Archive\Obsolete\package_data.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\idna\uts46data.py" "Archive\Obsolete\uts46data.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\msgpack\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\msgpack\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\msgpack\ext.py" "Archive\Obsolete\ext.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\msgpack\fallback.py" "Archive\Obsolete\fallback.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\__about__.py" "Archive\Obsolete\__about__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py" "Archive\Obsolete\_manylinux.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\_structures.py" "Archive\Obsolete\_structures.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\markers.py" "Archive\Obsolete\markers.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\requirements.py" "Archive\Obsolete\requirements.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\specifiers.py" "Archive\Obsolete\specifiers.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\tags.py" "Archive\Obsolete\tags.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\utils.py" "Archive\Obsolete\utils.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\packaging\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\android.py" "Archive\Obsolete\android.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\api.py" "Archive\Obsolete\api.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py" "Archive\Obsolete\macos.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\unix.py" "Archive\Obsolete\unix.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\platformdirs\windows.py" "Archive\Obsolete\windows.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\__main__.py" "Archive\Obsolete\__main__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\console.py" "Archive\Obsolete\console.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\filter.py" "Archive\Obsolete\filter.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatter.py" "Archive\Obsolete\formatter.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\bbcode.py" "Archive\Obsolete\bbcode.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\groff.py" "Archive\Obsolete\groff.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\img.py" "Archive\Obsolete\img.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\irc.py" "Archive\Obsolete\irc.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\latex.py" "Archive\Obsolete\latex.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\other.py" "Archive\Obsolete\other.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\pangomarkup.py" "Archive\Obsolete\pangomarkup.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\rtf.py" "Archive\Obsolete\rtf.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\svg.py" "Archive\Obsolete\svg.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\terminal.py" "Archive\Obsolete\terminal.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\formatters\terminal256.py" "Archive\Obsolete\terminal256.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\lexer.py" "Archive\Obsolete\lexer.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\modeline.py" "Archive\Obsolete\modeline.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\plugin.py" "Archive\Obsolete\plugin.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\regexopt.py" "Archive\Obsolete\regexopt.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\scanner.py" "Archive\Obsolete\scanner.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\sphinxext.py" "Archive\Obsolete\sphinxext.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\style.py" "Archive\Obsolete\style.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\token.py" "Archive\Obsolete\token.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\unistring.py" "Archive\Obsolete\unistring.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pygments\util.py" "Archive\Obsolete\util.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\actions.py" "Archive\Obsolete\actions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\common.py" "Archive\Obsolete\common.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\core.py" "Archive\Obsolete\core.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\diagram\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\helpers.py" "Archive\Obsolete\helpers.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\results.py" "Archive\Obsolete\results.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\testing.py" "Archive\Obsolete\testing.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\unicode.py" "Archive\Obsolete\unicode.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyparsing\util.py" "Archive\Obsolete\util.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyproject_hooks\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_compat.py" "Archive\Obsolete\_compat.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\__version__.py" "Archive\Obsolete\__version__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\_internal_utils.py" "Archive\Obsolete\_internal_utils.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\adapters.py" "Archive\Obsolete\adapters.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\api.py" "Archive\Obsolete\api.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\auth.py" "Archive\Obsolete\auth.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\compat.py" "Archive\Obsolete\compat.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\cookies.py" "Archive\Obsolete\cookies.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\hooks.py" "Archive\Obsolete\hooks.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\models.py" "Archive\Obsolete\models.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\packages.py" "Archive\Obsolete\packages.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\sessions.py" "Archive\Obsolete\sessions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\status_codes.py" "Archive\Obsolete\status_codes.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\structures.py" "Archive\Obsolete\structures.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\requests\utils.py" "Archive\Obsolete\utils.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\compat\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\compat\collections_abc.py" "Archive\Obsolete\collections_abc.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\providers.py" "Archive\Obsolete\providers.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\reporters.py" "Archive\Obsolete\reporters.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers.py" "Archive\Obsolete\resolvers.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\resolvelib\structs.py" "Archive\Obsolete\structs.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_cell_widths.py" "Archive\Obsolete\_cell_widths.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_emoji_codes.py" "Archive\Obsolete\_emoji_codes.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_emoji_replace.py" "Archive\Obsolete\_emoji_replace.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_export_format.py" "Archive\Obsolete\_export_format.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_extension.py" "Archive\Obsolete\_extension.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_fileno.py" "Archive\Obsolete\_fileno.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_inspect.py" "Archive\Obsolete\_inspect.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_loop.py" "Archive\Obsolete\_loop.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_null_file.py" "Archive\Obsolete\_null_file.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_palettes.py" "Archive\Obsolete\_palettes.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_pick.py" "Archive\Obsolete\_pick.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_spinners.py" "Archive\Obsolete\_spinners.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_stack.py" "Archive\Obsolete\_stack.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_timer.py" "Archive\Obsolete\_timer.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\_windows_renderer.py" "Archive\Obsolete\_windows_renderer.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\bar.py" "Archive\Obsolete\bar.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\color_triplet.py" "Archive\Obsolete\color_triplet.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\constrain.py" "Archive\Obsolete\constrain.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\containers.py" "Archive\Obsolete\containers.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\errors.py" "Archive\Obsolete\errors.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\file_proxy.py" "Archive\Obsolete\file_proxy.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\filesize.py" "Archive\Obsolete\filesize.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\jupyter.py" "Archive\Obsolete\jupyter.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\live_render.py" "Archive\Obsolete\live_render.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\measure.py" "Archive\Obsolete\measure.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\protocol.py" "Archive\Obsolete\protocol.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\region.py" "Archive\Obsolete\region.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\screen.py" "Archive\Obsolete\screen.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\style.py" "Archive\Obsolete\style.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\terminal_theme.py" "Archive\Obsolete\terminal_theme.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\rich\themes.py" "Archive\Obsolete\themes.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\six.py" "Archive\Obsolete\six.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\_asyncio.py" "Archive\Obsolete\_asyncio.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\_utils.py" "Archive\Obsolete\_utils.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\after.py" "Archive\Obsolete\after.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\before.py" "Archive\Obsolete\before.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\before_sleep.py" "Archive\Obsolete\before_sleep.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\nap.py" "Archive\Obsolete\nap.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\retry.py" "Archive\Obsolete\retry.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\stop.py" "Archive\Obsolete\stop.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\tornadoweb.py" "Archive\Obsolete\tornadoweb.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tenacity\wait.py" "Archive\Obsolete\wait.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tomli\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tomli\_parser.py" "Archive\Obsolete\_parser.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tomli\_re.py" "Archive\Obsolete\_re.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\tomli\_types.py" "Archive\Obsolete\_types.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\typing_extensions.py" "Archive\Obsolete\typing_extensions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\_collections.py" "Archive\Obsolete\_collections.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\_version.py" "Archive\Obsolete\_version.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\connection.py" "Archive\Obsolete\connection.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_appengine_environ.py" "Archive\Obsolete\_appengine_environ.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\bindings.py" "Archive\Obsolete\bindings.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\low_level.py" "Archive\Obsolete\low_level.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\appengine.py" "Archive\Obsolete\appengine.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\ntlmpool.py" "Archive\Obsolete\ntlmpool.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py" "Archive\Obsolete\pyopenssl.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\securetransport.py" "Archive\Obsolete\securetransport.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py" "Archive\Obsolete\socks.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\fields.py" "Archive\Obsolete\fields.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\filepost.py" "Archive\Obsolete\filepost.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\packages\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\packages\backports\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\packages\backports\makefile.py" "Archive\Obsolete\makefile.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\packages\six.py" "Archive\Obsolete\six.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py" "Archive\Obsolete\poolmanager.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\request.py" "Archive\Obsolete\request.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\response.py" "Archive\Obsolete\response.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\connection.py" "Archive\Obsolete\connection.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\proxy.py" "Archive\Obsolete\proxy.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\queue.py" "Archive\Obsolete\queue.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\request.py" "Archive\Obsolete\request.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\response.py" "Archive\Obsolete\response.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py" "Archive\Obsolete\retry.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py" "Archive\Obsolete\ssl_match_hostname.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\ssltransport.py" "Archive\Obsolete\ssltransport.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py" "Archive\Obsolete\timeout.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py" "Archive\Obsolete\url.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\urllib3\util\wait.py" "Archive\Obsolete\wait.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\vendor.txt" "Archive\Obsolete\vendor.txt"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\labels.py" "Archive\Obsolete\labels.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\tests.py" "Archive\Obsolete\tests.py"
move "n8n_builder\venv\Lib\site-packages\pip\_vendor\webencodings\x_user_defined.py" "Archive\Obsolete\x_user_defined.py"
move "n8n_builder\venv\Lib\site-packages\pip\py.typed" "Archive\Obsolete\py.typed"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_adapters.py" "Archive\Obsolete\_adapters.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_common.py" "Archive\Obsolete\_common.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_compat.py" "Archive\Obsolete\_compat.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_itertools.py" "Archive\Obsolete\_itertools.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_legacy.py" "Archive\Obsolete\_legacy.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\abc.py" "Archive\Obsolete\abc.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\readers.py" "Archive\Obsolete\readers.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\simple.py" "Archive\Obsolete\simple.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\jaraco\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\jaraco\context.py" "Archive\Obsolete\context.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\jaraco\functools.py" "Archive\Obsolete\functools.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\jaraco\text\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\more.py" "Archive\Obsolete\more.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\recipes.py" "Archive\Obsolete\recipes.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\__about__.py" "Archive\Obsolete\__about__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\_manylinux.py" "Archive\Obsolete\_manylinux.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\_structures.py" "Archive\Obsolete\_structures.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\markers.py" "Archive\Obsolete\markers.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\requirements.py" "Archive\Obsolete\requirements.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\specifiers.py" "Archive\Obsolete\specifiers.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\tags.py" "Archive\Obsolete\tags.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\utils.py" "Archive\Obsolete\utils.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\packaging\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\actions.py" "Archive\Obsolete\actions.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\common.py" "Archive\Obsolete\common.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\core.py" "Archive\Obsolete\core.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\diagram\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\helpers.py" "Archive\Obsolete\helpers.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\results.py" "Archive\Obsolete\results.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\testing.py" "Archive\Obsolete\testing.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\unicode.py" "Archive\Obsolete\unicode.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\util.py" "Archive\Obsolete\util.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\_vendor\zipp.py" "Archive\Obsolete\zipp.py"
move "n8n_builder\venv\Lib\site-packages\pkg_resources\extern\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "n8n_builder\venv\Lib\site-packages\pluggy-1.6.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "n8n_builder\venv\Lib\site-packages\pluggy\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\_callers.py" "Archive\Obsolete\_callers.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\_hooks.py" "Archive\Obsolete\_hooks.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\_manager.py" "Archive\Obsolete\_manager.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\_result.py" "Archive\Obsolete\_result.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\_tracing.py" "Archive\Obsolete\_tracing.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\_version.py" "Archive\Obsolete\_version.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\_warnings.py" "Archive\Obsolete\_warnings.py"
move "n8n_builder\venv\Lib\site-packages\pluggy\py.typed" "Archive\Obsolete\py.typed"
move "n8n_builder\venv\Lib\site-packages\py.py" "Archive\Obsolete\py.py"
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\licenses\AUTHORS" "Archive\Obsolete\AUTHORS"
move "n8n_builder\venv\Lib\site-packages\pygments-2.19.1.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "n8n_builder\venv\Lib\site-packages\pygments\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pygments\__main__.py" "Archive\Obsolete\__main__.py"
move "n8n_builder\venv\Lib\site-packages\pygments\console.py" "Archive\Obsolete\console.py"
move "n8n_builder\venv\Lib\site-packages\pygments\filter.py" "Archive\Obsolete\filter.py"
move "n8n_builder\venv\Lib\site-packages\pygments\filters\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatter.py" "Archive\Obsolete\formatter.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\bbcode.py" "Archive\Obsolete\bbcode.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\groff.py" "Archive\Obsolete\groff.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\img.py" "Archive\Obsolete\img.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\irc.py" "Archive\Obsolete\irc.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\latex.py" "Archive\Obsolete\latex.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\other.py" "Archive\Obsolete\other.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\pangomarkup.py" "Archive\Obsolete\pangomarkup.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\rtf.py" "Archive\Obsolete\rtf.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\svg.py" "Archive\Obsolete\svg.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\terminal.py" "Archive\Obsolete\terminal.py"
move "n8n_builder\venv\Lib\site-packages\pygments\formatters\terminal256.py" "Archive\Obsolete\terminal256.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexer.py" "Archive\Obsolete\lexer.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_ada_builtins.py" "Archive\Obsolete\_ada_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_asy_builtins.py" "Archive\Obsolete\_asy_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_cl_builtins.py" "Archive\Obsolete\_cl_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_cocoa_builtins.py" "Archive\Obsolete\_cocoa_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_csound_builtins.py" "Archive\Obsolete\_csound_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_css_builtins.py" "Archive\Obsolete\_css_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_googlesql_builtins.py" "Archive\Obsolete\_googlesql_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_julia_builtins.py" "Archive\Obsolete\_julia_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_lasso_builtins.py" "Archive\Obsolete\_lasso_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_lilypond_builtins.py" "Archive\Obsolete\_lilypond_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_lua_builtins.py" "Archive\Obsolete\_lua_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_luau_builtins.py" "Archive\Obsolete\_luau_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_mql_builtins.py" "Archive\Obsolete\_mql_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_mysql_builtins.py" "Archive\Obsolete\_mysql_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_openedge_builtins.py" "Archive\Obsolete\_openedge_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_postgres_builtins.py" "Archive\Obsolete\_postgres_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_qlik_builtins.py" "Archive\Obsolete\_qlik_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_scheme_builtins.py" "Archive\Obsolete\_scheme_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_scilab_builtins.py" "Archive\Obsolete\_scilab_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_stan_builtins.py" "Archive\Obsolete\_stan_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_stata_builtins.py" "Archive\Obsolete\_stata_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_tsql_builtins.py" "Archive\Obsolete\_tsql_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_usd_builtins.py" "Archive\Obsolete\_usd_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_vbscript_builtins.py" "Archive\Obsolete\_vbscript_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\_vim_builtins.py" "Archive\Obsolete\_vim_builtins.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ada.py" "Archive\Obsolete\ada.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\agile.py" "Archive\Obsolete\agile.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\algebra.py" "Archive\Obsolete\algebra.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ambient.py" "Archive\Obsolete\ambient.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\amdgpu.py" "Archive\Obsolete\amdgpu.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ampl.py" "Archive\Obsolete\ampl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\apdlexer.py" "Archive\Obsolete\apdlexer.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\apl.py" "Archive\Obsolete\apl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\arrow.py" "Archive\Obsolete\arrow.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\arturo.py" "Archive\Obsolete\arturo.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\asc.py" "Archive\Obsolete\asc.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\asn1.py" "Archive\Obsolete\asn1.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\automation.py" "Archive\Obsolete\automation.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\bare.py" "Archive\Obsolete\bare.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\bdd.py" "Archive\Obsolete\bdd.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\berry.py" "Archive\Obsolete\berry.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\bibtex.py" "Archive\Obsolete\bibtex.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\blueprint.py" "Archive\Obsolete\blueprint.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\boa.py" "Archive\Obsolete\boa.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\business.py" "Archive\Obsolete\business.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\c_cpp.py" "Archive\Obsolete\c_cpp.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\capnproto.py" "Archive\Obsolete\capnproto.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\carbon.py" "Archive\Obsolete\carbon.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\cddl.py" "Archive\Obsolete\cddl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\chapel.py" "Archive\Obsolete\chapel.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\clean.py" "Archive\Obsolete\clean.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\codeql.py" "Archive\Obsolete\codeql.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\comal.py" "Archive\Obsolete\comal.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\compiled.py" "Archive\Obsolete\compiled.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\console.py" "Archive\Obsolete\console.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\cplint.py" "Archive\Obsolete\cplint.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\crystal.py" "Archive\Obsolete\crystal.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\csound.py" "Archive\Obsolete\csound.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\d.py" "Archive\Obsolete\d.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\dalvik.py" "Archive\Obsolete\dalvik.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\dax.py" "Archive\Obsolete\dax.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\devicetree.py" "Archive\Obsolete\devicetree.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\diff.py" "Archive\Obsolete\diff.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\dns.py" "Archive\Obsolete\dns.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\dotnet.py" "Archive\Obsolete\dotnet.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\dsls.py" "Archive\Obsolete\dsls.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\dylan.py" "Archive\Obsolete\dylan.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ecl.py" "Archive\Obsolete\ecl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\eiffel.py" "Archive\Obsolete\eiffel.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\elm.py" "Archive\Obsolete\elm.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\elpi.py" "Archive\Obsolete\elpi.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\email.py" "Archive\Obsolete\email.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\erlang.py" "Archive\Obsolete\erlang.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\esoteric.py" "Archive\Obsolete\esoteric.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ezhil.py" "Archive\Obsolete\ezhil.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\factor.py" "Archive\Obsolete\factor.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\fantom.py" "Archive\Obsolete\fantom.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\felix.py" "Archive\Obsolete\felix.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\fift.py" "Archive\Obsolete\fift.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\floscript.py" "Archive\Obsolete\floscript.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\forth.py" "Archive\Obsolete\forth.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\fortran.py" "Archive\Obsolete\fortran.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\foxpro.py" "Archive\Obsolete\foxpro.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\freefem.py" "Archive\Obsolete\freefem.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\func.py" "Archive\Obsolete\func.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\functional.py" "Archive\Obsolete\functional.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\futhark.py" "Archive\Obsolete\futhark.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\gcodelexer.py" "Archive\Obsolete\gcodelexer.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\gdscript.py" "Archive\Obsolete\gdscript.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\gleam.py" "Archive\Obsolete\gleam.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\go.py" "Archive\Obsolete\go.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\grammar_notation.py" "Archive\Obsolete\grammar_notation.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\graph.py" "Archive\Obsolete\graph.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\graphics.py" "Archive\Obsolete\graphics.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\graphql.py" "Archive\Obsolete\graphql.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\gsql.py" "Archive\Obsolete\gsql.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\hare.py" "Archive\Obsolete\hare.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\hdl.py" "Archive\Obsolete\hdl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\hexdump.py" "Archive\Obsolete\hexdump.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\igor.py" "Archive\Obsolete\igor.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\int_fiction.py" "Archive\Obsolete\int_fiction.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\iolang.py" "Archive\Obsolete\iolang.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\j.py" "Archive\Obsolete\j.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\jmespath.py" "Archive\Obsolete\jmespath.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\jslt.py" "Archive\Obsolete\jslt.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\json5.py" "Archive\Obsolete\json5.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\jsonnet.py" "Archive\Obsolete\jsonnet.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\julia.py" "Archive\Obsolete\julia.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\jvm.py" "Archive\Obsolete\jvm.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\kuin.py" "Archive\Obsolete\kuin.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\kusto.py" "Archive\Obsolete\kusto.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ldap.py" "Archive\Obsolete\ldap.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\lean.py" "Archive\Obsolete\lean.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\lilypond.py" "Archive\Obsolete\lilypond.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\macaulay2.py" "Archive\Obsolete\macaulay2.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\make.py" "Archive\Obsolete\make.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\maple.py" "Archive\Obsolete\maple.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\math.py" "Archive\Obsolete\math.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\maxima.py" "Archive\Obsolete\maxima.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\meson.py" "Archive\Obsolete\meson.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\mime.py" "Archive\Obsolete\mime.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\minecraft.py" "Archive\Obsolete\minecraft.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\mips.py" "Archive\Obsolete\mips.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ml.py" "Archive\Obsolete\ml.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\modeling.py" "Archive\Obsolete\modeling.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\modula2.py" "Archive\Obsolete\modula2.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\mojo.py" "Archive\Obsolete\mojo.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\monte.py" "Archive\Obsolete\monte.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ncl.py" "Archive\Obsolete\ncl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\nimrod.py" "Archive\Obsolete\nimrod.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\nit.py" "Archive\Obsolete\nit.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\nix.py" "Archive\Obsolete\nix.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\numbair.py" "Archive\Obsolete\numbair.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\oberon.py" "Archive\Obsolete\oberon.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ooc.py" "Archive\Obsolete\ooc.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\openscad.py" "Archive\Obsolete\openscad.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\other.py" "Archive\Obsolete\other.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\parasail.py" "Archive\Obsolete\parasail.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\parsers.py" "Archive\Obsolete\parsers.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\pascal.py" "Archive\Obsolete\pascal.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\pddl.py" "Archive\Obsolete\pddl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\perl.py" "Archive\Obsolete\perl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\phix.py" "Archive\Obsolete\phix.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\php.py" "Archive\Obsolete\php.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\pointless.py" "Archive\Obsolete\pointless.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\pony.py" "Archive\Obsolete\pony.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\praat.py" "Archive\Obsolete\praat.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\procfile.py" "Archive\Obsolete\procfile.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\prolog.py" "Archive\Obsolete\prolog.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\promql.py" "Archive\Obsolete\promql.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\prql.py" "Archive\Obsolete\prql.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ptx.py" "Archive\Obsolete\ptx.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\q.py" "Archive\Obsolete\q.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\qlik.py" "Archive\Obsolete\qlik.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\qvt.py" "Archive\Obsolete\qvt.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\rdf.py" "Archive\Obsolete\rdf.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\rebol.py" "Archive\Obsolete\rebol.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\rego.py" "Archive\Obsolete\rego.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ride.py" "Archive\Obsolete\ride.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\rita.py" "Archive\Obsolete\rita.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\rnc.py" "Archive\Obsolete\rnc.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\robotframework.py" "Archive\Obsolete\robotframework.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\ruby.py" "Archive\Obsolete\ruby.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\rust.py" "Archive\Obsolete\rust.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\sas.py" "Archive\Obsolete\sas.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\savi.py" "Archive\Obsolete\savi.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\scdoc.py" "Archive\Obsolete\scdoc.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\sgf.py" "Archive\Obsolete\sgf.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\shell.py" "Archive\Obsolete\shell.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\sieve.py" "Archive\Obsolete\sieve.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\slash.py" "Archive\Obsolete\slash.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\smalltalk.py" "Archive\Obsolete\smalltalk.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\smithy.py" "Archive\Obsolete\smithy.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\smv.py" "Archive\Obsolete\smv.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\snobol.py" "Archive\Obsolete\snobol.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\solidity.py" "Archive\Obsolete\solidity.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\soong.py" "Archive\Obsolete\soong.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\sophia.py" "Archive\Obsolete\sophia.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\special.py" "Archive\Obsolete\special.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\spice.py" "Archive\Obsolete\spice.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\srcinfo.py" "Archive\Obsolete\srcinfo.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\stata.py" "Archive\Obsolete\stata.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\supercollider.py" "Archive\Obsolete\supercollider.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\tact.py" "Archive\Obsolete\tact.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\teal.py" "Archive\Obsolete\teal.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\teraterm.py" "Archive\Obsolete\teraterm.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\testing.py" "Archive\Obsolete\testing.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\text.py" "Archive\Obsolete\text.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\textedit.py" "Archive\Obsolete\textedit.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\textfmts.py" "Archive\Obsolete\textfmts.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\theorem.py" "Archive\Obsolete\theorem.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\thingsdb.py" "Archive\Obsolete\thingsdb.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\tlb.py" "Archive\Obsolete\tlb.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\tls.py" "Archive\Obsolete\tls.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\tnt.py" "Archive\Obsolete\tnt.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\trafficscript.py" "Archive\Obsolete\trafficscript.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\typoscript.py" "Archive\Obsolete\typoscript.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\typst.py" "Archive\Obsolete\typst.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\unicon.py" "Archive\Obsolete\unicon.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\urbi.py" "Archive\Obsolete\urbi.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\varnish.py" "Archive\Obsolete\varnish.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\verification.py" "Archive\Obsolete\verification.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\verifpal.py" "Archive\Obsolete\verifpal.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\vip.py" "Archive\Obsolete\vip.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\vyper.py" "Archive\Obsolete\vyper.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\web.py" "Archive\Obsolete\web.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\webassembly.py" "Archive\Obsolete\webassembly.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\webidl.py" "Archive\Obsolete\webidl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\wgsl.py" "Archive\Obsolete\wgsl.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\whiley.py" "Archive\Obsolete\whiley.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\wowtoc.py" "Archive\Obsolete\wowtoc.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\wren.py" "Archive\Obsolete\wren.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\x10.py" "Archive\Obsolete\x10.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\xorg.py" "Archive\Obsolete\xorg.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\yang.py" "Archive\Obsolete\yang.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\yara.py" "Archive\Obsolete\yara.py"
move "n8n_builder\venv\Lib\site-packages\pygments\lexers\zig.py" "Archive\Obsolete\zig.py"
move "n8n_builder\venv\Lib\site-packages\pygments\modeline.py" "Archive\Obsolete\modeline.py"
move "n8n_builder\venv\Lib\site-packages\pygments\plugin.py" "Archive\Obsolete\plugin.py"
move "n8n_builder\venv\Lib\site-packages\pygments\regexopt.py" "Archive\Obsolete\regexopt.py"
move "n8n_builder\venv\Lib\site-packages\pygments\scanner.py" "Archive\Obsolete\scanner.py"
move "n8n_builder\venv\Lib\site-packages\pygments\sphinxext.py" "Archive\Obsolete\sphinxext.py"
move "n8n_builder\venv\Lib\site-packages\pygments\style.py" "Archive\Obsolete\style.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\_mapping.py" "Archive\Obsolete\_mapping.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\abap.py" "Archive\Obsolete\abap.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\algol.py" "Archive\Obsolete\algol.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\algol_nu.py" "Archive\Obsolete\algol_nu.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\arduino.py" "Archive\Obsolete\arduino.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\autumn.py" "Archive\Obsolete\autumn.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\borland.py" "Archive\Obsolete\borland.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\bw.py" "Archive\Obsolete\bw.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\coffee.py" "Archive\Obsolete\coffee.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\colorful.py" "Archive\Obsolete\colorful.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\default.py" "Archive\Obsolete\default.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\dracula.py" "Archive\Obsolete\dracula.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\emacs.py" "Archive\Obsolete\emacs.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\friendly.py" "Archive\Obsolete\friendly.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\friendly_grayscale.py" "Archive\Obsolete\friendly_grayscale.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\fruity.py" "Archive\Obsolete\fruity.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\gh_dark.py" "Archive\Obsolete\gh_dark.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\gruvbox.py" "Archive\Obsolete\gruvbox.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\igor.py" "Archive\Obsolete\igor.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\inkpot.py" "Archive\Obsolete\inkpot.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\lightbulb.py" "Archive\Obsolete\lightbulb.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\lilypond.py" "Archive\Obsolete\lilypond.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\lovelace.py" "Archive\Obsolete\lovelace.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\manni.py" "Archive\Obsolete\manni.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\material.py" "Archive\Obsolete\material.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\monokai.py" "Archive\Obsolete\monokai.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\murphy.py" "Archive\Obsolete\murphy.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\native.py" "Archive\Obsolete\native.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\nord.py" "Archive\Obsolete\nord.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\onedark.py" "Archive\Obsolete\onedark.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\paraiso_dark.py" "Archive\Obsolete\paraiso_dark.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\paraiso_light.py" "Archive\Obsolete\paraiso_light.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\pastie.py" "Archive\Obsolete\pastie.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\perldoc.py" "Archive\Obsolete\perldoc.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\rainbow_dash.py" "Archive\Obsolete\rainbow_dash.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\rrt.py" "Archive\Obsolete\rrt.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\sas.py" "Archive\Obsolete\sas.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\solarized.py" "Archive\Obsolete\solarized.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\staroffice.py" "Archive\Obsolete\staroffice.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\stata_dark.py" "Archive\Obsolete\stata_dark.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\stata_light.py" "Archive\Obsolete\stata_light.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\tango.py" "Archive\Obsolete\tango.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\trac.py" "Archive\Obsolete\trac.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\vim.py" "Archive\Obsolete\vim.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\vs.py" "Archive\Obsolete\vs.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\xcode.py" "Archive\Obsolete\xcode.py"
move "n8n_builder\venv\Lib\site-packages\pygments\styles\zenburn.py" "Archive\Obsolete\zenburn.py"
move "n8n_builder\venv\Lib\site-packages\pygments\token.py" "Archive\Obsolete\token.py"
move "n8n_builder\venv\Lib\site-packages\pygments\unistring.py" "Archive\Obsolete\unistring.py"
move "n8n_builder\venv\Lib\site-packages\pygments\util.py" "Archive\Obsolete\util.py"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\licenses\AUTHORS" "Archive\Obsolete\AUTHORS"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "n8n_builder\venv\Lib\site-packages\pytest-8.4.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "n8n_builder\venv\Lib\site-packages\pytest\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\pytest\py.typed" "Archive\Obsolete\py.typed"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "n8n_builder\venv\Lib\site-packages\setuptools-65.5.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "n8n_builder\venv\Lib\site-packages\setuptools\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_deprecation_warning.py" "Archive\Obsolete\_deprecation_warning.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\_collections.py" "Archive\Obsolete\_collections.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\_functools.py" "Archive\Obsolete\_functools.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\_macos_compat.py" "Archive\Obsolete\_macos_compat.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\_msvccompiler.py" "Archive\Obsolete\_msvccompiler.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\archive_util.py" "Archive\Obsolete\archive_util.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\bcppcompiler.py" "Archive\Obsolete\bcppcompiler.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\ccompiler.py" "Archive\Obsolete\ccompiler.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\cmd.py" "Archive\Obsolete\cmd.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\_framework_compat.py" "Archive\Obsolete\_framework_compat.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\bdist.py" "Archive\Obsolete\bdist.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\bdist_dumb.py" "Archive\Obsolete\bdist_dumb.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\bdist_rpm.py" "Archive\Obsolete\bdist_rpm.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build.py" "Archive\Obsolete\build.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build_clib.py" "Archive\Obsolete\build_clib.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build_ext.py" "Archive\Obsolete\build_ext.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\build_scripts.py" "Archive\Obsolete\build_scripts.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\clean.py" "Archive\Obsolete\clean.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\config.py" "Archive\Obsolete\config.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install.py" "Archive\Obsolete\install.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_data.py" "Archive\Obsolete\install_data.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_egg_info.py" "Archive\Obsolete\install_egg_info.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_headers.py" "Archive\Obsolete\install_headers.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\install_scripts.py" "Archive\Obsolete\install_scripts.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\py37compat.py" "Archive\Obsolete\py37compat.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\register.py" "Archive\Obsolete\register.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\command\upload.py" "Archive\Obsolete\upload.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\config.py" "Archive\Obsolete\config.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\core.py" "Archive\Obsolete\core.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\cygwinccompiler.py" "Archive\Obsolete\cygwinccompiler.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\debug.py" "Archive\Obsolete\debug.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\dep_util.py" "Archive\Obsolete\dep_util.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\dir_util.py" "Archive\Obsolete\dir_util.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\dist.py" "Archive\Obsolete\dist.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\errors.py" "Archive\Obsolete\errors.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\extension.py" "Archive\Obsolete\extension.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\file_util.py" "Archive\Obsolete\file_util.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\log.py" "Archive\Obsolete\log.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\msvc9compiler.py" "Archive\Obsolete\msvc9compiler.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\msvccompiler.py" "Archive\Obsolete\msvccompiler.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\py38compat.py" "Archive\Obsolete\py38compat.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\py39compat.py" "Archive\Obsolete\py39compat.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\spawn.py" "Archive\Obsolete\spawn.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\sysconfig.py" "Archive\Obsolete\sysconfig.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\text_file.py" "Archive\Obsolete\text_file.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\unixccompiler.py" "Archive\Obsolete\unixccompiler.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_distutils\versionpredicate.py" "Archive\Obsolete\versionpredicate.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_entry_points.py" "Archive\Obsolete\_entry_points.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_importlib.py" "Archive\Obsolete\_importlib.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_itertools.py" "Archive\Obsolete\_itertools.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_path.py" "Archive\Obsolete\_path.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_reqs.py" "Archive\Obsolete\_reqs.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_adapters.py" "Archive\Obsolete\_adapters.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_collections.py" "Archive\Obsolete\_collections.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_compat.py" "Archive\Obsolete\_compat.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_functools.py" "Archive\Obsolete\_functools.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_itertools.py" "Archive\Obsolete\_itertools.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_meta.py" "Archive\Obsolete\_meta.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_text.py" "Archive\Obsolete\_text.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_adapters.py" "Archive\Obsolete\_adapters.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_common.py" "Archive\Obsolete\_common.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_compat.py" "Archive\Obsolete\_compat.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_itertools.py" "Archive\Obsolete\_itertools.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_legacy.py" "Archive\Obsolete\_legacy.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\abc.py" "Archive\Obsolete\abc.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\readers.py" "Archive\Obsolete\readers.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\importlib_resources\simple.py" "Archive\Obsolete\simple.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\jaraco\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\jaraco\context.py" "Archive\Obsolete\context.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\jaraco\functools.py" "Archive\Obsolete\functools.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\jaraco\text\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\more_itertools\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\more_itertools\more.py" "Archive\Obsolete\more.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\more_itertools\recipes.py" "Archive\Obsolete\recipes.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\ordered_set.py" "Archive\Obsolete\ordered_set.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\__about__.py" "Archive\Obsolete\__about__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\_manylinux.py" "Archive\Obsolete\_manylinux.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\_structures.py" "Archive\Obsolete\_structures.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\markers.py" "Archive\Obsolete\markers.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\requirements.py" "Archive\Obsolete\requirements.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\specifiers.py" "Archive\Obsolete\specifiers.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\tags.py" "Archive\Obsolete\tags.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\utils.py" "Archive\Obsolete\utils.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\packaging\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\actions.py" "Archive\Obsolete\actions.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\common.py" "Archive\Obsolete\common.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\core.py" "Archive\Obsolete\core.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\diagram\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\exceptions.py" "Archive\Obsolete\exceptions.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\helpers.py" "Archive\Obsolete\helpers.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\results.py" "Archive\Obsolete\results.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\testing.py" "Archive\Obsolete\testing.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\unicode.py" "Archive\Obsolete\unicode.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\pyparsing\util.py" "Archive\Obsolete\util.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\tomli\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\tomli\_parser.py" "Archive\Obsolete\_parser.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\tomli\_re.py" "Archive\Obsolete\_re.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\tomli\_types.py" "Archive\Obsolete\_types.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\typing_extensions.py" "Archive\Obsolete\typing_extensions.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\_vendor\zipp.py" "Archive\Obsolete\zipp.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\archive_util.py" "Archive\Obsolete\archive_util.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\cli-32.exe" "Archive\Obsolete\cli-32.exe"
move "n8n_builder\venv\Lib\site-packages\setuptools\cli-64.exe" "Archive\Obsolete\cli-64.exe"
move "n8n_builder\venv\Lib\site-packages\setuptools\cli-arm64.exe" "Archive\Obsolete\cli-arm64.exe"
move "n8n_builder\venv\Lib\site-packages\setuptools\cli.exe" "Archive\Obsolete\cli.exe"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\alias.py" "Archive\Obsolete\alias.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\bdist_rpm.py" "Archive\Obsolete\bdist_rpm.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\build.py" "Archive\Obsolete\build.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\build_clib.py" "Archive\Obsolete\build_clib.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\develop.py" "Archive\Obsolete\develop.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\dist_info.py" "Archive\Obsolete\dist_info.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\install.py" "Archive\Obsolete\install.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\install_egg_info.py" "Archive\Obsolete\install_egg_info.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\install_scripts.py" "Archive\Obsolete\install_scripts.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\launcher manifest.xml" "Archive\Obsolete\launcher manifest.xml"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\register.py" "Archive\Obsolete\register.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\rotate.py" "Archive\Obsolete\rotate.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\saveopts.py" "Archive\Obsolete\saveopts.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\sdist.py" "Archive\Obsolete\sdist.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\setopt.py" "Archive\Obsolete\setopt.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\upload.py" "Archive\Obsolete\upload.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\command\upload_docs.py" "Archive\Obsolete\upload_docs.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\_apply_pyprojecttoml.py" "Archive\Obsolete\_apply_pyprojecttoml.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\error_reporting.py" "Archive\Obsolete\error_reporting.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\extra_validations.py" "Archive\Obsolete\extra_validations.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_exceptions.py" "Archive\Obsolete\fastjsonschema_exceptions.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\_validate_pyproject\formats.py" "Archive\Obsolete\formats.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\pyprojecttoml.py" "Archive\Obsolete\pyprojecttoml.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\config\setupcfg.py" "Archive\Obsolete\setupcfg.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\dep_util.py" "Archive\Obsolete\dep_util.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\depends.py" "Archive\Obsolete\depends.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\errors.py" "Archive\Obsolete\errors.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\extension.py" "Archive\Obsolete\extension.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\extern\__init__.py" "Archive\Obsolete\__init__.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\glob.py" "Archive\Obsolete\glob.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\gui-32.exe" "Archive\Obsolete\gui-32.exe"
move "n8n_builder\venv\Lib\site-packages\setuptools\gui-64.exe" "Archive\Obsolete\gui-64.exe"
move "n8n_builder\venv\Lib\site-packages\setuptools\gui-arm64.exe" "Archive\Obsolete\gui-arm64.exe"
move "n8n_builder\venv\Lib\site-packages\setuptools\gui.exe" "Archive\Obsolete\gui.exe"
move "n8n_builder\venv\Lib\site-packages\setuptools\installer.py" "Archive\Obsolete\installer.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\launch.py" "Archive\Obsolete\launch.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\logging.py" "Archive\Obsolete\logging.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\monkey.py" "Archive\Obsolete\monkey.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\namespaces.py" "Archive\Obsolete\namespaces.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\py34compat.py" "Archive\Obsolete\py34compat.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\sandbox.py" "Archive\Obsolete\sandbox.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\script (dev).tmpl" "Archive\Obsolete\script (dev).tmpl"
move "n8n_builder\venv\Lib\site-packages\setuptools\script.tmpl" "Archive\Obsolete\script.tmpl"
move "n8n_builder\venv\Lib\site-packages\setuptools\unicode_utils.py" "Archive\Obsolete\unicode_utils.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\version.py" "Archive\Obsolete\version.py"
move "n8n_builder\venv\Lib\site-packages\setuptools\windows_support.py" "Archive\Obsolete\windows_support.py"
move "n8n_builder\venv\Scripts\Activate.ps1" "Archive\Obsolete\Activate.ps1"
move "n8n_builder\venv\Scripts\activate" "Archive\Obsolete\activate"
move "n8n_builder\venv\Scripts\activate.bat" "Archive\Obsolete\activate.bat"
move "n8n_builder\venv\Scripts\deactivate.bat" "Archive\Obsolete\deactivate.bat"
move "n8n_builder\venv\Scripts\pip.exe" "Archive\Obsolete\pip.exe"
move "n8n_builder\venv\Scripts\pip3.11.exe" "Archive\Obsolete\pip3.11.exe"
move "n8n_builder\venv\Scripts\pip3.exe" "Archive\Obsolete\pip3.exe"
move "n8n_builder\venv\Scripts\py.test.exe" "Archive\Obsolete\py.test.exe"
move "n8n_builder\venv\Scripts\pygmentize.exe" "Archive\Obsolete\pygmentize.exe"
move "n8n_builder\venv\Scripts\pytest.exe" "Archive\Obsolete\pytest.exe"
move "n8n_builder\venv\Scripts\python.exe" "Archive\Obsolete\python.exe"
move "n8n_builder\venv\Scripts\pythonw.exe" "Archive\Obsolete\pythonw.exe"
move "n8n_builder\venv\pyvenv.cfg" "Archive\Obsolete\pyvenv.cfg"
move "projects\test-1\Test1 Workflow A.json" "Archive\Obsolete\Test1 Workflow A.json"
move "projects\test-1\create-a-workflow-that-sends-an-email-to-markeltho.json" "Archive\Obsolete\create-a-workflow-that-sends-an-email-to-markeltho.json"
move "projects\test-1\test-workflow.json" "Archive\Obsolete\test-workflow.json"
move "projects\test-1\test-workflow_2025-06-14_10-23-49.json" "Archive\Obsolete\test-workflow_2025-06-14_10-23-49.json"
move "projects\test-1\test-workflow_2025-06-14_10-23-56.json" "Archive\Obsolete\test-workflow_2025-06-14_10-23-56.json"
move "static\index.html" "Archive\Obsolete\index.html"
move "test_workflows\basic_email_workflow.json" "Archive\Obsolete\basic_email_workflow.json"
move "test_workflows\complex_processing_workflow.json" "Archive\Obsolete\complex_processing_workflow.json"
move "test_workflows\error_handling_workflow.json" "Archive\Obsolete\error_handling_workflow.json"
move "test_workflows\file_processing_workflow.json" "Archive\Obsolete\file_processing_workflow.json"
move "tests\integration_results\integration_test_report.json" "Archive\Obsolete\integration_test_report.json"
move "tests\integration_results\iteration_1_result.json" "Archive\Obsolete\iteration_1_result.json"
move "tests\integration_results\iteration_2_result.json" "Archive\Obsolete\iteration_2_result.json"
move "tests\integration_results\iteration_3_result.json" "Archive\Obsolete\iteration_3_result.json"
move "tests\integration_results\llm_performance_results.json" "Archive\Obsolete\llm_performance_results.json"
move "tests\integration_results\modification_1_result.json" "Archive\Obsolete\modification_1_result.json"
move "tests\integration_results\modification_2_result.json" "Archive\Obsolete\modification_2_result.json"
move "tests\integration_results\modification_3_result.json" "Archive\Obsolete\modification_3_result.json"
move "tests\integration_results\performance_benchmark.json" "Archive\Obsolete\performance_benchmark.json"
move "tests\integration_results\performance_metrics.json" "Archive\Obsolete\performance_metrics.json"
move "tests\test_agent_integration_manager.py" "Archive\Obsolete\test_agent_integration_manager.py"
move "tests\test_config.json" "Archive\Obsolete\test_config.json"
move "tests\test_enhanced_error_handling.py" "Archive\Obsolete\test_enhanced_error_handling.py"
move "tests\test_error_recovery.py" "Archive\Obsolete\test_error_recovery.py"
move "tests\test_event_stream.py" "Archive\Obsolete\test_event_stream.py"
move "tests\test_message_broker.py" "Archive\Obsolete\test_message_broker.py"
move "tests\test_monitoring.py" "Archive\Obsolete\test_monitoring.py"
move "tests\test_performance_optimization.py" "Archive\Obsolete\test_performance_optimization.py"
move "tests\test_retry_logic.py" "Archive\Obsolete\test_retry_logic.py"
move "tests\test_security.py" "Archive\Obsolete\test_security.py"
move "tests\test_state_manager.py" "Archive\Obsolete\test_state_manager.py"
move "tests\test_ui_controller.py" "Archive\Obsolete\test_ui_controller.py"
move "tests\test_validation_with_working_workflow.py" "Archive\Obsolete\test_validation_with_working_workflow.py"
move "tests\test_workflow.py" "Archive\Obsolete\test_workflow.py"
move "tests\test_workflow_core.py" "Archive\Obsolete\test_workflow_core.py"
move "tests\test_workflow_diffing.py" "Archive\Obsolete\test_workflow_diffing.py"
move "tests\test_workflow_execution.py" "Archive\Obsolete\test_workflow_execution.py"
move "tests\test_workflow_execution_manager.py" "Archive\Obsolete\test_workflow_execution_manager.py"
move "tests\test_workflow_execution_result.py" "Archive\Obsolete\test_workflow_execution_result.py"
move "tests\test_workflow_execution_validator.py" "Archive\Obsolete\test_workflow_execution_validator.py"
move "tests\test_workflow_executor.py" "Archive\Obsolete\test_workflow_executor.py"
move "tests\test_workflow_step.py" "Archive\Obsolete\test_workflow_step.py"
move "tests\test_workflow_step_error.py" "Archive\Obsolete\test_workflow_step_error.py"
move "tests\test_workflow_step_executor.py" "Archive\Obsolete\test_workflow_step_executor.py"
move "tests\test_workflow_step_input.py" "Archive\Obsolete\test_workflow_step_input.py"
move "tests\test_workflow_step_metrics.py" "Archive\Obsolete\test_workflow_step_metrics.py"
move "tests\test_workflow_step_output.py" "Archive\Obsolete\test_workflow_step_output.py"
move "tests\test_workflow_step_parameter.py" "Archive\Obsolete\test_workflow_step_parameter.py"
move "tests\test_workflow_step_result.py" "Archive\Obsolete\test_workflow_step_result.py"
move "tests\test_workflow_step_status.py" "Archive\Obsolete\test_workflow_step_status.py"
move "tests\test_workflow_step_transition.py" "Archive\Obsolete\test_workflow_step_transition.py"
move "tests\test_workflow_step_type.py" "Archive\Obsolete\test_workflow_step_type.py"
move "tests\test_workflow_step_validator.py" "Archive\Obsolete\test_workflow_step_validator.py"
move "tests\test_workflow_validator.py" "Archive\Obsolete\test_workflow_validator.py"
move "tests\validation\conftest.py" "Archive\Obsolete\conftest.py"
move "tests\validation\test_connection.py" "Archive\Obsolete\test_connection.py"
move "tests\validation\test_node.py" "Archive\Obsolete\test_node.py"
move "tests\validation\test_workflow_logic.py" "Archive\Obsolete\test_workflow_logic.py"
move "tests\validation\test_workflow_structure.py" "Archive\Obsolete\test_workflow_structure.py"
move "tests\validation_test_output.txt" "Archive\Obsolete\validation_test_output.txt"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\AUTHORS.rst" "Archive\Obsolete\AUTHORS.rst"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\PyJWT-2.10.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\__editable__.n8n_builder-0.1.0.pth" "Archive\Obsolete\__editable__.n8n_builder-0.1.0.pth"
move "venv\Lib\site-packages\_cffi_backend.cp311-win_amd64.pyd" "Archive\Obsolete\_cffi_backend.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\_distutils_hack\override.py" "Archive\Obsolete\override.py"
move "venv\Lib\site-packages\_pytest\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\_pytest\_argcomplete.py" "Archive\Obsolete\_argcomplete.py"
move "venv\Lib\site-packages\_pytest\_code\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\_pytest\_code\source.py" "Archive\Obsolete\source.py"
move "venv\Lib\site-packages\_pytest\_io\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\_pytest\_io\pprint.py" "Archive\Obsolete\pprint.py"
move "venv\Lib\site-packages\_pytest\_io\saferepr.py" "Archive\Obsolete\saferepr.py"
move "venv\Lib\site-packages\_pytest\_io\terminalwriter.py" "Archive\Obsolete\terminalwriter.py"
move "venv\Lib\site-packages\_pytest\_io\wcwidth.py" "Archive\Obsolete\wcwidth.py"
move "venv\Lib\site-packages\_pytest\_py\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\_pytest\_py\error.py" "Archive\Obsolete\error.py"
move "venv\Lib\site-packages\_pytest\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\_pytest\assertion\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\_pytest\assertion\truncate.py" "Archive\Obsolete\truncate.py"
move "venv\Lib\site-packages\_pytest\assertion\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\_pytest\cacheprovider.py" "Archive\Obsolete\cacheprovider.py"
move "venv\Lib\site-packages\_pytest\capture.py" "Archive\Obsolete\capture.py"
move "venv\Lib\site-packages\_pytest\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\_pytest\config\argparsing.py" "Archive\Obsolete\argparsing.py"
move "venv\Lib\site-packages\_pytest\config\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\_pytest\config\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\_pytest\debugging.py" "Archive\Obsolete\debugging.py"
move "venv\Lib\site-packages\_pytest\faulthandler.py" "Archive\Obsolete\faulthandler.py"
move "venv\Lib\site-packages\_pytest\freeze_support.py" "Archive\Obsolete\freeze_support.py"
move "venv\Lib\site-packages\_pytest\helpconfig.py" "Archive\Obsolete\helpconfig.py"
move "venv\Lib\site-packages\_pytest\hookspec.py" "Archive\Obsolete\hookspec.py"
move "venv\Lib\site-packages\_pytest\junitxml.py" "Archive\Obsolete\junitxml.py"
move "venv\Lib\site-packages\_pytest\legacypath.py" "Archive\Obsolete\legacypath.py"
move "venv\Lib\site-packages\_pytest\logging.py" "Archive\Obsolete\logging.py"
move "venv\Lib\site-packages\_pytest\mark\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\_pytest\mark\expression.py" "Archive\Obsolete\expression.py"
move "venv\Lib\site-packages\_pytest\monkeypatch.py" "Archive\Obsolete\monkeypatch.py"
move "venv\Lib\site-packages\_pytest\outcomes.py" "Archive\Obsolete\outcomes.py"
move "venv\Lib\site-packages\_pytest\pastebin.py" "Archive\Obsolete\pastebin.py"
move "venv\Lib\site-packages\_pytest\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\_pytest\pytester_assertions.py" "Archive\Obsolete\pytester_assertions.py"
move "venv\Lib\site-packages\_pytest\python_api.py" "Archive\Obsolete\python_api.py"
move "venv\Lib\site-packages\_pytest\raises.py" "Archive\Obsolete\raises.py"
move "venv\Lib\site-packages\_pytest\recwarn.py" "Archive\Obsolete\recwarn.py"
move "venv\Lib\site-packages\_pytest\reports.py" "Archive\Obsolete\reports.py"
move "venv\Lib\site-packages\_pytest\runner.py" "Archive\Obsolete\runner.py"
move "venv\Lib\site-packages\_pytest\scope.py" "Archive\Obsolete\scope.py"
move "venv\Lib\site-packages\_pytest\setuponly.py" "Archive\Obsolete\setuponly.py"
move "venv\Lib\site-packages\_pytest\setupplan.py" "Archive\Obsolete\setupplan.py"
move "venv\Lib\site-packages\_pytest\skipping.py" "Archive\Obsolete\skipping.py"
move "venv\Lib\site-packages\_pytest\stash.py" "Archive\Obsolete\stash.py"
move "venv\Lib\site-packages\_pytest\stepwise.py" "Archive\Obsolete\stepwise.py"
move "venv\Lib\site-packages\_pytest\threadexception.py" "Archive\Obsolete\threadexception.py"
move "venv\Lib\site-packages\_pytest\timing.py" "Archive\Obsolete\timing.py"
move "venv\Lib\site-packages\_pytest\tmpdir.py" "Archive\Obsolete\tmpdir.py"
move "venv\Lib\site-packages\_pytest\tracemalloc.py" "Archive\Obsolete\tracemalloc.py"
move "venv\Lib\site-packages\_pytest\unittest.py" "Archive\Obsolete\unittest.py"
move "venv\Lib\site-packages\_pytest\unraisableexception.py" "Archive\Obsolete\unraisableexception.py"
move "venv\Lib\site-packages\_pytest\warning_types.py" "Archive\Obsolete\warning_types.py"
move "venv\Lib\site-packages\_pytest\warnings.py" "Archive\Obsolete\warnings.py"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\aiodns-3.4.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\aiodns\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\aiodns\error.py" "Archive\Obsolete\error.py"
move "venv\Lib\site-packages\aiodns\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\aiofiles-23.2.1.dist-info\licenses\NOTICE" "Archive\Obsolete\NOTICE"
move "venv\Lib\site-packages\aiofiles\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\aiofiles\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\aiofiles\os.py" "Archive\Obsolete\os.py"
move "venv\Lib\site-packages\aiofiles\ospath.py" "Archive\Obsolete\ospath.py"
move "venv\Lib\site-packages\aiofiles\tempfile\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\aiofiles\tempfile\temptypes.py" "Archive\Obsolete\temptypes.py"
move "venv\Lib\site-packages\aiofiles\threadpool\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\aiofiles\threadpool\binary.py" "Archive\Obsolete\binary.py"
move "venv\Lib\site-packages\aiofiles\threadpool\text.py" "Archive\Obsolete\text.py"
move "venv\Lib\site-packages\aiofiles\threadpool\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\aiohappyeyeballs-2.6.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\aiohappyeyeballs-2.6.1.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\aiohappyeyeballs-2.6.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\aiohappyeyeballs-2.6.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\aiohappyeyeballs-2.6.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\aiohappyeyeballs\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\aiohappyeyeballs\_staggered.py" "Archive\Obsolete\_staggered.py"
move "venv\Lib\site-packages\aiohappyeyeballs\impl.py" "Archive\Obsolete\impl.py"
move "venv\Lib\site-packages\aiohappyeyeballs\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\aiohappyeyeballs\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\aiohappyeyeballs\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\aiohttp-3.9.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\aiohttp\.hash\_cparser.pxd.hash" "Archive\Obsolete\_cparser.pxd.hash"
move "venv\Lib\site-packages\aiohttp\.hash\_find_header.pxd.hash" "Archive\Obsolete\_find_header.pxd.hash"
move "venv\Lib\site-packages\aiohttp\.hash\_helpers.pyi.hash" "Archive\Obsolete\_helpers.pyi.hash"
move "venv\Lib\site-packages\aiohttp\.hash\_helpers.pyx.hash" "Archive\Obsolete\_helpers.pyx.hash"
move "venv\Lib\site-packages\aiohttp\.hash\_http_parser.pyx.hash" "Archive\Obsolete\_http_parser.pyx.hash"
move "venv\Lib\site-packages\aiohttp\.hash\_http_writer.pyx.hash" "Archive\Obsolete\_http_writer.pyx.hash"
move "venv\Lib\site-packages\aiohttp\.hash\_websocket.pyx.hash" "Archive\Obsolete\_websocket.pyx.hash"
move "venv\Lib\site-packages\aiohttp\.hash\hdrs.py.hash" "Archive\Obsolete\hdrs.py.hash"
move "venv\Lib\site-packages\aiohttp\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\aiohttp\_cparser.pxd" "Archive\Obsolete\_cparser.pxd"
move "venv\Lib\site-packages\aiohttp\_find_header.pxd" "Archive\Obsolete\_find_header.pxd"
move "venv\Lib\site-packages\aiohttp\_headers.pxi" "Archive\Obsolete\_headers.pxi"
move "venv\Lib\site-packages\aiohttp\_helpers.cp311-win_amd64.pyd" "Archive\Obsolete\_helpers.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\aiohttp\_helpers.pyi" "Archive\Obsolete\_helpers.pyi"
move "venv\Lib\site-packages\aiohttp\_helpers.pyx" "Archive\Obsolete\_helpers.pyx"
move "venv\Lib\site-packages\aiohttp\_http_parser.cp311-win_amd64.pyd" "Archive\Obsolete\_http_parser.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\aiohttp\_http_parser.pyx" "Archive\Obsolete\_http_parser.pyx"
move "venv\Lib\site-packages\aiohttp\_http_writer.cp311-win_amd64.pyd" "Archive\Obsolete\_http_writer.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\aiohttp\_http_writer.pyx" "Archive\Obsolete\_http_writer.pyx"
move "venv\Lib\site-packages\aiohttp\_websocket.cp311-win_amd64.pyd" "Archive\Obsolete\_websocket.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\aiohttp\_websocket.pyx" "Archive\Obsolete\_websocket.pyx"
move "venv\Lib\site-packages\aiohttp\abc.py" "Archive\Obsolete\abc.py"
move "venv\Lib\site-packages\aiohttp\base_protocol.py" "Archive\Obsolete\base_protocol.py"
move "venv\Lib\site-packages\aiohttp\client.py" "Archive\Obsolete\client.py"
move "venv\Lib\site-packages\aiohttp\client_exceptions.py" "Archive\Obsolete\client_exceptions.py"
move "venv\Lib\site-packages\aiohttp\client_proto.py" "Archive\Obsolete\client_proto.py"
move "venv\Lib\site-packages\aiohttp\client_reqrep.py" "Archive\Obsolete\client_reqrep.py"
move "venv\Lib\site-packages\aiohttp\client_ws.py" "Archive\Obsolete\client_ws.py"
move "venv\Lib\site-packages\aiohttp\compression_utils.py" "Archive\Obsolete\compression_utils.py"
move "venv\Lib\site-packages\aiohttp\cookiejar.py" "Archive\Obsolete\cookiejar.py"
move "venv\Lib\site-packages\aiohttp\formdata.py" "Archive\Obsolete\formdata.py"
move "venv\Lib\site-packages\aiohttp\hdrs.py" "Archive\Obsolete\hdrs.py"
move "venv\Lib\site-packages\aiohttp\helpers.py" "Archive\Obsolete\helpers.py"
move "venv\Lib\site-packages\aiohttp\http.py" "Archive\Obsolete\http.py"
move "venv\Lib\site-packages\aiohttp\http_exceptions.py" "Archive\Obsolete\http_exceptions.py"
move "venv\Lib\site-packages\aiohttp\http_parser.py" "Archive\Obsolete\http_parser.py"
move "venv\Lib\site-packages\aiohttp\http_websocket.py" "Archive\Obsolete\http_websocket.py"
move "venv\Lib\site-packages\aiohttp\http_writer.py" "Archive\Obsolete\http_writer.py"
move "venv\Lib\site-packages\aiohttp\locks.py" "Archive\Obsolete\locks.py"
move "venv\Lib\site-packages\aiohttp\log.py" "Archive\Obsolete\log.py"
move "venv\Lib\site-packages\aiohttp\multipart.py" "Archive\Obsolete\multipart.py"
move "venv\Lib\site-packages\aiohttp\payload.py" "Archive\Obsolete\payload.py"
move "venv\Lib\site-packages\aiohttp\payload_streamer.py" "Archive\Obsolete\payload_streamer.py"
move "venv\Lib\site-packages\aiohttp\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\aiohttp\pytest_plugin.py" "Archive\Obsolete\pytest_plugin.py"
move "venv\Lib\site-packages\aiohttp\resolver.py" "Archive\Obsolete\resolver.py"
move "venv\Lib\site-packages\aiohttp\streams.py" "Archive\Obsolete\streams.py"
move "venv\Lib\site-packages\aiohttp\tcp_helpers.py" "Archive\Obsolete\tcp_helpers.py"
move "venv\Lib\site-packages\aiohttp\test_utils.py" "Archive\Obsolete\test_utils.py"
move "venv\Lib\site-packages\aiohttp\tracing.py" "Archive\Obsolete\tracing.py"
move "venv\Lib\site-packages\aiohttp\typedefs.py" "Archive\Obsolete\typedefs.py"
move "venv\Lib\site-packages\aiohttp\web_exceptions.py" "Archive\Obsolete\web_exceptions.py"
move "venv\Lib\site-packages\aiohttp\web_fileresponse.py" "Archive\Obsolete\web_fileresponse.py"
move "venv\Lib\site-packages\aiohttp\web_log.py" "Archive\Obsolete\web_log.py"
move "venv\Lib\site-packages\aiohttp\web_middlewares.py" "Archive\Obsolete\web_middlewares.py"
move "venv\Lib\site-packages\aiohttp\web_protocol.py" "Archive\Obsolete\web_protocol.py"
move "venv\Lib\site-packages\aiohttp\web_request.py" "Archive\Obsolete\web_request.py"
move "venv\Lib\site-packages\aiohttp\web_response.py" "Archive\Obsolete\web_response.py"
move "venv\Lib\site-packages\aiohttp\web_routedef.py" "Archive\Obsolete\web_routedef.py"
move "venv\Lib\site-packages\aiohttp\web_runner.py" "Archive\Obsolete\web_runner.py"
move "venv\Lib\site-packages\aiohttp\web_server.py" "Archive\Obsolete\web_server.py"
move "venv\Lib\site-packages\aiohttp\web_urldispatcher.py" "Archive\Obsolete\web_urldispatcher.py"
move "venv\Lib\site-packages\aiohttp\web_ws.py" "Archive\Obsolete\web_ws.py"
move "venv\Lib\site-packages\aiosignal-1.3.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\aiosignal-1.3.2.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\aiosignal-1.3.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\aiosignal-1.3.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\aiosignal-1.3.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\aiosignal-1.3.2.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\aiosignal\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\aiosignal\__init__.pyi" "Archive\Obsolete\__init__.pyi"
move "venv\Lib\site-packages\aiosignal\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\annotated_types-0.7.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\annotated_types-0.7.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\annotated_types-0.7.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\annotated_types-0.7.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\annotated_types-0.7.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\annotated_types\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\annotated_types\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\annotated_types\test_cases.py" "Archive\Obsolete\test_cases.py"
move "venv\Lib\site-packages\anyio-4.9.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\anyio-4.9.0.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\anyio-4.9.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\anyio-4.9.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\anyio-4.9.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\anyio-4.9.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\anyio-4.9.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\anyio\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\anyio\_backends\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\anyio\_backends\_asyncio.py" "Archive\Obsolete\_asyncio.py"
move "venv\Lib\site-packages\anyio\_backends\_trio.py" "Archive\Obsolete\_trio.py"
move "venv\Lib\site-packages\anyio\_core\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\anyio\_core\_asyncio_selector_thread.py" "Archive\Obsolete\_asyncio_selector_thread.py"
move "venv\Lib\site-packages\anyio\_core\_eventloop.py" "Archive\Obsolete\_eventloop.py"
move "venv\Lib\site-packages\anyio\_core\_exceptions.py" "Archive\Obsolete\_exceptions.py"
move "venv\Lib\site-packages\anyio\_core\_fileio.py" "Archive\Obsolete\_fileio.py"
move "venv\Lib\site-packages\anyio\_core\_resources.py" "Archive\Obsolete\_resources.py"
move "venv\Lib\site-packages\anyio\_core\_signals.py" "Archive\Obsolete\_signals.py"
move "venv\Lib\site-packages\anyio\_core\_sockets.py" "Archive\Obsolete\_sockets.py"
move "venv\Lib\site-packages\anyio\_core\_streams.py" "Archive\Obsolete\_streams.py"
move "venv\Lib\site-packages\anyio\_core\_subprocesses.py" "Archive\Obsolete\_subprocesses.py"
move "venv\Lib\site-packages\anyio\_core\_synchronization.py" "Archive\Obsolete\_synchronization.py"
move "venv\Lib\site-packages\anyio\_core\_tasks.py" "Archive\Obsolete\_tasks.py"
move "venv\Lib\site-packages\anyio\_core\_tempfile.py" "Archive\Obsolete\_tempfile.py"
move "venv\Lib\site-packages\anyio\_core\_testing.py" "Archive\Obsolete\_testing.py"
move "venv\Lib\site-packages\anyio\_core\_typedattr.py" "Archive\Obsolete\_typedattr.py"
move "venv\Lib\site-packages\anyio\abc\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\anyio\abc\_eventloop.py" "Archive\Obsolete\_eventloop.py"
move "venv\Lib\site-packages\anyio\abc\_resources.py" "Archive\Obsolete\_resources.py"
move "venv\Lib\site-packages\anyio\abc\_sockets.py" "Archive\Obsolete\_sockets.py"
move "venv\Lib\site-packages\anyio\abc\_streams.py" "Archive\Obsolete\_streams.py"
move "venv\Lib\site-packages\anyio\abc\_subprocesses.py" "Archive\Obsolete\_subprocesses.py"
move "venv\Lib\site-packages\anyio\abc\_tasks.py" "Archive\Obsolete\_tasks.py"
move "venv\Lib\site-packages\anyio\abc\_testing.py" "Archive\Obsolete\_testing.py"
move "venv\Lib\site-packages\anyio\from_thread.py" "Archive\Obsolete\from_thread.py"
move "venv\Lib\site-packages\anyio\lowlevel.py" "Archive\Obsolete\lowlevel.py"
move "venv\Lib\site-packages\anyio\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\anyio\pytest_plugin.py" "Archive\Obsolete\pytest_plugin.py"
move "venv\Lib\site-packages\anyio\streams\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\anyio\streams\buffered.py" "Archive\Obsolete\buffered.py"
move "venv\Lib\site-packages\anyio\streams\file.py" "Archive\Obsolete\file.py"
move "venv\Lib\site-packages\anyio\streams\memory.py" "Archive\Obsolete\memory.py"
move "venv\Lib\site-packages\anyio\streams\stapled.py" "Archive\Obsolete\stapled.py"
move "venv\Lib\site-packages\anyio\streams\text.py" "Archive\Obsolete\text.py"
move "venv\Lib\site-packages\anyio\streams\tls.py" "Archive\Obsolete\tls.py"
move "venv\Lib\site-packages\anyio\to_interpreter.py" "Archive\Obsolete\to_interpreter.py"
move "venv\Lib\site-packages\anyio\to_thread.py" "Archive\Obsolete\to_thread.py"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\DESCRIPTION.rst" "Archive\Obsolete\DESCRIPTION.rst"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\metadata.json" "Archive\Obsolete\metadata.json"
move "venv\Lib\site-packages\asyncio-3.4.3.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\asyncio\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\asyncio\base_events.py" "Archive\Obsolete\base_events.py"
move "venv\Lib\site-packages\asyncio\base_subprocess.py" "Archive\Obsolete\base_subprocess.py"
move "venv\Lib\site-packages\asyncio\constants.py" "Archive\Obsolete\constants.py"
move "venv\Lib\site-packages\asyncio\coroutines.py" "Archive\Obsolete\coroutines.py"
move "venv\Lib\site-packages\asyncio\events.py" "Archive\Obsolete\events.py"
move "venv\Lib\site-packages\asyncio\futures.py" "Archive\Obsolete\futures.py"
move "venv\Lib\site-packages\asyncio\locks.py" "Archive\Obsolete\locks.py"
move "venv\Lib\site-packages\asyncio\log.py" "Archive\Obsolete\log.py"
move "venv\Lib\site-packages\asyncio\proactor_events.py" "Archive\Obsolete\proactor_events.py"
move "venv\Lib\site-packages\asyncio\protocols.py" "Archive\Obsolete\protocols.py"
move "venv\Lib\site-packages\asyncio\queues.py" "Archive\Obsolete\queues.py"
move "venv\Lib\site-packages\asyncio\selector_events.py" "Archive\Obsolete\selector_events.py"
move "venv\Lib\site-packages\asyncio\selectors.py" "Archive\Obsolete\selectors.py"
move "venv\Lib\site-packages\asyncio\sslproto.py" "Archive\Obsolete\sslproto.py"
move "venv\Lib\site-packages\asyncio\streams.py" "Archive\Obsolete\streams.py"
move "venv\Lib\site-packages\asyncio\subprocess.py" "Archive\Obsolete\subprocess.py"
move "venv\Lib\site-packages\asyncio\tasks.py" "Archive\Obsolete\tasks.py"
move "venv\Lib\site-packages\asyncio\test_support.py" "Archive\Obsolete\test_support.py"
move "venv\Lib\site-packages\asyncio\test_utils.py" "Archive\Obsolete\test_utils.py"
move "venv\Lib\site-packages\asyncio\transports.py" "Archive\Obsolete\transports.py"
move "venv\Lib\site-packages\asyncio\unix_events.py" "Archive\Obsolete\unix_events.py"
move "venv\Lib\site-packages\asyncio\windows_events.py" "Archive\Obsolete\windows_events.py"
move "venv\Lib\site-packages\asyncio\windows_utils.py" "Archive\Obsolete\windows_utils.py"
move "venv\Lib\site-packages\attr\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\attr\__init__.pyi" "Archive\Obsolete\__init__.pyi"
move "venv\Lib\site-packages\attr\_cmp.py" "Archive\Obsolete\_cmp.py"
move "venv\Lib\site-packages\attr\_cmp.pyi" "Archive\Obsolete\_cmp.pyi"
move "venv\Lib\site-packages\attr\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\attr\_config.py" "Archive\Obsolete\_config.py"
move "venv\Lib\site-packages\attr\_funcs.py" "Archive\Obsolete\_funcs.py"
move "venv\Lib\site-packages\attr\_make.py" "Archive\Obsolete\_make.py"
move "venv\Lib\site-packages\attr\_next_gen.py" "Archive\Obsolete\_next_gen.py"
move "venv\Lib\site-packages\attr\_typing_compat.pyi" "Archive\Obsolete\_typing_compat.pyi"
move "venv\Lib\site-packages\attr\_version_info.py" "Archive\Obsolete\_version_info.py"
move "venv\Lib\site-packages\attr\_version_info.pyi" "Archive\Obsolete\_version_info.pyi"
move "venv\Lib\site-packages\attr\converters.py" "Archive\Obsolete\converters.py"
move "venv\Lib\site-packages\attr\converters.pyi" "Archive\Obsolete\converters.pyi"
move "venv\Lib\site-packages\attr\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\attr\exceptions.pyi" "Archive\Obsolete\exceptions.pyi"
move "venv\Lib\site-packages\attr\filters.py" "Archive\Obsolete\filters.py"
move "venv\Lib\site-packages\attr\filters.pyi" "Archive\Obsolete\filters.pyi"
move "venv\Lib\site-packages\attr\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\attr\setters.py" "Archive\Obsolete\setters.py"
move "venv\Lib\site-packages\attr\setters.pyi" "Archive\Obsolete\setters.pyi"
move "venv\Lib\site-packages\attr\validators.py" "Archive\Obsolete\validators.py"
move "venv\Lib\site-packages\attr\validators.pyi" "Archive\Obsolete\validators.pyi"
move "venv\Lib\site-packages\attrs-25.3.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\attrs-25.3.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\attrs-25.3.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\attrs-25.3.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\attrs-25.3.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\attrs\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\attrs\__init__.pyi" "Archive\Obsolete\__init__.pyi"
move "venv\Lib\site-packages\attrs\converters.py" "Archive\Obsolete\converters.py"
move "venv\Lib\site-packages\attrs\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\attrs\filters.py" "Archive\Obsolete\filters.py"
move "venv\Lib\site-packages\attrs\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\attrs\setters.py" "Archive\Obsolete\setters.py"
move "venv\Lib\site-packages\attrs\validators.py" "Archive\Obsolete\validators.py"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\bcrypt-4.3.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\bcrypt\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\bcrypt\__init__.pyi" "Archive\Obsolete\__init__.pyi"
move "venv\Lib\site-packages\bcrypt\_bcrypt.pyd" "Archive\Obsolete\_bcrypt.pyd"
move "venv\Lib\site-packages\bcrypt\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\certifi-2025.4.26.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\certifi-2025.4.26.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\certifi-2025.4.26.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\certifi-2025.4.26.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\certifi-2025.4.26.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\certifi-2025.4.26.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\certifi\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\certifi\__main__.py" "Archive\Obsolete\__main__.py"
move "venv\Lib\site-packages\certifi\cacert.pem" "Archive\Obsolete\cacert.pem"
move "venv\Lib\site-packages\certifi\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\certifi\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\cffi-1.17.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\cffi-1.17.1.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\cffi-1.17.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\cffi-1.17.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\cffi-1.17.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\cffi-1.17.1.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\cffi-1.17.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\cffi\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cffi\_cffi_errors.h" "Archive\Obsolete\_cffi_errors.h"
move "venv\Lib\site-packages\cffi\_cffi_include.h" "Archive\Obsolete\_cffi_include.h"
move "venv\Lib\site-packages\cffi\_embedding.h" "Archive\Obsolete\_embedding.h"
move "venv\Lib\site-packages\cffi\_shimmed_dist_utils.py" "Archive\Obsolete\_shimmed_dist_utils.py"
move "venv\Lib\site-packages\cffi\api.py" "Archive\Obsolete\api.py"
move "venv\Lib\site-packages\cffi\backend_ctypes.py" "Archive\Obsolete\backend_ctypes.py"
move "venv\Lib\site-packages\cffi\cffi_opcode.py" "Archive\Obsolete\cffi_opcode.py"
move "venv\Lib\site-packages\cffi\commontypes.py" "Archive\Obsolete\commontypes.py"
move "venv\Lib\site-packages\cffi\cparser.py" "Archive\Obsolete\cparser.py"
move "venv\Lib\site-packages\cffi\error.py" "Archive\Obsolete\error.py"
move "venv\Lib\site-packages\cffi\ffiplatform.py" "Archive\Obsolete\ffiplatform.py"
move "venv\Lib\site-packages\cffi\lock.py" "Archive\Obsolete\lock.py"
move "venv\Lib\site-packages\cffi\model.py" "Archive\Obsolete\model.py"
move "venv\Lib\site-packages\cffi\parse_c_type.h" "Archive\Obsolete\parse_c_type.h"
move "venv\Lib\site-packages\cffi\pkgconfig.py" "Archive\Obsolete\pkgconfig.py"
move "venv\Lib\site-packages\cffi\vengine_cpy.py" "Archive\Obsolete\vengine_cpy.py"
move "venv\Lib\site-packages\cffi\vengine_gen.py" "Archive\Obsolete\vengine_gen.py"
move "venv\Lib\site-packages\cffi\verifier.py" "Archive\Obsolete\verifier.py"
move "venv\Lib\site-packages\charset_normalizer-3.4.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\charset_normalizer-3.4.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\charset_normalizer-3.4.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\charset_normalizer-3.4.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\charset_normalizer-3.4.2.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\charset_normalizer-3.4.2.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\charset_normalizer-3.4.2.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\charset_normalizer\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\charset_normalizer\api.py" "Archive\Obsolete\api.py"
move "venv\Lib\site-packages\charset_normalizer\cd.py" "Archive\Obsolete\cd.py"
move "venv\Lib\site-packages\charset_normalizer\cli\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\charset_normalizer\constant.py" "Archive\Obsolete\constant.py"
move "venv\Lib\site-packages\charset_normalizer\legacy.py" "Archive\Obsolete\legacy.py"
move "venv\Lib\site-packages\charset_normalizer\md.cp311-win_amd64.pyd" "Archive\Obsolete\md.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\charset_normalizer\md.py" "Archive\Obsolete\md.py"
move "venv\Lib\site-packages\charset_normalizer\md__mypyc.cp311-win_amd64.pyd" "Archive\Obsolete\md__mypyc.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\charset_normalizer\models.py" "Archive\Obsolete\models.py"
move "venv\Lib\site-packages\charset_normalizer\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\charset_normalizer\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\charset_normalizer\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\click-8.2.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\click-8.2.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\click-8.2.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\click-8.2.1.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\click-8.2.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\click-8.2.1.dist-info\licenses\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "venv\Lib\site-packages\click\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\click\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\click\_termui_impl.py" "Archive\Obsolete\_termui_impl.py"
move "venv\Lib\site-packages\click\_textwrap.py" "Archive\Obsolete\_textwrap.py"
move "venv\Lib\site-packages\click\_winconsole.py" "Archive\Obsolete\_winconsole.py"
move "venv\Lib\site-packages\click\decorators.py" "Archive\Obsolete\decorators.py"
move "venv\Lib\site-packages\click\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\click\formatting.py" "Archive\Obsolete\formatting.py"
move "venv\Lib\site-packages\click\globals.py" "Archive\Obsolete\globals.py"
move "venv\Lib\site-packages\click\parser.py" "Archive\Obsolete\parser.py"
move "venv\Lib\site-packages\click\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\click\shell_completion.py" "Archive\Obsolete\shell_completion.py"
move "venv\Lib\site-packages\click\termui.py" "Archive\Obsolete\termui.py"
move "venv\Lib\site-packages\click\testing.py" "Archive\Obsolete\testing.py"
move "venv\Lib\site-packages\click\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\colorama-0.4.6.dist-info\licenses\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "venv\Lib\site-packages\colorama\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\colorama\ansi.py" "Archive\Obsolete\ansi.py"
move "venv\Lib\site-packages\colorama\ansitowin32.py" "Archive\Obsolete\ansitowin32.py"
move "venv\Lib\site-packages\colorama\initialise.py" "Archive\Obsolete\initialise.py"
move "venv\Lib\site-packages\colorama\tests\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\colorama\tests\ansi_test.py" "Archive\Obsolete\ansi_test.py"
move "venv\Lib\site-packages\colorama\tests\ansitowin32_test.py" "Archive\Obsolete\ansitowin32_test.py"
move "venv\Lib\site-packages\colorama\tests\initialise_test.py" "Archive\Obsolete\initialise_test.py"
move "venv\Lib\site-packages\colorama\tests\isatty_test.py" "Archive\Obsolete\isatty_test.py"
move "venv\Lib\site-packages\colorama\tests\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\colorama\tests\winterm_test.py" "Archive\Obsolete\winterm_test.py"
move "venv\Lib\site-packages\colorama\win32.py" "Archive\Obsolete\win32.py"
move "venv\Lib\site-packages\colorama\winterm.py" "Archive\Obsolete\winterm.py"
move "venv\Lib\site-packages\coverage-7.8.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\coverage-7.8.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\coverage-7.8.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\coverage-7.8.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\coverage-7.8.2.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\coverage-7.8.2.dist-info\licenses\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "venv\Lib\site-packages\coverage-7.8.2.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\coverage\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\coverage\collector.py" "Archive\Obsolete\collector.py"
move "venv\Lib\site-packages\coverage\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\coverage\data.py" "Archive\Obsolete\data.py"
move "venv\Lib\site-packages\coverage\debug.py" "Archive\Obsolete\debug.py"
move "venv\Lib\site-packages\coverage\disposition.py" "Archive\Obsolete\disposition.py"
move "venv\Lib\site-packages\coverage\env.py" "Archive\Obsolete\env.py"
move "venv\Lib\site-packages\coverage\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\coverage\htmlfiles\coverage_html.js" "Archive\Obsolete\coverage_html.js"
move "venv\Lib\site-packages\coverage\htmlfiles\favicon_32.png" "Archive\Obsolete\favicon_32.png"
move "venv\Lib\site-packages\coverage\htmlfiles\index.html" "Archive\Obsolete\index.html"
move "venv\Lib\site-packages\coverage\htmlfiles\keybd_closed.png" "Archive\Obsolete\keybd_closed.png"
move "venv\Lib\site-packages\coverage\htmlfiles\pyfile.html" "Archive\Obsolete\pyfile.html"
move "venv\Lib\site-packages\coverage\htmlfiles\style.css" "Archive\Obsolete\style.css"
move "venv\Lib\site-packages\coverage\htmlfiles\style.scss" "Archive\Obsolete\style.scss"
move "venv\Lib\site-packages\coverage\lcovreport.py" "Archive\Obsolete\lcovreport.py"
move "venv\Lib\site-packages\coverage\numbits.py" "Archive\Obsolete\numbits.py"
move "venv\Lib\site-packages\coverage\parser.py" "Archive\Obsolete\parser.py"
move "venv\Lib\site-packages\coverage\phystokens.py" "Archive\Obsolete\phystokens.py"
move "venv\Lib\site-packages\coverage\plugin_support.py" "Archive\Obsolete\plugin_support.py"
move "venv\Lib\site-packages\coverage\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\coverage\pytracer.py" "Archive\Obsolete\pytracer.py"
move "venv\Lib\site-packages\coverage\regions.py" "Archive\Obsolete\regions.py"
move "venv\Lib\site-packages\coverage\report.py" "Archive\Obsolete\report.py"
move "venv\Lib\site-packages\coverage\report_core.py" "Archive\Obsolete\report_core.py"
move "venv\Lib\site-packages\coverage\results.py" "Archive\Obsolete\results.py"
move "venv\Lib\site-packages\coverage\sqldata.py" "Archive\Obsolete\sqldata.py"
move "venv\Lib\site-packages\coverage\templite.py" "Archive\Obsolete\templite.py"
move "venv\Lib\site-packages\coverage\tracer.cp311-win_amd64.pyd" "Archive\Obsolete\tracer.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\coverage\tracer.pyi" "Archive\Obsolete\tracer.pyi"
move "venv\Lib\site-packages\coverage\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\licenses\LICENSE.APACHE" "Archive\Obsolete\LICENSE.APACHE"
move "venv\Lib\site-packages\cryptography-45.0.3.dist-info\licenses\LICENSE.BSD" "Archive\Obsolete\LICENSE.BSD"
move "venv\Lib\site-packages\cryptography\__about__.py" "Archive\Obsolete\__about__.py"
move "venv\Lib\site-packages\cryptography\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\cryptography\fernet.py" "Archive\Obsolete\fernet.py"
move "venv\Lib\site-packages\cryptography\hazmat\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\_oid.py" "Archive\Obsolete\_oid.py"
move "venv\Lib\site-packages\cryptography\hazmat\backends\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\backends\openssl\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\backends\openssl\backend.py" "Archive\Obsolete\backend.py"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust.pyd" "Archive\Obsolete\_rust.pyd"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\__init__.pyi" "Archive\Obsolete\__init__.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\_openssl.pyi" "Archive\Obsolete\_openssl.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\asn1.pyi" "Archive\Obsolete\asn1.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\exceptions.pyi" "Archive\Obsolete\exceptions.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\ocsp.pyi" "Archive\Obsolete\ocsp.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\__init__.pyi" "Archive\Obsolete\__init__.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\aead.pyi" "Archive\Obsolete\aead.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\ciphers.pyi" "Archive\Obsolete\ciphers.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\cmac.pyi" "Archive\Obsolete\cmac.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\dh.pyi" "Archive\Obsolete\dh.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\dsa.pyi" "Archive\Obsolete\dsa.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\ec.pyi" "Archive\Obsolete\ec.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\ed25519.pyi" "Archive\Obsolete\ed25519.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\ed448.pyi" "Archive\Obsolete\ed448.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\hashes.pyi" "Archive\Obsolete\hashes.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\hmac.pyi" "Archive\Obsolete\hmac.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\kdf.pyi" "Archive\Obsolete\kdf.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\keys.pyi" "Archive\Obsolete\keys.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\poly1305.pyi" "Archive\Obsolete\poly1305.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\rsa.pyi" "Archive\Obsolete\rsa.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\x25519.pyi" "Archive\Obsolete\x25519.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\openssl\x448.pyi" "Archive\Obsolete\x448.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\pkcs12.pyi" "Archive\Obsolete\pkcs12.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\pkcs7.pyi" "Archive\Obsolete\pkcs7.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\test_support.pyi" "Archive\Obsolete\test_support.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\_rust\x509.pyi" "Archive\Obsolete\x509.pyi"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\openssl\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\openssl\_conditional.py" "Archive\Obsolete\_conditional.py"
move "venv\Lib\site-packages\cryptography\hazmat\bindings\openssl\binding.py" "Archive\Obsolete\binding.py"
move "venv\Lib\site-packages\cryptography\hazmat\decrepit\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\decrepit\ciphers\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\decrepit\ciphers\algorithms.py" "Archive\Obsolete\algorithms.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\_asymmetric.py" "Archive\Obsolete\_asymmetric.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\_cipheralgorithm.py" "Archive\Obsolete\_cipheralgorithm.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\_serialization.py" "Archive\Obsolete\_serialization.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\dh.py" "Archive\Obsolete\dh.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\dsa.py" "Archive\Obsolete\dsa.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\ec.py" "Archive\Obsolete\ec.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\ed25519.py" "Archive\Obsolete\ed25519.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\ed448.py" "Archive\Obsolete\ed448.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\padding.py" "Archive\Obsolete\padding.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\rsa.py" "Archive\Obsolete\rsa.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\x25519.py" "Archive\Obsolete\x25519.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\x448.py" "Archive\Obsolete\x448.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\ciphers\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\ciphers\aead.py" "Archive\Obsolete\aead.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\ciphers\algorithms.py" "Archive\Obsolete\algorithms.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\ciphers\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\ciphers\modes.py" "Archive\Obsolete\modes.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\cmac.py" "Archive\Obsolete\cmac.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\constant_time.py" "Archive\Obsolete\constant_time.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\hashes.py" "Archive\Obsolete\hashes.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\hmac.py" "Archive\Obsolete\hmac.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\argon2.py" "Archive\Obsolete\argon2.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\concatkdf.py" "Archive\Obsolete\concatkdf.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\hkdf.py" "Archive\Obsolete\hkdf.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\kbkdf.py" "Archive\Obsolete\kbkdf.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\pbkdf2.py" "Archive\Obsolete\pbkdf2.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\scrypt.py" "Archive\Obsolete\scrypt.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\x963kdf.py" "Archive\Obsolete\x963kdf.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\keywrap.py" "Archive\Obsolete\keywrap.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\padding.py" "Archive\Obsolete\padding.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\poly1305.py" "Archive\Obsolete\poly1305.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\serialization\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\serialization\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\serialization\pkcs12.py" "Archive\Obsolete\pkcs12.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\serialization\pkcs7.py" "Archive\Obsolete\pkcs7.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\serialization\ssh.py" "Archive\Obsolete\ssh.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\twofactor\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\twofactor\hotp.py" "Archive\Obsolete\hotp.py"
move "venv\Lib\site-packages\cryptography\hazmat\primitives\twofactor\totp.py" "Archive\Obsolete\totp.py"
move "venv\Lib\site-packages\cryptography\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\cryptography\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\cryptography\x509\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\cryptography\x509\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\cryptography\x509\certificate_transparency.py" "Archive\Obsolete\certificate_transparency.py"
move "venv\Lib\site-packages\cryptography\x509\extensions.py" "Archive\Obsolete\extensions.py"
move "venv\Lib\site-packages\cryptography\x509\general_name.py" "Archive\Obsolete\general_name.py"
move "venv\Lib\site-packages\cryptography\x509\name.py" "Archive\Obsolete\name.py"
move "venv\Lib\site-packages\cryptography\x509\ocsp.py" "Archive\Obsolete\ocsp.py"
move "venv\Lib\site-packages\cryptography\x509\oid.py" "Archive\Obsolete\oid.py"
move "venv\Lib\site-packages\cryptography\x509\verification.py" "Archive\Obsolete\verification.py"
move "venv\Lib\site-packages\dateutil\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\dateutil\_common.py" "Archive\Obsolete\_common.py"
move "venv\Lib\site-packages\dateutil\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\dateutil\easter.py" "Archive\Obsolete\easter.py"
move "venv\Lib\site-packages\dateutil\parser\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\dateutil\parser\_parser.py" "Archive\Obsolete\_parser.py"
move "venv\Lib\site-packages\dateutil\parser\isoparser.py" "Archive\Obsolete\isoparser.py"
move "venv\Lib\site-packages\dateutil\relativedelta.py" "Archive\Obsolete\relativedelta.py"
move "venv\Lib\site-packages\dateutil\rrule.py" "Archive\Obsolete\rrule.py"
move "venv\Lib\site-packages\dateutil\tz\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\dateutil\tz\_common.py" "Archive\Obsolete\_common.py"
move "venv\Lib\site-packages\dateutil\tz\_factories.py" "Archive\Obsolete\_factories.py"
move "venv\Lib\site-packages\dateutil\tz\tz.py" "Archive\Obsolete\tz.py"
move "venv\Lib\site-packages\dateutil\tz\win.py" "Archive\Obsolete\win.py"
move "venv\Lib\site-packages\dateutil\tzwin.py" "Archive\Obsolete\tzwin.py"
move "venv\Lib\site-packages\dateutil\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\dateutil\zoneinfo\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\dateutil\zoneinfo\dateutil-zoneinfo.tar.gz" "Archive\Obsolete\dateutil-zoneinfo.tar.gz"
move "venv\Lib\site-packages\dateutil\zoneinfo\rebuild.py" "Archive\Obsolete\rebuild.py"
move "venv\Lib\site-packages\distutils-precedence.pth" "Archive\Obsolete\distutils-precedence.pth"
move "venv\Lib\site-packages\dotenv\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\dotenv\cli.py" "Archive\Obsolete\cli.py"
move "venv\Lib\site-packages\dotenv\ipython.py" "Archive\Obsolete\ipython.py"
move "venv\Lib\site-packages\dotenv\main.py" "Archive\Obsolete\main.py"
move "venv\Lib\site-packages\dotenv\parser.py" "Archive\Obsolete\parser.py"
move "venv\Lib\site-packages\dotenv\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\dotenv\variables.py" "Archive\Obsolete\variables.py"
move "venv\Lib\site-packages\dotenv\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\ecdsa-0.19.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\ecdsa-0.19.1.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\ecdsa-0.19.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\ecdsa-0.19.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\ecdsa-0.19.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\ecdsa-0.19.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\ecdsa\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\ecdsa\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\ecdsa\_rwlock.py" "Archive\Obsolete\_rwlock.py"
move "venv\Lib\site-packages\ecdsa\_sha3.py" "Archive\Obsolete\_sha3.py"
move "venv\Lib\site-packages\ecdsa\curves.py" "Archive\Obsolete\curves.py"
move "venv\Lib\site-packages\ecdsa\der.py" "Archive\Obsolete\der.py"
move "venv\Lib\site-packages\ecdsa\ecdh.py" "Archive\Obsolete\ecdh.py"
move "venv\Lib\site-packages\ecdsa\ecdsa.py" "Archive\Obsolete\ecdsa.py"
move "venv\Lib\site-packages\ecdsa\eddsa.py" "Archive\Obsolete\eddsa.py"
move "venv\Lib\site-packages\ecdsa\ellipticcurve.py" "Archive\Obsolete\ellipticcurve.py"
move "venv\Lib\site-packages\ecdsa\errors.py" "Archive\Obsolete\errors.py"
move "venv\Lib\site-packages\ecdsa\keys.py" "Archive\Obsolete\keys.py"
move "venv\Lib\site-packages\ecdsa\numbertheory.py" "Archive\Obsolete\numbertheory.py"
move "venv\Lib\site-packages\ecdsa\rfc6979.py" "Archive\Obsolete\rfc6979.py"
move "venv\Lib\site-packages\ecdsa\ssh.py" "Archive\Obsolete\ssh.py"
move "venv\Lib\site-packages\ecdsa\test_curves.py" "Archive\Obsolete\test_curves.py"
move "venv\Lib\site-packages\ecdsa\test_der.py" "Archive\Obsolete\test_der.py"
move "venv\Lib\site-packages\ecdsa\test_ecdh.py" "Archive\Obsolete\test_ecdh.py"
move "venv\Lib\site-packages\ecdsa\test_ecdsa.py" "Archive\Obsolete\test_ecdsa.py"
move "venv\Lib\site-packages\ecdsa\test_eddsa.py" "Archive\Obsolete\test_eddsa.py"
move "venv\Lib\site-packages\ecdsa\test_ellipticcurve.py" "Archive\Obsolete\test_ellipticcurve.py"
move "venv\Lib\site-packages\ecdsa\test_jacobi.py" "Archive\Obsolete\test_jacobi.py"
move "venv\Lib\site-packages\ecdsa\test_keys.py" "Archive\Obsolete\test_keys.py"
move "venv\Lib\site-packages\ecdsa\test_malformed_sigs.py" "Archive\Obsolete\test_malformed_sigs.py"
move "venv\Lib\site-packages\ecdsa\test_numbertheory.py" "Archive\Obsolete\test_numbertheory.py"
move "venv\Lib\site-packages\ecdsa\test_pyecdsa.py" "Archive\Obsolete\test_pyecdsa.py"
move "venv\Lib\site-packages\ecdsa\test_rw_lock.py" "Archive\Obsolete\test_rw_lock.py"
move "venv\Lib\site-packages\ecdsa\test_sha3.py" "Archive\Obsolete\test_sha3.py"
move "venv\Lib\site-packages\ecdsa\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\fastapi-0.115.12.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\fastapi\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\fastapi\__main__.py" "Archive\Obsolete\__main__.py"
move "venv\Lib\site-packages\fastapi\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\fastapi\background.py" "Archive\Obsolete\background.py"
move "venv\Lib\site-packages\fastapi\concurrency.py" "Archive\Obsolete\concurrency.py"
move "venv\Lib\site-packages\fastapi\datastructures.py" "Archive\Obsolete\datastructures.py"
move "venv\Lib\site-packages\fastapi\dependencies\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\fastapi\dependencies\models.py" "Archive\Obsolete\models.py"
move "venv\Lib\site-packages\fastapi\dependencies\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\fastapi\encoders.py" "Archive\Obsolete\encoders.py"
move "venv\Lib\site-packages\fastapi\exception_handlers.py" "Archive\Obsolete\exception_handlers.py"
move "venv\Lib\site-packages\fastapi\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\fastapi\logger.py" "Archive\Obsolete\logger.py"
move "venv\Lib\site-packages\fastapi\middleware\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\fastapi\middleware\cors.py" "Archive\Obsolete\cors.py"
move "venv\Lib\site-packages\fastapi\middleware\gzip.py" "Archive\Obsolete\gzip.py"
move "venv\Lib\site-packages\fastapi\middleware\httpsredirect.py" "Archive\Obsolete\httpsredirect.py"
move "venv\Lib\site-packages\fastapi\middleware\trustedhost.py" "Archive\Obsolete\trustedhost.py"
move "venv\Lib\site-packages\fastapi\middleware\wsgi.py" "Archive\Obsolete\wsgi.py"
move "venv\Lib\site-packages\fastapi\openapi\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\fastapi\openapi\constants.py" "Archive\Obsolete\constants.py"
move "venv\Lib\site-packages\fastapi\openapi\models.py" "Archive\Obsolete\models.py"
move "venv\Lib\site-packages\fastapi\openapi\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\fastapi\param_functions.py" "Archive\Obsolete\param_functions.py"
move "venv\Lib\site-packages\fastapi\params.py" "Archive\Obsolete\params.py"
move "venv\Lib\site-packages\fastapi\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\fastapi\requests.py" "Archive\Obsolete\requests.py"
move "venv\Lib\site-packages\fastapi\responses.py" "Archive\Obsolete\responses.py"
move "venv\Lib\site-packages\fastapi\routing.py" "Archive\Obsolete\routing.py"
move "venv\Lib\site-packages\fastapi\security\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\fastapi\security\api_key.py" "Archive\Obsolete\api_key.py"
move "venv\Lib\site-packages\fastapi\security\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\fastapi\security\http.py" "Archive\Obsolete\http.py"
move "venv\Lib\site-packages\fastapi\security\oauth2.py" "Archive\Obsolete\oauth2.py"
move "venv\Lib\site-packages\fastapi\security\open_id_connect_url.py" "Archive\Obsolete\open_id_connect_url.py"
move "venv\Lib\site-packages\fastapi\security\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\fastapi\staticfiles.py" "Archive\Obsolete\staticfiles.py"
move "venv\Lib\site-packages\fastapi\templating.py" "Archive\Obsolete\templating.py"
move "venv\Lib\site-packages\fastapi\testclient.py" "Archive\Obsolete\testclient.py"
move "venv\Lib\site-packages\fastapi\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\fastapi\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\fastapi\websockets.py" "Archive\Obsolete\websockets.py"
move "venv\Lib\site-packages\frozenlist-1.6.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\frozenlist-1.6.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\frozenlist-1.6.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\frozenlist-1.6.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\frozenlist-1.6.2.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\frozenlist-1.6.2.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\frozenlist\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\frozenlist\__init__.pyi" "Archive\Obsolete\__init__.pyi"
move "venv\Lib\site-packages\frozenlist\_frozenlist.cp311-win_amd64.pyd" "Archive\Obsolete\_frozenlist.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\frozenlist\_frozenlist.pyx" "Archive\Obsolete\_frozenlist.pyx"
move "venv\Lib\site-packages\frozenlist\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\h11-0.16.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\h11-0.16.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\h11-0.16.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\h11-0.16.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\h11-0.16.0.dist-info\licenses\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "venv\Lib\site-packages\h11-0.16.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\h11\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\h11\_abnf.py" "Archive\Obsolete\_abnf.py"
move "venv\Lib\site-packages\h11\_connection.py" "Archive\Obsolete\_connection.py"
move "venv\Lib\site-packages\h11\_headers.py" "Archive\Obsolete\_headers.py"
move "venv\Lib\site-packages\h11\_readers.py" "Archive\Obsolete\_readers.py"
move "venv\Lib\site-packages\h11\_receivebuffer.py" "Archive\Obsolete\_receivebuffer.py"
move "venv\Lib\site-packages\h11\_state.py" "Archive\Obsolete\_state.py"
move "venv\Lib\site-packages\h11\_util.py" "Archive\Obsolete\_util.py"
move "venv\Lib\site-packages\h11\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\h11\_writers.py" "Archive\Obsolete\_writers.py"
move "venv\Lib\site-packages\h11\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\httpcore-1.0.9.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\httpcore-1.0.9.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\httpcore-1.0.9.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\httpcore-1.0.9.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\httpcore-1.0.9.dist-info\licenses\LICENSE.md" "Archive\Obsolete\LICENSE.md"
move "venv\Lib\site-packages\httpcore\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\httpcore\_api.py" "Archive\Obsolete\_api.py"
move "venv\Lib\site-packages\httpcore\_async\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\httpcore\_async\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\httpcore\_async\connection_pool.py" "Archive\Obsolete\connection_pool.py"
move "venv\Lib\site-packages\httpcore\_async\http11.py" "Archive\Obsolete\http11.py"
move "venv\Lib\site-packages\httpcore\_async\http2.py" "Archive\Obsolete\http2.py"
move "venv\Lib\site-packages\httpcore\_async\http_proxy.py" "Archive\Obsolete\http_proxy.py"
move "venv\Lib\site-packages\httpcore\_async\interfaces.py" "Archive\Obsolete\interfaces.py"
move "venv\Lib\site-packages\httpcore\_async\socks_proxy.py" "Archive\Obsolete\socks_proxy.py"
move "venv\Lib\site-packages\httpcore\_backends\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\httpcore\_backends\anyio.py" "Archive\Obsolete\anyio.py"
move "venv\Lib\site-packages\httpcore\_backends\auto.py" "Archive\Obsolete\auto.py"
move "venv\Lib\site-packages\httpcore\_backends\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\httpcore\_backends\mock.py" "Archive\Obsolete\mock.py"
move "venv\Lib\site-packages\httpcore\_backends\sync.py" "Archive\Obsolete\sync.py"
move "venv\Lib\site-packages\httpcore\_backends\trio.py" "Archive\Obsolete\trio.py"
move "venv\Lib\site-packages\httpcore\_exceptions.py" "Archive\Obsolete\_exceptions.py"
move "venv\Lib\site-packages\httpcore\_models.py" "Archive\Obsolete\_models.py"
move "venv\Lib\site-packages\httpcore\_ssl.py" "Archive\Obsolete\_ssl.py"
move "venv\Lib\site-packages\httpcore\_sync\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\httpcore\_sync\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\httpcore\_sync\connection_pool.py" "Archive\Obsolete\connection_pool.py"
move "venv\Lib\site-packages\httpcore\_sync\http11.py" "Archive\Obsolete\http11.py"
move "venv\Lib\site-packages\httpcore\_sync\http2.py" "Archive\Obsolete\http2.py"
move "venv\Lib\site-packages\httpcore\_sync\http_proxy.py" "Archive\Obsolete\http_proxy.py"
move "venv\Lib\site-packages\httpcore\_sync\interfaces.py" "Archive\Obsolete\interfaces.py"
move "venv\Lib\site-packages\httpcore\_sync\socks_proxy.py" "Archive\Obsolete\socks_proxy.py"
move "venv\Lib\site-packages\httpcore\_synchronization.py" "Archive\Obsolete\_synchronization.py"
move "venv\Lib\site-packages\httpcore\_trace.py" "Archive\Obsolete\_trace.py"
move "venv\Lib\site-packages\httpcore\_utils.py" "Archive\Obsolete\_utils.py"
move "venv\Lib\site-packages\httpcore\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\httpx-0.25.1.dist-info\licenses\LICENSE.md" "Archive\Obsolete\LICENSE.md"
move "venv\Lib\site-packages\httpx\__version__.py" "Archive\Obsolete\__version__.py"
move "venv\Lib\site-packages\httpx\_api.py" "Archive\Obsolete\_api.py"
move "venv\Lib\site-packages\httpx\_auth.py" "Archive\Obsolete\_auth.py"
move "venv\Lib\site-packages\httpx\_client.py" "Archive\Obsolete\_client.py"
move "venv\Lib\site-packages\httpx\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\httpx\_config.py" "Archive\Obsolete\_config.py"
move "venv\Lib\site-packages\httpx\_content.py" "Archive\Obsolete\_content.py"
move "venv\Lib\site-packages\httpx\_decoders.py" "Archive\Obsolete\_decoders.py"
move "venv\Lib\site-packages\httpx\_exceptions.py" "Archive\Obsolete\_exceptions.py"
move "venv\Lib\site-packages\httpx\_models.py" "Archive\Obsolete\_models.py"
move "venv\Lib\site-packages\httpx\_multipart.py" "Archive\Obsolete\_multipart.py"
move "venv\Lib\site-packages\httpx\_status_codes.py" "Archive\Obsolete\_status_codes.py"
move "venv\Lib\site-packages\httpx\_transports\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\httpx\_transports\asgi.py" "Archive\Obsolete\asgi.py"
move "venv\Lib\site-packages\httpx\_transports\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\httpx\_transports\default.py" "Archive\Obsolete\default.py"
move "venv\Lib\site-packages\httpx\_transports\mock.py" "Archive\Obsolete\mock.py"
move "venv\Lib\site-packages\httpx\_transports\wsgi.py" "Archive\Obsolete\wsgi.py"
move "venv\Lib\site-packages\httpx\_types.py" "Archive\Obsolete\_types.py"
move "venv\Lib\site-packages\httpx\_urlparse.py" "Archive\Obsolete\_urlparse.py"
move "venv\Lib\site-packages\httpx\_urls.py" "Archive\Obsolete\_urls.py"
move "venv\Lib\site-packages\httpx\_utils.py" "Archive\Obsolete\_utils.py"
move "venv\Lib\site-packages\httpx\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\idna-3.10.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\idna-3.10.dist-info\LICENSE.md" "Archive\Obsolete\LICENSE.md"
move "venv\Lib\site-packages\idna-3.10.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\idna-3.10.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\idna-3.10.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\idna\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\idna\codec.py" "Archive\Obsolete\codec.py"
move "venv\Lib\site-packages\idna\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\idna\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\idna\idnadata.py" "Archive\Obsolete\idnadata.py"
move "venv\Lib\site-packages\idna\intranges.py" "Archive\Obsolete\intranges.py"
move "venv\Lib\site-packages\idna\package_data.py" "Archive\Obsolete\package_data.py"
move "venv\Lib\site-packages\idna\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\idna\uts46data.py" "Archive\Obsolete\uts46data.py"
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\iniconfig-2.1.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\iniconfig\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\iniconfig\_parse.py" "Archive\Obsolete\_parse.py"
move "venv\Lib\site-packages\iniconfig\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\iniconfig\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\iniconfig\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\jose\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\jose\backends\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\jose\backends\_asn1.py" "Archive\Obsolete\_asn1.py"
move "venv\Lib\site-packages\jose\backends\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\jose\backends\cryptography_backend.py" "Archive\Obsolete\cryptography_backend.py"
move "venv\Lib\site-packages\jose\backends\ecdsa_backend.py" "Archive\Obsolete\ecdsa_backend.py"
move "venv\Lib\site-packages\jose\backends\native.py" "Archive\Obsolete\native.py"
move "venv\Lib\site-packages\jose\backends\rsa_backend.py" "Archive\Obsolete\rsa_backend.py"
move "venv\Lib\site-packages\jose\constants.py" "Archive\Obsolete\constants.py"
move "venv\Lib\site-packages\jose\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\jose\jwe.py" "Archive\Obsolete\jwe.py"
move "venv\Lib\site-packages\jose\jwk.py" "Archive\Obsolete\jwk.py"
move "venv\Lib\site-packages\jose\jws.py" "Archive\Obsolete\jws.py"
move "venv\Lib\site-packages\jose\jwt.py" "Archive\Obsolete\jwt.py"
move "venv\Lib\site-packages\jose\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\jwt\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\jwt\algorithms.py" "Archive\Obsolete\algorithms.py"
move "venv\Lib\site-packages\jwt\api_jwk.py" "Archive\Obsolete\api_jwk.py"
move "venv\Lib\site-packages\jwt\api_jws.py" "Archive\Obsolete\api_jws.py"
move "venv\Lib\site-packages\jwt\api_jwt.py" "Archive\Obsolete\api_jwt.py"
move "venv\Lib\site-packages\jwt\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\jwt\jwk_set_cache.py" "Archive\Obsolete\jwk_set_cache.py"
move "venv\Lib\site-packages\jwt\jwks_client.py" "Archive\Obsolete\jwks_client.py"
move "venv\Lib\site-packages\jwt\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\jwt\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\jwt\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\jwt\warnings.py" "Archive\Obsolete\warnings.py"
move "venv\Lib\site-packages\markdown_it\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\markdown_it\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\markdown_it\_punycode.py" "Archive\Obsolete\_punycode.py"
move "venv\Lib\site-packages\markdown_it\cli\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\markdown_it\common\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\markdown_it\common\entities.py" "Archive\Obsolete\entities.py"
move "venv\Lib\site-packages\markdown_it\common\html_blocks.py" "Archive\Obsolete\html_blocks.py"
move "venv\Lib\site-packages\markdown_it\common\html_re.py" "Archive\Obsolete\html_re.py"
move "venv\Lib\site-packages\markdown_it\common\normalize_url.py" "Archive\Obsolete\normalize_url.py"
move "venv\Lib\site-packages\markdown_it\common\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\markdown_it\helpers\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\markdown_it\helpers\parse_link_destination.py" "Archive\Obsolete\parse_link_destination.py"
move "venv\Lib\site-packages\markdown_it\helpers\parse_link_label.py" "Archive\Obsolete\parse_link_label.py"
move "venv\Lib\site-packages\markdown_it\helpers\parse_link_title.py" "Archive\Obsolete\parse_link_title.py"
move "venv\Lib\site-packages\markdown_it\main.py" "Archive\Obsolete\main.py"
move "venv\Lib\site-packages\markdown_it\parser_block.py" "Archive\Obsolete\parser_block.py"
move "venv\Lib\site-packages\markdown_it\parser_core.py" "Archive\Obsolete\parser_core.py"
move "venv\Lib\site-packages\markdown_it\parser_inline.py" "Archive\Obsolete\parser_inline.py"
move "venv\Lib\site-packages\markdown_it\port.yaml" "Archive\Obsolete\port.yaml"
move "venv\Lib\site-packages\markdown_it\presets\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\markdown_it\presets\commonmark.py" "Archive\Obsolete\commonmark.py"
move "venv\Lib\site-packages\markdown_it\presets\default.py" "Archive\Obsolete\default.py"
move "venv\Lib\site-packages\markdown_it\presets\zero.py" "Archive\Obsolete\zero.py"
move "venv\Lib\site-packages\markdown_it\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\markdown_it\renderer.py" "Archive\Obsolete\renderer.py"
move "venv\Lib\site-packages\markdown_it\ruler.py" "Archive\Obsolete\ruler.py"
move "venv\Lib\site-packages\markdown_it\rules_block\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\markdown_it\rules_block\blockquote.py" "Archive\Obsolete\blockquote.py"
move "venv\Lib\site-packages\markdown_it\rules_block\code.py" "Archive\Obsolete\code.py"
move "venv\Lib\site-packages\markdown_it\rules_block\fence.py" "Archive\Obsolete\fence.py"
move "venv\Lib\site-packages\markdown_it\rules_block\heading.py" "Archive\Obsolete\heading.py"
move "venv\Lib\site-packages\markdown_it\rules_block\hr.py" "Archive\Obsolete\hr.py"
move "venv\Lib\site-packages\markdown_it\rules_block\html_block.py" "Archive\Obsolete\html_block.py"
move "venv\Lib\site-packages\markdown_it\rules_block\lheading.py" "Archive\Obsolete\lheading.py"
move "venv\Lib\site-packages\markdown_it\rules_block\list.py" "Archive\Obsolete\list.py"
move "venv\Lib\site-packages\markdown_it\rules_block\paragraph.py" "Archive\Obsolete\paragraph.py"
move "venv\Lib\site-packages\markdown_it\rules_block\reference.py" "Archive\Obsolete\reference.py"
move "venv\Lib\site-packages\markdown_it\rules_block\state_block.py" "Archive\Obsolete\state_block.py"
move "venv\Lib\site-packages\markdown_it\rules_block\table.py" "Archive\Obsolete\table.py"
move "venv\Lib\site-packages\markdown_it\rules_core\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\markdown_it\rules_core\block.py" "Archive\Obsolete\block.py"
move "venv\Lib\site-packages\markdown_it\rules_core\inline.py" "Archive\Obsolete\inline.py"
move "venv\Lib\site-packages\markdown_it\rules_core\linkify.py" "Archive\Obsolete\linkify.py"
move "venv\Lib\site-packages\markdown_it\rules_core\normalize.py" "Archive\Obsolete\normalize.py"
move "venv\Lib\site-packages\markdown_it\rules_core\replacements.py" "Archive\Obsolete\replacements.py"
move "venv\Lib\site-packages\markdown_it\rules_core\smartquotes.py" "Archive\Obsolete\smartquotes.py"
move "venv\Lib\site-packages\markdown_it\rules_core\state_core.py" "Archive\Obsolete\state_core.py"
move "venv\Lib\site-packages\markdown_it\rules_core\text_join.py" "Archive\Obsolete\text_join.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\autolink.py" "Archive\Obsolete\autolink.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\backticks.py" "Archive\Obsolete\backticks.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\balance_pairs.py" "Archive\Obsolete\balance_pairs.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\emphasis.py" "Archive\Obsolete\emphasis.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\entity.py" "Archive\Obsolete\entity.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\escape.py" "Archive\Obsolete\escape.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\fragments_join.py" "Archive\Obsolete\fragments_join.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\html_inline.py" "Archive\Obsolete\html_inline.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\image.py" "Archive\Obsolete\image.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\link.py" "Archive\Obsolete\link.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\linkify.py" "Archive\Obsolete\linkify.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\newline.py" "Archive\Obsolete\newline.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\state_inline.py" "Archive\Obsolete\state_inline.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\strikethrough.py" "Archive\Obsolete\strikethrough.py"
move "venv\Lib\site-packages\markdown_it\rules_inline\text.py" "Archive\Obsolete\text.py"
move "venv\Lib\site-packages\markdown_it\token.py" "Archive\Obsolete\token.py"
move "venv\Lib\site-packages\markdown_it\tree.py" "Archive\Obsolete\tree.py"
move "venv\Lib\site-packages\markdown_it\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\LICENSE.markdown-it" "Archive\Obsolete\LICENSE.markdown-it"
move "venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\markdown_it_py-3.0.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\mdurl-0.1.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\mdurl-0.1.2.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\mdurl-0.1.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\mdurl-0.1.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\mdurl-0.1.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\mdurl\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\mdurl\_decode.py" "Archive\Obsolete\_decode.py"
move "venv\Lib\site-packages\mdurl\_encode.py" "Archive\Obsolete\_encode.py"
move "venv\Lib\site-packages\mdurl\_format.py" "Archive\Obsolete\_format.py"
move "venv\Lib\site-packages\mdurl\_parse.py" "Archive\Obsolete\_parse.py"
move "venv\Lib\site-packages\mdurl\_url.py" "Archive\Obsolete\_url.py"
move "venv\Lib\site-packages\mdurl\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\multidict-6.4.4.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\multidict-6.4.4.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\multidict-6.4.4.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\multidict-6.4.4.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\multidict-6.4.4.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\multidict-6.4.4.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\multidict\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\multidict\_abc.py" "Archive\Obsolete\_abc.py"
move "venv\Lib\site-packages\multidict\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\multidict\_multidict.cp311-win_amd64.pyd" "Archive\Obsolete\_multidict.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\multidict\_multidict_py.py" "Archive\Obsolete\_multidict_py.py"
move "venv\Lib\site-packages\multidict\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\multipart\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\multipart\decoders.py" "Archive\Obsolete\decoders.py"
move "venv\Lib\site-packages\multipart\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\multipart\multipart.py" "Archive\Obsolete\multipart.py"
move "venv\Lib\site-packages\multipart\tests\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\multipart\tests\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\multipart\tests\test_data\http\CR_in_header.http" "Archive\Obsolete\CR_in_header.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\CR_in_header.yaml" "Archive\Obsolete\CR_in_header.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\CR_in_header_value.http" "Archive\Obsolete\CR_in_header_value.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\CR_in_header_value.yaml" "Archive\Obsolete\CR_in_header_value.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\almost_match_boundary.http" "Archive\Obsolete\almost_match_boundary.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\almost_match_boundary.yaml" "Archive\Obsolete\almost_match_boundary.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\almost_match_boundary_without_CR.http" "Archive\Obsolete\almost_match_boundary_without_CR.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\almost_match_boundary_without_CR.yaml" "Archive\Obsolete\almost_match_boundary_without_CR.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\almost_match_boundary_without_LF.http" "Archive\Obsolete\almost_match_boundary_without_LF.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\almost_match_boundary_without_LF.yaml" "Archive\Obsolete\almost_match_boundary_without_LF.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\almost_match_boundary_without_final_hyphen.http" "Archive\Obsolete\almost_match_boundary_without_final_hyphen.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\almost_match_boundary_without_final_hyphen.yaml" "Archive\Obsolete\almost_match_boundary_without_final_hyphen.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\bad_end_of_headers.http" "Archive\Obsolete\bad_end_of_headers.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\bad_end_of_headers.yaml" "Archive\Obsolete\bad_end_of_headers.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\bad_header_char.http" "Archive\Obsolete\bad_header_char.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\bad_header_char.yaml" "Archive\Obsolete\bad_header_char.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\bad_initial_boundary.http" "Archive\Obsolete\bad_initial_boundary.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\bad_initial_boundary.yaml" "Archive\Obsolete\bad_initial_boundary.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\base64_encoding.http" "Archive\Obsolete\base64_encoding.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\base64_encoding.yaml" "Archive\Obsolete\base64_encoding.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\empty_header.http" "Archive\Obsolete\empty_header.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\empty_header.yaml" "Archive\Obsolete\empty_header.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\multiple_fields.http" "Archive\Obsolete\multiple_fields.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\multiple_fields.yaml" "Archive\Obsolete\multiple_fields.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\multiple_files.http" "Archive\Obsolete\multiple_files.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\multiple_files.yaml" "Archive\Obsolete\multiple_files.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\quoted_printable_encoding.http" "Archive\Obsolete\quoted_printable_encoding.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\quoted_printable_encoding.yaml" "Archive\Obsolete\quoted_printable_encoding.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field.http" "Archive\Obsolete\single_field.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field.yaml" "Archive\Obsolete\single_field.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field_blocks.http" "Archive\Obsolete\single_field_blocks.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field_blocks.yaml" "Archive\Obsolete\single_field_blocks.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field_longer.http" "Archive\Obsolete\single_field_longer.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field_longer.yaml" "Archive\Obsolete\single_field_longer.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field_single_file.http" "Archive\Obsolete\single_field_single_file.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field_single_file.yaml" "Archive\Obsolete\single_field_single_file.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field_with_leading_newlines.http" "Archive\Obsolete\single_field_with_leading_newlines.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_field_with_leading_newlines.yaml" "Archive\Obsolete\single_field_with_leading_newlines.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_file.http" "Archive\Obsolete\single_file.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\single_file.yaml" "Archive\Obsolete\single_file.yaml"
move "venv\Lib\site-packages\multipart\tests\test_data\http\utf8_filename.http" "Archive\Obsolete\utf8_filename.http"
move "venv\Lib\site-packages\multipart\tests\test_data\http\utf8_filename.yaml" "Archive\Obsolete\utf8_filename.yaml"
move "venv\Lib\site-packages\multipart\tests\test_multipart.py" "Archive\Obsolete\test_multipart.py"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\direct_url.json" "Archive\Obsolete\direct_url.json"
move "venv\Lib\site-packages\n8n_builder-0.1.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\packaging-25.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\packaging-25.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\packaging-25.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\packaging-25.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE.APACHE" "Archive\Obsolete\LICENSE.APACHE"
move "venv\Lib\site-packages\packaging-25.0.dist-info\licenses\LICENSE.BSD" "Archive\Obsolete\LICENSE.BSD"
move "venv\Lib\site-packages\packaging\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\packaging\_elffile.py" "Archive\Obsolete\_elffile.py"
move "venv\Lib\site-packages\packaging\_manylinux.py" "Archive\Obsolete\_manylinux.py"
move "venv\Lib\site-packages\packaging\_parser.py" "Archive\Obsolete\_parser.py"
move "venv\Lib\site-packages\packaging\_structures.py" "Archive\Obsolete\_structures.py"
move "venv\Lib\site-packages\packaging\_tokenizer.py" "Archive\Obsolete\_tokenizer.py"
move "venv\Lib\site-packages\packaging\licenses\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\packaging\licenses\_spdx.py" "Archive\Obsolete\_spdx.py"
move "venv\Lib\site-packages\packaging\markers.py" "Archive\Obsolete\markers.py"
move "venv\Lib\site-packages\packaging\metadata.py" "Archive\Obsolete\metadata.py"
move "venv\Lib\site-packages\packaging\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\packaging\requirements.py" "Archive\Obsolete\requirements.py"
move "venv\Lib\site-packages\packaging\specifiers.py" "Archive\Obsolete\specifiers.py"
move "venv\Lib\site-packages\packaging\tags.py" "Archive\Obsolete\tags.py"
move "venv\Lib\site-packages\packaging\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\packaging\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\passlib-1.7.4.dist-info\zip-safe" "Archive\Obsolete\zip-safe"
move "venv\Lib\site-packages\passlib\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\_data\wordsets\bip39.txt" "Archive\Obsolete\bip39.txt"
move "venv\Lib\site-packages\passlib\_data\wordsets\eff_long.txt" "Archive\Obsolete\eff_long.txt"
move "venv\Lib\site-packages\passlib\_data\wordsets\eff_prefixed.txt" "Archive\Obsolete\eff_prefixed.txt"
move "venv\Lib\site-packages\passlib\_data\wordsets\eff_short.txt" "Archive\Obsolete\eff_short.txt"
move "venv\Lib\site-packages\passlib\apache.py" "Archive\Obsolete\apache.py"
move "venv\Lib\site-packages\passlib\apps.py" "Archive\Obsolete\apps.py"
move "venv\Lib\site-packages\passlib\context.py" "Archive\Obsolete\context.py"
move "venv\Lib\site-packages\passlib\crypto\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\crypto\_blowfish\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\crypto\_blowfish\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\passlib\crypto\_blowfish\unrolled.py" "Archive\Obsolete\unrolled.py"
move "venv\Lib\site-packages\passlib\crypto\_md4.py" "Archive\Obsolete\_md4.py"
move "venv\Lib\site-packages\passlib\crypto\des.py" "Archive\Obsolete\des.py"
move "venv\Lib\site-packages\passlib\crypto\digest.py" "Archive\Obsolete\digest.py"
move "venv\Lib\site-packages\passlib\crypto\scrypt\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\crypto\scrypt\_builtin.py" "Archive\Obsolete\_builtin.py"
move "venv\Lib\site-packages\passlib\exc.py" "Archive\Obsolete\exc.py"
move "venv\Lib\site-packages\passlib\ext\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\ext\django\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\ext\django\models.py" "Archive\Obsolete\models.py"
move "venv\Lib\site-packages\passlib\ext\django\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\passlib\handlers\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\handlers\argon2.py" "Archive\Obsolete\argon2.py"
move "venv\Lib\site-packages\passlib\handlers\bcrypt.py" "Archive\Obsolete\bcrypt.py"
move "venv\Lib\site-packages\passlib\handlers\cisco.py" "Archive\Obsolete\cisco.py"
move "venv\Lib\site-packages\passlib\handlers\des_crypt.py" "Archive\Obsolete\des_crypt.py"
move "venv\Lib\site-packages\passlib\handlers\digests.py" "Archive\Obsolete\digests.py"
move "venv\Lib\site-packages\passlib\handlers\django.py" "Archive\Obsolete\django.py"
move "venv\Lib\site-packages\passlib\handlers\fshp.py" "Archive\Obsolete\fshp.py"
move "venv\Lib\site-packages\passlib\handlers\ldap_digests.py" "Archive\Obsolete\ldap_digests.py"
move "venv\Lib\site-packages\passlib\handlers\md5_crypt.py" "Archive\Obsolete\md5_crypt.py"
move "venv\Lib\site-packages\passlib\handlers\misc.py" "Archive\Obsolete\misc.py"
move "venv\Lib\site-packages\passlib\handlers\mssql.py" "Archive\Obsolete\mssql.py"
move "venv\Lib\site-packages\passlib\handlers\mysql.py" "Archive\Obsolete\mysql.py"
move "venv\Lib\site-packages\passlib\handlers\oracle.py" "Archive\Obsolete\oracle.py"
move "venv\Lib\site-packages\passlib\handlers\pbkdf2.py" "Archive\Obsolete\pbkdf2.py"
move "venv\Lib\site-packages\passlib\handlers\phpass.py" "Archive\Obsolete\phpass.py"
move "venv\Lib\site-packages\passlib\handlers\postgres.py" "Archive\Obsolete\postgres.py"
move "venv\Lib\site-packages\passlib\handlers\roundup.py" "Archive\Obsolete\roundup.py"
move "venv\Lib\site-packages\passlib\handlers\scram.py" "Archive\Obsolete\scram.py"
move "venv\Lib\site-packages\passlib\handlers\scrypt.py" "Archive\Obsolete\scrypt.py"
move "venv\Lib\site-packages\passlib\handlers\sha1_crypt.py" "Archive\Obsolete\sha1_crypt.py"
move "venv\Lib\site-packages\passlib\handlers\sha2_crypt.py" "Archive\Obsolete\sha2_crypt.py"
move "venv\Lib\site-packages\passlib\handlers\sun_md5_crypt.py" "Archive\Obsolete\sun_md5_crypt.py"
move "venv\Lib\site-packages\passlib\handlers\windows.py" "Archive\Obsolete\windows.py"
move "venv\Lib\site-packages\passlib\hash.py" "Archive\Obsolete\hash.py"
move "venv\Lib\site-packages\passlib\hosts.py" "Archive\Obsolete\hosts.py"
move "venv\Lib\site-packages\passlib\ifc.py" "Archive\Obsolete\ifc.py"
move "venv\Lib\site-packages\passlib\pwd.py" "Archive\Obsolete\pwd.py"
move "venv\Lib\site-packages\passlib\registry.py" "Archive\Obsolete\registry.py"
move "venv\Lib\site-packages\passlib\tests\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\tests\__main__.py" "Archive\Obsolete\__main__.py"
move "venv\Lib\site-packages\passlib\tests\backports.py" "Archive\Obsolete\backports.py"
move "venv\Lib\site-packages\passlib\tests\sample1.cfg" "Archive\Obsolete\sample1.cfg"
move "venv\Lib\site-packages\passlib\tests\sample1b.cfg" "Archive\Obsolete\sample1b.cfg"
move "venv\Lib\site-packages\passlib\tests\sample1c.cfg" "Archive\Obsolete\sample1c.cfg"
move "venv\Lib\site-packages\passlib\tests\sample_config_1s.cfg" "Archive\Obsolete\sample_config_1s.cfg"
move "venv\Lib\site-packages\passlib\tests\test_apache.py" "Archive\Obsolete\test_apache.py"
move "venv\Lib\site-packages\passlib\tests\test_apps.py" "Archive\Obsolete\test_apps.py"
move "venv\Lib\site-packages\passlib\tests\test_context.py" "Archive\Obsolete\test_context.py"
move "venv\Lib\site-packages\passlib\tests\test_context_deprecated.py" "Archive\Obsolete\test_context_deprecated.py"
move "venv\Lib\site-packages\passlib\tests\test_crypto_builtin_md4.py" "Archive\Obsolete\test_crypto_builtin_md4.py"
move "venv\Lib\site-packages\passlib\tests\test_crypto_des.py" "Archive\Obsolete\test_crypto_des.py"
move "venv\Lib\site-packages\passlib\tests\test_crypto_digest.py" "Archive\Obsolete\test_crypto_digest.py"
move "venv\Lib\site-packages\passlib\tests\test_crypto_scrypt.py" "Archive\Obsolete\test_crypto_scrypt.py"
move "venv\Lib\site-packages\passlib\tests\test_ext_django.py" "Archive\Obsolete\test_ext_django.py"
move "venv\Lib\site-packages\passlib\tests\test_ext_django_source.py" "Archive\Obsolete\test_ext_django_source.py"
move "venv\Lib\site-packages\passlib\tests\test_handlers.py" "Archive\Obsolete\test_handlers.py"
move "venv\Lib\site-packages\passlib\tests\test_handlers_argon2.py" "Archive\Obsolete\test_handlers_argon2.py"
move "venv\Lib\site-packages\passlib\tests\test_handlers_bcrypt.py" "Archive\Obsolete\test_handlers_bcrypt.py"
move "venv\Lib\site-packages\passlib\tests\test_handlers_cisco.py" "Archive\Obsolete\test_handlers_cisco.py"
move "venv\Lib\site-packages\passlib\tests\test_handlers_django.py" "Archive\Obsolete\test_handlers_django.py"
move "venv\Lib\site-packages\passlib\tests\test_handlers_pbkdf2.py" "Archive\Obsolete\test_handlers_pbkdf2.py"
move "venv\Lib\site-packages\passlib\tests\test_handlers_scrypt.py" "Archive\Obsolete\test_handlers_scrypt.py"
move "venv\Lib\site-packages\passlib\tests\test_hosts.py" "Archive\Obsolete\test_hosts.py"
move "venv\Lib\site-packages\passlib\tests\test_pwd.py" "Archive\Obsolete\test_pwd.py"
move "venv\Lib\site-packages\passlib\tests\test_registry.py" "Archive\Obsolete\test_registry.py"
move "venv\Lib\site-packages\passlib\tests\test_totp.py" "Archive\Obsolete\test_totp.py"
move "venv\Lib\site-packages\passlib\tests\test_utils.py" "Archive\Obsolete\test_utils.py"
move "venv\Lib\site-packages\passlib\tests\test_utils_handlers.py" "Archive\Obsolete\test_utils_handlers.py"
move "venv\Lib\site-packages\passlib\tests\test_utils_md4.py" "Archive\Obsolete\test_utils_md4.py"
move "venv\Lib\site-packages\passlib\tests\test_utils_pbkdf2.py" "Archive\Obsolete\test_utils_pbkdf2.py"
move "venv\Lib\site-packages\passlib\tests\test_win32.py" "Archive\Obsolete\test_win32.py"
move "venv\Lib\site-packages\passlib\tests\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\passlib\totp.py" "Archive\Obsolete\totp.py"
move "venv\Lib\site-packages\passlib\utils\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\utils\binary.py" "Archive\Obsolete\binary.py"
move "venv\Lib\site-packages\passlib\utils\compat\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\passlib\utils\compat\_ordered_dict.py" "Archive\Obsolete\_ordered_dict.py"
move "venv\Lib\site-packages\passlib\utils\decor.py" "Archive\Obsolete\decor.py"
move "venv\Lib\site-packages\passlib\utils\des.py" "Archive\Obsolete\des.py"
move "venv\Lib\site-packages\passlib\utils\handlers.py" "Archive\Obsolete\handlers.py"
move "venv\Lib\site-packages\passlib\utils\md4.py" "Archive\Obsolete\md4.py"
move "venv\Lib\site-packages\passlib\utils\pbkdf2.py" "Archive\Obsolete\pbkdf2.py"
move "venv\Lib\site-packages\passlib\win32.py" "Archive\Obsolete\win32.py"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\AUTHORS.txt" "Archive\Obsolete\AUTHORS.txt"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\pip-23.1.2.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pip\__pip-runner__.py" "Archive\Obsolete\__pip-runner__.py"
move "venv\Lib\site-packages\pip\_internal\cli\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\cli\autocompletion.py" "Archive\Obsolete\autocompletion.py"
move "venv\Lib\site-packages\pip\_internal\cli\cmdoptions.py" "Archive\Obsolete\cmdoptions.py"
move "venv\Lib\site-packages\pip\_internal\cli\command_context.py" "Archive\Obsolete\command_context.py"
move "venv\Lib\site-packages\pip\_internal\cli\main_parser.py" "Archive\Obsolete\main_parser.py"
move "venv\Lib\site-packages\pip\_internal\cli\parser.py" "Archive\Obsolete\parser.py"
move "venv\Lib\site-packages\pip\_internal\cli\progress_bars.py" "Archive\Obsolete\progress_bars.py"
move "venv\Lib\site-packages\pip\_internal\cli\req_command.py" "Archive\Obsolete\req_command.py"
move "venv\Lib\site-packages\pip\_internal\cli\spinners.py" "Archive\Obsolete\spinners.py"
move "venv\Lib\site-packages\pip\_internal\cli\status_codes.py" "Archive\Obsolete\status_codes.py"
move "venv\Lib\site-packages\pip\_internal\commands\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\commands\cache.py" "Archive\Obsolete\cache.py"
move "venv\Lib\site-packages\pip\_internal\commands\check.py" "Archive\Obsolete\check.py"
move "venv\Lib\site-packages\pip\_internal\commands\completion.py" "Archive\Obsolete\completion.py"
move "venv\Lib\site-packages\pip\_internal\commands\configuration.py" "Archive\Obsolete\configuration.py"
move "venv\Lib\site-packages\pip\_internal\commands\debug.py" "Archive\Obsolete\debug.py"
move "venv\Lib\site-packages\pip\_internal\commands\download.py" "Archive\Obsolete\download.py"
move "venv\Lib\site-packages\pip\_internal\commands\freeze.py" "Archive\Obsolete\freeze.py"
move "venv\Lib\site-packages\pip\_internal\commands\hash.py" "Archive\Obsolete\hash.py"
move "venv\Lib\site-packages\pip\_internal\commands\help.py" "Archive\Obsolete\help.py"
move "venv\Lib\site-packages\pip\_internal\commands\index.py" "Archive\Obsolete\index.py"
move "venv\Lib\site-packages\pip\_internal\commands\inspect.py" "Archive\Obsolete\inspect.py"
move "venv\Lib\site-packages\pip\_internal\commands\install.py" "Archive\Obsolete\install.py"
move "venv\Lib\site-packages\pip\_internal\commands\list.py" "Archive\Obsolete\list.py"
move "venv\Lib\site-packages\pip\_internal\commands\search.py" "Archive\Obsolete\search.py"
move "venv\Lib\site-packages\pip\_internal\commands\show.py" "Archive\Obsolete\show.py"
move "venv\Lib\site-packages\pip\_internal\commands\uninstall.py" "Archive\Obsolete\uninstall.py"
move "venv\Lib\site-packages\pip\_internal\commands\wheel.py" "Archive\Obsolete\wheel.py"
move "venv\Lib\site-packages\pip\_internal\configuration.py" "Archive\Obsolete\configuration.py"
move "venv\Lib\site-packages\pip\_internal\distributions\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\distributions\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\pip\_internal\distributions\installed.py" "Archive\Obsolete\installed.py"
move "venv\Lib\site-packages\pip\_internal\distributions\sdist.py" "Archive\Obsolete\sdist.py"
move "venv\Lib\site-packages\pip\_internal\distributions\wheel.py" "Archive\Obsolete\wheel.py"
move "venv\Lib\site-packages\pip\_internal\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\pip\_internal\index\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\index\package_finder.py" "Archive\Obsolete\package_finder.py"
move "venv\Lib\site-packages\pip\_internal\index\sources.py" "Archive\Obsolete\sources.py"
move "venv\Lib\site-packages\pip\_internal\locations\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\locations\_distutils.py" "Archive\Obsolete\_distutils.py"
move "venv\Lib\site-packages\pip\_internal\locations\_sysconfig.py" "Archive\Obsolete\_sysconfig.py"
move "venv\Lib\site-packages\pip\_internal\locations\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\pip\_internal\metadata\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\metadata\_json.py" "Archive\Obsolete\_json.py"
move "venv\Lib\site-packages\pip\_internal\metadata\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\pip\_internal\metadata\importlib\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\metadata\importlib\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\pip\_internal\metadata\importlib\_dists.py" "Archive\Obsolete\_dists.py"
move "venv\Lib\site-packages\pip\_internal\metadata\importlib\_envs.py" "Archive\Obsolete\_envs.py"
move "venv\Lib\site-packages\pip\_internal\metadata\pkg_resources.py" "Archive\Obsolete\pkg_resources.py"
move "venv\Lib\site-packages\pip\_internal\models\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\models\candidate.py" "Archive\Obsolete\candidate.py"
move "venv\Lib\site-packages\pip\_internal\models\format_control.py" "Archive\Obsolete\format_control.py"
move "venv\Lib\site-packages\pip\_internal\models\index.py" "Archive\Obsolete\index.py"
move "venv\Lib\site-packages\pip\_internal\models\installation_report.py" "Archive\Obsolete\installation_report.py"
move "venv\Lib\site-packages\pip\_internal\models\link.py" "Archive\Obsolete\link.py"
move "venv\Lib\site-packages\pip\_internal\models\scheme.py" "Archive\Obsolete\scheme.py"
move "venv\Lib\site-packages\pip\_internal\models\search_scope.py" "Archive\Obsolete\search_scope.py"
move "venv\Lib\site-packages\pip\_internal\models\selection_prefs.py" "Archive\Obsolete\selection_prefs.py"
move "venv\Lib\site-packages\pip\_internal\models\wheel.py" "Archive\Obsolete\wheel.py"
move "venv\Lib\site-packages\pip\_internal\network\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\network\auth.py" "Archive\Obsolete\auth.py"
move "venv\Lib\site-packages\pip\_internal\network\cache.py" "Archive\Obsolete\cache.py"
move "venv\Lib\site-packages\pip\_internal\network\download.py" "Archive\Obsolete\download.py"
move "venv\Lib\site-packages\pip\_internal\network\lazy_wheel.py" "Archive\Obsolete\lazy_wheel.py"
move "venv\Lib\site-packages\pip\_internal\network\session.py" "Archive\Obsolete\session.py"
move "venv\Lib\site-packages\pip\_internal\network\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\pip\_internal\network\xmlrpc.py" "Archive\Obsolete\xmlrpc.py"
move "venv\Lib\site-packages\pip\_internal\operations\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\build_tracker.py" "Archive\Obsolete\build_tracker.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\metadata.py" "Archive\Obsolete\metadata.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\metadata_editable.py" "Archive\Obsolete\metadata_editable.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\metadata_legacy.py" "Archive\Obsolete\metadata_legacy.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\wheel.py" "Archive\Obsolete\wheel.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\wheel_editable.py" "Archive\Obsolete\wheel_editable.py"
move "venv\Lib\site-packages\pip\_internal\operations\build\wheel_legacy.py" "Archive\Obsolete\wheel_legacy.py"
move "venv\Lib\site-packages\pip\_internal\operations\check.py" "Archive\Obsolete\check.py"
move "venv\Lib\site-packages\pip\_internal\operations\freeze.py" "Archive\Obsolete\freeze.py"
move "venv\Lib\site-packages\pip\_internal\operations\install\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\operations\install\editable_legacy.py" "Archive\Obsolete\editable_legacy.py"
move "venv\Lib\site-packages\pip\_internal\operations\prepare.py" "Archive\Obsolete\prepare.py"
move "venv\Lib\site-packages\pip\_internal\req\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\req\req_file.py" "Archive\Obsolete\req_file.py"
move "venv\Lib\site-packages\pip\_internal\req\req_set.py" "Archive\Obsolete\req_set.py"
move "venv\Lib\site-packages\pip\_internal\resolution\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\resolution\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\pip\_internal\resolution\legacy\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\resolution\legacy\resolver.py" "Archive\Obsolete\resolver.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\candidates.py" "Archive\Obsolete\candidates.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\factory.py" "Archive\Obsolete\factory.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\found_candidates.py" "Archive\Obsolete\found_candidates.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\provider.py" "Archive\Obsolete\provider.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\reporter.py" "Archive\Obsolete\reporter.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\requirements.py" "Archive\Obsolete\requirements.py"
move "venv\Lib\site-packages\pip\_internal\resolution\resolvelib\resolver.py" "Archive\Obsolete\resolver.py"
move "venv\Lib\site-packages\pip\_internal\self_outdated_check.py" "Archive\Obsolete\self_outdated_check.py"
move "venv\Lib\site-packages\pip\_internal\utils\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\utils\_jaraco_text.py" "Archive\Obsolete\_jaraco_text.py"
move "venv\Lib\site-packages\pip\_internal\utils\_log.py" "Archive\Obsolete\_log.py"
move "venv\Lib\site-packages\pip\_internal\utils\appdirs.py" "Archive\Obsolete\appdirs.py"
move "venv\Lib\site-packages\pip\_internal\utils\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\pip\_internal\utils\compatibility_tags.py" "Archive\Obsolete\compatibility_tags.py"
move "venv\Lib\site-packages\pip\_internal\utils\datetime.py" "Archive\Obsolete\datetime.py"
move "venv\Lib\site-packages\pip\_internal\utils\deprecation.py" "Archive\Obsolete\deprecation.py"
move "venv\Lib\site-packages\pip\_internal\utils\direct_url_helpers.py" "Archive\Obsolete\direct_url_helpers.py"
move "venv\Lib\site-packages\pip\_internal\utils\egg_link.py" "Archive\Obsolete\egg_link.py"
move "venv\Lib\site-packages\pip\_internal\utils\encoding.py" "Archive\Obsolete\encoding.py"
move "venv\Lib\site-packages\pip\_internal\utils\entrypoints.py" "Archive\Obsolete\entrypoints.py"
move "venv\Lib\site-packages\pip\_internal\utils\filesystem.py" "Archive\Obsolete\filesystem.py"
move "venv\Lib\site-packages\pip\_internal\utils\filetypes.py" "Archive\Obsolete\filetypes.py"
move "venv\Lib\site-packages\pip\_internal\utils\glibc.py" "Archive\Obsolete\glibc.py"
move "venv\Lib\site-packages\pip\_internal\utils\hashes.py" "Archive\Obsolete\hashes.py"
move "venv\Lib\site-packages\pip\_internal\utils\inject_securetransport.py" "Archive\Obsolete\inject_securetransport.py"
move "venv\Lib\site-packages\pip\_internal\utils\logging.py" "Archive\Obsolete\logging.py"
move "venv\Lib\site-packages\pip\_internal\utils\models.py" "Archive\Obsolete\models.py"
move "venv\Lib\site-packages\pip\_internal\utils\packaging.py" "Archive\Obsolete\packaging.py"
move "venv\Lib\site-packages\pip\_internal\utils\setuptools_build.py" "Archive\Obsolete\setuptools_build.py"
move "venv\Lib\site-packages\pip\_internal\utils\subprocess.py" "Archive\Obsolete\subprocess.py"
move "venv\Lib\site-packages\pip\_internal\utils\temp_dir.py" "Archive\Obsolete\temp_dir.py"
move "venv\Lib\site-packages\pip\_internal\utils\unpacking.py" "Archive\Obsolete\unpacking.py"
move "venv\Lib\site-packages\pip\_internal\utils\urls.py" "Archive\Obsolete\urls.py"
move "venv\Lib\site-packages\pip\_internal\utils\virtualenv.py" "Archive\Obsolete\virtualenv.py"
move "venv\Lib\site-packages\pip\_internal\utils\wheel.py" "Archive\Obsolete\wheel.py"
move "venv\Lib\site-packages\pip\_internal\vcs\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_internal\vcs\bazaar.py" "Archive\Obsolete\bazaar.py"
move "venv\Lib\site-packages\pip\_internal\vcs\git.py" "Archive\Obsolete\git.py"
move "venv\Lib\site-packages\pip\_internal\vcs\mercurial.py" "Archive\Obsolete\mercurial.py"
move "venv\Lib\site-packages\pip\_internal\vcs\subversion.py" "Archive\Obsolete\subversion.py"
move "venv\Lib\site-packages\pip\_internal\vcs\versioncontrol.py" "Archive\Obsolete\versioncontrol.py"
move "venv\Lib\site-packages\pip\_internal\wheel_builder.py" "Archive\Obsolete\wheel_builder.py"
move "venv\Lib\site-packages\pip\_vendor\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\adapter.py" "Archive\Obsolete\adapter.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\cache.py" "Archive\Obsolete\cache.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\file_cache.py" "Archive\Obsolete\file_cache.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\redis_cache.py" "Archive\Obsolete\redis_cache.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\controller.py" "Archive\Obsolete\controller.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\filewrapper.py" "Archive\Obsolete\filewrapper.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\heuristics.py" "Archive\Obsolete\heuristics.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\serialize.py" "Archive\Obsolete\serialize.py"
move "venv\Lib\site-packages\pip\_vendor\cachecontrol\wrapper.py" "Archive\Obsolete\wrapper.py"
move "venv\Lib\site-packages\pip\_vendor\certifi\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\certifi\__main__.py" "Archive\Obsolete\__main__.py"
move "venv\Lib\site-packages\pip\_vendor\certifi\cacert.pem" "Archive\Obsolete\cacert.pem"
move "venv\Lib\site-packages\pip\_vendor\certifi\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\big5freq.py" "Archive\Obsolete\big5freq.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\big5prober.py" "Archive\Obsolete\big5prober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\chardistribution.py" "Archive\Obsolete\chardistribution.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\charsetgroupprober.py" "Archive\Obsolete\charsetgroupprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\charsetprober.py" "Archive\Obsolete\charsetprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\cli\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\codingstatemachine.py" "Archive\Obsolete\codingstatemachine.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\codingstatemachinedict.py" "Archive\Obsolete\codingstatemachinedict.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\cp949prober.py" "Archive\Obsolete\cp949prober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\enums.py" "Archive\Obsolete\enums.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\escprober.py" "Archive\Obsolete\escprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\escsm.py" "Archive\Obsolete\escsm.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\eucjpprober.py" "Archive\Obsolete\eucjpprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\euckrfreq.py" "Archive\Obsolete\euckrfreq.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\euckrprober.py" "Archive\Obsolete\euckrprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\euctwfreq.py" "Archive\Obsolete\euctwfreq.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\euctwprober.py" "Archive\Obsolete\euctwprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\gb2312freq.py" "Archive\Obsolete\gb2312freq.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\gb2312prober.py" "Archive\Obsolete\gb2312prober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\hebrewprober.py" "Archive\Obsolete\hebrewprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\jisfreq.py" "Archive\Obsolete\jisfreq.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\johabfreq.py" "Archive\Obsolete\johabfreq.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\johabprober.py" "Archive\Obsolete\johabprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\jpcntx.py" "Archive\Obsolete\jpcntx.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\langbulgarianmodel.py" "Archive\Obsolete\langbulgarianmodel.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\langgreekmodel.py" "Archive\Obsolete\langgreekmodel.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\langhebrewmodel.py" "Archive\Obsolete\langhebrewmodel.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\langhungarianmodel.py" "Archive\Obsolete\langhungarianmodel.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\langrussianmodel.py" "Archive\Obsolete\langrussianmodel.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\langthaimodel.py" "Archive\Obsolete\langthaimodel.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\langturkishmodel.py" "Archive\Obsolete\langturkishmodel.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\latin1prober.py" "Archive\Obsolete\latin1prober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\macromanprober.py" "Archive\Obsolete\macromanprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\mbcharsetprober.py" "Archive\Obsolete\mbcharsetprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\mbcsgroupprober.py" "Archive\Obsolete\mbcsgroupprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\mbcssm.py" "Archive\Obsolete\mbcssm.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\metadata\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\metadata\languages.py" "Archive\Obsolete\languages.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\resultdict.py" "Archive\Obsolete\resultdict.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\sbcharsetprober.py" "Archive\Obsolete\sbcharsetprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\sbcsgroupprober.py" "Archive\Obsolete\sbcsgroupprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\sjisprober.py" "Archive\Obsolete\sjisprober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\universaldetector.py" "Archive\Obsolete\universaldetector.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\utf1632prober.py" "Archive\Obsolete\utf1632prober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\utf8prober.py" "Archive\Obsolete\utf8prober.py"
move "venv\Lib\site-packages\pip\_vendor\chardet\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\ansi.py" "Archive\Obsolete\ansi.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\ansitowin32.py" "Archive\Obsolete\ansitowin32.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\initialise.py" "Archive\Obsolete\initialise.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\ansi_test.py" "Archive\Obsolete\ansi_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\ansitowin32_test.py" "Archive\Obsolete\ansitowin32_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\initialise_test.py" "Archive\Obsolete\initialise_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\isatty_test.py" "Archive\Obsolete\isatty_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\tests\winterm_test.py" "Archive\Obsolete\winterm_test.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\win32.py" "Archive\Obsolete\win32.py"
move "venv\Lib\site-packages\pip\_vendor\colorama\winterm.py" "Archive\Obsolete\winterm.py"
move "venv\Lib\site-packages\pip\_vendor\distlib\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\distlib\markers.py" "Archive\Obsolete\markers.py"
move "venv\Lib\site-packages\pip\_vendor\distlib\resources.py" "Archive\Obsolete\resources.py"
move "venv\Lib\site-packages\pip\_vendor\distlib\t32.exe" "Archive\Obsolete\t32.exe"
move "venv\Lib\site-packages\pip\_vendor\distlib\t64-arm.exe" "Archive\Obsolete\t64-arm.exe"
move "venv\Lib\site-packages\pip\_vendor\distlib\t64.exe" "Archive\Obsolete\t64.exe"
move "venv\Lib\site-packages\pip\_vendor\distlib\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\pip\_vendor\distlib\w32.exe" "Archive\Obsolete\w32.exe"
move "venv\Lib\site-packages\pip\_vendor\distlib\w64-arm.exe" "Archive\Obsolete\w64-arm.exe"
move "venv\Lib\site-packages\pip\_vendor\distlib\w64.exe" "Archive\Obsolete\w64.exe"
move "venv\Lib\site-packages\pip\_vendor\distro\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\idna\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\idna\codec.py" "Archive\Obsolete\codec.py"
move "venv\Lib\site-packages\pip\_vendor\idna\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\pip\_vendor\idna\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\pip\_vendor\idna\idnadata.py" "Archive\Obsolete\idnadata.py"
move "venv\Lib\site-packages\pip\_vendor\idna\intranges.py" "Archive\Obsolete\intranges.py"
move "venv\Lib\site-packages\pip\_vendor\idna\package_data.py" "Archive\Obsolete\package_data.py"
move "venv\Lib\site-packages\pip\_vendor\idna\uts46data.py" "Archive\Obsolete\uts46data.py"
move "venv\Lib\site-packages\pip\_vendor\msgpack\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\msgpack\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\pip\_vendor\msgpack\ext.py" "Archive\Obsolete\ext.py"
move "venv\Lib\site-packages\pip\_vendor\msgpack\fallback.py" "Archive\Obsolete\fallback.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\__about__.py" "Archive\Obsolete\__about__.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\_manylinux.py" "Archive\Obsolete\_manylinux.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\_structures.py" "Archive\Obsolete\_structures.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\markers.py" "Archive\Obsolete\markers.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\requirements.py" "Archive\Obsolete\requirements.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\specifiers.py" "Archive\Obsolete\specifiers.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\tags.py" "Archive\Obsolete\tags.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\pip\_vendor\packaging\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\platformdirs\android.py" "Archive\Obsolete\android.py"
move "venv\Lib\site-packages\pip\_vendor\platformdirs\api.py" "Archive\Obsolete\api.py"
move "venv\Lib\site-packages\pip\_vendor\platformdirs\macos.py" "Archive\Obsolete\macos.py"
move "venv\Lib\site-packages\pip\_vendor\platformdirs\unix.py" "Archive\Obsolete\unix.py"
move "venv\Lib\site-packages\pip\_vendor\platformdirs\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\pip\_vendor\platformdirs\windows.py" "Archive\Obsolete\windows.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\__main__.py" "Archive\Obsolete\__main__.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\console.py" "Archive\Obsolete\console.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\filter.py" "Archive\Obsolete\filter.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatter.py" "Archive\Obsolete\formatter.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\bbcode.py" "Archive\Obsolete\bbcode.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\groff.py" "Archive\Obsolete\groff.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\img.py" "Archive\Obsolete\img.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\irc.py" "Archive\Obsolete\irc.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\latex.py" "Archive\Obsolete\latex.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\other.py" "Archive\Obsolete\other.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\pangomarkup.py" "Archive\Obsolete\pangomarkup.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\rtf.py" "Archive\Obsolete\rtf.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\svg.py" "Archive\Obsolete\svg.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\terminal.py" "Archive\Obsolete\terminal.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\formatters\terminal256.py" "Archive\Obsolete\terminal256.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\lexer.py" "Archive\Obsolete\lexer.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\modeline.py" "Archive\Obsolete\modeline.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\plugin.py" "Archive\Obsolete\plugin.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\regexopt.py" "Archive\Obsolete\regexopt.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\scanner.py" "Archive\Obsolete\scanner.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\sphinxext.py" "Archive\Obsolete\sphinxext.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\style.py" "Archive\Obsolete\style.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\token.py" "Archive\Obsolete\token.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\unistring.py" "Archive\Obsolete\unistring.py"
move "venv\Lib\site-packages\pip\_vendor\pygments\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\actions.py" "Archive\Obsolete\actions.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\common.py" "Archive\Obsolete\common.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\diagram\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\helpers.py" "Archive\Obsolete\helpers.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\results.py" "Archive\Obsolete\results.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\testing.py" "Archive\Obsolete\testing.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\unicode.py" "Archive\Obsolete\unicode.py"
move "venv\Lib\site-packages\pip\_vendor\pyparsing\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\pip\_vendor\pyproject_hooks\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\pip\_vendor\requests\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\requests\__version__.py" "Archive\Obsolete\__version__.py"
move "venv\Lib\site-packages\pip\_vendor\requests\_internal_utils.py" "Archive\Obsolete\_internal_utils.py"
move "venv\Lib\site-packages\pip\_vendor\requests\adapters.py" "Archive\Obsolete\adapters.py"
move "venv\Lib\site-packages\pip\_vendor\requests\api.py" "Archive\Obsolete\api.py"
move "venv\Lib\site-packages\pip\_vendor\requests\auth.py" "Archive\Obsolete\auth.py"
move "venv\Lib\site-packages\pip\_vendor\requests\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\pip\_vendor\requests\cookies.py" "Archive\Obsolete\cookies.py"
move "venv\Lib\site-packages\pip\_vendor\requests\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\pip\_vendor\requests\hooks.py" "Archive\Obsolete\hooks.py"
move "venv\Lib\site-packages\pip\_vendor\requests\models.py" "Archive\Obsolete\models.py"
move "venv\Lib\site-packages\pip\_vendor\requests\packages.py" "Archive\Obsolete\packages.py"
move "venv\Lib\site-packages\pip\_vendor\requests\sessions.py" "Archive\Obsolete\sessions.py"
move "venv\Lib\site-packages\pip\_vendor\requests\status_codes.py" "Archive\Obsolete\status_codes.py"
move "venv\Lib\site-packages\pip\_vendor\requests\structures.py" "Archive\Obsolete\structures.py"
move "venv\Lib\site-packages\pip\_vendor\requests\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\pip\_vendor\resolvelib\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\resolvelib\compat\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\resolvelib\compat\collections_abc.py" "Archive\Obsolete\collections_abc.py"
move "venv\Lib\site-packages\pip\_vendor\resolvelib\providers.py" "Archive\Obsolete\providers.py"
move "venv\Lib\site-packages\pip\_vendor\resolvelib\reporters.py" "Archive\Obsolete\reporters.py"
move "venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers.py" "Archive\Obsolete\resolvers.py"
move "venv\Lib\site-packages\pip\_vendor\resolvelib\structs.py" "Archive\Obsolete\structs.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_cell_widths.py" "Archive\Obsolete\_cell_widths.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_emoji_codes.py" "Archive\Obsolete\_emoji_codes.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_emoji_replace.py" "Archive\Obsolete\_emoji_replace.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_export_format.py" "Archive\Obsolete\_export_format.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_extension.py" "Archive\Obsolete\_extension.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_fileno.py" "Archive\Obsolete\_fileno.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_inspect.py" "Archive\Obsolete\_inspect.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_loop.py" "Archive\Obsolete\_loop.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_null_file.py" "Archive\Obsolete\_null_file.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_palettes.py" "Archive\Obsolete\_palettes.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_pick.py" "Archive\Obsolete\_pick.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_spinners.py" "Archive\Obsolete\_spinners.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_stack.py" "Archive\Obsolete\_stack.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_timer.py" "Archive\Obsolete\_timer.py"
move "venv\Lib\site-packages\pip\_vendor\rich\_windows_renderer.py" "Archive\Obsolete\_windows_renderer.py"
move "venv\Lib\site-packages\pip\_vendor\rich\bar.py" "Archive\Obsolete\bar.py"
move "venv\Lib\site-packages\pip\_vendor\rich\color_triplet.py" "Archive\Obsolete\color_triplet.py"
move "venv\Lib\site-packages\pip\_vendor\rich\constrain.py" "Archive\Obsolete\constrain.py"
move "venv\Lib\site-packages\pip\_vendor\rich\containers.py" "Archive\Obsolete\containers.py"
move "venv\Lib\site-packages\pip\_vendor\rich\errors.py" "Archive\Obsolete\errors.py"
move "venv\Lib\site-packages\pip\_vendor\rich\file_proxy.py" "Archive\Obsolete\file_proxy.py"
move "venv\Lib\site-packages\pip\_vendor\rich\filesize.py" "Archive\Obsolete\filesize.py"
move "venv\Lib\site-packages\pip\_vendor\rich\jupyter.py" "Archive\Obsolete\jupyter.py"
move "venv\Lib\site-packages\pip\_vendor\rich\live_render.py" "Archive\Obsolete\live_render.py"
move "venv\Lib\site-packages\pip\_vendor\rich\measure.py" "Archive\Obsolete\measure.py"
move "venv\Lib\site-packages\pip\_vendor\rich\protocol.py" "Archive\Obsolete\protocol.py"
move "venv\Lib\site-packages\pip\_vendor\rich\region.py" "Archive\Obsolete\region.py"
move "venv\Lib\site-packages\pip\_vendor\rich\screen.py" "Archive\Obsolete\screen.py"
move "venv\Lib\site-packages\pip\_vendor\rich\style.py" "Archive\Obsolete\style.py"
move "venv\Lib\site-packages\pip\_vendor\rich\terminal_theme.py" "Archive\Obsolete\terminal_theme.py"
move "venv\Lib\site-packages\pip\_vendor\rich\themes.py" "Archive\Obsolete\themes.py"
move "venv\Lib\site-packages\pip\_vendor\six.py" "Archive\Obsolete\six.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\_asyncio.py" "Archive\Obsolete\_asyncio.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\_utils.py" "Archive\Obsolete\_utils.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\after.py" "Archive\Obsolete\after.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\before.py" "Archive\Obsolete\before.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\before_sleep.py" "Archive\Obsolete\before_sleep.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\nap.py" "Archive\Obsolete\nap.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\retry.py" "Archive\Obsolete\retry.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\stop.py" "Archive\Obsolete\stop.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\tornadoweb.py" "Archive\Obsolete\tornadoweb.py"
move "venv\Lib\site-packages\pip\_vendor\tenacity\wait.py" "Archive\Obsolete\wait.py"
move "venv\Lib\site-packages\pip\_vendor\tomli\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\tomli\_parser.py" "Archive\Obsolete\_parser.py"
move "venv\Lib\site-packages\pip\_vendor\tomli\_re.py" "Archive\Obsolete\_re.py"
move "venv\Lib\site-packages\pip\_vendor\tomli\_types.py" "Archive\Obsolete\_types.py"
move "venv\Lib\site-packages\pip\_vendor\typing_extensions.py" "Archive\Obsolete\typing_extensions.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\_collections.py" "Archive\Obsolete\_collections.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_appengine_environ.py" "Archive\Obsolete\_appengine_environ.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\bindings.py" "Archive\Obsolete\bindings.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\_securetransport\low_level.py" "Archive\Obsolete\low_level.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\appengine.py" "Archive\Obsolete\appengine.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\ntlmpool.py" "Archive\Obsolete\ntlmpool.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\pyopenssl.py" "Archive\Obsolete\pyopenssl.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\securetransport.py" "Archive\Obsolete\securetransport.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\contrib\socks.py" "Archive\Obsolete\socks.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\fields.py" "Archive\Obsolete\fields.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\filepost.py" "Archive\Obsolete\filepost.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\packages\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\packages\backports\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\packages\backports\makefile.py" "Archive\Obsolete\makefile.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\packages\six.py" "Archive\Obsolete\six.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\poolmanager.py" "Archive\Obsolete\poolmanager.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\request.py" "Archive\Obsolete\request.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\response.py" "Archive\Obsolete\response.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\proxy.py" "Archive\Obsolete\proxy.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\queue.py" "Archive\Obsolete\queue.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\request.py" "Archive\Obsolete\request.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\response.py" "Archive\Obsolete\response.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\retry.py" "Archive\Obsolete\retry.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\ssl_match_hostname.py" "Archive\Obsolete\ssl_match_hostname.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\ssltransport.py" "Archive\Obsolete\ssltransport.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\timeout.py" "Archive\Obsolete\timeout.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\url.py" "Archive\Obsolete\url.py"
move "venv\Lib\site-packages\pip\_vendor\urllib3\util\wait.py" "Archive\Obsolete\wait.py"
move "venv\Lib\site-packages\pip\_vendor\vendor.txt" "Archive\Obsolete\vendor.txt"
move "venv\Lib\site-packages\pip\_vendor\webencodings\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pip\_vendor\webencodings\labels.py" "Archive\Obsolete\labels.py"
move "venv\Lib\site-packages\pip\_vendor\webencodings\tests.py" "Archive\Obsolete\tests.py"
move "venv\Lib\site-packages\pip\_vendor\webencodings\x_user_defined.py" "Archive\Obsolete\x_user_defined.py"
move "venv\Lib\site-packages\pip\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\pkg_resources\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_adapters.py" "Archive\Obsolete\_adapters.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_common.py" "Archive\Obsolete\_common.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_itertools.py" "Archive\Obsolete\_itertools.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\_legacy.py" "Archive\Obsolete\_legacy.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\abc.py" "Archive\Obsolete\abc.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\readers.py" "Archive\Obsolete\readers.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\simple.py" "Archive\Obsolete\simple.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\jaraco\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\jaraco\context.py" "Archive\Obsolete\context.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\jaraco\functools.py" "Archive\Obsolete\functools.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\jaraco\text\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\more.py" "Archive\Obsolete\more.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\recipes.py" "Archive\Obsolete\recipes.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\__about__.py" "Archive\Obsolete\__about__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\_manylinux.py" "Archive\Obsolete\_manylinux.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\_structures.py" "Archive\Obsolete\_structures.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\markers.py" "Archive\Obsolete\markers.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\requirements.py" "Archive\Obsolete\requirements.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\specifiers.py" "Archive\Obsolete\specifiers.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\tags.py" "Archive\Obsolete\tags.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\packaging\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\actions.py" "Archive\Obsolete\actions.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\common.py" "Archive\Obsolete\common.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\diagram\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\helpers.py" "Archive\Obsolete\helpers.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\results.py" "Archive\Obsolete\results.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\testing.py" "Archive\Obsolete\testing.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\unicode.py" "Archive\Obsolete\unicode.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\pkg_resources\_vendor\zipp.py" "Archive\Obsolete\zipp.py"
move "venv\Lib\site-packages\pkg_resources\extern\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pluggy-1.6.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pluggy\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pluggy\_callers.py" "Archive\Obsolete\_callers.py"
move "venv\Lib\site-packages\pluggy\_hooks.py" "Archive\Obsolete\_hooks.py"
move "venv\Lib\site-packages\pluggy\_manager.py" "Archive\Obsolete\_manager.py"
move "venv\Lib\site-packages\pluggy\_result.py" "Archive\Obsolete\_result.py"
move "venv\Lib\site-packages\pluggy\_tracing.py" "Archive\Obsolete\_tracing.py"
move "venv\Lib\site-packages\pluggy\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\pluggy\_warnings.py" "Archive\Obsolete\_warnings.py"
move "venv\Lib\site-packages\pluggy\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\licenses\NOTICE" "Archive\Obsolete\NOTICE"
move "venv\Lib\site-packages\propcache-0.3.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\propcache\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\propcache\_helpers.py" "Archive\Obsolete\_helpers.py"
move "venv\Lib\site-packages\propcache\_helpers_c.cp311-win_amd64.pyd" "Archive\Obsolete\_helpers_c.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\propcache\_helpers_c.pyx" "Archive\Obsolete\_helpers_c.pyx"
move "venv\Lib\site-packages\propcache\_helpers_py.py" "Archive\Obsolete\_helpers_py.py"
move "venv\Lib\site-packages\propcache\api.py" "Archive\Obsolete\api.py"
move "venv\Lib\site-packages\propcache\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\psutil-5.9.7.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\psutil\_common.py" "Archive\Obsolete\_common.py"
move "venv\Lib\site-packages\psutil\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\psutil\_psaix.py" "Archive\Obsolete\_psaix.py"
move "venv\Lib\site-packages\psutil\_psbsd.py" "Archive\Obsolete\_psbsd.py"
move "venv\Lib\site-packages\psutil\_pslinux.py" "Archive\Obsolete\_pslinux.py"
move "venv\Lib\site-packages\psutil\_psosx.py" "Archive\Obsolete\_psosx.py"
move "venv\Lib\site-packages\psutil\_psposix.py" "Archive\Obsolete\_psposix.py"
move "venv\Lib\site-packages\psutil\_pssunos.py" "Archive\Obsolete\_pssunos.py"
move "venv\Lib\site-packages\psutil\_psutil_windows.pyd" "Archive\Obsolete\_psutil_windows.pyd"
move "venv\Lib\site-packages\psutil\_pswindows.py" "Archive\Obsolete\_pswindows.py"
move "venv\Lib\site-packages\psutil\tests\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\psutil\tests\__main__.py" "Archive\Obsolete\__main__.py"
move "venv\Lib\site-packages\psutil\tests\test_aix.py" "Archive\Obsolete\test_aix.py"
move "venv\Lib\site-packages\psutil\tests\test_bsd.py" "Archive\Obsolete\test_bsd.py"
move "venv\Lib\site-packages\psutil\tests\test_connections.py" "Archive\Obsolete\test_connections.py"
move "venv\Lib\site-packages\psutil\tests\test_contracts.py" "Archive\Obsolete\test_contracts.py"
move "venv\Lib\site-packages\psutil\tests\test_linux.py" "Archive\Obsolete\test_linux.py"
move "venv\Lib\site-packages\psutil\tests\test_memleaks.py" "Archive\Obsolete\test_memleaks.py"
move "venv\Lib\site-packages\psutil\tests\test_osx.py" "Archive\Obsolete\test_osx.py"
move "venv\Lib\site-packages\psutil\tests\test_posix.py" "Archive\Obsolete\test_posix.py"
move "venv\Lib\site-packages\psutil\tests\test_process.py" "Archive\Obsolete\test_process.py"
move "venv\Lib\site-packages\psutil\tests\test_sunos.py" "Archive\Obsolete\test_sunos.py"
move "venv\Lib\site-packages\psutil\tests\test_system.py" "Archive\Obsolete\test_system.py"
move "venv\Lib\site-packages\psutil\tests\test_testutils.py" "Archive\Obsolete\test_testutils.py"
move "venv\Lib\site-packages\psutil\tests\test_unicode.py" "Archive\Obsolete\test_unicode.py"
move "venv\Lib\site-packages\psutil\tests\test_windows.py" "Archive\Obsolete\test_windows.py"
move "venv\Lib\site-packages\py.py" "Archive\Obsolete\py.py"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\LICENSE.rst" "Archive\Obsolete\LICENSE.rst"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pyasn1-0.6.1.dist-info\zip-safe" "Archive\Obsolete\zip-safe"
move "venv\Lib\site-packages\pyasn1\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\ber\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\ber\decoder.py" "Archive\Obsolete\decoder.py"
move "venv\Lib\site-packages\pyasn1\codec\ber\encoder.py" "Archive\Obsolete\encoder.py"
move "venv\Lib\site-packages\pyasn1\codec\ber\eoo.py" "Archive\Obsolete\eoo.py"
move "venv\Lib\site-packages\pyasn1\codec\cer\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\cer\decoder.py" "Archive\Obsolete\decoder.py"
move "venv\Lib\site-packages\pyasn1\codec\cer\encoder.py" "Archive\Obsolete\encoder.py"
move "venv\Lib\site-packages\pyasn1\codec\der\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\der\decoder.py" "Archive\Obsolete\decoder.py"
move "venv\Lib\site-packages\pyasn1\codec\der\encoder.py" "Archive\Obsolete\encoder.py"
move "venv\Lib\site-packages\pyasn1\codec\native\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pyasn1\codec\native\decoder.py" "Archive\Obsolete\decoder.py"
move "venv\Lib\site-packages\pyasn1\codec\native\encoder.py" "Archive\Obsolete\encoder.py"
move "venv\Lib\site-packages\pyasn1\codec\streaming.py" "Archive\Obsolete\streaming.py"
move "venv\Lib\site-packages\pyasn1\compat\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pyasn1\compat\integer.py" "Archive\Obsolete\integer.py"
move "venv\Lib\site-packages\pyasn1\debug.py" "Archive\Obsolete\debug.py"
move "venv\Lib\site-packages\pyasn1\error.py" "Archive\Obsolete\error.py"
move "venv\Lib\site-packages\pyasn1\type\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pyasn1\type\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\pyasn1\type\char.py" "Archive\Obsolete\char.py"
move "venv\Lib\site-packages\pyasn1\type\constraint.py" "Archive\Obsolete\constraint.py"
move "venv\Lib\site-packages\pyasn1\type\error.py" "Archive\Obsolete\error.py"
move "venv\Lib\site-packages\pyasn1\type\namedtype.py" "Archive\Obsolete\namedtype.py"
move "venv\Lib\site-packages\pyasn1\type\namedval.py" "Archive\Obsolete\namedval.py"
move "venv\Lib\site-packages\pyasn1\type\opentype.py" "Archive\Obsolete\opentype.py"
move "venv\Lib\site-packages\pyasn1\type\tag.py" "Archive\Obsolete\tag.py"
move "venv\Lib\site-packages\pyasn1\type\tagmap.py" "Archive\Obsolete\tagmap.py"
move "venv\Lib\site-packages\pyasn1\type\univ.py" "Archive\Obsolete\univ.py"
move "venv\Lib\site-packages\pyasn1\type\useful.py" "Archive\Obsolete\useful.py"
move "venv\Lib\site-packages\pycares-4.8.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pycares-4.8.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pycares-4.8.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pycares-4.8.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pycares-4.8.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pycares-4.8.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pycares\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pycares\__main__.py" "Archive\Obsolete\__main__.py"
move "venv\Lib\site-packages\pycares\_cares.pyd" "Archive\Obsolete\_cares.pyd"
move "venv\Lib\site-packages\pycares\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\pycares\errno.py" "Archive\Obsolete\errno.py"
move "venv\Lib\site-packages\pycares\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\pycares\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\pycparser-2.22.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pycparser-2.22.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pycparser-2.22.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pycparser-2.22.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pycparser-2.22.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pycparser-2.22.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pycparser\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pycparser\_ast_gen.py" "Archive\Obsolete\_ast_gen.py"
move "venv\Lib\site-packages\pycparser\_c_ast.cfg" "Archive\Obsolete\_c_ast.cfg"
move "venv\Lib\site-packages\pycparser\ast_transforms.py" "Archive\Obsolete\ast_transforms.py"
move "venv\Lib\site-packages\pycparser\c_ast.py" "Archive\Obsolete\c_ast.py"
move "venv\Lib\site-packages\pycparser\c_generator.py" "Archive\Obsolete\c_generator.py"
move "venv\Lib\site-packages\pycparser\c_lexer.py" "Archive\Obsolete\c_lexer.py"
move "venv\Lib\site-packages\pycparser\c_parser.py" "Archive\Obsolete\c_parser.py"
move "venv\Lib\site-packages\pycparser\lextab.py" "Archive\Obsolete\lextab.py"
move "venv\Lib\site-packages\pycparser\ply\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pycparser\ply\cpp.py" "Archive\Obsolete\cpp.py"
move "venv\Lib\site-packages\pycparser\ply\ctokens.py" "Archive\Obsolete\ctokens.py"
move "venv\Lib\site-packages\pycparser\plyparser.py" "Archive\Obsolete\plyparser.py"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pydantic-2.11.5.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pydantic\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pydantic\_internal\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pydantic\_internal\_config.py" "Archive\Obsolete\_config.py"
move "venv\Lib\site-packages\pydantic\_internal\_core_metadata.py" "Archive\Obsolete\_core_metadata.py"
move "venv\Lib\site-packages\pydantic\_internal\_core_utils.py" "Archive\Obsolete\_core_utils.py"
move "venv\Lib\site-packages\pydantic\_internal\_dataclasses.py" "Archive\Obsolete\_dataclasses.py"
move "venv\Lib\site-packages\pydantic\_internal\_decorators.py" "Archive\Obsolete\_decorators.py"
move "venv\Lib\site-packages\pydantic\_internal\_decorators_v1.py" "Archive\Obsolete\_decorators_v1.py"
move "venv\Lib\site-packages\pydantic\_internal\_discriminated_union.py" "Archive\Obsolete\_discriminated_union.py"
move "venv\Lib\site-packages\pydantic\_internal\_docs_extraction.py" "Archive\Obsolete\_docs_extraction.py"
move "venv\Lib\site-packages\pydantic\_internal\_fields.py" "Archive\Obsolete\_fields.py"
move "venv\Lib\site-packages\pydantic\_internal\_forward_ref.py" "Archive\Obsolete\_forward_ref.py"
move "venv\Lib\site-packages\pydantic\_internal\_generate_schema.py" "Archive\Obsolete\_generate_schema.py"
move "venv\Lib\site-packages\pydantic\_internal\_generics.py" "Archive\Obsolete\_generics.py"
move "venv\Lib\site-packages\pydantic\_internal\_git.py" "Archive\Obsolete\_git.py"
move "venv\Lib\site-packages\pydantic\_internal\_import_utils.py" "Archive\Obsolete\_import_utils.py"
move "venv\Lib\site-packages\pydantic\_internal\_internal_dataclass.py" "Archive\Obsolete\_internal_dataclass.py"
move "venv\Lib\site-packages\pydantic\_internal\_known_annotated_metadata.py" "Archive\Obsolete\_known_annotated_metadata.py"
move "venv\Lib\site-packages\pydantic\_internal\_mock_val_ser.py" "Archive\Obsolete\_mock_val_ser.py"
move "venv\Lib\site-packages\pydantic\_internal\_model_construction.py" "Archive\Obsolete\_model_construction.py"
move "venv\Lib\site-packages\pydantic\_internal\_namespace_utils.py" "Archive\Obsolete\_namespace_utils.py"
move "venv\Lib\site-packages\pydantic\_internal\_repr.py" "Archive\Obsolete\_repr.py"
move "venv\Lib\site-packages\pydantic\_internal\_schema_gather.py" "Archive\Obsolete\_schema_gather.py"
move "venv\Lib\site-packages\pydantic\_internal\_schema_generation_shared.py" "Archive\Obsolete\_schema_generation_shared.py"
move "venv\Lib\site-packages\pydantic\_internal\_serializers.py" "Archive\Obsolete\_serializers.py"
move "venv\Lib\site-packages\pydantic\_internal\_signature.py" "Archive\Obsolete\_signature.py"
move "venv\Lib\site-packages\pydantic\_internal\_typing_extra.py" "Archive\Obsolete\_typing_extra.py"
move "venv\Lib\site-packages\pydantic\_internal\_utils.py" "Archive\Obsolete\_utils.py"
move "venv\Lib\site-packages\pydantic\_internal\_validate_call.py" "Archive\Obsolete\_validate_call.py"
move "venv\Lib\site-packages\pydantic\_internal\_validators.py" "Archive\Obsolete\_validators.py"
move "venv\Lib\site-packages\pydantic\_migration.py" "Archive\Obsolete\_migration.py"
move "venv\Lib\site-packages\pydantic\alias_generators.py" "Archive\Obsolete\alias_generators.py"
move "venv\Lib\site-packages\pydantic\aliases.py" "Archive\Obsolete\aliases.py"
move "venv\Lib\site-packages\pydantic\annotated_handlers.py" "Archive\Obsolete\annotated_handlers.py"
move "venv\Lib\site-packages\pydantic\class_validators.py" "Archive\Obsolete\class_validators.py"
move "venv\Lib\site-packages\pydantic\color.py" "Archive\Obsolete\color.py"
move "venv\Lib\site-packages\pydantic\config.py" "Archive\Obsolete\config.py"
move "venv\Lib\site-packages\pydantic\dataclasses.py" "Archive\Obsolete\dataclasses.py"
move "venv\Lib\site-packages\pydantic\datetime_parse.py" "Archive\Obsolete\datetime_parse.py"
move "venv\Lib\site-packages\pydantic\decorator.py" "Archive\Obsolete\decorator.py"
move "venv\Lib\site-packages\pydantic\deprecated\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pydantic\deprecated\class_validators.py" "Archive\Obsolete\class_validators.py"
move "venv\Lib\site-packages\pydantic\deprecated\config.py" "Archive\Obsolete\config.py"
move "venv\Lib\site-packages\pydantic\deprecated\copy_internals.py" "Archive\Obsolete\copy_internals.py"
move "venv\Lib\site-packages\pydantic\deprecated\decorator.py" "Archive\Obsolete\decorator.py"
move "venv\Lib\site-packages\pydantic\deprecated\json.py" "Archive\Obsolete\json.py"
move "venv\Lib\site-packages\pydantic\deprecated\tools.py" "Archive\Obsolete\tools.py"
move "venv\Lib\site-packages\pydantic\env_settings.py" "Archive\Obsolete\env_settings.py"
move "venv\Lib\site-packages\pydantic\error_wrappers.py" "Archive\Obsolete\error_wrappers.py"
move "venv\Lib\site-packages\pydantic\errors.py" "Archive\Obsolete\errors.py"
move "venv\Lib\site-packages\pydantic\experimental\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pydantic\experimental\arguments_schema.py" "Archive\Obsolete\arguments_schema.py"
move "venv\Lib\site-packages\pydantic\experimental\pipeline.py" "Archive\Obsolete\pipeline.py"
move "venv\Lib\site-packages\pydantic\fields.py" "Archive\Obsolete\fields.py"
move "venv\Lib\site-packages\pydantic\functional_serializers.py" "Archive\Obsolete\functional_serializers.py"
move "venv\Lib\site-packages\pydantic\functional_validators.py" "Archive\Obsolete\functional_validators.py"
move "venv\Lib\site-packages\pydantic\generics.py" "Archive\Obsolete\generics.py"
move "venv\Lib\site-packages\pydantic\json.py" "Archive\Obsolete\json.py"
move "venv\Lib\site-packages\pydantic\json_schema.py" "Archive\Obsolete\json_schema.py"
move "venv\Lib\site-packages\pydantic\main.py" "Archive\Obsolete\main.py"
move "venv\Lib\site-packages\pydantic\mypy.py" "Archive\Obsolete\mypy.py"
move "venv\Lib\site-packages\pydantic\networks.py" "Archive\Obsolete\networks.py"
move "venv\Lib\site-packages\pydantic\parse.py" "Archive\Obsolete\parse.py"
move "venv\Lib\site-packages\pydantic\plugin\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pydantic\plugin\_loader.py" "Archive\Obsolete\_loader.py"
move "venv\Lib\site-packages\pydantic\plugin\_schema_validator.py" "Archive\Obsolete\_schema_validator.py"
move "venv\Lib\site-packages\pydantic\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\pydantic\root_model.py" "Archive\Obsolete\root_model.py"
move "venv\Lib\site-packages\pydantic\schema.py" "Archive\Obsolete\schema.py"
move "venv\Lib\site-packages\pydantic\tools.py" "Archive\Obsolete\tools.py"
move "venv\Lib\site-packages\pydantic\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\pydantic\typing.py" "Archive\Obsolete\typing.py"
move "venv\Lib\site-packages\pydantic\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\pydantic\v1\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pydantic\v1\_hypothesis_plugin.py" "Archive\Obsolete\_hypothesis_plugin.py"
move "venv\Lib\site-packages\pydantic\v1\annotated_types.py" "Archive\Obsolete\annotated_types.py"
move "venv\Lib\site-packages\pydantic\v1\class_validators.py" "Archive\Obsolete\class_validators.py"
move "venv\Lib\site-packages\pydantic\v1\color.py" "Archive\Obsolete\color.py"
move "venv\Lib\site-packages\pydantic\v1\config.py" "Archive\Obsolete\config.py"
move "venv\Lib\site-packages\pydantic\v1\dataclasses.py" "Archive\Obsolete\dataclasses.py"
move "venv\Lib\site-packages\pydantic\v1\datetime_parse.py" "Archive\Obsolete\datetime_parse.py"
move "venv\Lib\site-packages\pydantic\v1\decorator.py" "Archive\Obsolete\decorator.py"
move "venv\Lib\site-packages\pydantic\v1\env_settings.py" "Archive\Obsolete\env_settings.py"
move "venv\Lib\site-packages\pydantic\v1\error_wrappers.py" "Archive\Obsolete\error_wrappers.py"
move "venv\Lib\site-packages\pydantic\v1\errors.py" "Archive\Obsolete\errors.py"
move "venv\Lib\site-packages\pydantic\v1\fields.py" "Archive\Obsolete\fields.py"
move "venv\Lib\site-packages\pydantic\v1\generics.py" "Archive\Obsolete\generics.py"
move "venv\Lib\site-packages\pydantic\v1\json.py" "Archive\Obsolete\json.py"
move "venv\Lib\site-packages\pydantic\v1\main.py" "Archive\Obsolete\main.py"
move "venv\Lib\site-packages\pydantic\v1\mypy.py" "Archive\Obsolete\mypy.py"
move "venv\Lib\site-packages\pydantic\v1\networks.py" "Archive\Obsolete\networks.py"
move "venv\Lib\site-packages\pydantic\v1\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\pydantic\v1\schema.py" "Archive\Obsolete\schema.py"
move "venv\Lib\site-packages\pydantic\v1\tools.py" "Archive\Obsolete\tools.py"
move "venv\Lib\site-packages\pydantic\v1\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\pydantic\v1\typing.py" "Archive\Obsolete\typing.py"
move "venv\Lib\site-packages\pydantic\v1\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\pydantic\v1\validators.py" "Archive\Obsolete\validators.py"
move "venv\Lib\site-packages\pydantic\v1\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\pydantic\validate_call_decorator.py" "Archive\Obsolete\validate_call_decorator.py"
move "venv\Lib\site-packages\pydantic\validators.py" "Archive\Obsolete\validators.py"
move "venv\Lib\site-packages\pydantic\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\pydantic\warnings.py" "Archive\Obsolete\warnings.py"
move "venv\Lib\site-packages\pydantic_core-2.33.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pydantic_core-2.33.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pydantic_core-2.33.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pydantic_core-2.33.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pydantic_core-2.33.2.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pydantic_core\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pydantic_core\_pydantic_core.cp311-win_amd64.pyd" "Archive\Obsolete\_pydantic_core.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\pydantic_core\_pydantic_core.pyi" "Archive\Obsolete\_pydantic_core.pyi"
move "venv\Lib\site-packages\pydantic_core\core_schema.py" "Archive\Obsolete\core_schema.py"
move "venv\Lib\site-packages\pydantic_core\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\licenses\AUTHORS" "Archive\Obsolete\AUTHORS"
move "venv\Lib\site-packages\pygments-2.19.1.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pygments\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pygments\__main__.py" "Archive\Obsolete\__main__.py"
move "venv\Lib\site-packages\pygments\console.py" "Archive\Obsolete\console.py"
move "venv\Lib\site-packages\pygments\filter.py" "Archive\Obsolete\filter.py"
move "venv\Lib\site-packages\pygments\filters\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pygments\formatter.py" "Archive\Obsolete\formatter.py"
move "venv\Lib\site-packages\pygments\formatters\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pygments\formatters\bbcode.py" "Archive\Obsolete\bbcode.py"
move "venv\Lib\site-packages\pygments\formatters\groff.py" "Archive\Obsolete\groff.py"
move "venv\Lib\site-packages\pygments\formatters\img.py" "Archive\Obsolete\img.py"
move "venv\Lib\site-packages\pygments\formatters\irc.py" "Archive\Obsolete\irc.py"
move "venv\Lib\site-packages\pygments\formatters\latex.py" "Archive\Obsolete\latex.py"
move "venv\Lib\site-packages\pygments\formatters\other.py" "Archive\Obsolete\other.py"
move "venv\Lib\site-packages\pygments\formatters\pangomarkup.py" "Archive\Obsolete\pangomarkup.py"
move "venv\Lib\site-packages\pygments\formatters\rtf.py" "Archive\Obsolete\rtf.py"
move "venv\Lib\site-packages\pygments\formatters\svg.py" "Archive\Obsolete\svg.py"
move "venv\Lib\site-packages\pygments\formatters\terminal.py" "Archive\Obsolete\terminal.py"
move "venv\Lib\site-packages\pygments\formatters\terminal256.py" "Archive\Obsolete\terminal256.py"
move "venv\Lib\site-packages\pygments\lexer.py" "Archive\Obsolete\lexer.py"
move "venv\Lib\site-packages\pygments\lexers\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pygments\lexers\_ada_builtins.py" "Archive\Obsolete\_ada_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_asy_builtins.py" "Archive\Obsolete\_asy_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_cl_builtins.py" "Archive\Obsolete\_cl_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_cocoa_builtins.py" "Archive\Obsolete\_cocoa_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_csound_builtins.py" "Archive\Obsolete\_csound_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_css_builtins.py" "Archive\Obsolete\_css_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_googlesql_builtins.py" "Archive\Obsolete\_googlesql_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_julia_builtins.py" "Archive\Obsolete\_julia_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_lasso_builtins.py" "Archive\Obsolete\_lasso_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_lilypond_builtins.py" "Archive\Obsolete\_lilypond_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_lua_builtins.py" "Archive\Obsolete\_lua_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_luau_builtins.py" "Archive\Obsolete\_luau_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_mql_builtins.py" "Archive\Obsolete\_mql_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_mysql_builtins.py" "Archive\Obsolete\_mysql_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_openedge_builtins.py" "Archive\Obsolete\_openedge_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_postgres_builtins.py" "Archive\Obsolete\_postgres_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_qlik_builtins.py" "Archive\Obsolete\_qlik_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_scheme_builtins.py" "Archive\Obsolete\_scheme_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_scilab_builtins.py" "Archive\Obsolete\_scilab_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_stan_builtins.py" "Archive\Obsolete\_stan_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_stata_builtins.py" "Archive\Obsolete\_stata_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_tsql_builtins.py" "Archive\Obsolete\_tsql_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_usd_builtins.py" "Archive\Obsolete\_usd_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_vbscript_builtins.py" "Archive\Obsolete\_vbscript_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\_vim_builtins.py" "Archive\Obsolete\_vim_builtins.py"
move "venv\Lib\site-packages\pygments\lexers\ada.py" "Archive\Obsolete\ada.py"
move "venv\Lib\site-packages\pygments\lexers\agile.py" "Archive\Obsolete\agile.py"
move "venv\Lib\site-packages\pygments\lexers\algebra.py" "Archive\Obsolete\algebra.py"
move "venv\Lib\site-packages\pygments\lexers\ambient.py" "Archive\Obsolete\ambient.py"
move "venv\Lib\site-packages\pygments\lexers\amdgpu.py" "Archive\Obsolete\amdgpu.py"
move "venv\Lib\site-packages\pygments\lexers\ampl.py" "Archive\Obsolete\ampl.py"
move "venv\Lib\site-packages\pygments\lexers\apdlexer.py" "Archive\Obsolete\apdlexer.py"
move "venv\Lib\site-packages\pygments\lexers\apl.py" "Archive\Obsolete\apl.py"
move "venv\Lib\site-packages\pygments\lexers\arrow.py" "Archive\Obsolete\arrow.py"
move "venv\Lib\site-packages\pygments\lexers\arturo.py" "Archive\Obsolete\arturo.py"
move "venv\Lib\site-packages\pygments\lexers\asc.py" "Archive\Obsolete\asc.py"
move "venv\Lib\site-packages\pygments\lexers\asn1.py" "Archive\Obsolete\asn1.py"
move "venv\Lib\site-packages\pygments\lexers\automation.py" "Archive\Obsolete\automation.py"
move "venv\Lib\site-packages\pygments\lexers\bare.py" "Archive\Obsolete\bare.py"
move "venv\Lib\site-packages\pygments\lexers\bdd.py" "Archive\Obsolete\bdd.py"
move "venv\Lib\site-packages\pygments\lexers\berry.py" "Archive\Obsolete\berry.py"
move "venv\Lib\site-packages\pygments\lexers\bibtex.py" "Archive\Obsolete\bibtex.py"
move "venv\Lib\site-packages\pygments\lexers\blueprint.py" "Archive\Obsolete\blueprint.py"
move "venv\Lib\site-packages\pygments\lexers\boa.py" "Archive\Obsolete\boa.py"
move "venv\Lib\site-packages\pygments\lexers\business.py" "Archive\Obsolete\business.py"
move "venv\Lib\site-packages\pygments\lexers\c_cpp.py" "Archive\Obsolete\c_cpp.py"
move "venv\Lib\site-packages\pygments\lexers\capnproto.py" "Archive\Obsolete\capnproto.py"
move "venv\Lib\site-packages\pygments\lexers\carbon.py" "Archive\Obsolete\carbon.py"
move "venv\Lib\site-packages\pygments\lexers\cddl.py" "Archive\Obsolete\cddl.py"
move "venv\Lib\site-packages\pygments\lexers\chapel.py" "Archive\Obsolete\chapel.py"
move "venv\Lib\site-packages\pygments\lexers\clean.py" "Archive\Obsolete\clean.py"
move "venv\Lib\site-packages\pygments\lexers\codeql.py" "Archive\Obsolete\codeql.py"
move "venv\Lib\site-packages\pygments\lexers\comal.py" "Archive\Obsolete\comal.py"
move "venv\Lib\site-packages\pygments\lexers\compiled.py" "Archive\Obsolete\compiled.py"
move "venv\Lib\site-packages\pygments\lexers\console.py" "Archive\Obsolete\console.py"
move "venv\Lib\site-packages\pygments\lexers\cplint.py" "Archive\Obsolete\cplint.py"
move "venv\Lib\site-packages\pygments\lexers\crystal.py" "Archive\Obsolete\crystal.py"
move "venv\Lib\site-packages\pygments\lexers\csound.py" "Archive\Obsolete\csound.py"
move "venv\Lib\site-packages\pygments\lexers\d.py" "Archive\Obsolete\d.py"
move "venv\Lib\site-packages\pygments\lexers\dalvik.py" "Archive\Obsolete\dalvik.py"
move "venv\Lib\site-packages\pygments\lexers\dax.py" "Archive\Obsolete\dax.py"
move "venv\Lib\site-packages\pygments\lexers\devicetree.py" "Archive\Obsolete\devicetree.py"
move "venv\Lib\site-packages\pygments\lexers\diff.py" "Archive\Obsolete\diff.py"
move "venv\Lib\site-packages\pygments\lexers\dns.py" "Archive\Obsolete\dns.py"
move "venv\Lib\site-packages\pygments\lexers\dotnet.py" "Archive\Obsolete\dotnet.py"
move "venv\Lib\site-packages\pygments\lexers\dsls.py" "Archive\Obsolete\dsls.py"
move "venv\Lib\site-packages\pygments\lexers\dylan.py" "Archive\Obsolete\dylan.py"
move "venv\Lib\site-packages\pygments\lexers\ecl.py" "Archive\Obsolete\ecl.py"
move "venv\Lib\site-packages\pygments\lexers\eiffel.py" "Archive\Obsolete\eiffel.py"
move "venv\Lib\site-packages\pygments\lexers\elm.py" "Archive\Obsolete\elm.py"
move "venv\Lib\site-packages\pygments\lexers\elpi.py" "Archive\Obsolete\elpi.py"
move "venv\Lib\site-packages\pygments\lexers\email.py" "Archive\Obsolete\email.py"
move "venv\Lib\site-packages\pygments\lexers\erlang.py" "Archive\Obsolete\erlang.py"
move "venv\Lib\site-packages\pygments\lexers\esoteric.py" "Archive\Obsolete\esoteric.py"
move "venv\Lib\site-packages\pygments\lexers\ezhil.py" "Archive\Obsolete\ezhil.py"
move "venv\Lib\site-packages\pygments\lexers\factor.py" "Archive\Obsolete\factor.py"
move "venv\Lib\site-packages\pygments\lexers\fantom.py" "Archive\Obsolete\fantom.py"
move "venv\Lib\site-packages\pygments\lexers\felix.py" "Archive\Obsolete\felix.py"
move "venv\Lib\site-packages\pygments\lexers\fift.py" "Archive\Obsolete\fift.py"
move "venv\Lib\site-packages\pygments\lexers\floscript.py" "Archive\Obsolete\floscript.py"
move "venv\Lib\site-packages\pygments\lexers\forth.py" "Archive\Obsolete\forth.py"
move "venv\Lib\site-packages\pygments\lexers\fortran.py" "Archive\Obsolete\fortran.py"
move "venv\Lib\site-packages\pygments\lexers\foxpro.py" "Archive\Obsolete\foxpro.py"
move "venv\Lib\site-packages\pygments\lexers\freefem.py" "Archive\Obsolete\freefem.py"
move "venv\Lib\site-packages\pygments\lexers\func.py" "Archive\Obsolete\func.py"
move "venv\Lib\site-packages\pygments\lexers\functional.py" "Archive\Obsolete\functional.py"
move "venv\Lib\site-packages\pygments\lexers\futhark.py" "Archive\Obsolete\futhark.py"
move "venv\Lib\site-packages\pygments\lexers\gcodelexer.py" "Archive\Obsolete\gcodelexer.py"
move "venv\Lib\site-packages\pygments\lexers\gdscript.py" "Archive\Obsolete\gdscript.py"
move "venv\Lib\site-packages\pygments\lexers\gleam.py" "Archive\Obsolete\gleam.py"
move "venv\Lib\site-packages\pygments\lexers\go.py" "Archive\Obsolete\go.py"
move "venv\Lib\site-packages\pygments\lexers\grammar_notation.py" "Archive\Obsolete\grammar_notation.py"
move "venv\Lib\site-packages\pygments\lexers\graph.py" "Archive\Obsolete\graph.py"
move "venv\Lib\site-packages\pygments\lexers\graphics.py" "Archive\Obsolete\graphics.py"
move "venv\Lib\site-packages\pygments\lexers\graphql.py" "Archive\Obsolete\graphql.py"
move "venv\Lib\site-packages\pygments\lexers\gsql.py" "Archive\Obsolete\gsql.py"
move "venv\Lib\site-packages\pygments\lexers\hare.py" "Archive\Obsolete\hare.py"
move "venv\Lib\site-packages\pygments\lexers\hdl.py" "Archive\Obsolete\hdl.py"
move "venv\Lib\site-packages\pygments\lexers\hexdump.py" "Archive\Obsolete\hexdump.py"
move "venv\Lib\site-packages\pygments\lexers\igor.py" "Archive\Obsolete\igor.py"
move "venv\Lib\site-packages\pygments\lexers\int_fiction.py" "Archive\Obsolete\int_fiction.py"
move "venv\Lib\site-packages\pygments\lexers\iolang.py" "Archive\Obsolete\iolang.py"
move "venv\Lib\site-packages\pygments\lexers\j.py" "Archive\Obsolete\j.py"
move "venv\Lib\site-packages\pygments\lexers\jmespath.py" "Archive\Obsolete\jmespath.py"
move "venv\Lib\site-packages\pygments\lexers\jslt.py" "Archive\Obsolete\jslt.py"
move "venv\Lib\site-packages\pygments\lexers\json5.py" "Archive\Obsolete\json5.py"
move "venv\Lib\site-packages\pygments\lexers\jsonnet.py" "Archive\Obsolete\jsonnet.py"
move "venv\Lib\site-packages\pygments\lexers\julia.py" "Archive\Obsolete\julia.py"
move "venv\Lib\site-packages\pygments\lexers\jvm.py" "Archive\Obsolete\jvm.py"
move "venv\Lib\site-packages\pygments\lexers\kuin.py" "Archive\Obsolete\kuin.py"
move "venv\Lib\site-packages\pygments\lexers\kusto.py" "Archive\Obsolete\kusto.py"
move "venv\Lib\site-packages\pygments\lexers\ldap.py" "Archive\Obsolete\ldap.py"
move "venv\Lib\site-packages\pygments\lexers\lean.py" "Archive\Obsolete\lean.py"
move "venv\Lib\site-packages\pygments\lexers\lilypond.py" "Archive\Obsolete\lilypond.py"
move "venv\Lib\site-packages\pygments\lexers\macaulay2.py" "Archive\Obsolete\macaulay2.py"
move "venv\Lib\site-packages\pygments\lexers\make.py" "Archive\Obsolete\make.py"
move "venv\Lib\site-packages\pygments\lexers\maple.py" "Archive\Obsolete\maple.py"
move "venv\Lib\site-packages\pygments\lexers\math.py" "Archive\Obsolete\math.py"
move "venv\Lib\site-packages\pygments\lexers\maxima.py" "Archive\Obsolete\maxima.py"
move "venv\Lib\site-packages\pygments\lexers\meson.py" "Archive\Obsolete\meson.py"
move "venv\Lib\site-packages\pygments\lexers\mime.py" "Archive\Obsolete\mime.py"
move "venv\Lib\site-packages\pygments\lexers\minecraft.py" "Archive\Obsolete\minecraft.py"
move "venv\Lib\site-packages\pygments\lexers\mips.py" "Archive\Obsolete\mips.py"
move "venv\Lib\site-packages\pygments\lexers\ml.py" "Archive\Obsolete\ml.py"
move "venv\Lib\site-packages\pygments\lexers\modeling.py" "Archive\Obsolete\modeling.py"
move "venv\Lib\site-packages\pygments\lexers\modula2.py" "Archive\Obsolete\modula2.py"
move "venv\Lib\site-packages\pygments\lexers\mojo.py" "Archive\Obsolete\mojo.py"
move "venv\Lib\site-packages\pygments\lexers\monte.py" "Archive\Obsolete\monte.py"
move "venv\Lib\site-packages\pygments\lexers\ncl.py" "Archive\Obsolete\ncl.py"
move "venv\Lib\site-packages\pygments\lexers\nimrod.py" "Archive\Obsolete\nimrod.py"
move "venv\Lib\site-packages\pygments\lexers\nit.py" "Archive\Obsolete\nit.py"
move "venv\Lib\site-packages\pygments\lexers\nix.py" "Archive\Obsolete\nix.py"
move "venv\Lib\site-packages\pygments\lexers\numbair.py" "Archive\Obsolete\numbair.py"
move "venv\Lib\site-packages\pygments\lexers\oberon.py" "Archive\Obsolete\oberon.py"
move "venv\Lib\site-packages\pygments\lexers\ooc.py" "Archive\Obsolete\ooc.py"
move "venv\Lib\site-packages\pygments\lexers\openscad.py" "Archive\Obsolete\openscad.py"
move "venv\Lib\site-packages\pygments\lexers\other.py" "Archive\Obsolete\other.py"
move "venv\Lib\site-packages\pygments\lexers\parasail.py" "Archive\Obsolete\parasail.py"
move "venv\Lib\site-packages\pygments\lexers\parsers.py" "Archive\Obsolete\parsers.py"
move "venv\Lib\site-packages\pygments\lexers\pascal.py" "Archive\Obsolete\pascal.py"
move "venv\Lib\site-packages\pygments\lexers\pddl.py" "Archive\Obsolete\pddl.py"
move "venv\Lib\site-packages\pygments\lexers\perl.py" "Archive\Obsolete\perl.py"
move "venv\Lib\site-packages\pygments\lexers\phix.py" "Archive\Obsolete\phix.py"
move "venv\Lib\site-packages\pygments\lexers\php.py" "Archive\Obsolete\php.py"
move "venv\Lib\site-packages\pygments\lexers\pointless.py" "Archive\Obsolete\pointless.py"
move "venv\Lib\site-packages\pygments\lexers\pony.py" "Archive\Obsolete\pony.py"
move "venv\Lib\site-packages\pygments\lexers\praat.py" "Archive\Obsolete\praat.py"
move "venv\Lib\site-packages\pygments\lexers\procfile.py" "Archive\Obsolete\procfile.py"
move "venv\Lib\site-packages\pygments\lexers\prolog.py" "Archive\Obsolete\prolog.py"
move "venv\Lib\site-packages\pygments\lexers\promql.py" "Archive\Obsolete\promql.py"
move "venv\Lib\site-packages\pygments\lexers\prql.py" "Archive\Obsolete\prql.py"
move "venv\Lib\site-packages\pygments\lexers\ptx.py" "Archive\Obsolete\ptx.py"
move "venv\Lib\site-packages\pygments\lexers\q.py" "Archive\Obsolete\q.py"
move "venv\Lib\site-packages\pygments\lexers\qlik.py" "Archive\Obsolete\qlik.py"
move "venv\Lib\site-packages\pygments\lexers\qvt.py" "Archive\Obsolete\qvt.py"
move "venv\Lib\site-packages\pygments\lexers\rdf.py" "Archive\Obsolete\rdf.py"
move "venv\Lib\site-packages\pygments\lexers\rebol.py" "Archive\Obsolete\rebol.py"
move "venv\Lib\site-packages\pygments\lexers\rego.py" "Archive\Obsolete\rego.py"
move "venv\Lib\site-packages\pygments\lexers\ride.py" "Archive\Obsolete\ride.py"
move "venv\Lib\site-packages\pygments\lexers\rita.py" "Archive\Obsolete\rita.py"
move "venv\Lib\site-packages\pygments\lexers\rnc.py" "Archive\Obsolete\rnc.py"
move "venv\Lib\site-packages\pygments\lexers\robotframework.py" "Archive\Obsolete\robotframework.py"
move "venv\Lib\site-packages\pygments\lexers\ruby.py" "Archive\Obsolete\ruby.py"
move "venv\Lib\site-packages\pygments\lexers\rust.py" "Archive\Obsolete\rust.py"
move "venv\Lib\site-packages\pygments\lexers\sas.py" "Archive\Obsolete\sas.py"
move "venv\Lib\site-packages\pygments\lexers\savi.py" "Archive\Obsolete\savi.py"
move "venv\Lib\site-packages\pygments\lexers\scdoc.py" "Archive\Obsolete\scdoc.py"
move "venv\Lib\site-packages\pygments\lexers\sgf.py" "Archive\Obsolete\sgf.py"
move "venv\Lib\site-packages\pygments\lexers\shell.py" "Archive\Obsolete\shell.py"
move "venv\Lib\site-packages\pygments\lexers\sieve.py" "Archive\Obsolete\sieve.py"
move "venv\Lib\site-packages\pygments\lexers\slash.py" "Archive\Obsolete\slash.py"
move "venv\Lib\site-packages\pygments\lexers\smalltalk.py" "Archive\Obsolete\smalltalk.py"
move "venv\Lib\site-packages\pygments\lexers\smithy.py" "Archive\Obsolete\smithy.py"
move "venv\Lib\site-packages\pygments\lexers\smv.py" "Archive\Obsolete\smv.py"
move "venv\Lib\site-packages\pygments\lexers\snobol.py" "Archive\Obsolete\snobol.py"
move "venv\Lib\site-packages\pygments\lexers\solidity.py" "Archive\Obsolete\solidity.py"
move "venv\Lib\site-packages\pygments\lexers\soong.py" "Archive\Obsolete\soong.py"
move "venv\Lib\site-packages\pygments\lexers\sophia.py" "Archive\Obsolete\sophia.py"
move "venv\Lib\site-packages\pygments\lexers\special.py" "Archive\Obsolete\special.py"
move "venv\Lib\site-packages\pygments\lexers\spice.py" "Archive\Obsolete\spice.py"
move "venv\Lib\site-packages\pygments\lexers\srcinfo.py" "Archive\Obsolete\srcinfo.py"
move "venv\Lib\site-packages\pygments\lexers\stata.py" "Archive\Obsolete\stata.py"
move "venv\Lib\site-packages\pygments\lexers\supercollider.py" "Archive\Obsolete\supercollider.py"
move "venv\Lib\site-packages\pygments\lexers\tact.py" "Archive\Obsolete\tact.py"
move "venv\Lib\site-packages\pygments\lexers\teal.py" "Archive\Obsolete\teal.py"
move "venv\Lib\site-packages\pygments\lexers\teraterm.py" "Archive\Obsolete\teraterm.py"
move "venv\Lib\site-packages\pygments\lexers\testing.py" "Archive\Obsolete\testing.py"
move "venv\Lib\site-packages\pygments\lexers\text.py" "Archive\Obsolete\text.py"
move "venv\Lib\site-packages\pygments\lexers\textedit.py" "Archive\Obsolete\textedit.py"
move "venv\Lib\site-packages\pygments\lexers\textfmts.py" "Archive\Obsolete\textfmts.py"
move "venv\Lib\site-packages\pygments\lexers\theorem.py" "Archive\Obsolete\theorem.py"
move "venv\Lib\site-packages\pygments\lexers\thingsdb.py" "Archive\Obsolete\thingsdb.py"
move "venv\Lib\site-packages\pygments\lexers\tlb.py" "Archive\Obsolete\tlb.py"
move "venv\Lib\site-packages\pygments\lexers\tls.py" "Archive\Obsolete\tls.py"
move "venv\Lib\site-packages\pygments\lexers\tnt.py" "Archive\Obsolete\tnt.py"
move "venv\Lib\site-packages\pygments\lexers\trafficscript.py" "Archive\Obsolete\trafficscript.py"
move "venv\Lib\site-packages\pygments\lexers\typoscript.py" "Archive\Obsolete\typoscript.py"
move "venv\Lib\site-packages\pygments\lexers\typst.py" "Archive\Obsolete\typst.py"
move "venv\Lib\site-packages\pygments\lexers\unicon.py" "Archive\Obsolete\unicon.py"
move "venv\Lib\site-packages\pygments\lexers\urbi.py" "Archive\Obsolete\urbi.py"
move "venv\Lib\site-packages\pygments\lexers\varnish.py" "Archive\Obsolete\varnish.py"
move "venv\Lib\site-packages\pygments\lexers\verification.py" "Archive\Obsolete\verification.py"
move "venv\Lib\site-packages\pygments\lexers\verifpal.py" "Archive\Obsolete\verifpal.py"
move "venv\Lib\site-packages\pygments\lexers\vip.py" "Archive\Obsolete\vip.py"
move "venv\Lib\site-packages\pygments\lexers\vyper.py" "Archive\Obsolete\vyper.py"
move "venv\Lib\site-packages\pygments\lexers\web.py" "Archive\Obsolete\web.py"
move "venv\Lib\site-packages\pygments\lexers\webassembly.py" "Archive\Obsolete\webassembly.py"
move "venv\Lib\site-packages\pygments\lexers\webidl.py" "Archive\Obsolete\webidl.py"
move "venv\Lib\site-packages\pygments\lexers\wgsl.py" "Archive\Obsolete\wgsl.py"
move "venv\Lib\site-packages\pygments\lexers\whiley.py" "Archive\Obsolete\whiley.py"
move "venv\Lib\site-packages\pygments\lexers\wowtoc.py" "Archive\Obsolete\wowtoc.py"
move "venv\Lib\site-packages\pygments\lexers\wren.py" "Archive\Obsolete\wren.py"
move "venv\Lib\site-packages\pygments\lexers\x10.py" "Archive\Obsolete\x10.py"
move "venv\Lib\site-packages\pygments\lexers\xorg.py" "Archive\Obsolete\xorg.py"
move "venv\Lib\site-packages\pygments\lexers\yang.py" "Archive\Obsolete\yang.py"
move "venv\Lib\site-packages\pygments\lexers\yara.py" "Archive\Obsolete\yara.py"
move "venv\Lib\site-packages\pygments\lexers\zig.py" "Archive\Obsolete\zig.py"
move "venv\Lib\site-packages\pygments\modeline.py" "Archive\Obsolete\modeline.py"
move "venv\Lib\site-packages\pygments\plugin.py" "Archive\Obsolete\plugin.py"
move "venv\Lib\site-packages\pygments\regexopt.py" "Archive\Obsolete\regexopt.py"
move "venv\Lib\site-packages\pygments\scanner.py" "Archive\Obsolete\scanner.py"
move "venv\Lib\site-packages\pygments\sphinxext.py" "Archive\Obsolete\sphinxext.py"
move "venv\Lib\site-packages\pygments\style.py" "Archive\Obsolete\style.py"
move "venv\Lib\site-packages\pygments\styles\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pygments\styles\_mapping.py" "Archive\Obsolete\_mapping.py"
move "venv\Lib\site-packages\pygments\styles\abap.py" "Archive\Obsolete\abap.py"
move "venv\Lib\site-packages\pygments\styles\algol.py" "Archive\Obsolete\algol.py"
move "venv\Lib\site-packages\pygments\styles\algol_nu.py" "Archive\Obsolete\algol_nu.py"
move "venv\Lib\site-packages\pygments\styles\arduino.py" "Archive\Obsolete\arduino.py"
move "venv\Lib\site-packages\pygments\styles\autumn.py" "Archive\Obsolete\autumn.py"
move "venv\Lib\site-packages\pygments\styles\borland.py" "Archive\Obsolete\borland.py"
move "venv\Lib\site-packages\pygments\styles\bw.py" "Archive\Obsolete\bw.py"
move "venv\Lib\site-packages\pygments\styles\coffee.py" "Archive\Obsolete\coffee.py"
move "venv\Lib\site-packages\pygments\styles\colorful.py" "Archive\Obsolete\colorful.py"
move "venv\Lib\site-packages\pygments\styles\default.py" "Archive\Obsolete\default.py"
move "venv\Lib\site-packages\pygments\styles\dracula.py" "Archive\Obsolete\dracula.py"
move "venv\Lib\site-packages\pygments\styles\emacs.py" "Archive\Obsolete\emacs.py"
move "venv\Lib\site-packages\pygments\styles\friendly.py" "Archive\Obsolete\friendly.py"
move "venv\Lib\site-packages\pygments\styles\friendly_grayscale.py" "Archive\Obsolete\friendly_grayscale.py"
move "venv\Lib\site-packages\pygments\styles\fruity.py" "Archive\Obsolete\fruity.py"
move "venv\Lib\site-packages\pygments\styles\gh_dark.py" "Archive\Obsolete\gh_dark.py"
move "venv\Lib\site-packages\pygments\styles\gruvbox.py" "Archive\Obsolete\gruvbox.py"
move "venv\Lib\site-packages\pygments\styles\igor.py" "Archive\Obsolete\igor.py"
move "venv\Lib\site-packages\pygments\styles\inkpot.py" "Archive\Obsolete\inkpot.py"
move "venv\Lib\site-packages\pygments\styles\lightbulb.py" "Archive\Obsolete\lightbulb.py"
move "venv\Lib\site-packages\pygments\styles\lilypond.py" "Archive\Obsolete\lilypond.py"
move "venv\Lib\site-packages\pygments\styles\lovelace.py" "Archive\Obsolete\lovelace.py"
move "venv\Lib\site-packages\pygments\styles\manni.py" "Archive\Obsolete\manni.py"
move "venv\Lib\site-packages\pygments\styles\material.py" "Archive\Obsolete\material.py"
move "venv\Lib\site-packages\pygments\styles\monokai.py" "Archive\Obsolete\monokai.py"
move "venv\Lib\site-packages\pygments\styles\murphy.py" "Archive\Obsolete\murphy.py"
move "venv\Lib\site-packages\pygments\styles\native.py" "Archive\Obsolete\native.py"
move "venv\Lib\site-packages\pygments\styles\nord.py" "Archive\Obsolete\nord.py"
move "venv\Lib\site-packages\pygments\styles\onedark.py" "Archive\Obsolete\onedark.py"
move "venv\Lib\site-packages\pygments\styles\paraiso_dark.py" "Archive\Obsolete\paraiso_dark.py"
move "venv\Lib\site-packages\pygments\styles\paraiso_light.py" "Archive\Obsolete\paraiso_light.py"
move "venv\Lib\site-packages\pygments\styles\pastie.py" "Archive\Obsolete\pastie.py"
move "venv\Lib\site-packages\pygments\styles\perldoc.py" "Archive\Obsolete\perldoc.py"
move "venv\Lib\site-packages\pygments\styles\rainbow_dash.py" "Archive\Obsolete\rainbow_dash.py"
move "venv\Lib\site-packages\pygments\styles\rrt.py" "Archive\Obsolete\rrt.py"
move "venv\Lib\site-packages\pygments\styles\sas.py" "Archive\Obsolete\sas.py"
move "venv\Lib\site-packages\pygments\styles\solarized.py" "Archive\Obsolete\solarized.py"
move "venv\Lib\site-packages\pygments\styles\staroffice.py" "Archive\Obsolete\staroffice.py"
move "venv\Lib\site-packages\pygments\styles\stata_dark.py" "Archive\Obsolete\stata_dark.py"
move "venv\Lib\site-packages\pygments\styles\stata_light.py" "Archive\Obsolete\stata_light.py"
move "venv\Lib\site-packages\pygments\styles\tango.py" "Archive\Obsolete\tango.py"
move "venv\Lib\site-packages\pygments\styles\trac.py" "Archive\Obsolete\trac.py"
move "venv\Lib\site-packages\pygments\styles\vim.py" "Archive\Obsolete\vim.py"
move "venv\Lib\site-packages\pygments\styles\vs.py" "Archive\Obsolete\vs.py"
move "venv\Lib\site-packages\pygments\styles\xcode.py" "Archive\Obsolete\xcode.py"
move "venv\Lib\site-packages\pygments\styles\zenburn.py" "Archive\Obsolete\zenburn.py"
move "venv\Lib\site-packages\pygments\token.py" "Archive\Obsolete\token.py"
move "venv\Lib\site-packages\pygments\unistring.py" "Archive\Obsolete\unistring.py"
move "venv\Lib\site-packages\pygments\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\licenses\AUTHORS" "Archive\Obsolete\AUTHORS"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pytest-8.4.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pytest-cov.pth" "Archive\Obsolete\pytest-cov.pth"
move "venv\Lib\site-packages\pytest\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pytest\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pytest_asyncio-1.0.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pytest_asyncio\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pytest_asyncio\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\pytest_asyncio\plugin.py" "Archive\Obsolete\plugin.py"
move "venv\Lib\site-packages\pytest_asyncio\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\licenses\AUTHORS.rst" "Archive\Obsolete\AUTHORS.rst"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pytest_cov-6.1.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pytest_cov\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pytest_cov\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\pytest_cov\embed.py" "Archive\Obsolete\embed.py"
move "venv\Lib\site-packages\pytest_cov\engine.py" "Archive\Obsolete\engine.py"
move "venv\Lib\site-packages\pytest_cov\plugin.py" "Archive\Obsolete\plugin.py"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\pytest_mock-3.14.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\pytest_mock\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\pytest_mock\_util.py" "Archive\Obsolete\_util.py"
move "venv\Lib\site-packages\pytest_mock\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\pytest_mock\plugin.py" "Archive\Obsolete\plugin.py"
move "venv\Lib\site-packages\pytest_mock\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\python_dateutil-2.9.0.post0.dist-info\zip-safe" "Archive\Obsolete\zip-safe"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\python_dotenv-1.1.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\python_jose-3.5.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\python_multipart-0.0.6.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\python_multipart-0.0.6.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\python_multipart-0.0.6.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\python_multipart-0.0.6.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\python_multipart-0.0.6.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\python_multipart-0.0.6.dist-info\licenses\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\requests-2.32.3.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\requests\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\requests\__version__.py" "Archive\Obsolete\__version__.py"
move "venv\Lib\site-packages\requests\_internal_utils.py" "Archive\Obsolete\_internal_utils.py"
move "venv\Lib\site-packages\requests\adapters.py" "Archive\Obsolete\adapters.py"
move "venv\Lib\site-packages\requests\api.py" "Archive\Obsolete\api.py"
move "venv\Lib\site-packages\requests\auth.py" "Archive\Obsolete\auth.py"
move "venv\Lib\site-packages\requests\compat.py" "Archive\Obsolete\compat.py"
move "venv\Lib\site-packages\requests\cookies.py" "Archive\Obsolete\cookies.py"
move "venv\Lib\site-packages\requests\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\requests\hooks.py" "Archive\Obsolete\hooks.py"
move "venv\Lib\site-packages\requests\models.py" "Archive\Obsolete\models.py"
move "venv\Lib\site-packages\requests\packages.py" "Archive\Obsolete\packages.py"
move "venv\Lib\site-packages\requests\sessions.py" "Archive\Obsolete\sessions.py"
move "venv\Lib\site-packages\requests\status_codes.py" "Archive\Obsolete\status_codes.py"
move "venv\Lib\site-packages\requests\structures.py" "Archive\Obsolete\structures.py"
move "venv\Lib\site-packages\requests\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\rich-14.0.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\rich-14.0.0.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\rich-14.0.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\rich-14.0.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\rich-14.0.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\rich-14.0.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\rich\_cell_widths.py" "Archive\Obsolete\_cell_widths.py"
move "venv\Lib\site-packages\rich\_emoji_codes.py" "Archive\Obsolete\_emoji_codes.py"
move "venv\Lib\site-packages\rich\_emoji_replace.py" "Archive\Obsolete\_emoji_replace.py"
move "venv\Lib\site-packages\rich\_export_format.py" "Archive\Obsolete\_export_format.py"
move "venv\Lib\site-packages\rich\_extension.py" "Archive\Obsolete\_extension.py"
move "venv\Lib\site-packages\rich\_fileno.py" "Archive\Obsolete\_fileno.py"
move "venv\Lib\site-packages\rich\_inspect.py" "Archive\Obsolete\_inspect.py"
move "venv\Lib\site-packages\rich\_loop.py" "Archive\Obsolete\_loop.py"
move "venv\Lib\site-packages\rich\_null_file.py" "Archive\Obsolete\_null_file.py"
move "venv\Lib\site-packages\rich\_palettes.py" "Archive\Obsolete\_palettes.py"
move "venv\Lib\site-packages\rich\_pick.py" "Archive\Obsolete\_pick.py"
move "venv\Lib\site-packages\rich\_spinners.py" "Archive\Obsolete\_spinners.py"
move "venv\Lib\site-packages\rich\_stack.py" "Archive\Obsolete\_stack.py"
move "venv\Lib\site-packages\rich\_timer.py" "Archive\Obsolete\_timer.py"
move "venv\Lib\site-packages\rich\_windows_renderer.py" "Archive\Obsolete\_windows_renderer.py"
move "venv\Lib\site-packages\rich\bar.py" "Archive\Obsolete\bar.py"
move "venv\Lib\site-packages\rich\color_triplet.py" "Archive\Obsolete\color_triplet.py"
move "venv\Lib\site-packages\rich\constrain.py" "Archive\Obsolete\constrain.py"
move "venv\Lib\site-packages\rich\containers.py" "Archive\Obsolete\containers.py"
move "venv\Lib\site-packages\rich\errors.py" "Archive\Obsolete\errors.py"
move "venv\Lib\site-packages\rich\file_proxy.py" "Archive\Obsolete\file_proxy.py"
move "venv\Lib\site-packages\rich\filesize.py" "Archive\Obsolete\filesize.py"
move "venv\Lib\site-packages\rich\jupyter.py" "Archive\Obsolete\jupyter.py"
move "venv\Lib\site-packages\rich\live_render.py" "Archive\Obsolete\live_render.py"
move "venv\Lib\site-packages\rich\measure.py" "Archive\Obsolete\measure.py"
move "venv\Lib\site-packages\rich\protocol.py" "Archive\Obsolete\protocol.py"
move "venv\Lib\site-packages\rich\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\rich\region.py" "Archive\Obsolete\region.py"
move "venv\Lib\site-packages\rich\screen.py" "Archive\Obsolete\screen.py"
move "venv\Lib\site-packages\rich\style.py" "Archive\Obsolete\style.py"
move "venv\Lib\site-packages\rich\terminal_theme.py" "Archive\Obsolete\terminal_theme.py"
move "venv\Lib\site-packages\rich\themes.py" "Archive\Obsolete\themes.py"
move "venv\Lib\site-packages\rsa-4.9.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\rsa-4.9.1.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\rsa-4.9.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\rsa-4.9.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\rsa-4.9.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\rsa-4.9.1.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\rsa\asn1.py" "Archive\Obsolete\asn1.py"
move "venv\Lib\site-packages\rsa\cli.py" "Archive\Obsolete\cli.py"
move "venv\Lib\site-packages\rsa\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\rsa\pem.py" "Archive\Obsolete\pem.py"
move "venv\Lib\site-packages\rsa\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\rsa\randnum.py" "Archive\Obsolete\randnum.py"
move "venv\Lib\site-packages\rsa\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\setuptools-65.5.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\setuptools\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_deprecation_warning.py" "Archive\Obsolete\_deprecation_warning.py"
move "venv\Lib\site-packages\setuptools\_distutils\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_distutils\_collections.py" "Archive\Obsolete\_collections.py"
move "venv\Lib\site-packages\setuptools\_distutils\_functools.py" "Archive\Obsolete\_functools.py"
move "venv\Lib\site-packages\setuptools\_distutils\_macos_compat.py" "Archive\Obsolete\_macos_compat.py"
move "venv\Lib\site-packages\setuptools\_distutils\_msvccompiler.py" "Archive\Obsolete\_msvccompiler.py"
move "venv\Lib\site-packages\setuptools\_distutils\archive_util.py" "Archive\Obsolete\archive_util.py"
move "venv\Lib\site-packages\setuptools\_distutils\bcppcompiler.py" "Archive\Obsolete\bcppcompiler.py"
move "venv\Lib\site-packages\setuptools\_distutils\ccompiler.py" "Archive\Obsolete\ccompiler.py"
move "venv\Lib\site-packages\setuptools\_distutils\cmd.py" "Archive\Obsolete\cmd.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\_framework_compat.py" "Archive\Obsolete\_framework_compat.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\bdist.py" "Archive\Obsolete\bdist.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\bdist_dumb.py" "Archive\Obsolete\bdist_dumb.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\bdist_rpm.py" "Archive\Obsolete\bdist_rpm.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\build.py" "Archive\Obsolete\build.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\build_clib.py" "Archive\Obsolete\build_clib.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\build_ext.py" "Archive\Obsolete\build_ext.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\build_scripts.py" "Archive\Obsolete\build_scripts.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\clean.py" "Archive\Obsolete\clean.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\config.py" "Archive\Obsolete\config.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\install.py" "Archive\Obsolete\install.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\install_data.py" "Archive\Obsolete\install_data.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\install_egg_info.py" "Archive\Obsolete\install_egg_info.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\install_headers.py" "Archive\Obsolete\install_headers.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\install_scripts.py" "Archive\Obsolete\install_scripts.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\py37compat.py" "Archive\Obsolete\py37compat.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\register.py" "Archive\Obsolete\register.py"
move "venv\Lib\site-packages\setuptools\_distutils\command\upload.py" "Archive\Obsolete\upload.py"
move "venv\Lib\site-packages\setuptools\_distutils\config.py" "Archive\Obsolete\config.py"
move "venv\Lib\site-packages\setuptools\_distutils\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\setuptools\_distutils\cygwinccompiler.py" "Archive\Obsolete\cygwinccompiler.py"
move "venv\Lib\site-packages\setuptools\_distutils\debug.py" "Archive\Obsolete\debug.py"
move "venv\Lib\site-packages\setuptools\_distutils\dep_util.py" "Archive\Obsolete\dep_util.py"
move "venv\Lib\site-packages\setuptools\_distutils\dir_util.py" "Archive\Obsolete\dir_util.py"
move "venv\Lib\site-packages\setuptools\_distutils\dist.py" "Archive\Obsolete\dist.py"
move "venv\Lib\site-packages\setuptools\_distutils\errors.py" "Archive\Obsolete\errors.py"
move "venv\Lib\site-packages\setuptools\_distutils\extension.py" "Archive\Obsolete\extension.py"
move "venv\Lib\site-packages\setuptools\_distutils\file_util.py" "Archive\Obsolete\file_util.py"
move "venv\Lib\site-packages\setuptools\_distutils\log.py" "Archive\Obsolete\log.py"
move "venv\Lib\site-packages\setuptools\_distutils\msvc9compiler.py" "Archive\Obsolete\msvc9compiler.py"
move "venv\Lib\site-packages\setuptools\_distutils\msvccompiler.py" "Archive\Obsolete\msvccompiler.py"
move "venv\Lib\site-packages\setuptools\_distutils\py38compat.py" "Archive\Obsolete\py38compat.py"
move "venv\Lib\site-packages\setuptools\_distutils\py39compat.py" "Archive\Obsolete\py39compat.py"
move "venv\Lib\site-packages\setuptools\_distutils\spawn.py" "Archive\Obsolete\spawn.py"
move "venv\Lib\site-packages\setuptools\_distutils\sysconfig.py" "Archive\Obsolete\sysconfig.py"
move "venv\Lib\site-packages\setuptools\_distutils\text_file.py" "Archive\Obsolete\text_file.py"
move "venv\Lib\site-packages\setuptools\_distutils\unixccompiler.py" "Archive\Obsolete\unixccompiler.py"
move "venv\Lib\site-packages\setuptools\_distutils\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\setuptools\_distutils\versionpredicate.py" "Archive\Obsolete\versionpredicate.py"
move "venv\Lib\site-packages\setuptools\_entry_points.py" "Archive\Obsolete\_entry_points.py"
move "venv\Lib\site-packages\setuptools\_importlib.py" "Archive\Obsolete\_importlib.py"
move "venv\Lib\site-packages\setuptools\_itertools.py" "Archive\Obsolete\_itertools.py"
move "venv\Lib\site-packages\setuptools\_path.py" "Archive\Obsolete\_path.py"
move "venv\Lib\site-packages\setuptools\_reqs.py" "Archive\Obsolete\_reqs.py"
move "venv\Lib\site-packages\setuptools\_vendor\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_adapters.py" "Archive\Obsolete\_adapters.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_collections.py" "Archive\Obsolete\_collections.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_functools.py" "Archive\Obsolete\_functools.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_itertools.py" "Archive\Obsolete\_itertools.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_meta.py" "Archive\Obsolete\_meta.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\_text.py" "Archive\Obsolete\_text.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_adapters.py" "Archive\Obsolete\_adapters.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_common.py" "Archive\Obsolete\_common.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_compat.py" "Archive\Obsolete\_compat.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_itertools.py" "Archive\Obsolete\_itertools.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\_legacy.py" "Archive\Obsolete\_legacy.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\abc.py" "Archive\Obsolete\abc.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\readers.py" "Archive\Obsolete\readers.py"
move "venv\Lib\site-packages\setuptools\_vendor\importlib_resources\simple.py" "Archive\Obsolete\simple.py"
move "venv\Lib\site-packages\setuptools\_vendor\jaraco\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\jaraco\context.py" "Archive\Obsolete\context.py"
move "venv\Lib\site-packages\setuptools\_vendor\jaraco\functools.py" "Archive\Obsolete\functools.py"
move "venv\Lib\site-packages\setuptools\_vendor\jaraco\text\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\more_itertools\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\more_itertools\more.py" "Archive\Obsolete\more.py"
move "venv\Lib\site-packages\setuptools\_vendor\more_itertools\recipes.py" "Archive\Obsolete\recipes.py"
move "venv\Lib\site-packages\setuptools\_vendor\ordered_set.py" "Archive\Obsolete\ordered_set.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\__about__.py" "Archive\Obsolete\__about__.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\_manylinux.py" "Archive\Obsolete\_manylinux.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\_structures.py" "Archive\Obsolete\_structures.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\markers.py" "Archive\Obsolete\markers.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\requirements.py" "Archive\Obsolete\requirements.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\specifiers.py" "Archive\Obsolete\specifiers.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\tags.py" "Archive\Obsolete\tags.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\setuptools\_vendor\packaging\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\actions.py" "Archive\Obsolete\actions.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\common.py" "Archive\Obsolete\common.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\core.py" "Archive\Obsolete\core.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\diagram\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\helpers.py" "Archive\Obsolete\helpers.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\results.py" "Archive\Obsolete\results.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\testing.py" "Archive\Obsolete\testing.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\unicode.py" "Archive\Obsolete\unicode.py"
move "venv\Lib\site-packages\setuptools\_vendor\pyparsing\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\setuptools\_vendor\tomli\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\_vendor\tomli\_parser.py" "Archive\Obsolete\_parser.py"
move "venv\Lib\site-packages\setuptools\_vendor\tomli\_re.py" "Archive\Obsolete\_re.py"
move "venv\Lib\site-packages\setuptools\_vendor\tomli\_types.py" "Archive\Obsolete\_types.py"
move "venv\Lib\site-packages\setuptools\_vendor\typing_extensions.py" "Archive\Obsolete\typing_extensions.py"
move "venv\Lib\site-packages\setuptools\_vendor\zipp.py" "Archive\Obsolete\zipp.py"
move "venv\Lib\site-packages\setuptools\archive_util.py" "Archive\Obsolete\archive_util.py"
move "venv\Lib\site-packages\setuptools\cli-32.exe" "Archive\Obsolete\cli-32.exe"
move "venv\Lib\site-packages\setuptools\cli-64.exe" "Archive\Obsolete\cli-64.exe"
move "venv\Lib\site-packages\setuptools\cli-arm64.exe" "Archive\Obsolete\cli-arm64.exe"
move "venv\Lib\site-packages\setuptools\cli.exe" "Archive\Obsolete\cli.exe"
move "venv\Lib\site-packages\setuptools\command\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\command\alias.py" "Archive\Obsolete\alias.py"
move "venv\Lib\site-packages\setuptools\command\bdist_rpm.py" "Archive\Obsolete\bdist_rpm.py"
move "venv\Lib\site-packages\setuptools\command\build.py" "Archive\Obsolete\build.py"
move "venv\Lib\site-packages\setuptools\command\build_clib.py" "Archive\Obsolete\build_clib.py"
move "venv\Lib\site-packages\setuptools\command\develop.py" "Archive\Obsolete\develop.py"
move "venv\Lib\site-packages\setuptools\command\dist_info.py" "Archive\Obsolete\dist_info.py"
move "venv\Lib\site-packages\setuptools\command\install.py" "Archive\Obsolete\install.py"
move "venv\Lib\site-packages\setuptools\command\install_egg_info.py" "Archive\Obsolete\install_egg_info.py"
move "venv\Lib\site-packages\setuptools\command\install_scripts.py" "Archive\Obsolete\install_scripts.py"
move "venv\Lib\site-packages\setuptools\command\launcher manifest.xml" "Archive\Obsolete\launcher manifest.xml"
move "venv\Lib\site-packages\setuptools\command\register.py" "Archive\Obsolete\register.py"
move "venv\Lib\site-packages\setuptools\command\rotate.py" "Archive\Obsolete\rotate.py"
move "venv\Lib\site-packages\setuptools\command\saveopts.py" "Archive\Obsolete\saveopts.py"
move "venv\Lib\site-packages\setuptools\command\sdist.py" "Archive\Obsolete\sdist.py"
move "venv\Lib\site-packages\setuptools\command\setopt.py" "Archive\Obsolete\setopt.py"
move "venv\Lib\site-packages\setuptools\command\upload.py" "Archive\Obsolete\upload.py"
move "venv\Lib\site-packages\setuptools\command\upload_docs.py" "Archive\Obsolete\upload_docs.py"
move "venv\Lib\site-packages\setuptools\config\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\config\_apply_pyprojecttoml.py" "Archive\Obsolete\_apply_pyprojecttoml.py"
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\error_reporting.py" "Archive\Obsolete\error_reporting.py"
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\extra_validations.py" "Archive\Obsolete\extra_validations.py"
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\fastjsonschema_exceptions.py" "Archive\Obsolete\fastjsonschema_exceptions.py"
move "venv\Lib\site-packages\setuptools\config\_validate_pyproject\formats.py" "Archive\Obsolete\formats.py"
move "venv\Lib\site-packages\setuptools\config\pyprojecttoml.py" "Archive\Obsolete\pyprojecttoml.py"
move "venv\Lib\site-packages\setuptools\config\setupcfg.py" "Archive\Obsolete\setupcfg.py"
move "venv\Lib\site-packages\setuptools\dep_util.py" "Archive\Obsolete\dep_util.py"
move "venv\Lib\site-packages\setuptools\depends.py" "Archive\Obsolete\depends.py"
move "venv\Lib\site-packages\setuptools\errors.py" "Archive\Obsolete\errors.py"
move "venv\Lib\site-packages\setuptools\extension.py" "Archive\Obsolete\extension.py"
move "venv\Lib\site-packages\setuptools\extern\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\setuptools\glob.py" "Archive\Obsolete\glob.py"
move "venv\Lib\site-packages\setuptools\gui-32.exe" "Archive\Obsolete\gui-32.exe"
move "venv\Lib\site-packages\setuptools\gui-64.exe" "Archive\Obsolete\gui-64.exe"
move "venv\Lib\site-packages\setuptools\gui-arm64.exe" "Archive\Obsolete\gui-arm64.exe"
move "venv\Lib\site-packages\setuptools\gui.exe" "Archive\Obsolete\gui.exe"
move "venv\Lib\site-packages\setuptools\installer.py" "Archive\Obsolete\installer.py"
move "venv\Lib\site-packages\setuptools\launch.py" "Archive\Obsolete\launch.py"
move "venv\Lib\site-packages\setuptools\logging.py" "Archive\Obsolete\logging.py"
move "venv\Lib\site-packages\setuptools\monkey.py" "Archive\Obsolete\monkey.py"
move "venv\Lib\site-packages\setuptools\namespaces.py" "Archive\Obsolete\namespaces.py"
move "venv\Lib\site-packages\setuptools\py34compat.py" "Archive\Obsolete\py34compat.py"
move "venv\Lib\site-packages\setuptools\sandbox.py" "Archive\Obsolete\sandbox.py"
move "venv\Lib\site-packages\setuptools\script (dev).tmpl" "Archive\Obsolete\script (dev).tmpl"
move "venv\Lib\site-packages\setuptools\script.tmpl" "Archive\Obsolete\script.tmpl"
move "venv\Lib\site-packages\setuptools\unicode_utils.py" "Archive\Obsolete\unicode_utils.py"
move "venv\Lib\site-packages\setuptools\version.py" "Archive\Obsolete\version.py"
move "venv\Lib\site-packages\setuptools\windows_support.py" "Archive\Obsolete\windows_support.py"
move "venv\Lib\site-packages\six-1.17.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\six-1.17.0.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\six-1.17.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\six-1.17.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\six-1.17.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\six-1.17.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\six.py" "Archive\Obsolete\six.py"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\LICENSE.APACHE2" "Archive\Obsolete\LICENSE.APACHE2"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\LICENSE.MIT" "Archive\Obsolete\LICENSE.MIT"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\sniffio-1.3.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\sniffio\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\sniffio\_impl.py" "Archive\Obsolete\_impl.py"
move "venv\Lib\site-packages\sniffio\_tests\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\sniffio\_tests\test_sniffio.py" "Archive\Obsolete\test_sniffio.py"
move "venv\Lib\site-packages\sniffio\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\sniffio\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\starlette-0.46.2.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\starlette-0.46.2.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\starlette-0.46.2.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\starlette-0.46.2.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\starlette-0.46.2.dist-info\licenses\LICENSE.md" "Archive\Obsolete\LICENSE.md"
move "venv\Lib\site-packages\starlette\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\starlette\_exception_handler.py" "Archive\Obsolete\_exception_handler.py"
move "venv\Lib\site-packages\starlette\_utils.py" "Archive\Obsolete\_utils.py"
move "venv\Lib\site-packages\starlette\applications.py" "Archive\Obsolete\applications.py"
move "venv\Lib\site-packages\starlette\authentication.py" "Archive\Obsolete\authentication.py"
move "venv\Lib\site-packages\starlette\background.py" "Archive\Obsolete\background.py"
move "venv\Lib\site-packages\starlette\concurrency.py" "Archive\Obsolete\concurrency.py"
move "venv\Lib\site-packages\starlette\config.py" "Archive\Obsolete\config.py"
move "venv\Lib\site-packages\starlette\convertors.py" "Archive\Obsolete\convertors.py"
move "venv\Lib\site-packages\starlette\datastructures.py" "Archive\Obsolete\datastructures.py"
move "venv\Lib\site-packages\starlette\endpoints.py" "Archive\Obsolete\endpoints.py"
move "venv\Lib\site-packages\starlette\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\starlette\formparsers.py" "Archive\Obsolete\formparsers.py"
move "venv\Lib\site-packages\starlette\middleware\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\starlette\middleware\authentication.py" "Archive\Obsolete\authentication.py"
move "venv\Lib\site-packages\starlette\middleware\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\starlette\middleware\cors.py" "Archive\Obsolete\cors.py"
move "venv\Lib\site-packages\starlette\middleware\errors.py" "Archive\Obsolete\errors.py"
move "venv\Lib\site-packages\starlette\middleware\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\starlette\middleware\gzip.py" "Archive\Obsolete\gzip.py"
move "venv\Lib\site-packages\starlette\middleware\httpsredirect.py" "Archive\Obsolete\httpsredirect.py"
move "venv\Lib\site-packages\starlette\middleware\sessions.py" "Archive\Obsolete\sessions.py"
move "venv\Lib\site-packages\starlette\middleware\trustedhost.py" "Archive\Obsolete\trustedhost.py"
move "venv\Lib\site-packages\starlette\middleware\wsgi.py" "Archive\Obsolete\wsgi.py"
move "venv\Lib\site-packages\starlette\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\starlette\requests.py" "Archive\Obsolete\requests.py"
move "venv\Lib\site-packages\starlette\responses.py" "Archive\Obsolete\responses.py"
move "venv\Lib\site-packages\starlette\routing.py" "Archive\Obsolete\routing.py"
move "venv\Lib\site-packages\starlette\schemas.py" "Archive\Obsolete\schemas.py"
move "venv\Lib\site-packages\starlette\status.py" "Archive\Obsolete\status.py"
move "venv\Lib\site-packages\starlette\testclient.py" "Archive\Obsolete\testclient.py"
move "venv\Lib\site-packages\starlette\types.py" "Archive\Obsolete\types.py"
move "venv\Lib\site-packages\starlette\websockets.py" "Archive\Obsolete\websockets.py"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\typing_extensions-4.14.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\typing_extensions.py" "Archive\Obsolete\typing_extensions.py"
move "venv\Lib\site-packages\typing_inspection-0.4.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\typing_inspection-0.4.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\typing_inspection-0.4.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\typing_inspection-0.4.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\typing_inspection-0.4.1.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\typing_inspection\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\typing_inspection\introspection.py" "Archive\Obsolete\introspection.py"
move "venv\Lib\site-packages\typing_inspection\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\typing_inspection\typing_objects.py" "Archive\Obsolete\typing_objects.py"
move "venv\Lib\site-packages\typing_inspection\typing_objects.pyi" "Archive\Obsolete\typing_objects.pyi"
move "venv\Lib\site-packages\urllib3-2.4.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\urllib3-2.4.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\urllib3-2.4.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\urllib3-2.4.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\urllib3-2.4.0.dist-info\licenses\LICENSE.txt" "Archive\Obsolete\LICENSE.txt"
move "venv\Lib\site-packages\urllib3\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\urllib3\_base_connection.py" "Archive\Obsolete\_base_connection.py"
move "venv\Lib\site-packages\urllib3\_collections.py" "Archive\Obsolete\_collections.py"
move "venv\Lib\site-packages\urllib3\_request_methods.py" "Archive\Obsolete\_request_methods.py"
move "venv\Lib\site-packages\urllib3\_version.py" "Archive\Obsolete\_version.py"
move "venv\Lib\site-packages\urllib3\contrib\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\urllib3\contrib\emscripten\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\urllib3\contrib\emscripten\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\urllib3\contrib\emscripten\emscripten_fetch_worker.js" "Archive\Obsolete\emscripten_fetch_worker.js"
move "venv\Lib\site-packages\urllib3\contrib\emscripten\request.py" "Archive\Obsolete\request.py"
move "venv\Lib\site-packages\urllib3\contrib\emscripten\response.py" "Archive\Obsolete\response.py"
move "venv\Lib\site-packages\urllib3\contrib\pyopenssl.py" "Archive\Obsolete\pyopenssl.py"
move "venv\Lib\site-packages\urllib3\contrib\socks.py" "Archive\Obsolete\socks.py"
move "venv\Lib\site-packages\urllib3\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\urllib3\fields.py" "Archive\Obsolete\fields.py"
move "venv\Lib\site-packages\urllib3\filepost.py" "Archive\Obsolete\filepost.py"
move "venv\Lib\site-packages\urllib3\http2\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\urllib3\http2\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\urllib3\http2\probe.py" "Archive\Obsolete\probe.py"
move "venv\Lib\site-packages\urllib3\poolmanager.py" "Archive\Obsolete\poolmanager.py"
move "venv\Lib\site-packages\urllib3\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\urllib3\response.py" "Archive\Obsolete\response.py"
move "venv\Lib\site-packages\urllib3\util\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\urllib3\util\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\urllib3\util\proxy.py" "Archive\Obsolete\proxy.py"
move "venv\Lib\site-packages\urllib3\util\request.py" "Archive\Obsolete\request.py"
move "venv\Lib\site-packages\urllib3\util\response.py" "Archive\Obsolete\response.py"
move "venv\Lib\site-packages\urllib3\util\retry.py" "Archive\Obsolete\retry.py"
move "venv\Lib\site-packages\urllib3\util\ssl_.py" "Archive\Obsolete\ssl_.py"
move "venv\Lib\site-packages\urllib3\util\ssl_match_hostname.py" "Archive\Obsolete\ssl_match_hostname.py"
move "venv\Lib\site-packages\urllib3\util\ssltransport.py" "Archive\Obsolete\ssltransport.py"
move "venv\Lib\site-packages\urllib3\util\timeout.py" "Archive\Obsolete\timeout.py"
move "venv\Lib\site-packages\urllib3\util\url.py" "Archive\Obsolete\url.py"
move "venv\Lib\site-packages\urllib3\util\util.py" "Archive\Obsolete\util.py"
move "venv\Lib\site-packages\urllib3\util\wait.py" "Archive\Obsolete\wait.py"
move "venv\Lib\site-packages\uuid-1.30.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\uuid-1.30.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\uuid-1.30.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\uuid-1.30.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\uuid-1.30.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\uuid-1.30.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\uuid.py" "Archive\Obsolete\uuid.py"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\uvicorn-0.24.0.dist-info\licenses\LICENSE.md" "Archive\Obsolete\LICENSE.md"
move "venv\Lib\site-packages\uvicorn\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\uvicorn\_subprocess.py" "Archive\Obsolete\_subprocess.py"
move "venv\Lib\site-packages\uvicorn\_types.py" "Archive\Obsolete\_types.py"
move "venv\Lib\site-packages\uvicorn\importer.py" "Archive\Obsolete\importer.py"
move "venv\Lib\site-packages\uvicorn\lifespan\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\uvicorn\lifespan\off.py" "Archive\Obsolete\off.py"
move "venv\Lib\site-packages\uvicorn\logging.py" "Archive\Obsolete\logging.py"
move "venv\Lib\site-packages\uvicorn\loops\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\uvicorn\loops\asyncio.py" "Archive\Obsolete\asyncio.py"
move "venv\Lib\site-packages\uvicorn\loops\auto.py" "Archive\Obsolete\auto.py"
move "venv\Lib\site-packages\uvicorn\loops\uvloop.py" "Archive\Obsolete\uvloop.py"
move "venv\Lib\site-packages\uvicorn\middleware\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\uvicorn\middleware\asgi2.py" "Archive\Obsolete\asgi2.py"
move "venv\Lib\site-packages\uvicorn\middleware\message_logger.py" "Archive\Obsolete\message_logger.py"
move "venv\Lib\site-packages\uvicorn\middleware\proxy_headers.py" "Archive\Obsolete\proxy_headers.py"
move "venv\Lib\site-packages\uvicorn\middleware\wsgi.py" "Archive\Obsolete\wsgi.py"
move "venv\Lib\site-packages\uvicorn\protocols\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\uvicorn\protocols\http\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\uvicorn\protocols\http\auto.py" "Archive\Obsolete\auto.py"
move "venv\Lib\site-packages\uvicorn\protocols\http\flow_control.py" "Archive\Obsolete\flow_control.py"
move "venv\Lib\site-packages\uvicorn\protocols\http\h11_impl.py" "Archive\Obsolete\h11_impl.py"
move "venv\Lib\site-packages\uvicorn\protocols\http\httptools_impl.py" "Archive\Obsolete\httptools_impl.py"
move "venv\Lib\site-packages\uvicorn\protocols\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\uvicorn\protocols\websockets\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\uvicorn\protocols\websockets\auto.py" "Archive\Obsolete\auto.py"
move "venv\Lib\site-packages\uvicorn\protocols\websockets\websockets_impl.py" "Archive\Obsolete\websockets_impl.py"
move "venv\Lib\site-packages\uvicorn\protocols\websockets\wsproto_impl.py" "Archive\Obsolete\wsproto_impl.py"
move "venv\Lib\site-packages\uvicorn\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\uvicorn\server.py" "Archive\Obsolete\server.py"
move "venv\Lib\site-packages\uvicorn\supervisors\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\uvicorn\supervisors\basereload.py" "Archive\Obsolete\basereload.py"
move "venv\Lib\site-packages\uvicorn\supervisors\multiprocess.py" "Archive\Obsolete\multiprocess.py"
move "venv\Lib\site-packages\uvicorn\workers.py" "Archive\Obsolete\workers.py"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\REQUESTED" "Archive\Obsolete\REQUESTED"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\entry_points.txt" "Archive\Obsolete\entry_points.txt"
move "venv\Lib\site-packages\websockets-15.0.1.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\websockets\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\websockets\asyncio\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\websockets\asyncio\async_timeout.py" "Archive\Obsolete\async_timeout.py"
move "venv\Lib\site-packages\websockets\asyncio\client.py" "Archive\Obsolete\client.py"
move "venv\Lib\site-packages\websockets\asyncio\compatibility.py" "Archive\Obsolete\compatibility.py"
move "venv\Lib\site-packages\websockets\asyncio\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\websockets\asyncio\messages.py" "Archive\Obsolete\messages.py"
move "venv\Lib\site-packages\websockets\asyncio\router.py" "Archive\Obsolete\router.py"
move "venv\Lib\site-packages\websockets\asyncio\server.py" "Archive\Obsolete\server.py"
move "venv\Lib\site-packages\websockets\auth.py" "Archive\Obsolete\auth.py"
move "venv\Lib\site-packages\websockets\client.py" "Archive\Obsolete\client.py"
move "venv\Lib\site-packages\websockets\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\websockets\datastructures.py" "Archive\Obsolete\datastructures.py"
move "venv\Lib\site-packages\websockets\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\websockets\extensions\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\websockets\extensions\base.py" "Archive\Obsolete\base.py"
move "venv\Lib\site-packages\websockets\extensions\permessage_deflate.py" "Archive\Obsolete\permessage_deflate.py"
move "venv\Lib\site-packages\websockets\frames.py" "Archive\Obsolete\frames.py"
move "venv\Lib\site-packages\websockets\headers.py" "Archive\Obsolete\headers.py"
move "venv\Lib\site-packages\websockets\http.py" "Archive\Obsolete\http.py"
move "venv\Lib\site-packages\websockets\http11.py" "Archive\Obsolete\http11.py"
move "venv\Lib\site-packages\websockets\imports.py" "Archive\Obsolete\imports.py"
move "venv\Lib\site-packages\websockets\legacy\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\websockets\legacy\auth.py" "Archive\Obsolete\auth.py"
move "venv\Lib\site-packages\websockets\legacy\client.py" "Archive\Obsolete\client.py"
move "venv\Lib\site-packages\websockets\legacy\exceptions.py" "Archive\Obsolete\exceptions.py"
move "venv\Lib\site-packages\websockets\legacy\framing.py" "Archive\Obsolete\framing.py"
move "venv\Lib\site-packages\websockets\legacy\handshake.py" "Archive\Obsolete\handshake.py"
move "venv\Lib\site-packages\websockets\legacy\http.py" "Archive\Obsolete\http.py"
move "venv\Lib\site-packages\websockets\legacy\protocol.py" "Archive\Obsolete\protocol.py"
move "venv\Lib\site-packages\websockets\legacy\server.py" "Archive\Obsolete\server.py"
move "venv\Lib\site-packages\websockets\protocol.py" "Archive\Obsolete\protocol.py"
move "venv\Lib\site-packages\websockets\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\websockets\server.py" "Archive\Obsolete\server.py"
move "venv\Lib\site-packages\websockets\speedups.c" "Archive\Obsolete\speedups.c"
move "venv\Lib\site-packages\websockets\speedups.cp311-win_amd64.pyd" "Archive\Obsolete\speedups.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\websockets\speedups.pyi" "Archive\Obsolete\speedups.pyi"
move "venv\Lib\site-packages\websockets\streams.py" "Archive\Obsolete\streams.py"
move "venv\Lib\site-packages\websockets\sync\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\websockets\sync\client.py" "Archive\Obsolete\client.py"
move "venv\Lib\site-packages\websockets\sync\connection.py" "Archive\Obsolete\connection.py"
move "venv\Lib\site-packages\websockets\sync\messages.py" "Archive\Obsolete\messages.py"
move "venv\Lib\site-packages\websockets\sync\router.py" "Archive\Obsolete\router.py"
move "venv\Lib\site-packages\websockets\sync\server.py" "Archive\Obsolete\server.py"
move "venv\Lib\site-packages\websockets\sync\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\websockets\typing.py" "Archive\Obsolete\typing.py"
move "venv\Lib\site-packages\websockets\uri.py" "Archive\Obsolete\uri.py"
move "venv\Lib\site-packages\websockets\utils.py" "Archive\Obsolete\utils.py"
move "venv\Lib\site-packages\yarl-1.20.0.dist-info\INSTALLER" "Archive\Obsolete\INSTALLER"
move "venv\Lib\site-packages\yarl-1.20.0.dist-info\METADATA" "Archive\Obsolete\METADATA"
move "venv\Lib\site-packages\yarl-1.20.0.dist-info\RECORD" "Archive\Obsolete\RECORD"
move "venv\Lib\site-packages\yarl-1.20.0.dist-info\WHEEL" "Archive\Obsolete\WHEEL"
move "venv\Lib\site-packages\yarl-1.20.0.dist-info\licenses\LICENSE" "Archive\Obsolete\LICENSE"
move "venv\Lib\site-packages\yarl-1.20.0.dist-info\licenses\NOTICE" "Archive\Obsolete\NOTICE"
move "venv\Lib\site-packages\yarl-1.20.0.dist-info\top_level.txt" "Archive\Obsolete\top_level.txt"
move "venv\Lib\site-packages\yarl\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\yarl\_parse.py" "Archive\Obsolete\_parse.py"
move "venv\Lib\site-packages\yarl\_path.py" "Archive\Obsolete\_path.py"
move "venv\Lib\site-packages\yarl\_query.py" "Archive\Obsolete\_query.py"
move "venv\Lib\site-packages\yarl\_quoters.py" "Archive\Obsolete\_quoters.py"
move "venv\Lib\site-packages\yarl\_quoting.py" "Archive\Obsolete\_quoting.py"
move "venv\Lib\site-packages\yarl\_quoting_c.cp311-win_amd64.pyd" "Archive\Obsolete\_quoting_c.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\yarl\_quoting_c.pyx" "Archive\Obsolete\_quoting_c.pyx"
move "venv\Lib\site-packages\yarl\_quoting_py.py" "Archive\Obsolete\_quoting_py.py"
move "venv\Lib\site-packages\yarl\_url.py" "Archive\Obsolete\_url.py"
move "venv\Lib\site-packages\yarl\py.typed" "Archive\Obsolete\py.typed"
move "venv\Lib\site-packages\~ydantic_core\__init__.py" "Archive\Obsolete\__init__.py"
move "venv\Lib\site-packages\~ydantic_core\_pydantic_core.cp311-win_amd64.pyd" "Archive\Obsolete\_pydantic_core.cp311-win_amd64.pyd"
move "venv\Lib\site-packages\~ydantic_core\_pydantic_core.pyi" "Archive\Obsolete\_pydantic_core.pyi"
move "venv\Scripts\Activate.ps1" "Archive\Obsolete\Activate.ps1"
move "venv\Scripts\activate" "Archive\Obsolete\activate"
move "venv\Scripts\activate.bat" "Archive\Obsolete\activate.bat"
move "venv\Scripts\coverage-3.11.exe" "Archive\Obsolete\coverage-3.11.exe"
move "venv\Scripts\coverage.exe" "Archive\Obsolete\coverage.exe"
move "venv\Scripts\coverage3.exe" "Archive\Obsolete\coverage3.exe"
move "venv\Scripts\deactivate.bat" "Archive\Obsolete\deactivate.bat"
move "venv\Scripts\dotenv.exe" "Archive\Obsolete\dotenv.exe"
move "venv\Scripts\fastapi.exe" "Archive\Obsolete\fastapi.exe"
move "venv\Scripts\httpx.exe" "Archive\Obsolete\httpx.exe"
move "venv\Scripts\markdown-it.exe" "Archive\Obsolete\markdown-it.exe"
move "venv\Scripts\normalizer.exe" "Archive\Obsolete\normalizer.exe"
move "venv\Scripts\pip.exe" "Archive\Obsolete\pip.exe"
move "venv\Scripts\pip3.11.exe" "Archive\Obsolete\pip3.11.exe"
move "venv\Scripts\pip3.exe" "Archive\Obsolete\pip3.exe"
move "venv\Scripts\py.test.exe" "Archive\Obsolete\py.test.exe"
move "venv\Scripts\pygmentize.exe" "Archive\Obsolete\pygmentize.exe"
move "venv\Scripts\pyrsa-decrypt.exe" "Archive\Obsolete\pyrsa-decrypt.exe"
move "venv\Scripts\pyrsa-encrypt.exe" "Archive\Obsolete\pyrsa-encrypt.exe"
move "venv\Scripts\pyrsa-keygen.exe" "Archive\Obsolete\pyrsa-keygen.exe"
move "venv\Scripts\pyrsa-priv2pub.exe" "Archive\Obsolete\pyrsa-priv2pub.exe"
move "venv\Scripts\pyrsa-sign.exe" "Archive\Obsolete\pyrsa-sign.exe"
move "venv\Scripts\pyrsa-verify.exe" "Archive\Obsolete\pyrsa-verify.exe"
move "venv\Scripts\pytest.exe" "Archive\Obsolete\pytest.exe"
move "venv\Scripts\python.exe" "Archive\Obsolete\python.exe"
move "venv\Scripts\pythonw.exe" "Archive\Obsolete\pythonw.exe"
move "venv\Scripts\uvicorn.exe" "Archive\Obsolete\uvicorn.exe"
move "venv\Scripts\websockets.exe" "Archive\Obsolete\websockets.exe"
move "venv\pyvenv.cfg" "Archive\Obsolete\pyvenv.cfg"
move "workflow_response.txt" "Archive\Obsolete\workflow_response.txt"