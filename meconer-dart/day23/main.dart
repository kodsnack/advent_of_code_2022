import '../util/linepos.dart';
import '../util/util.dart';

const String inputFile = 'day23/example.txt';
//const String inputFile = 'day23/input.txt';

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
  grid.draw();
  grid.makeEmptyAtBorder();
  grid.draw();
  for (var i = 0; i < 10; i++) {
    doRound(grid);
  }
  grid.shrink();
  grid.draw();
  return grid.countEmpty();
}

int calcResultP2(List<String> inputLines) {
  // Reset the diretions list
  directions = [Direction.Up, Direction.Down, Direction.Left, Direction.Right];

  Grid grid = Grid(inputLines);
  grid.makeEmptyAtBorder();
  bool didMove = true;
  int roundNo = 0;
  while (didMove) {
    didMove = doRound(grid);
    roundNo++;
    if (roundNo > 895) grid.draw();
  }
  return roundNo;
}

List<Direction> directions = [
  Direction.Up,
  Direction.Down,
  Direction.Left,
  Direction.Right
];

class Elf {
  LinePos elfPos;

  LinePos? proposedPos;

  Elf(this.elfPos);

  void calcProposedPos(List<Direction> directions, Grid grid,
      Map<LinePos, int> proposedPositionCounts) {
    // First check if all positions around elf is empty. Then the elf doesn't move at all
    if (!allCellsAroundAreEmpty(grid)) {
      // Consider moving
      List<Direction> directionsCopy = List.from(directions);
      while (directionsCopy.isNotEmpty) {
        final direction = directionsCopy.removeAt(0);

        List<LinePos> positionsToCheck = getPositions(elfPos, direction);
        if (!elfInPositions(positionsToCheck, grid)) {
          // This direction is free
          proposedPos = elfPos.moveDir(direction);
          if (proposedPositionCounts.containsKey(proposedPos)) {
            proposedPositionCounts[proposedPos!] =
                proposedPositionCounts[proposedPos!]! + 1;
          } else {
            proposedPositionCounts[proposedPos!] = 1;
          }

          break;
        }
      }
    }
  }

  bool elfInPositions(List<LinePos> positionsToCheck, Grid grid) {
    return positionsToCheck.any((pos) => grid.grid[pos.row][pos.col] == '#');
  }

  List<LinePos> getPositions(LinePos elfPos, Direction direction) {
    switch (direction) {
      case Direction.Up:
        return [
          elfPos.moveNW(),
          elfPos.moveUp(),
          elfPos.moveNE(),
        ];
      case Direction.Left:
        return [
          elfPos.moveSW(),
          elfPos.moveLeft(),
          elfPos.moveNW(),
        ];
      case Direction.Down:
        return [
          elfPos.moveSW(),
          elfPos.moveDown(),
          elfPos.moveSE(),
        ];
      case Direction.Right:
        return [
          elfPos.moveNE(),
          elfPos.moveRight(),
          elfPos.moveSE(),
        ];
    }
  }

  bool allCellsAroundAreEmpty(Grid grid) {
    List<LinePos> cellsAround = [
      elfPos.moveNW(),
      elfPos.moveN(),
      elfPos.moveNE(),
      elfPos.moveW(),
      elfPos.moveE(),
      elfPos.moveSW(),
      elfPos.moveS(),
      elfPos.moveSE(),
    ];
    return !(cellsAround.any((pos) => grid.grid[pos.row][pos.col] == '#'));
  }
}

bool doRound(Grid grid) {
  grid.makeEmptyAtBorder();
  Set<Elf> elfs = findElfs(grid);
  //grid.draw();

  Map<LinePos, int> proposedPositionCounts = Map();
  elfs.forEach((elf) {
    elf.calcProposedPos(directions, grid, proposedPositionCounts);
  });

  // Try to do the proposed moves
  bool didMove = false;
  elfs.forEach((elf) {
    if (elf.proposedPos != null) {
      if (proposedPositionCounts[elf.proposedPos] == 1) {
        // Don't move if more elves wants to move here
        elf.elfPos = elf.proposedPos!;
        didMove = true;
      }
      elf.proposedPos = null;
    }
  });

  grid.makeFromElfs(elfs);
  //grid.draw();
  directions = [...directions.sublist(1, 4), directions.first];
  return didMove;
}

Set<Elf> findElfs(Grid grid) {
  Set<Elf> elfs = {};
  for (var rowIdx = 0; rowIdx < grid.height; rowIdx++) {
    for (var colIdx = 0; colIdx < grid.width; colIdx++) {
      if (grid.grid[rowIdx][colIdx] == '#') {
        elfs.add(Elf(LinePos(colIdx, rowIdx)));
      }
    }
  }
  return elfs;
}

class Grid {
  late List<List<String>> grid;
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
  }

  void expandUp() {
    List<String> newRow = List.generate(width, (_) => '.');
    grid = [newRow, ...grid];
  }

  void expandDown() {
    List<String> newRow = List.generate(width, (_) => '.');
    grid = [...grid, newRow];
  }

  void expandLeft() {
    List<List<String>> newGrid = [];
    for (var gridLine in grid) {
      newGrid.add(['.', ...gridLine]);
    }
    grid = newGrid;
  }

  void expandRight() {
    List<List<String>> newGrid = [];
    for (var gridLine in grid) {
      newGrid.add([...gridLine, '.']);
    }
    grid = newGrid;
  }

  void draw() {
    for (final gridLine in grid) {
      print(gridLine.join(''));
    }
    print(List.filled(width + 5, '-').join());
  }

  // Expand grid so we have an empty border around the entire grid
  void makeEmptyAtBorder() {
    // Check top row
    if (grid[0].contains('#')) {
      expandUp();
    }
    // Check bottom row
    if (grid.last.contains('#')) {
      expandDown();
    }

    // Check first column
    bool elfInFirstCol = false;
    for (final gridLine in grid) {
      if (gridLine.first == '#') {
        elfInFirstCol = true;
        break;
      }
    }
    if (elfInFirstCol) {
      expandLeft();
    }

    // Check rightmost column
    bool elfInLastCol = false;
    for (final gridLine in grid) {
      if (gridLine.last == '#') {
        elfInLastCol = true;
        break;
      }
    }
    if (elfInLastCol) {
      expandRight();
    }
  }

  void makeFromElfs(Set<Elf> elfs) {
    int lastHeight = height;
    int lastWidth = width;
    grid = [];
    for (int rowIdx = 0; rowIdx < lastHeight; rowIdx++) {
      grid.add(List.generate(lastWidth, (_) => '.'));
    }
    elfs.forEach((elf) {
      grid[elf.elfPos.row][elf.elfPos.col] = '#';
    });
  }

  void shrink() {
    // remove rows from top
    while (!grid[0].contains('#')) {
      grid.removeAt(0);
    }
    // Remove rows from bottom
    while (!grid.last.contains('#')) {
      grid.removeLast();
    }
    // Remove first empty columns
    bool isEmpty = true;
    while (isEmpty) {
      for (int row = 0; row < height; row++) {
        if (grid[row][0] == '#') {
          isEmpty = false;
          break;
        }
      }
      if (isEmpty) {
        for (int row = 0; row < height; row++) {
          grid[row].removeAt(0);
        }
      }
    }

    // Remove empty columns at end
    isEmpty = true;
    while (isEmpty) {
      for (int row = 0; row < height; row++) {
        if (grid[row].last == '#') {
          isEmpty = false;
          break;
        }
      }
      if (isEmpty) {
        for (int row = 0; row < height; row++) {
          grid[row].removeLast();
        }
      }
    }
  }

  int countEmpty() {
    int count = 0;
    for (int row = 0; row < height; row++) {
      count += grid[row].where((element) => element == '.').length;
    }
    return count;
  }
}
