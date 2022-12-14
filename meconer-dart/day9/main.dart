import '../util/util.dart';

//const String inputFile = 'day9/example.txt';
//const String inputFile = 'day9/example2.txt';
const String inputFile = 'day9/input.txt';

Future<void> main(List<String> args) async {
  var lines = await readInput(inputFile);
  print('Part 1:');
  print(calcResultPart1(lines));

  print('Part 2:');
  print(calcResultPart2(lines));
}

int calcResultPart1(List<String> lines) {
  Range range = Range();
  Pos headPos = Pos(0, 0);
  Pos tailPos = Pos(0, 0);
  Set<Pos> visitedTailPositions = {};
  visitedTailPositions.add(tailPos);
  for (final line in lines) {
    final command = line.split(' ');
    int noOfMoves = int.parse(command[1]);
    for (var moveCount = 0; moveCount < noOfMoves; moveCount++) {
      headPos = headPos.moveDir(command[0]);
      range.extendRange(headPos.x, headPos.y);
      tailPos = tailPos.calcNewTailPos(headPos);
      visitedTailPositions.add(tailPos);
    }
  }
  //drawVisitedTailPositions(range, visitedTailPositions);
  return visitedTailPositions.length;
}

int calcResultPart2(List<String> lines) {
  Range range = Range();
  List<Pos> rope = List.generate(10, (_) => Pos(0, 0));
  Set<Pos> visitedTailPositions = {};
  visitedTailPositions.add(rope[9]);
  for (final line in lines) {
    final command = line.split(' ');
    int noOfMoves = int.parse(command[1]);
    for (var moveCount = 0; moveCount < noOfMoves; moveCount++) {
      rope[0] = rope[0].moveDir(command[0]);
      range.extendRange(rope[0].x, rope[0].y);
      for (int knot = 1; knot < rope.length; knot++) {
        rope[knot] = rope[knot].calcNewTailPos(rope[knot - 1]);
      }
      visitedTailPositions.add(rope[9]);
    }
  }
  drawGrid(range, rope);
  drawVisitedTailPositions(range, visitedTailPositions);
  return visitedTailPositions.length;
}

void drawGrid(Range range, List<Pos> rope) {
  print('------------');
  for (int y = range.maxY; y >= range.minY; y--) {
    String line = '';
    for (int x = range.minX; x <= range.maxX; x++) {
      String charToAdd = '.';
      for (int knot = 9; knot >= 0; knot--) {
        if (rope[knot].x == x && rope[knot].y == y) {
          charToAdd = knot.toString();
        }
      }
      line += charToAdd;
    }
    print(line);
  }
}

void drawVisitedTailPositions(Range range, Set<Pos> visitedTailPositions) {
  for (int y = range.maxY; y >= range.minY; y--) {
    String line = '';
    for (int x = range.minX; x < range.maxX; x++) {
      if (visitedTailPositions.contains(Pos(x, y))) {
        if (x == 0 && y == 0) {
          line += 's';
        } else {
          line += '#';
        }
      } else {
        line += '.';
      }
    }
    print(line);
  }
}

class Range {
  int minX = 0, minY = 0, maxX = 0, maxY = 0;

  void extendRange(x, y) {
    if (x < minX) minX = x;
    if (y < minY) minY = y;
    if (x > maxX) maxX = x;
    if (y > maxY) maxY = y;
  }
}

class Pos {
  final int x, y;
  Pos(this.x, this.y);

  Pos moveUp() {
    return Pos(x, y + 1);
  }

  Pos moveDown() {
    return Pos(x, y - 1);
  }

  Pos moveLeft() {
    return Pos(x - 1, y);
  }

  Pos moveRight() {
    return Pos(x + 1, y);
  }

  Pos moveDir(String command) {
    switch (command) {
      case 'U':
        return moveUp();
      case 'D':
        return moveDown();
      case 'L':
        return moveLeft();
      case 'R':
        return moveRight();
      default:
        throw Exception('Wrong command');
    }
  }

  Pos calcNewTailPos(Pos headPos) {
    int dx = headPos.x - x;
    int dy = headPos.y - y;

    int newTailx = x;
    int newTaily = y;

    if (dx.abs() == 2) {
      // We need to move tail in x
      newTailx += dx.sign;
      // In this case we move y to same as head
      if (dy.abs() == 2) {
        newTaily += dy.sign;
      } else {
        newTaily = headPos.y;
      }
    } else if (dy.abs() == 2) {
      // We need to move tail in x
      newTaily = dy.sign + y;
      // In this case we move y to same as head
      newTailx = headPos.x;
    }
    return Pos(newTailx, newTaily);
  }

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Pos && (x == other.x && y == other.y);
  }

  int get hashCode => x * 100000 + y;
}
