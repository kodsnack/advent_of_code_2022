import 'dart:math';

import '../util/pos.dart';
import '../util/util.dart';

//const String inputFile = 'day14/example.txt';
const String inputFile = 'day14/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);
  print('Part 1:');
  print(calcResult(inputLines));

  inputLines = await readInput(inputFile);
  print('Part 2:');
  print(calcResult(inputLines, part2: true));
}

class RockLine {
  Pos startPoint;
  Pos endPoint;
  RockLine(this.startPoint, this.endPoint);

  bool inRange(int n, int n1, int n2) {
    if (n2 < n1) {
      int tmp = n1;
      n1 = n2;
      n2 = tmp;
    }
    return (n >= n1 && n <= n2);
  }

  bool pointIsOnLine(Pos point) {
    if (endPoint.y == startPoint.y) {
      // Horizontal line
      if (point.y == startPoint.y &&
          inRange(point.x, startPoint.x, endPoint.x)) {
        return true;
      }
    }
    if (endPoint.x == startPoint.x) {
      // Vertical line
      if (point.x == startPoint.x &&
          inRange(point.y, startPoint.y, endPoint.y)) {
        return true;
      }
    }
    return false;
  }
}

int calcResult(List<String> inputLines, {bool part2 = false}) {
  Grid grid = Grid(buildRockLineList(inputLines), part2: part2);
  grid.drawGrid();
  bool finished = false;
  while (!finished) {
    finished = grid.dropSand(part2: part2);
  }
  grid.drawGrid();
  return grid.restingSandList.length;
}

class Grid {
  List<RockLine> rockLines;
  List<Sand> restingSandList = [];
  Sand fallingSand = Sand();
  Range range = Range();

  int floorLevel = 0;

  Grid(this.rockLines, {bool part2 = false}) {
    for (final rockLine in rockLines) {
      range.extend(rockLine.startPoint);
      range.extend(rockLine.endPoint);
    }
    range.extend(Pos(500, 0));
    if (part2) {
      floorLevel = range.yMax + 2;
      range.yMax = floorLevel;
    }
  }

  void drawGrid() {
    for (int row = range.yMin; row <= range.yMax; row++) {
      String printLine = '$row ';
      while (printLine.length < 3) {
        printLine = ' ' + printLine;
      }
      for (int col = range.xMin; col <= range.xMax; col++) {
        String media = '.';
        if (floorLevel != 0 && row == floorLevel) {
          media = '#';
        }
        if (col == 500 && row == 0) {
          media = '+';
        }
        if (col == fallingSand.pos.x && row == fallingSand.pos.y) {
          media = 'O';
        }
        for (final rockLine in rockLines) {
          if (rockLine.pointIsOnLine(Pos(col, row))) {
            media = '#';
            break;
          }
        }
        for (Sand sand in restingSandList) {
          if (col == sand.pos.x && row == sand.pos.y) {
            media = 'o';
            break;
          }
        }
        printLine += media;
      }
      print(printLine);
    }
  }

  bool dropSand({bool part2 = false}) {
    // Check if sand source is blocked
    if (isBlocked(Pos(500, 0))) {
      return true;
    }
    fallingSand = Sand();
    bool isResting = false;
    while (!isResting) {
      //drawGrid();
      // Check pos below
      Pos nextPos = fallingSand.getPosBelow();
      if (!isBlocked(nextPos, part2: part2)) {
        fallingSand.pos = nextPos;
        // Check if we are out of range, meaning that we are dropping forever
        if (fallingSand.pos.y > range.yMax) {
          return true;
        }
        continue;
      }
      // Pos below was blocked. Check below left
      nextPos = fallingSand.getPosBelowLeft();
      range.extend(nextPos); // Extend grid if needed
      if (!isBlocked(nextPos, part2: part2)) {
        fallingSand.pos = nextPos;
        continue;
      }
      // Pos below left was blocked. Check below right
      nextPos = fallingSand.getPosBelowRight();
      range.extend(nextPos); // Extend grid if needed
      if (!isBlocked(nextPos, part2: part2)) {
        fallingSand.pos = nextPos;
        continue;
      }
      // All is blocked sand is resting
      isResting = true;
      restingSandList.add(fallingSand);
    }
    return false;
  }

  bool isBlocked(Pos nextPos, {bool part2 = false}) {
    for (final rockLine in rockLines) {
      if (rockLine.pointIsOnLine(nextPos)) {
        return true;
      }
    }
    for (Sand sand in restingSandList) {
      if (nextPos == sand.pos) {
        return true;
      }
    }
    if (part2 && nextPos.y == floorLevel) return true;
    return false;
  }
}

class Sand {
  Pos pos = Pos(500, 0);

  Pos getPosBelow() {
    return Pos(pos.x, pos.y + 1);
  }

  Pos getPosBelowLeft() {
    return Pos(pos.x - 1, pos.y + 1);
  }

  Pos getPosBelowRight() {
    return Pos(pos.x + 1, pos.y + 1);
  }
}

class Range {
  int xMin = veryLargeNumber;
  int xMax = -veryLargeNumber;
  int yMin = veryLargeNumber;
  int yMax = -veryLargeNumber;

  void extend(Pos point) {
    xMin = min(xMin, point.x);
    xMax = max(xMax, point.x);
    yMin = min(yMin, point.y);
    yMax = max(yMax, point.y);
  }
}

List<RockLine> buildRockLineList(List<String> inputLines) {
  List<RockLine> rockLines = [];
  for (final inputLine in inputLines) {
    final lineParts = inputLine.split('->');
    int xStart = int.parse(lineParts[0].split(',')[0].trim());
    int yStart = int.parse(lineParts[0].split(',')[1].trim());
    Pos lineStart = Pos(xStart, yStart);
    lineParts.removeAt(0);
    while (lineParts.isNotEmpty) {
      int xEnd = int.parse(lineParts[0].split(',')[0].trim());
      int yEnd = int.parse(lineParts[0].split(',')[1].trim());
      Pos lineEnd = Pos(xEnd, yEnd);
      rockLines.add(RockLine(lineStart, lineEnd));
      lineStart = Pos(xEnd, yEnd);
      lineParts.removeAt(0);
    }
  }
  return rockLines;
}
