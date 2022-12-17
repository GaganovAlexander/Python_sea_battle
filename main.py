from field import *
import socket as sk


client = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
client.connect(("127.0.0.1", 10666))

pg.init()
screen = pg.display.set_mode((1900, 1000))
screen.fill((150, 150, 150))
my_field = Field(screen, 150, 100)
oponents_field = Field(screen, screen.get_width() - CELL_WIDTH*10 - 150, 100)


run = True
preparation = 2
complited = False
first_turn = False
end = False
while run:    
    if complited:
        if not first_turn:
            data = client.recv(1024).decode("utf-8")
            if data[0] not in 'wl':
                data = list(map(int, data))
                my_field.field[data[0]][data[1]] = data[2]
            elif data[0] == 'w':
                client.close()
                end = True
                win = True
                break
            else:
                client.close()
                end = True
                win = False
                break
        if not end:
            first_turn = False
            pos = None
            while not pos:
                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        run = False
                    if event.type == pg.MOUSEBUTTONDOWN:
                        pos = oponents_field.get_pos(event.pos)
            client.send(pos.encode("utf-8"))
            data = client.recv(1024).decode("utf-8")
            if data[0] not in 'wl':
                oponents_field.field[int(pos[0])][int(pos[1])] = int(data)
            elif data[0] == 'w':
                client.close()
                end = True
                win = True
                break
            else:
                client.close()
                end = True
                win = False
                break

    else:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN and preparation:
                if my_field.check(event.pos, 2):
                    preparation -= 1

        if not complited and not preparation:
            my_field.draw()
            pg.display.flip()
            client.send(''.join([''.join(map(str, my_field.field[i])) for i in range(10)]).encode("utf-8"))
            complited = client.recv(1024).decode('utf-8')
            if complited == '1':
                first_turn = True
            complited = True
    

    oponents_field.draw()
    my_field.draw()
    pg.display.flip()

oponents_field.draw()
my_field.draw()
pg.display.flip()
updated = False
if end:
    font1 = pg.font.Font(None, 300)
    run = True
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                run = False

        screen.fill((150, 150, 150))
        if win:
            yw = font1.render('YOU WON!', True, (0, 255, 0))
            screen.blit(yw, ((screen.get_width() - yw.get_width())//2, (screen.get_height()- yw.get_height())//2))
        else:   
            yl = font1.render('YOU LOSE!', True, (255, 0, 0))
            screen.blit(yl, ((screen.get_width() - yl.get_width())//2, (screen.get_height()- yl.get_height())//2))
        if not updated:
            pg.display.flip()
            updated = True

client.close()
pg.quit()
