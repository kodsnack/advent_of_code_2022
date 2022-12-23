import '../util/util.dart';

//const String inputFile = 'day8/example.txt';
const String inputFile = 'day8/input.txt';

Future<void> main(List<String> args) async {
  var lines = await readInput(inputFile);
  print('Part 1:');
  print(calcResultPart1(lines));

  print('Part 2:');
  print(calcResultPart2(lines));
}

int calcResultPart2(List<String> lines) {
  int gridWidth = lines[0].length;
  int gridHeight = lines.length;
  int maxScenicScore = 0;
  for (int lineNo = 0; lineNo < gridHeight; lineNo++) {
    for (int pos = 0; pos < gridWidth; pos++) {
      int scenicScore = calcScenicScore(lines, lineNo, pos);
      if (scenicScore > maxScenicScore) maxScenicScore = scenicScore;
    }
  }
  return maxScenicScore;
}

int calcScenicScore(List<String> lines, int lineNo, int pos) {
  // Look up
  int countUp = countVisibleTreesUp(lineNo, lines, pos);
  int countDown = countVisibleTreesDown(lineNo, lines, pos);
  int countLeft = countVisibleTreesLeft(lineNo, lines, pos);
  int countRight = countVisibleTreesRight(lineNo, lines, pos);

  return countLeft * countRight * countDown * countUp;
}

int countVisibleTreesUp(int lineNo, List<String> lines, int pos) {
  int count = 0;
  if (lineNo > 0) {
    int thisTreeHeight = getTreeHeightAt(lines, lineNo, pos);
    int lineNoToLookAt = lineNo - 1;
    bool stop = false;
    while (!stop) {
      int currTreeHeight = getTreeHeightAt(lines, lineNoToLookAt, pos);
      if (currTreeHeight >= thisTreeHeight) {
        // View is blocked here. We stop
        count++;
        stop = true;
      } else {
        // View is not blocked. Go to next tree if we are not on an edge
        count++;
        lineNoToLookAt--;
        stop = lineNoToLookAt < 0;
      }
    }
  }
  return count;
}

int countVisibleTreesDown(int lineNo, List<String> lines, int pos) {
  int count = 0;
  if (lineNo < lines.length - 1) {
    int thisTreeHeight = getTreeHeightAt(lines, lineNo, pos);
    int lineNoToLookAt = lineNo + 1;
    bool stop = false;
    while (!stop) {
      int currTreeHeight = getTreeHeightAt(lines, lineNoToLookAt, pos);
      if (currTreeHeight >= thisTreeHeight) {
        // View is blocked here. We stop
        count++;
        stop = true;
      } else {
        // View is not blocked. Go to next tree if we are not on an edge
        count++;
        lineNoToLookAt++;
        stop = lineNoToLookAt >= lines.length;
      }
    }
  }
  return count;
}

int countVisibleTreesLeft(int lineNo, List<String> lines, int pos) {
  int count = 0;
  if (pos > 0) {
    int thisTreeHeight = getTreeHeightAt(lines, lineNo, pos);
    int posToLookAt = pos - 1;
    bool stop = false;
    while (!stop) {
      int currTreeHeight = getTreeHeightAt(lines, lineNo, posToLookAt);
      if (currTreeHeight >= thisTreeHeight) {
        // View is blocked here. We stop
        count++;
        stop = true;
      } else {
        // View is not blocked. Go to next tree if we are not on an edge
        count++;
        posToLookAt--;
        stop = posToLookAt < 0;
      }
    }
  }
  return count;
}

int countVisibleTreesRight(int lineNo, List<String> lines, int pos) {
  int count = 0;
  if (pos < lines[0].length - 1) {
    int thisTreeHeight = getTreeHeightAt(lines, lineNo, pos);
    int posToLookAt = pos + 1;
    bool stop = false;
    while (!stop) {
      int currTreeHeight = getTreeHeightAt(lines, lineNo, posToLookAt);
      if (currTreeHeight >= thisTreeHeight) {
        // View is blocked here. We stop
        count++;
        stop = true;
      } else {
        // View is not blocked. Go to next tree if we are not on an edge
        count++;
        posToLookAt++;
        stop = posToLookAt >= lines[0].length;
      }
    }
  }
  return count;
}

int getTreeHeightAt(List<String> lines, int lineNo, int pos) {
  return int.parse(lines[lineNo].substring(pos, pos + 1));
}

int calcResultPart1(List<String> lines) {
  int gridWidth = lines[0].length;
  int gridHeight = lines.length;
  Set<int> visibleSet = {};
  // Check from top and bottom
  for (int pos = 0; pos < gridWidth; pos++) {
    // top
    checkFromTop(lines, pos, visibleSet, gridWidth, gridHeight);
    checkFromBottom(lines, pos, visibleSet, gridWidth, gridHeight);
  }
  // Check from left and right
  for (int lineNo = 0; lineNo < gridHeight; lineNo++) {
    // top
    checkFromLeft(lines, lineNo, visibleSet, gridWidth);
    checkFromRight(lines, lineNo, visibleSet, gridWidth);
  }
  for (var lineNo = 0; lineNo < gridHeight; lineNo++) {
    String line = '';
    for (var pos = 0; pos < gridWidth; pos++) {
      if (isVisible(lineNo, pos, visibleSet, gridWidth)) {
        line += lines[lineNo].substring(pos, pos + 1);
      } else {
        line += ' ';
      }
    }
    print(line);
  }
  return visibleSet.length;
}

bool isVisible(int lineNo, int pos, Set<int> visibleSet, int gridWidth) {
  return visibleSet.contains(lineNo * gridWidth + pos);
}

void checkFromLeft(
    List<String> lines, int lineNo, Set<int> visibleSet, int gridWidth) {
  int currVisibleHeightLimit = -1;
  for (var pos = 0; pos < gridWidth; pos++) {
    int treeHeight = getTreeHeightAt(lines, lineNo, pos);

    if (treeHeight > currVisibleHeightLimit) {
      currVisibleHeightLimit = treeHeight;
      visibleSet.add(pos + lineNo * gridWidth);
    }
  }
}

void checkFromRight(
    List<String> lines, int lineNo, Set<int> visibleSet, int gridWidth) {
  int currVisibleHeightLimit = -1;
  for (var pos = gridWidth - 1; pos >= 0; pos--) {
    int treeHeight = getTreeHeightAt(lines, lineNo, pos);
    if (treeHeight > currVisibleHeightLimit) {
      currVisibleHeightLimit = treeHeight;
      visibleSet.add(pos + lineNo * gridWidth);
    }
  }
}

void checkFromTop(List<String> lines, int pos, Set<int> visibleSet,
    int gridWidth, int gridHeight) {
  int currVisibleHeightLimit = -1;
  for (var lineNo = 0; lineNo < gridHeight; lineNo++) {
    int treeHeight = getTreeHeightAt(lines, lineNo, pos);
    if (treeHeight > currVisibleHeightLimit) {
      currVisibleHeightLimit = treeHeight;
      visibleSet.add(pos + lineNo * gridWidth);
    }
  }
}

void checkFromBottom(List<String> lines, int pos, Set<int> visibleSet,
    int gridWidth, int gridHeight) {
  int currVisibleHeightLimit = -1;
  for (var lineNo = gridWidth - 1; lineNo >= 0; lineNo--) {
    int treeHeight = getTreeHeightAt(lines, lineNo, pos);
    if (treeHeight > currVisibleHeightLimit) {
      currVisibleHeightLimit = treeHeight;
      visibleSet.add(pos + lineNo * gridWidth);
    }
  }
}
