from PIL import Image, ImageDraw

# Tamanho da imagem
width, height = 320, 240

# Criar imagem com fundo transparente
img = Image.new('RGBA', (width, height), (0, 0, 0, 255))
draw = ImageDraw.Draw(img)

# Desenhar fundo preto (noite)
draw.rectangle([0, 0, width, height], fill=(10, 10, 30))

# Desenhar lua cheia (círculo branco-amarelado)
moon_center = (260, 60)
moon_radius = 30
draw.ellipse([moon_center[0]-moon_radius, moon_center[1]-moon_radius,
              moon_center[0]+moon_radius, moon_center[1]+moon_radius],
             fill=(255, 255, 220))

# Janela do castelo - moldura grossa cinza escuro
window_x0, window_y0 = 40, 40
window_x1, window_y1 = 200, 180
frame_color = (50, 50, 60)
draw.rectangle([window_x0-10, window_y0-10, window_x1+10, window_y1+10], fill=frame_color)

# Grades da janela - linhas verticais e horizontais
for x in range(window_x0, window_x1, 20):
    draw.line([(x, window_y0), (x, window_y1)], fill=(30, 30, 40))
for y in range(window_y0, window_y1, 20):
    draw.line([(window_x0, y), (window_x1, y)], fill=(30, 30, 40))

# Dentro da janela - céu noturno (mais escuro que o fundo)
draw.rectangle([window_x0, window_y0, window_x1, window_y1], fill=(0, 0, 15))

# Lápides - retângulos com "cabeça" arredondada
tombstone_color = (60, 60, 60)
tombstones = [(60, 150), (120, 140), (170, 160)]
for tx, ty in tombstones:
    # corpo
    draw.rectangle([tx, ty, tx+20, ty+40], fill=tombstone_color)
    # topo arredondado
    draw.ellipse([tx, ty-10, tx+20, ty+10], fill=tombstone_color)

# Aranhas simples - pequenos quadrados pretos com linhas como patas
spider_color = (0, 0, 0)
spiders = [(100, 200), (180, 190)]
for sx, sy in spiders:
    # corpo
    draw.ellipse([sx, sy, sx+10, sy+10], fill=spider_color)
    # patas (4 linhas simples)
    draw.line([(sx, sy+5), (sx-5, sy)], fill=spider_color)
    draw.line([(sx, sy+5), (sx-5, sy+10)], fill=spider_color)
    draw.line([(sx+10, sy+5), (sx+15, sy)], fill=spider_color)
    draw.line([(sx+10, sy+5), (sx+15, sy+10)], fill=spider_color)

# Salvar imagem
img.save("castelo_noite_pixelart.png")
print("Imagem castelo_noite_pixelart.png gerada!")
