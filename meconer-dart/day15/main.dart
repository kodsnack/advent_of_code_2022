import 'dart:math';

import '../util/pos.dart';
import '../util/range.dart';
import '../util/util.dart';

//const String inputFile = 'day15/example.txt';
const String inputFile = 'day15/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);
  print('Part 1:');
  print(calcResultP1(inputLines));

  inputLines = await readInput(inputFile);
  print('Part 2:');
  print(calcResultP2(inputLines));
}

int calcResultP1(List<String> inputLines) {
  Grid grid = Grid.fromInputlines(inputLines);
  if (inputFile.contains('example')) grid.drawGrid();
  return grid.countCoveredPointsOnLine(2000000);
}

int calcResultP2(List<String> inputLines) {
  Grid grid = Grid.fromInputlines(inputLines);
  int maxCoord = 4000000;
  if (inputFile.contains('example')) {
    grid.drawGrid();
    maxCoord = 20;
  }
  Pos? pos = grid.getPosOfBeacon(maxCoord);
  if (pos != null) return pos.x * 4000000 + pos.y;
  return 0;
}

class Grid {
  Set<Sensor> sensorSet = {};
  Set<Beacon> beaconSet = {};
  Range range = Range();

  Grid.fromInputlines(List<String> inputLines) {
    for (var inputLine in inputLines) {
      Sensor sensor = Sensor.fromInputline(inputLine);
      range.extend(sensor.pos);

      Beacon beacon = Beacon.fromInputline(inputLine);
      range.extend(beacon.pos);

      sensor.mDistToClosestBeacon = sensor.pos.manhattanDistance(beacon.pos);

      sensorSet.add(sensor);
      beaconSet.add(beacon);
    }
  }

  void drawGrid() {
    for (int rowNo = range.yMin; rowNo <= range.yMax; rowNo++) {
      String printLine = '$rowNo ';
      while (printLine.length < 3) {
        printLine = ' ' + printLine;
      }
      for (int colNo = range.xMin; colNo <= range.xMax; colNo++) {
        String media = '.';
        for (final sensor in sensorSet) {
          if (sensor.pos == Pos(colNo, rowNo)) {
            media = 'S';
            break;
          }
        }
        for (final beacon in beaconSet) {
          if (beacon.pos == Pos(colNo, rowNo)) {
            media = 'B';
            break;
          }
        }
        printLine += media;
      }
      print(printLine);
    }
  }

  int countCoveredPointsOnLine(int rowNo) {
    CoveredRange coveredRange = CoveredRange();
    for (final sensor in sensorSet) {
      final xRange = sensor.getCoveredRangeOnY(rowNo);
      if (xRange != null) coveredRange.addRange(xRange);
    }
    // Count existing
    // beacons on this line
    int beaconCount = 0;
    for (final beacon in beaconSet) {
      if (beacon.pos.y == rowNo) {
        beaconCount++;
      }
    }
    int noOfCoveredPoints = coveredRange.getNoOfCoveredPoints();
    return noOfCoveredPoints - beaconCount;
  }

  Pos? getPosOfBeacon(int maxCoord) {
    int count = 0;
    Pos? pos;
    for (int y = 0; y < maxCoord; y++) {
      CoveredRange coveredRange = getCoveredRangeOnLine(y);
      CoveredRange searchRange = CoveredRange();
      searchRange.addRange(XRange(0, maxCoord));
      for (final rangeItem in coveredRange.rangeList) {
        searchRange.removeRange(rangeItem);
      }
      if (searchRange.rangeList.isNotEmpty) {
        int len = searchRange.rangeList.length;
        if (len != 1) print('!!!!');
        count++;
        pos = Pos(searchRange.rangeList.first.start, y);
      }
    }
    return pos;
  }

  CoveredRange getCoveredRangeOnLine(int rowNo) {
    CoveredRange coveredRange = CoveredRange();
    for (final sensor in sensorSet) {
      final xRange = sensor.getCoveredRangeOnY(rowNo);
      if (xRange != null) coveredRange.addRange(xRange);
    }
    return coveredRange;
  }
}

class Sensor {
  Pos pos;

  int mDistToClosestBeacon = -1;

  Sensor(Pos this.pos);

  factory Sensor.fromInputline(String inputLine) {
    final lineParts = inputLine.split(':');
    String xValuePart = lineParts[0].split(',')[0];
    final posXOfSensor = xValuePart.indexOf('x=') + 2;
    int sensorXPos = int.parse(xValuePart.substring(posXOfSensor));
    int sensorYPos = int.parse(lineParts[0].split(',')[1].substring(3));
    return Sensor(Pos(sensorXPos, sensorYPos));
  }

  XRange? getCoveredRangeOnY(int y) {
    int yDist = (pos.y - y).abs();
    if (yDist > mDistToClosestBeacon) return null;
    int startx = pos.x - mDistToClosestBeacon + yDist;
    int endx = pos.x + mDistToClosestBeacon - yDist;
    return XRange(startx, endx);
  }
}

class XRange {
  int start;
  int end;

  XRange(this.start, this.end);

  bool overlap(XRange range) {
    if (start <= range.start && end >= range.start) {
      return true;
    }
    if (range.start <= start && range.end >= start) {
      return true;
    }
    return false;
  }

  XRange combineRange(XRange nextRange) {
    return XRange(min(start, nextRange.start), max(end, nextRange.end));
  }

  bool isContained(XRange rangeToCheck) {
    return start < rangeToCheck.start && end > rangeToCheck.end;
  }

  XRange? removeNotContainedRange(XRange rangeToRemove) {
    if (start >= rangeToRemove.start && end <= rangeToRemove.end) return null;
    if (start < rangeToRemove.start)
      return XRange(start, rangeToRemove.start - 1);
    if (end > rangeToRemove.end) return XRange(rangeToRemove.end + 1, end);
    return XRange(start, end);
  }
}

class CoveredRange {
  List<XRange> rangeList = [];

  addRange(XRange rangeToAdd) {
    rangeList.add(rangeToAdd);
    eliminateOverlaps();
  }

  void eliminateOverlaps() {
    if (rangeList.length < 2) return;
    rangeList
        .sort((r1, r2) => r1.start.compareTo(r2.start)); // Sort on rangestart
    List<XRange> newList = [];

    var firstRange = rangeList[0];
    int idx = 1;
    while (idx < rangeList.length) {
      var nextRange = rangeList[idx];
      while (firstRange.overlap(nextRange)) {
        firstRange = firstRange.combineRange(nextRange);
        idx++;
        if (idx >= rangeList.length) {
          break;
        } else {
          nextRange = rangeList[idx];
        }
      }
      newList.add(firstRange);
      if (idx < rangeList.length) {
        firstRange = nextRange;
        nextRange = rangeList[idx];
      }
    }
    rangeList = newList;
  }

  int getNoOfCoveredPoints() {
    int noOfPoints = 0;
    for (var range in rangeList) {
      noOfPoints += range.end - range.start + 1;
    }
    return noOfPoints;
  }

  void removeRange(XRange rangeToRemove) {
    List<XRange> newList = [];
    for (int idx = 0; idx < rangeList.length; idx++) {
      var range = rangeList[idx];
      if (range.isContained(rangeToRemove)) {
        newList.add(XRange(range.start, rangeToRemove.start - 1));
        newList.add(XRange(rangeToRemove.end + 1, range.end));
        continue;
      }
      if (range.overlap(rangeToRemove)) {
        XRange? newRange = range.removeNotContainedRange(rangeToRemove);
        if (newRange != null) {
          newList.add(newRange);
        }
      }
    }
    rangeList = newList;
  }
}

class Beacon {
  Pos pos;

  @override
  bool operator ==(Object other) {
    if (identical(this, other)) return true;
    return other is Beacon && (pos.x == other.pos.x && pos.y == other.pos.y);
  }

  int get hashCode => pos.hashCode;

  Beacon(this.pos);

  factory Beacon.fromInputline(String inputLine) {
    final lineParts = inputLine.split(':');
    String xValuePart = lineParts[1].split(',')[0];
    final posXOfBeacon = xValuePart.indexOf('x=') + 2;
    int beaconXPos = int.parse(xValuePart.substring(posXOfBeacon));
    int beaconYPos = int.parse(lineParts[1].split(',')[1].substring(3));
    return Beacon(Pos(beaconXPos, beaconYPos));
  }
}
