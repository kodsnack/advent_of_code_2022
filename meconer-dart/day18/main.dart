import 'dart:math';

import '../util/util.dart';

//const String inputFile = 'day18/example.txt';
const String inputFile = 'day18/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);

  for (final inputLine in inputLines) {
    List<int> coordList =
        inputLine.split(',').map((e) => int.parse(e)).toList();
    Pos3D cube = Pos3D(coordList[0], coordList[1], coordList[2]);
    cubeSet.add(cube);
    range3d.extend(cube);
  }

  print('Part 1:');
  int resultP1 = calcResultP1();
  print(resultP1);

  print('Part 2:');
  print(calcResultP2(resultP1));
}

int calcResultP1() {
  int totalOpenSides = 0;
  for (final cube in cubeSet) {
    int openSides = countOpenSides(cube);
    totalOpenSides += openSides;
  }
  return totalOpenSides;
}

Range3D range3d = Range3D(1000, -1000, 1000, -1000, 1000, -1000);
Set<Pos3D> cubeSet = {};
Set<Pos3D> containedCubes = {};
Set<Pos3D> reachableCubes = {};
Set<Pos3D> unVisitedCubes = {};

int countOpenSides(Pos3D cube) {
  int openSides = 6;
  // Check if there is a cube above (Z+)
  if (cubeSet.contains(cube.above())) {
    openSides--;
  }
  if (cubeSet.contains(cube.below())) {
    openSides--;
  }
  if (cubeSet.contains(cube.left())) {
    openSides--;
  }
  if (cubeSet.contains(cube.right())) {
    openSides--;
  }
  if (cubeSet.contains(cube.infront())) {
    openSides--;
  }
  if (cubeSet.contains(cube.behind())) {
    openSides--;
  }
  return openSides;
}

int calcResultP2(int resultFromP1) {
  for (int x = range3d.xmin; x <= range3d.xmax; x++) {
    for (int y = range3d.ymin; y <= range3d.ymax; y++) {
      for (int z = range3d.zmin; z <= range3d.zmax; z++) {
        Pos3D cube = Pos3D(x, y, z);
        unVisitedCubes.add(cube);
      }
    }
  }

  // Check how many sides are reachable from the bottom and top
  int reachableSides = 0;
  for (int x = range3d.xmin; x <= range3d.xmax; x++) {
    for (int y = range3d.ymin; y <= range3d.ymax; y++) {
      reachableSides += zSides(x, y, range3d.zmin);
      reachableSides += zSides(x, y, range3d.zmax);
    }
  }
  // Check how many sides are reachable from left and right
  for (int z = range3d.zmin; z <= range3d.zmax; z++) {
    for (int y = range3d.ymin; y <= range3d.ymax; y++) {
      reachableSides += xSides(y, z, range3d.xmin);
      reachableSides += xSides(y, z, range3d.xmax);
    }
  }
  // Check how many sides are reachable from front and back
  for (int z = range3d.zmin; z <= range3d.zmax; z++) {
    for (int x = range3d.xmin; x <= range3d.xmax; x++) {
      reachableSides += ySides(x, z, range3d.ymin);
      reachableSides += ySides(x, z, range3d.ymax);
    }
  }

  return reachableSides;
}

int zSides(int x, int y, int z) {
  int reachableSides = 0;
  Pos3D cubeToTest = Pos3D(x, y, z);
  if (unVisitedCubes.contains(cubeToTest)) {
    unVisitedCubes.remove(cubeToTest);
    if (cubeSet.contains(cubeToTest)) {
      // A cube is on this position. Count the bottom side
      reachableSides++;
    } else {
      // Check
      Set<Pos3D> neighbours = cubeToTest.getNeighbours().toSet();
      int reachableSidesOfNeighbours = 0;
      for (final neighbour in neighbours) {
        reachableSidesOfNeighbours += countReachableSides(neighbour);
      }
      reachableSides += reachableSidesOfNeighbours;
    }
  }
  return reachableSides;
}

int ySides(int x, int z, int y) {
  int reachableSides = 0;
  Pos3D cubeToTest = Pos3D(x, y, z);
  if (unVisitedCubes.contains(cubeToTest)) {
    unVisitedCubes.remove(cubeToTest);
    if (cubeSet.contains(cubeToTest)) {
      // A cube is on this position. Count the bottom side
      reachableSides++;
    } else {
      // Check
      Set<Pos3D> neighbours = cubeToTest.getNeighbours().toSet();
      int reachableSidesOfNeighbours = 0;
      for (final neighbour in neighbours) {
        reachableSidesOfNeighbours += countReachableSides(neighbour);
      }
      reachableSides += reachableSidesOfNeighbours;
    }
  }
  return reachableSides;
}

int xSides(int y, int z, int x) {
  int reachableSides = 0;
  Pos3D cubeToTest = Pos3D(x, y, z);
  if (unVisitedCubes.contains(cubeToTest)) {
    unVisitedCubes.remove(cubeToTest);
    if (cubeSet.contains(cubeToTest)) {
      // A cube is on this position. Count the bottom side
      reachableSides++;
    } else {
      // Check
      Set<Pos3D> neighbours = cubeToTest.getNeighbours().toSet();
      int reachableSidesOfNeighbours = 0;
      for (final neighbour in neighbours) {
        reachableSidesOfNeighbours += countReachableSides(neighbour);
      }
      reachableSides += reachableSidesOfNeighbours;
    }
  }
  return reachableSides;
}

int sidesFromTop(int x, int y) {
  int z = range3d.zmax;
  int reachableSides = 0;
  Pos3D cubeToTest = Pos3D(x, y, z);
  if (unVisitedCubes.contains(cubeToTest)) {
    unVisitedCubes.remove(cubeToTest);
    if (cubeSet.contains(cubeToTest)) {
      // A cube is on this position. Count the top side
      reachableSides++;
    } else {
      // Check
      Set<Pos3D> neighbours = cubeToTest.getNeighbours().toSet();
      int reachableSidesOfNeighbours = 0;
      for (final neighbour in neighbours) {
        reachableSidesOfNeighbours += countReachableSides(neighbour);
      }
      reachableSides += reachableSidesOfNeighbours;
    }
  }
  return reachableSides;
}

int countReachableSides(Pos3D cubeToTest) {
  // Check if outside the range
  if (!range3d.contains(cubeToTest)) {
    return 0;
  }
  if (!unVisitedCubes.contains(cubeToTest)) {
    // We have been in this cube already.
    return 0;
  }
  int reachableSides = 0;
  unVisitedCubes.remove(cubeToTest);
  for (final neighbour in cubeToTest.getNeighbours()) {
    if (cubeSet.contains(neighbour)) {
      // Stop. There is a cube here. Count 1 side
      reachableSides++;
    } else {
      reachableSides += countReachableSides(neighbour);
    }
  }
  return reachableSides;
}

bool isContained(Pos3D cubeToTest) {
  if (containedCubes.contains(cubeToTest)) {
    return true;
  }
  if (reachableCubes.contains(cubeToTest)) {
    return false;
  }
  if (range3d.isOnEdge(cubeToTest)) {
    reachableCubes.add(cubeToTest);
    return false;
  }

  // Check neighbours
  List<Pos3D> neighbours = cubeToTest.getNeighbours();
  for (final neighbour in neighbours) {
    if (!cubeSet.contains(neighbour)) {
      if (isContained(neighbour)) {
        containedCubes.add(cubeToTest);
        return true;
      } else {
        reachableCubes.add(cubeToTest);
        return false;
      }
    }
  }
  containedCubes.add(cubeToTest);
  return true;
}

class Range3D {
  int xmin, xmax, ymin, ymax, zmin, zmax;
  Range3D(this.xmin, this.xmax, this.ymin, this.ymax, this.zmin, this.zmax);

  void extend(Pos3D cube) {
    xmin = min(cube.x, xmin);
    xmax = max(cube.x, xmax);
    ymin = min(cube.y, ymin);
    ymax = max(cube.y, ymax);
    zmin = min(cube.z, zmin);
    zmax = max(cube.z, zmax);
  }

  bool isOnEdge(Pos3D posToCheck) {
    if (posToCheck.x == xmin) return true;
    if (posToCheck.x == xmax) return true;
    if (posToCheck.y == ymin) return true;
    if (posToCheck.y == ymax) return true;
    if (posToCheck.z == zmin) return true;
    if (posToCheck.z == zmax) return true;
    return false;
  }

  bool contains(Pos3D posToCheck) {
    if (posToCheck.x < xmin) return false;
    if (posToCheck.x > xmax) return false;
    if (posToCheck.y < ymin) return false;
    if (posToCheck.y > ymax) return false;
    if (posToCheck.z < zmin) return false;
    if (posToCheck.z > zmax) return false;
    return true;
  }
}

class Pos3D {
  int x, y, z;
  Pos3D(this.x, this.y, this.z);

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Pos3D && (x == other.x && y == other.y && z == other.z);
  }

  int get hashCode => x * 1000000 + y * 1000 + z;

  Pos3D above() {
    return Pos3D(x, y, z + 1);
  }

  Pos3D below() {
    return Pos3D(x, y, z - 1);
  }

  Pos3D left() {
    return Pos3D(x - 1, y, z);
  }

  Pos3D right() {
    return Pos3D(x + 1, y, z);
  }

  Pos3D behind() {
    return Pos3D(x, y + 1, z);
  }

  Pos3D infront() {
    return Pos3D(x, y - 1, z);
  }

  void printCoords() {
    print('$x, $y, $z ');
  }

  List<Pos3D> getNeighbours() {
    List<Pos3D> neighbourList = [
      above(),
      below(),
      left(),
      right(),
      behind(),
      infront()
    ];
    return neighbourList;
  }
}
