import '../util/pos.dart';
import '../util/util.dart';

const String inputFile = 'day12/example.txt';
//const String inputFile = 'day12/input.txt';

Future<void> main(List<String> args) async {
  var lines = await readInput(inputFile);
  print('Part 1:');
  print(calcResultPart1(lines));

  print('Part 2:');
  print(calcResultPart2(lines));
}

int calcResultPart1(List<String> lines) {
  Grid grid = Grid.fromLines(lines);
  return grid.findPathFromStoE();
}

int calcResultPart2(List<String> lines) {
  Grid grid = Grid.fromLines(lines);
  return grid.findPathFromEtoLevelA();
}

class Node {
  int elevation;
  int dist = veryLargeNumber;

  Node(this.elevation);
}

class Grid {
  late List<List<Node>> grid;
  late Pos startPos;
  late Pos endPos;

  Grid.fromLines(List<String> lines) {
    grid = [];
    for (int row = 0; row < lines.length; row++) {
      final elevStrings = lines[row].split('');
      List<Node> elevationLine = [];
      for (int col = 0; col < elevStrings.length; col++) {
        if (elevStrings[col] == 'S') {
          startPos = Pos(col, lines.length - row - 1);
        }
        if (elevStrings[col] == 'E') {
          endPos = Pos(col, lines.length - row - 1);
        }
        elevationLine.add(Node(getElevationFromLetter(elevStrings[col])));
      }
      grid.add(elevationLine);
    }
    grid = grid.reversed.toList(); // To get y = 0 at the bottom like
    // a normal coord system
  }

  int getElevationFromLetter(String elevString) {
    if (elevString == 'S') {
      elevString = 'a';
    }
    if (elevString == 'E') {
      elevString = 'z';
    }
    return (elevString.codeUnitAt(0) - 'a'.codeUnitAt(0));
  }

  int findPathFromStoE() {
    int currElevation = 0;
    Pos currPos = startPos;
    setDistAt(currPos, 0);
    Set<Pos> unVisited = buildUnvisitedSet();
    unVisited.remove(currPos);
    Set<Pos> visited = {currPos};
    while (currPos != endPos) {
      currElevation = getElevationAt(currPos);
      Set<Pos> neighbours = findNeighbours(currPos, visited, currElevation + 1);
      for (final neighbour in neighbours) {
        int dist = getDistAt(currPos);
        int neighbourDist = getDistAt(neighbour);
        if (dist + 1 < neighbourDist) {
          setDistAt(neighbour, dist + 1);
        }
      }
      final nextPosToVisit = getUnvisitedWithLowestDist(unVisited);
      currPos = nextPosToVisit;
      visited.add(currPos);
      unVisited.remove(currPos);
      //drawGrid();
    }
    print('Found E in ${getDistAt(endPos)} steps');
    return getDistAt(endPos);
  }

  int findPathFromEtoLevelA() {
    Pos currPos = endPos;
    setDistAt(currPos, 0);
    Set<Pos> unVisited = buildUnvisitedSet();
    unVisited.remove(currPos);
    Set<Pos> visited = {currPos};
    int currElevation = getElevationAt(currPos);
    while (currElevation > 0) {
      // Stop when we found elevation 'a'
      Set<Pos> neighbours =
          findLowerNeighbours(currPos, visited, currElevation - 1);
      for (final neighbour in neighbours) {
        int dist = getDistAt(currPos);
        int neighbourDist = getDistAt(neighbour);
        if (dist + 1 < neighbourDist) {
          setDistAt(neighbour, dist + 1);
        }
      }
      final nextPosToVisit = getUnvisitedWithLowestDist(unVisited);
      currPos = nextPosToVisit;
      currElevation = getElevationAt(currPos);
      visited.add(currPos);
      unVisited.remove(currPos);
      //drawGrid();
    }
    print('Found level A in ${getDistAt(currPos)} steps');
    return getDistAt(currPos);
  }

  Set<Pos> findNeighbours(Pos currPos, Set<Pos> visited, int elevationLimit) {
    Set<Pos> neighbours = {};
    for (final dir in ['U', 'D', 'L', 'R']) {
      Pos neighbour =
          currPos.moveDirWithLimit(dir, grid[0].length - 1, grid.length - 1);
      if (!visited.contains(neighbour)) {
        int neighbourElevation = getElevationAt(neighbour);
        if (neighbourElevation <= elevationLimit) {
          neighbours.add(neighbour);
        }
      }
    }
    return neighbours;
  }

  Set<Pos> findLowerNeighbours(
      Pos currPos, Set<Pos> visited, int elevationLimit) {
    Set<Pos> neighbours = {};
    for (final dir in ['U', 'D', 'L', 'R']) {
      Pos neighbour =
          currPos.moveDirWithLimit(dir, grid[0].length - 1, grid.length - 1);
      if (!visited.contains(neighbour)) {
        int neighbourElevation = getElevationAt(neighbour);
        if (neighbourElevation >= elevationLimit) {
          neighbours.add(neighbour);
        }
      }
    }
    return neighbours;
  }

  int getElevationAt(Pos pos) {
    return grid[pos.y][pos.x].elevation;
  }

  int getDistAt(Pos pos) {
    return grid[pos.y][pos.x].dist;
  }

  void setDistAt(Pos pos, int dist) {
    grid[pos.y][pos.x].dist = dist;
  }

  Pos getUnvisitedWithLowestDist(Set<Pos> unvisited) {
    List<Pos> neighbourList = unvisited.toList();
    neighbourList
        .sort((posa, posb) => getDistAt(posa).compareTo(getDistAt(posb)));
    return neighbourList.first;
  }

  Set<Pos> buildUnvisitedSet() {
    Set<Pos> unvisitedSet = {};
    for (int x = 0; x < grid[0].length; x++) {
      for (int y = 0; y < grid.length; y++) {
        unvisitedSet.add(Pos(x, y));
      }
    }
    return unvisitedSet;
  }

  void drawGrid() {
    print('');
    print('--------------------------------------');
    print('       0   1   2   3   4   5   6   7  ');
    print('--:-----------------------------------');
    for (int y = grid.length - 1; y >= 0; y--) {
      String line = '$y :  ';
      for (int x = 0; x < grid[0].length; x++) {
        int dist = getDistAt(Pos(x, y));
        if (dist < 100) {
          String s = dist.toString();
          while (s.length < 4) s = ' ' + s;
          line += s;
        } else {
          line += ' XXX';
        }
      }
      print(line);
    }
  }
}
