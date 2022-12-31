import 'dart:math';

import '../util/linepos.dart';
import '../util/util.dart';

//const String inputFile = 'day24/example.txt';
const String inputFile = 'day24/input.txt';

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
  Grid grid = Grid(inputLines);
  //grid.draw();
  return grid.findPath();
}

int calcResultP2(List<String> inputLines) {
  Grid grid = Grid(inputLines);
  //grid.draw();
  int first = grid.findPath(start: grid.entryPoint, finish: grid.targetPoint);
  int second = grid.findPath(
      start: grid.targetPoint, finish: grid.entryPoint, time: first);
  int third = grid.findPath(
      start: grid.entryPoint, finish: grid.targetPoint, time: second);
  return third;
}

class Grid {
  Set<Blizzard> blizzards = {};
  late List<List<String>> grid;
  late LinePos entryPoint;
  late LinePos targetPoint;

  int currentTime = 0;

  int get width {
    return grid[0].length;
  }

  int get height {
    return grid.length;
  }

  Grid(List<String> inputLines) {
    grid = [];
    for (var line in inputLines) {
      grid.add(line.split(''));
    }
    entryPoint = LinePos(grid[0].indexOf('.'), 0);
    targetPoint = LinePos(grid.last.indexOf('.'), height - 1);
    for (int row = 1; row < height - 1; row++) {
      for (int col = 1; col < width - 1; col++) {
        if (grid[row][col] == '^')
          blizzards
              .add(Blizzard(pos: LinePos(col, row), direction: Direction.Up));
        if (grid[row][col] == '>')
          blizzards.add(
              Blizzard(pos: LinePos(col, row), direction: Direction.Right));
        if (grid[row][col] == 'v')
          blizzards
              .add(Blizzard(pos: LinePos(col, row), direction: Direction.Down));
        if (grid[row][col] == '<')
          blizzards
              .add(Blizzard(pos: LinePos(col, row), direction: Direction.Left));
      }
    }
  }

  void buildGridFromBlizzards() {
    for (int row = 1; row < height - 1; row++) {
      List<String> gridLine = ['#'];
      for (int col = 1; col < width - 1; col++) {
        Set<Blizzard> blizzardsOnThisPos = getBlizzardsOnPos(LinePos(col, row));
        if (blizzardsOnThisPos.isEmpty) gridLine.add('.');
        if (blizzardsOnThisPos.length > 1)
          gridLine.add(blizzardsOnThisPos.length.toString());
        if (blizzardsOnThisPos.length == 1)
          gridLine.add(getDirectionChar(blizzardsOnThisPos.first.direction));
      }
      gridLine.add('#');
      grid[row] = gridLine;
    }
  }

  void moveBlizzards() {
    for (final blizzard in blizzards) {
      LinePos newPos = blizzard.pos.moveDir(blizzard.direction);
      if (newPos.col == width - 1) newPos = LinePos(1, blizzard.pos.row);
      if (newPos.col == 0) newPos = LinePos(width - 2, blizzard.pos.row);
      if (newPos.row == height - 1) {
        if (newPos != targetPoint) {
          newPos = LinePos(blizzard.pos.col, 1);
        }
      }
      if (newPos.row == 0) {
        if (newPos != entryPoint) {
          newPos = LinePos(blizzard.pos.col, height - 2);
        }
      }
      blizzard.pos = newPos;
    }
  }

  void draw() {
    for (final gridLine in grid) {
      print(gridLine.join(''));
    }
    print(List.filled(width + 5, '-').join());
  }

  Set<Blizzard> getBlizzardsOnPos(LinePos linePos) {
    Set<Blizzard> blizzardsOnPos = {};
    for (final blizzard in blizzards) {
      if (blizzard.pos == linePos) blizzardsOnPos.add(blizzard);
    }
    return blizzardsOnPos;
  }

  String getDirectionChar(Direction direction) {
    switch (direction) {
      case Direction.Down:
        return 'v';
      case Direction.Up:
        return '^';
      case Direction.Left:
        return '<';
      case Direction.Right:
        return '>';
    }
  }

  int findPath({LinePos? start, LinePos? finish, int time = 0}) {
    if (start == null) start = entryPoint;
    if (finish == null) finish = targetPoint;
    Set<Node> nodes = {};

    Set<LinePos> neighbourPositions = [...start.getNeighbours(), start].toSet();
    while (true) {
      if (neighbourPositions.contains(finish)) {
        // Found target
        break;
      }
      final currentGrid = getGridAtTime(time);
      for (final pos in neighbourPositions) {
        if (pos.row < 0) continue;
        if (pos.row >= height) continue;
        if (currentGrid[pos.row][pos.col] == '.') {
          nodes.add(Node(pos, time));
        }
      }
      neighbourPositions = {};
      for (final node in nodes.where((n) => n.time == time)) {
        neighbourPositions.addAll(node.pos.getNeighbours());
        neighbourPositions.add(node.pos);
      }
      time++;
    }

    return time;
  }

  Set<Node> makePossibleNodes(Node node, int time,
      {bool hasLeftStartNode = true}) {
    Set<Node> possibleNodes = {};
    List<LinePos> neighbourPositions = [...node.pos.getNeighbours(), node.pos];
    final maze = getGridAtTime(time);
    for (var pos in neighbourPositions) {
      if (hasLeftStartNode && pos == entryPoint) continue;
      if (pos.row < 0) continue;
      if (maze[pos.row][pos.col] == '.') {
        // This pos is empty. We can go here
        Node newNode = Node(pos, time);
        possibleNodes.add(newNode);
      }
    }
    for (final nextNode in possibleNodes) {
      if (nextNode.pos == entryPoint) {
        nextNode.neighbours =
            makePossibleNodes(nextNode, time + 1, hasLeftStartNode: false);
      } else {
        nextNode.neighbours = makePossibleNodes(nextNode, time + 1);
      }
    }
    return possibleNodes;
  }

  List<List<String>> getGridAtTime(int time) {
    while (currentTime < time) {
      moveBlizzards();
      currentTime++;
    }
    buildGridFromBlizzards();
    return grid;
  }
}

class Node {
  LinePos pos;
  int time;
  Set<Node> neighbours = {};
  Node(this.pos, this.time);
}

class Blizzard {
  Direction direction;
  LinePos pos;
  Blizzard({required this.pos, required this.direction});
}
