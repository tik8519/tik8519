def move(n, old_kernel=1, new_kernel=3):
    if n == 1:
        print(f'Переложить диск {n} со стержня номер {old_kernel} на стержень номер {new_kernel}')
        return
    move(n-1, old_kernel=old_kernel, new_kernel=6-old_kernel-new_kernel)
    print(f'Переложить диск {n} со стержня номер {old_kernel} на стержень номер {new_kernel}')
    move(n-1, old_kernel=6-old_kernel-new_kernel, new_kernel=new_kernel)


if __name__ == '__main__':
    disc_num = int(input('Введите количество дисков: '))
    move(disc_num)
