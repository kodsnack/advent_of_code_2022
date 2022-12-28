import '../util/linepos.dart';
import '../util/util.dart';

//const String inputFile = 'day22/example.txt';
const String inputFile = 'day22/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);

  print('Part 1:');
  int resultP1 = calcResultP1(inputLines);
  print(resultP1);

  print('Part 2:');
  int resultP2 = calcResultP2(inputLines);
  print(resultP2);
}

int calcResultP1(List<String> inputLines) {
  List<List<String>> gridLines = [];
  for (final line in inputLines) {
    if (line.isEmpty) break;
    List<String> gridLine = line.split('');
    gridLines.add(gridLine);
  }

  Grid grid = Grid(gridLines, inputLines.last);
  grid.draw();
  grid.doMoves();

  return 1000 * (grid.myPos.row + 1) +
      4 * (grid.myPos.col + 1) +
      getDirPoints(grid.myDirection);
}

int calcResultP2(List<String> inputLines) {
  List<List<String>> gridLines = [];
  for (final line in inputLines) {
    if (line.isEmpty) break;
    List<String> gridLine = line.split('');
    gridLines.add(gridLine);
  }

  Grid grid = Grid(gridLines, inputLines.last);
  //printing = true;
  grid.draw();
  grid.doTests();
  grid.doMovesP2();

  return 1000 * (grid.myPos.row + 1) +
      4 * (grid.myPos.col + 1) +
      getDirPoints(grid.myDirection);
}

int getDirPoints(Direction dir) {
  return [Direction.Right, Direction.Down, Direction.Left, Direction.Up]
      .indexOf(dir);
}

bool printing = false;

class PosAndDir {
  LinePos pos;
  Direction direction;

  PosAndDir(this.pos, this.direction);
}

class Grid {
  List<List<String>> grid;
  String commandStr;
  LinePos myPos = LinePos(0, 0);
  Direction myDirection = Direction.Right;

  int gridSize = 50;

  Grid(this.grid, this.commandStr) {
    final firstGridLine = grid.first;
    for (int x = 0; x < firstGridLine.length; x++) {
      if (firstGridLine[x] != ' ') {
        myPos = LinePos(x, 0);
        break;
      }
    }
  }

  draw() {
    if (!printing) return;
    int rowStart = myPos.row - 10;
    if (rowStart < 0) rowStart = 0;
    int rowEnd = myPos.row + 10;
    if (rowEnd > grid.length) rowEnd = grid.length;
    for (int rowNo = rowStart; rowNo < rowEnd; rowNo++) {
      List<String> gridLine = List.from(grid[rowNo]);
      if (myPos.row == rowNo) {
        final dirChar = getDirChar(myDirection);
        gridLine[myPos.col] = dirChar;
      }
      print(gridLine.join());
    }
    print(' ');
    print(' ');
  }

  getDirChar(Direction dir) {
    return ['^', '>', 'v', '<'].elementAt(dir.index);
  }

  void doMoves() {
    final commandList = commandStr.split('');
    while (commandList.isNotEmpty) {
      num dist = 0;
      while (commandList.isNotEmpty && isDigit(commandList.first, 0)) {
        dist = dist * 10 + num.parse(commandList.removeAt(0));
      }
      moveDist(dist, myDirection);
      //draw();
      while (commandList.isNotEmpty && !isDigit(commandList.first, 0)) {
        myDirection = changeDir(myDirection, commandList.removeAt(0));
      }
      draw();
    }
  }

  void doMovesP2() {
    final commandList = commandStr.split('');
    while (commandList.isNotEmpty) {
      num dist = 0;
      while (commandList.isNotEmpty && isDigit(commandList.first, 0)) {
        dist = dist * 10 + num.parse(commandList.removeAt(0));
      }
      if (printing) print('Dist $dist');
      final posAndDir = moveDistP2(dist, myDirection);
      //myDirection = posAndDir.direction;
      draw();
      while (commandList.isNotEmpty && !isDigit(commandList.first, 0)) {
        if (printing) print('Turn ${commandList.first}');
        myDirection = changeDir(myDirection, commandList.removeAt(0));
      }
      draw();
    }
  }

  void moveDist(num dist, Direction dir) {
    for (var i = 0; i < dist; i++) {
      var newPos = myPos.moveDir(dir);
      newPos = wrapAroundMaybe(newPos, dir);
      String elAtNewPos = grid[newPos.row][newPos.col];
      if (elAtNewPos == '#') break; // Found block. Just stop
      myPos = newPos;
      draw();
    }
  }

  PosAndDir moveDistP2(num dist, Direction dir) {
    PosAndDir posAndDir = PosAndDir(myPos, dir);
    for (var i = 0; i < dist; i++) {
      posAndDir = wrapAroundMaybeP2(myPos, myPos.moveDir(dir), dir);
      var newPos = posAndDir.pos;
      var newDir = posAndDir.direction;
      String elAtNewPos = grid[newPos.row][newPos.col];
      if (elAtNewPos == '#') break; // Found block. Just stop
      myPos = newPos;
      dir = newDir;
      myDirection = dir;
      draw();
      if (printing) print(i);
    }
    return posAndDir;
  }

  LinePos wrapAroundMaybe(LinePos newPos, Direction dir) {
    switch (dir) {
      case Direction.Up:
        if (newPos.row < 0 || newPos.row < findHighestRowAt(newPos.col)) {
          newPos = LinePos(newPos.col, findLowestRowAt(newPos.col));
        }
        break;
      case Direction.Right:
        if (newPos.col > grid[newPos.row].length - 1) {
          newPos = LinePos(
            findLeftMostColAt(newPos.row),
            newPos.row,
          );
        }
        break;
      case Direction.Down:
        if (newPos.row > findLowestRowAt(newPos.col)) {
          newPos = LinePos(newPos.col, findHighestRowAt(newPos.col));
        }
        break;
      case Direction.Left:
        if (newPos.col < 0 || newPos.col < findLeftMostColAt(newPos.row)) {
          newPos = LinePos(findRightMostColAt(newPos.row), newPos.row);
        }
        break;
    }
    return newPos;
  }

/*
    1  R -> 2 -
    1  D -> 3 -
    1  L -> 4 - Dir L -> R Pos R -> -R
    1  U -> 6 - Dir U -> R Pos C -> R
    2  L -> 1 -
    2  D -> 3 - Dir D -> L Pos C -> R 
    2  R -> 5 - Dir R -> L Pos R -> -R
    2  U -> 6 - Dir U -> U Pos C -> C
    3  U -> 1 - 
    3  D -> 5 - 
    3  L -> 4 - Dir L -> D Pos R -> C
    3  R -> 2 - Dir R -> U Pos R -> C
    4  U -> 3 - Dir U -> R Pos C -> R
    4  R -> 5 - 
    4  D -> 6 -
    4  L -> 1 - Dir L -> R Pos R -> -R
    5  U -> 3 - 
    5  L -> 4 -
    5  R -> 2 - Dir R -> L Pos R -> -R
    5  D -> 6 - Dir D -> L Pos C -> R
    6  U -> 4 -
    6  R -> 5 - Dir R -> U Pos R -> C
    6  L -> 1 - Dir L -> D Pos R -> C
    6  D -> 2 - Dir D -> D Pos C -> C
  */
  PosAndDir wrapAroundMaybeP2(LinePos oldPos, LinePos newPos, Direction dir) {
    // Moving up
    if (dir == Direction.Up) {
      // Check if we are out of bounds
      if (newPos.row < 0 || newPos.row < findHighestRowAt(newPos.col)) {
        // We are on face 1, 2 or 4
        int oldFaceNo = getFaceNo(oldPos);
        if (oldFaceNo == 1) {
          // Moving face 1 -> 6
          LinePos newPosOnFace6 = LinePos(0, oldPos.col + gridSize * 2);
          assert(getFaceNo(newPosOnFace6) == 6);
          return PosAndDir(newPosOnFace6, Direction.Right);
        }
        if (oldFaceNo == 2) {
          // Face 2 -> 6
          LinePos newPosOnFace6 =
              LinePos(oldPos.col - gridSize * 2, gridSize * 4 - 1);
          assert(getFaceNo(newPosOnFace6) == 6);
          return PosAndDir(newPosOnFace6, Direction.Up);
        }
        if (oldFaceNo == 4) {
          // Face 4 -> 3
          final newPosOnFace3 = LinePos(gridSize, gridSize + oldPos.col);
          assert(getFaceNo(newPosOnFace3) == 3);
          return PosAndDir(newPosOnFace3, Direction.Right);
        }
        // Should not get here
        print('!! up');
        assert(false);
      } else {
        // No wrapping needed. Return the new position
        return PosAndDir(newPos, dir);
      }
    }

    // Moving right
    if (dir == Direction.Right) {
      // Check if new pos is out of bounds
      if (newPos.col > grid[newPos.row].length - 1) {
        // Old pos are on face 2,3, 5 or 6
        int oldFaceNo = getFaceNo(oldPos);
        if (oldFaceNo == 2) {
          // Face 2 -> 5
          final newPosOnFace5 = LinePos(
              gridSize * 2 - 1, gridSize - oldPos.row + gridSize * 2 - 1);
          assert(getFaceNo(newPosOnFace5) == 5);
          return PosAndDir(newPosOnFace5, Direction.Left);
        }
        if (oldFaceNo == 3) {
          // Face 3 -> 2
          final newPosOnFace2 = LinePos(gridSize + oldPos.row, gridSize - 1);
          assert(getFaceNo(newPosOnFace2) == 2);
          return PosAndDir(newPosOnFace2, Direction.Up);
        }
        if (oldFaceNo == 5) {
          // Face 5 -> 2
          final newPosOnFace2 =
              LinePos(gridSize * 3 - 1, gridSize * 3 - oldPos.row - 1);
          assert(getFaceNo(newPosOnFace2) == 2);
          return PosAndDir(newPosOnFace2, Direction.Left);
        }
        if (oldFaceNo == 6) {
          // Face 6 -> 5
          final newPosOnFace5 =
              LinePos(oldPos.row - gridSize * 3 + gridSize, gridSize * 3 - 1);
          assert(getFaceNo(newPosOnFace5) == 5);

          return PosAndDir(newPosOnFace5, Direction.Up);
        }
        // Should not get here
        print('Right');
        assert(false);
      } else {
        // No wrapping needed. Return the new position
        return PosAndDir(newPos, dir);
      }
    }

    // Moving down
    if (dir == Direction.Down) {
      // Check if out of bounds
      if (newPos.row > findLowestRowAt(newPos.col)) {
        // Old pos are on face 2, 5 or 6
        int oldFaceNo = getFaceNo(oldPos);
        if (oldFaceNo == 2) {
          // Face 2 -> 3
          final newPosOnFace3 =
              LinePos(gridSize * 2 - 1, oldPos.col - gridSize);
          assert(getFaceNo(newPosOnFace3) == 3);
          return PosAndDir(newPosOnFace3, Direction.Left);
        }
        if (oldFaceNo == 5) {
          // Face 5 -> 6
          final newPosOnFace6 =
              LinePos(gridSize - 1, oldPos.col + gridSize * 2);
          assert(getFaceNo(newPosOnFace6) == 6);
          return PosAndDir(newPosOnFace6, Direction.Left);
        }
        if (oldFaceNo == 6) {
          // Face 6 -> 2
          final newPosOnFace2 = LinePos(oldPos.col + gridSize * 2, 0);
          assert(getFaceNo(newPosOnFace2) == 2);
          return PosAndDir(newPosOnFace2, Direction.Down);
        }
        // Should not get here
        print('Down');
        assert(false);
      } else {
        // No wrapping needed. Return the new position
        return PosAndDir(newPos, dir);
      }
    }

    // Moving left
    if (dir == Direction.Left) {
      // Check if out of bounds
      if (newPos.col < 0 || newPos.col < findLeftMostColAt(newPos.row)) {
        // Old pos are on face 1,3, 4 or 6
        int oldFaceNo = getFaceNo(oldPos);
        if (oldFaceNo == 1) {
          // Face 1 -> 4
          final newPosOnFace4 = LinePos(0, gridSize * 3 - oldPos.row - 1);
          assert(getFaceNo(newPosOnFace4) == 4);
          return PosAndDir(newPosOnFace4, Direction.Right);
        }
        if (oldFaceNo == 3) {
          // Face 3 -> 4
          final newPosOnFace4 = LinePos(oldPos.row - gridSize, gridSize * 2);
          assert(getFaceNo(newPosOnFace4) == 4);
          return PosAndDir(newPosOnFace4, Direction.Down);
        }
        if (oldFaceNo == 4) {
          // Face 4 -> 1
          final newPosOnFace1 =
              LinePos(gridSize, gridSize * 3 - oldPos.row - 1);
          assert(getFaceNo(newPosOnFace1) == 1);
          return PosAndDir(newPosOnFace1, Direction.Right);
        }
        if (oldFaceNo == 6) {
          // Face 6 -> 1
          final newPosOnFace1 = LinePos(oldPos.row - gridSize * 2, 0);
          assert(getFaceNo(newPosOnFace1) == 1);
          return PosAndDir(newPosOnFace1, Direction.Down);
        }
        // Should not get here
        print('Down');
        assert(false);
      } else {
        // No wrapping needed. Return the new position
        return PosAndDir(newPos, dir);
      }
    }
    assert(false);
    return PosAndDir(LinePos(0, 0), Direction.Up);
  }

  int findLowestRowAt(int col) {
    int row = grid.length - 1;
    while (col >= grid[row].length || grid[row][col] == ' ') {
      row--;
    }
    return row;
  }

  int findLeftMostColAt(int row) {
    int col = 0;
    while (grid[row][col] == ' ') {
      col++;
    }
    return col;
  }

  int findHighestRowAt(int col) {
    int row = 0;
    while (grid[row][col] == ' ') {
      row++;
    }
    return row;
  }

  int findRightMostColAt(int row) {
    int col = grid[row].length - 1;
    while (grid[row][col] == ' ') {
      col--;
    }
    return col;
  }

  Direction changeDir(Direction currentDir, String dirChange) {
    int enumIdx = currentDir.index;
    if (dirChange == 'L') {
      enumIdx = (enumIdx - 1) % Direction.values.length;
    }
    if (dirChange == 'R') {
      enumIdx = (enumIdx + 1) % Direction.values.length;
    }
    return Direction.values[enumIdx];
  }

  /*
  Sida 1 

      1122
      1122
      33
      33
    4455
    4455
    66
    66
*/
  int getFaceNo(LinePos myPos) {
    if (myPos.row < gridSize) {
      // 1 or 2
      if (myPos.col < gridSize * 2) return 1;
      return 2;
    }

    if (myPos.row < gridSize * 2) return 3;

    if (myPos.row < gridSize * 3) {
      // 4 or 5
      if (myPos.col < gridSize) return 4;
      return 5;
    }
    return 6;
  }

  void doTests() {
    // 1 ^ 6
    var testPos = LinePos(50, 0);
    var dir = Direction.Up;
    var result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), Direction.Up);
    PosAndDir expectedResult = PosAndDir(LinePos(0, 150), Direction.Right);
    compare(result, expectedResult);
    checkFace(testPos, 1);
    checkFace(result.pos, 6);

    // 1 < 4
    testPos = LinePos(50, 0);
    dir = Direction.Left;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(0, 149), Direction.Right);
    compare(result, expectedResult);
    checkFace(testPos, 1);
    checkFace(result.pos, 4);

    // 2 ^ 6
    testPos = LinePos(100, 0);
    dir = Direction.Up;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(0, 199), Direction.Up);
    compare(result, expectedResult);
    checkFace(testPos, 2);
    checkFace(result.pos, 6);

    // 2 > 5
    testPos = LinePos(149, 0);
    dir = Direction.Right;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(99, 149), Direction.Left);
    checkFace(testPos, 2);
    checkFace(result.pos, 5);

    // 2 v 3
    testPos = LinePos(149, 49);
    dir = Direction.Down;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(99, 99), Direction.Left);
    compare(result, expectedResult);
    checkFace(testPos, 2);
    checkFace(result.pos, 3);

    // 3 < 4
    testPos = LinePos(50, 55);
    dir = Direction.Left;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(5, 100), Direction.Down);
    compare(result, expectedResult);
    checkFace(testPos, 3);
    checkFace(result.pos, 4);

    // 3 > 2
    testPos = LinePos(99, 55);
    dir = Direction.Right;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(105, 49), Direction.Up);
    compare(result, expectedResult);
    checkFace(testPos, 3);
    checkFace(result.pos, 2);

    // 4 ^ 3
    testPos = LinePos(5, 100);
    dir = Direction.Up;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(50, 55), Direction.Right);
    compare(result, expectedResult);
    checkFace(testPos, 4);
    checkFace(result.pos, 3);

    // 4 < 1
    testPos = LinePos(0, 100);
    dir = Direction.Left;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(50, 49), Direction.Right);
    compare(result, expectedResult);
    checkFace(testPos, 4);
    checkFace(result.pos, 1);

    // 5 > 2
    testPos = LinePos(99, 100);
    dir = Direction.Right;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(149, 49), Direction.Left);
    compare(result, expectedResult);
    checkFace(testPos, 5);
    checkFace(result.pos, 2);

    // 5 v 6
    testPos = LinePos(99, 149);
    dir = Direction.Down;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(49, 199), Direction.Left);
    compare(result, expectedResult);
    checkFace(testPos, 5);
    checkFace(result.pos, 6);

    // 6 < 1
    testPos = LinePos(0, 150);
    dir = Direction.Left;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(50, 0), Direction.Down);
    compare(result, expectedResult);
    checkFace(testPos, 6);
    checkFace(result.pos, 1);

    // 6 > 5
    testPos = LinePos(49, 150);
    dir = Direction.Right;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(50, 149), Direction.Up);
    compare(result, expectedResult);
    checkFace(testPos, 6);
    checkFace(result.pos, 5);

    // 6 v 2
    testPos = LinePos(0, 199);
    dir = Direction.Down;
    result = wrapAroundMaybeP2(testPos, testPos.moveDir(dir), dir);
    expectedResult = PosAndDir(LinePos(100, 0), Direction.Down);
    compare(result, expectedResult);
    checkFace(testPos, 6);
    checkFace(result.pos, 2);
  }

  void compare(PosAndDir result, PosAndDir expectedResult) {
    if (result.direction != expectedResult.direction)
      print(
          'Dir ${result.direction.name} borde vara ${expectedResult.direction.name}');
    if (result.pos.col != expectedResult.pos.col)
      print('Col = ${result.pos.col}. Borde vara ${expectedResult.pos.col}');
    if (result.pos.row != expectedResult.pos.row)
      print('Row = ${result.pos.row}. Borde vara ${expectedResult.pos.row}');
  }

  void checkFace(LinePos pos, int expectedFace) {
    int faceNo = getFaceNo(pos);
    if (faceNo != expectedFace)
      print('Face $faceNo borde vara face $expectedFace');
  }
}
