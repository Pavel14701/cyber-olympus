import subprocess
import os
import re

pattern = '.ts'
ts_file = 'test.ts'
file_name = re.sub(pattern, '', ts_file)

# Папка с исходными файлами TypeScript
src_dir = f'static\\ts\\{ts_file}'
# Папка для сохранения скомпилированных файлов
dist_dir = f'static\\{file_name}\\js'

# Убедитесь, что папка dist существует
if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

try:
    # Команда для компиляции TypeScript
    command = ['npx', 'tsc', '--outDir', dist_dir, src_dir]
    # Выполнение команды
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    # Проверка на ошибки
    if result.returncode == 0:
        print("Команда выполнена успешно")
        print(result.stdout)
    else:
        print("Ошибка выполнения команды")
        print(f"Код возврата: {result.returncode}")
        print(f"Стандартный вывод: {result.stdout}")
        print(f"Стандартный вывод ошибок: {result.stderr}")
except Exception as e:
    print(f"Произошла ошибка: {e}")
