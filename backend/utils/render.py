from PIL import Image, ImageDraw, ImageFilter

GRID_SIZE = 20
GRID = [[("", "", 0) for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]
GRID[0][0] = ("SQUARE", "RED", None)
GRID[1][1] = ("CIRCLE", "GREEN", None)
GRID[2][2] = ("TRIANGLE", "BLUE", None)
GRID[3][3] = ("SQUARE", "GREEN", None)
SCALE = 200  # number of pixels per cell

def drawGrid(draw, scale, rows, cols):
  for i in range(rows):
    draw.line([i*SCALE, 0, i*SCALE, rows*SCALE], fill=(0,0,0), width=1)
  for i in range(cols):
    draw.line([0, i*SCALE, cols*SCALE, i*SCALE], fill=(0,0,0), width=1)

def drawShape(draw, i, j, shape):
  shape_name = shape[0]
  color_name = shape[1]
  color = (0, 0, 0)
  print(color_name)

  if color_name == "RED":
    color = (255, 0, 0)
  elif color_name == "GREEN":
    color = (0, 255, 0)
  elif color_name == "BLUE":
    color = (0, 0, 255)

  if shape_name == "CIRCLE":
    draw.ellipse([i*SCALE,j*SCALE, (i+1)*SCALE, (j+1)*SCALE], fill=color, outline=(0, 0, 0), width=1)
  elif shape_name == "SQUARE":
    draw.rectangle([i*SCALE,j*SCALE, (i+1)*SCALE, (j+1)*SCALE], fill=color, outline=(0, 0, 0), width=1)
  elif shape_name == "TRIANGLE":
    top = ((i*SCALE)+int(SCALE/2), (j*SCALE))
    bottom_left = (i*SCALE, (j+1)*SCALE)
    bottom_right = ((i+1)*SCALE, (j+1)*SCALE)
    draw.polygon([top, bottom_left, bottom_right], fill=color, outline=(0, 0, 0))


def renderEnvironment(env):
    rows = len(env)
    cols = len(env[0])
    im = Image.new('RGB', (rows*SCALE, cols*SCALE), (255, 255, 255))
    draw = ImageDraw.Draw(im)
    for i in range(rows):
        for j in range(cols):
            if env[i][j][0] != "":
                drawShape(draw, i, j, env[i][j])
    im.filter(ImageFilter.GaussianBlur(100))
    drawGrid(draw, SCALE, rows, cols)
    im.show()

    print(im.format, im.size, im.mode)


renderEnvironment(GRID)
