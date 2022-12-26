import '../util/pos.dart';
import '../util/util.dart';

//const String inputFile = 'day17/example.txt';
const String inputFile = 'day17/input.txt';

const bool noDraw = false;
Future<void> main(List<String> args) async {
  var inputLine = await readInput(inputFile);
  print('Part 1:');
  print(calcResultP1(inputLine[0]));
  inputLine = await readInput(inputFile);
  print('Part 2:');
  print(calcResultP2(inputLine[0]));
}

int calcResultP1(String jetStreams) {
  Grid grid = Grid(jetStreams);
  int noOfRocksToDrop = 2022;
  for (int i = 0; i < noOfRocksToDrop; i++) {
    grid.dropRock();
  }
  return grid.topLevel();
}

int calcResultP2(String jetStreams) {
  Grid grid = Grid(jetStreams);
  int noOfRocksToDrop = 1000000000000;
  int shapeCycleLength = grid.shapeList.length;

  int count = 0;
  CycleChecker cycleChecker = CycleChecker(15);
  bool foundCycle = false;

  List<int> topLevels = [];

  while (!foundCycle) {
    for (int i = 0; i < shapeCycleLength; i++) {
      grid.dropRock();
      topLevels.add(grid.topLevel());
      count++;
    }
    foundCycle = cycleChecker.checkGridTop(grid, count, grid.jetStreamIndex);
    print('Top level ${grid.topLevel()}');
    print('Rock count : $count');
    grid.drawGrid();
    print('--');
  }

  // Top of stack at beginning of cycle
  int topOfStackAtBeginningOfCycle =
      topLevels[cycleChecker.rockCountAtFirstMatch];
  int topOfStackAtEndOfCycle = grid.topLevel();
  int cycleHeight = topOfStackAtEndOfCycle - topOfStackAtBeginningOfCycle;

  int noOfRocksDroppedPerCycle =
      cycleChecker.rockCountAtNextMatch - cycleChecker.rockCountAtFirstMatch;
  int noOfNeededCycles =
      (noOfRocksToDrop - cycleChecker.rockCountAtFirstMatch) ~/
          noOfRocksDroppedPerCycle;
  int totalHeight =
      topOfStackAtBeginningOfCycle + noOfNeededCycles * cycleHeight;
  int rest = noOfRocksToDrop -
      noOfRocksDroppedPerCycle * noOfNeededCycles -
      cycleChecker.rockCountAtFirstMatch;
  print('Total height if rest is 0 : $totalHeight');
  print('Rest : $rest');
  grid.jetStreamIndex = cycleChecker.jetStreamIndexAtNextMatch;
  int stackHeightBeforeLastPart = grid.topLevel();
  for (int i = 0; i < rest; i++) {
    grid.dropRock();
  }
  int restStackHeight = grid.topLevel() - stackHeightBeforeLastPart;
  return totalHeight + restStackHeight - 1;
}

class CycleChecker {
  int gridSize;
  List<List<String>> cycles = [];
  List<int> counts = [];
  List<int> jetStreamIndexes = [];

  int firstMatch = 0;
  int nextMatch = 0;

  int rockCountAtFirstMatch = 0;
  int rockCountAtNextMatch = 0;

  int jetStreamIndexAtNextMatch = 0;

  int jetStreamIndexAtFirstMatch = 0;

  CycleChecker(this.gridSize);

  bool checkGridTop(Grid grid, int count, int jetStreamIndex) {
    int gridTopLevel = grid.topLevel();
    if (gridTopLevel < gridSize) return false;
    List<String> gridTop =
        grid.gridLines.sublist(gridTopLevel - gridSize, gridTopLevel);
    if (cycles.isEmpty) {
      cycles.add(gridTop);
      counts.add(count - 1);
      jetStreamIndexes.add(jetStreamIndex);
    } else {
      int matchIdx = foundMatch(gridTop, jetStreamIndex);
      if (matchIdx >= 0) {
        print('Found topMatch');
        firstMatch = matchIdx;
        nextMatch = cycles.length;
        print('Cycle $matchIdx matches gridTop at $count');
        print('Cycle $matchIdx has rock count ${counts[matchIdx]}');
        rockCountAtFirstMatch = counts[matchIdx];
        rockCountAtNextMatch = count - 1;
        jetStreamIndexAtFirstMatch = jetStreamIndexes[matchIdx];
        jetStreamIndexAtNextMatch = jetStreamIndexes[matchIdx];
        grid.gridCycleSize = count - counts[matchIdx];
        return true;
      } else {
        cycles.add(gridTop);
        counts.add(count - 1);
        jetStreamIndexes.add(jetStreamIndex);
      }
    }
    return false;
  }

  int foundMatch(List<String> gridTop, int jetstreamIndex) {
    for (int matchingCycleNo = 0;
        matchingCycleNo < cycles.length;
        matchingCycleNo++) {
      bool equal = true;
      for (int i = 0; i < gridSize; i++) {
        if (cycles[matchingCycleNo][i] != gridTop[i]) {
          equal = false;
          break;
        }
      }
      if (equal) {
        if (jetstreamIndex != jetStreamIndexes[matchingCycleNo]) {
          equal = false;
          break;
        }
      }

      if (equal) return matchingCycleNo;
    }
    return -1;
  }
}

class Grid {
  int gridWidth = 7;
  List<String> gridLines = [];
  List<Shape> shapeList = buildShapeList();
  int shapeIndex = 0;

  late List<String> jetStreamList;
  int jetStreamIndex = 0;

  Shape? currentShape;
  Pos currentShapePos = Pos(0, 0);

  int gridCycleSize = 0;

  Grid(String jetStreams) {
    jetStreamList = jetStreams.split('');
  }

  int topLevel() {
    return gridLines.length;
  }

  void dropRock() {
    bool stopped = false;
    while (!stopped) {
      stopped = fall();
      if (stopped) continue;
      final jetStream = getNextJetstream();
      if (jetStream == '<') {
        moveLeft();
      } else {
        // >
        moveRight();
      }
    }
  }

  void selectShape() {
    currentShape = shapeList[shapeIndex];
    shapeIndex++;
    shapeIndex = shapeIndex % shapeList.length;
    currentShapePos = Pos(2, topLevel() + 3);
  }

  void moveLeft() {
    Pos newPos = currentShapePos.moveLeft();
    if (newPos.x < 0) {
      // Out of bounds
      return;
    }
    if (collidesAt(newPos)) {
      // Cannot move left
      return;
    }
    // We could move. Set new position
    currentShapePos = newPos;
  }

  void moveRight() {
    Pos newPos = currentShapePos.moveRight();
    if (newPos.x + currentShape!.width > gridWidth) {
      // Out of bounds
      return;
    }
    if (collidesAt(newPos)) {
      // Cannot move right
      return;
    }
    // We could move. Set new position
    currentShapePos = newPos;
  }

  bool fall() {
    if (currentShape == null) {
      // No shape. Select a new and drop it at start pos
      selectShape();
      return false;
    }
    ;
    // Check shape
    if (currentShapePos.y > topLevel() + 1) {
      // No problem to move down
      currentShapePos = currentShapePos.moveDown();
      return false;
    } else {
      //Shape is in grid. Try to move down and check if we have a collision
      final newShapePos = currentShapePos.moveDown();
      // If we are at the bottom we add it to the grid
      if (newShapePos.y < 0) {
        addShapeToGrid();
        currentShape = null;
        return true;
      }
      bool collides = collidesAt(newShapePos);
      if (collides) {
        // If we move down we collide so we need to copy shape in at currPos
        addShapeToGrid();
        currentShape = null;
        return true;
      }
      currentShapePos = newShapePos;
    }
    return false;
  }

  getNextJetstream() {
    String jetStream = jetStreamList[jetStreamIndex];
    jetStreamIndex++;
    jetStreamIndex %= jetStreamList.length;
    return jetStream;
  }

  bool collidesAt(Pos pos) {
    if (pos.y > topLevel()) return false;
    for (int yOffs = 0; yOffs < currentShape!.height; yOffs++) {
      if (pos.y + yOffs >= gridLines.length)
        return false; // No gridlines to check here. We are ready
      final shapeLineAsList = currentShape!.shape[yOffs].split('');
      final gridLineAsList = gridLines[pos.y + yOffs].split('');
      for (int shapeCol = 0; shapeCol < currentShape!.width; shapeCol++) {
        final shapeChar = shapeLineAsList[shapeCol];
        int gridCol = pos.x + shapeCol;
        final gridChar = gridLineAsList[gridCol];
        if (shapeChar != '.' && gridChar != '.') {
          return true;
        }
      }
    }
    return false;
  }

  void addShapeToGrid() {
    for (int yOffs = 0; yOffs < currentShape!.height; yOffs++) {
      if (currentShapePos.y + yOffs >= gridLines.length) {
        // We need to extend the grid.
        gridLines.add(List.generate(gridWidth, (_) => '.')
            .join()); // Adds '.......' with a gridWidth of 7
      }

      final shapeLineAsList = currentShape!.shape[yOffs].split('');
      final gridLineAsList = gridLines[currentShapePos.y + yOffs].split('');
      for (int xOffs = 0; xOffs < currentShape!.width; xOffs++) {
        if (shapeLineAsList[xOffs] != '.') {
          gridLineAsList[currentShapePos.x + xOffs] = '#';
        }
      }
      gridLines[currentShapePos.y + yOffs] = gridLineAsList.join();
    }
  }

  void drawGrid() {
    if (noDraw) return;

    int upperDraw = topLevel() + 3;
    int lowerDraw = topLevel() - 21;

    if (currentShape != null) {
      upperDraw = currentShapePos.y + 4;
      lowerDraw = currentShapePos.y - 21;
    }
    if (lowerDraw < 0) lowerDraw = 0;
    for (int y = upperDraw; y >= lowerDraw; y--) {
      String startOfLine = '$y |';
      while (startOfLine.length < 7) {
        startOfLine = ' ' + startOfLine;
      }

      List<String> startOfLineAsList = startOfLine.split('');
      List<String> lineAsList = List.generate(gridWidth, (_) => '.');

      if (currentShape != null) {
        if (y >= currentShapePos.y &&
            y < currentShapePos.y + currentShape!.height) {
          for (int x = 0; x < currentShape!.width; x++) {
            lineAsList[currentShapePos.x + x] =
                currentShape!.shape[y - currentShapePos.y][x];
          }
        }
      }

      if (y < gridLines.length) {
        final gridLineAsList = gridLines[y].split('');
        for (var x = 0; x < gridWidth; x++) {
          if (gridLineAsList[x] != '.') {
            lineAsList[x] = '#';
          }
        }
      }

      lineAsList.add('|');

      print(startOfLineAsList.join() + lineAsList.join());
    }

    if (lowerDraw == 0) {
      String startOfLine = '      |';
      List<String> lineAsList = startOfLine.split('');
      lineAsList.addAll(List.generate(gridWidth, (_) => '='));
      lineAsList.add('|');
      print(lineAsList.join());
    }
    print('');
  }
}

List<Shape> buildShapeList() {
  Shape s1 = Shape(['@@@@']);
  Shape s2 = Shape([
    '.@.',
    '@@@',
    '.@.',
  ]);

  // This one looks upside down because index 0 is at the bottom of the shape
  Shape s3 = Shape([
    '@@@',
    '..@',
    '..@',
  ]);
  Shape s4 = Shape([
    '@',
    '@',
    '@',
    '@',
  ]);
  Shape s5 = Shape([
    '@@',
    '@@',
  ]);
  return [s1, s2, s3, s4, s5];
}

class Shape {
  List<String> shape;

  Shape(this.shape);
  int get width {
    return shape[0].length;
  }

  int get height {
    return shape.length;
  }
}
