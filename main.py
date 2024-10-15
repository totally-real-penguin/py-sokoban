from json import loads
from os import system

system("")

COLOR = {
    "HEADER": "\033[95m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "RED": "\033[91m",
    "ENDC": "\033[0m",
}

player_pos = []
boxes = []
walls = []
map_size = []
flag_pos = []

bounds = []

level = 1

rewind = []


def print_map() -> None:
  print("Level " + str(level))
  for y in range(0, map_size[1]):
    line = ""
    for x in range(0, map_size[0]):
      if [x, y] == player_pos:
        line += COLOR["GREEN"] + "@ " + COLOR["ENDC"]
      elif [x, y] in boxes:
        line +=  "# "
      elif [x, y] in walls:
        line += COLOR["RED"] + "X " + COLOR["ENDC"]
      elif [x, y] == flag_pos:
        line += COLOR["GREEN"] + "F " + COLOR["ENDC"]
      else:
        line += COLOR["BLUE"] + "O " + COLOR["ENDC"]
    print(line)


def load_map() -> bool:
  global player_pos, boxes, walls, map_size, flag_pos, bounds, rewind

  try:
    file = open("level-" + str(level) + ".json", "r")
    data = loads(file.read())
    file.close()

  except FileNotFoundError:
    return False

  player_pos = data["player_pos"]
  boxes = data["boxes"]
  walls = data["walls"]
  map_size = data["map_size"]
  flag_pos = data["flag_pos"]
  rewind = []

  bounds = [[-1, map_size[0]], [-1, map_size[1]]]

  return True


def move_box(dir, box) -> bool:
  next_pos = [box[0] + dir[0], box[1] + dir[1]]
  if next_pos not in walls and next_pos not in boxes:
    if next_pos[0] not in bounds[0] and next_pos[1] not in bounds[
        1] and next_pos != flag_pos:
      for i in range(0, len(boxes)):
        if boxes[i] == box:
          boxes[i] = next_pos
          return True
  return False


def move_player(dir):
  global player_pos, rewind
  next_pos = [player_pos[0] + dir[0], player_pos[1] + dir[1]]
  if next_pos in walls or next_pos[0] in bounds[0] or next_pos[1] in bounds[1]:
    pass
  elif next_pos in boxes:
    box_moved = move_box(dir, next_pos)
    if box_moved is True:
      player_pos = next_pos
  else:
    player_pos = next_pos
  save_frame()


def undo() -> None:
  global player_pos, boxes, walls, flag_pos, rewind
  if len(rewind) > 1:
    last_frame = rewind[-2]
    player_pos = last_frame[0]
    boxes = last_frame[1].copy()
    rewind.pop(-1)


def save_frame() -> None:
  global rewind, boxes, player_pos
  rewind.append([player_pos, boxes.copy()])


has_level = load_map()

while has_level is True:
  save_frame()
  while player_pos != flag_pos:
    print_map()

    inp = input("Enter Direction: ")
    dir = [0, 0]
    sleep = False

    if inp == "w":
      dir = [0, -1]
    elif inp == "s":
      dir = [0, 1]
    elif inp == "a":
      dir = [-1, 0]
    elif inp == "d":
      dir = [1, 0]
    elif inp == "u":
      undo()
      sleep = True
    else:
      sleep = True
    if not sleep:
      move_player(dir)
  print_map()
  level += 1
  has_level = load_map()
