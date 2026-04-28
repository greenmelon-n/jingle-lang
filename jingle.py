# -*- coding: utf-8 -*-

class JingleInterpreter:
    def __init__(self):
        self.переменные = {}
        self.отладка = False
        self.в_блоке_если = False
        self.выполнять = True
        self.условие_верно = False
        self.жду_иначе = False
   
    def запустить_файл(self, имя_файла):
        with open(имя_файла, 'r', encoding='utf-8-sig') as f:
            строки = f.readlines()
       
        i = 0
        while i < len(строки):
            строка = строки[i].strip()
            i += 1
            if not строка:
                continue
           
            # Обработка команд, которые всегда выполняются (меняют состояние)
           
            # Команда "включить отладку"
            if строка == 'включить отладку':
                self.отладка = True
                if self.отладка:
                    print("[ОТЛАДКА] Режим отладки включён")
                continue
           
            if строка == 'выключить отладку':
                self.отладка = False
                continue
           
            # Команда "если"
            if строка.startswith('если') and 'то' in строка:
                # Извлекаем условие
                условие = строка[5:строка.find('то')].strip()
                if self.отладка:
                    print(f"[ОТЛАДКА] Условие: {условие}")
               
                # Подставляем переменные
                выраж = условие
                for var, val in self.переменные.items():
                    if var in выраж:
                        выраж = выраж.replace(var, str(val))
               
                # Вычисляем условие
                try:
                    результат = eval(выраж)
                    self.условие_верно = bool(результат)
                    self.выполнять = self.условие_верно
                    self.в_блоке_если = True
                    self.жду_иначе = False
                    if self.отладка:
                        print(f"[ОТЛАДКА] Условие верно: {self.условие_верно}, выполняем={self.выполнять}")
                except:
                    print(f"Ошибка в условии: {условие}")
                    self.выполнять = False
                continue
           
            # Команда "иначе"
            if строка == 'иначе' and self.в_блоке_если and not self.жду_иначе:
                self.выполнять = not self.условие_верно
                self.жду_иначе = True
                if self.отладка:
                    print(f"[ОТЛАДКА] Переход в иначе, выполняем={self.выполнять}")
                continue
           
            # Команда "все" (закрывает если)
            if строка == 'все' and self.в_блоке_если:
                self.в_блоке_если = False
                self.выполнять = True
                self.жду_иначе = False
                if self.отладка:
                    print("[ОТЛАДКА] Выход из блока если")
                continue
           
            # Если мы внутри блока если/иначе и выполнять=False, пропускаем строку
            if self.в_блоке_если and not self.выполнять:
                if self.отладка:
                    print(f"[ОТЛАДКА] Пропускаем: {строка}")
                continue
           
            # Обычные команды (переменная, скажи)
            if строка.startswith('переменная'):
                if self.отладка:
                    print(f"[ОТЛАДКА] Нашёл переменную: {строка}")
                остаток = строка[11:].strip()
                if '=' in остаток:
                    имя, значение = остаток.split('=', 1)
                    имя = имя.strip()
                    значение = значение.strip()
                   
                    if self.отладка:
                        print(f"[ОТЛАДКА] Имя: '{имя}', Значение: '{значение}'")
                   
                    if значение in self.переменные:
                        self.переменные[имя] = self.переменные[значение]
                    elif значение.startswith('"') and значение.endswith('"'):
                        self.переменные[имя] = значение[1:-1]
                    elif значение.isdigit():
                        self.переменные[имя] = int(значение)
                    elif any(оп in значение for оп in ['+', '-', '*', '/']):
                        выражение = значение
                        for var, val in self.переменные.items():
                            if var in выражение:
                                выражение = выражение.replace(var, str(val))
                        try:
                            результат = eval(выражение)
                            self.переменные[имя] = результат
                        except:
                            self.переменные[имя] = значение
                    else:
                        self.переменные[имя] = значение
           
            elif строка.startswith('скажи'):
                текст = строка[5:].strip()
                if текст.startswith('"') and текст.endswith('"'):
                    print(текст[1:-1])
                elif any(оп in текст for оп in ['+', '-', '*', '/']):
                    выражение = текст
                    for var, val in self.переменные.items():
                        if var in выражение:
                            выражение = выражение.replace(var, str(val))
                    try:
                        результат = eval(выражение)
                        print(результат)
                    except:
                        print(f"Ошибка в выражении: {текст}")
                elif текст in self.переменные:
                    print(self.переменные[текст])
                else:
                    print(текст)
           
            else:
                print(f"Неизвестная команда: {строка}")

if __name__ == '__main__':
    j = JingleInterpreter()
    j.запустить_файл('программа.jingle')
