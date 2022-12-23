import '../util/util.dart';

//const String inputFile = 'day10/example.txt';
const String inputFile = 'day10/input.txt';

Future<void> main(List<String> args) async {
  var lines = await readInput(inputFile);
  print('Part 1:');
  print(calcResultPart1(lines));

  print('Part 2:');
  doPart2(lines); // Shows FECZELHE
}

int calcResultPart1(List<String> lines) {
  int xReg = 1;
  List<int> xRegList = [xReg];
  for (final line in lines) {
    final lineParts = line.split(' ');
    if (lineParts[0] == 'noop') {
      xRegList.add(xReg);
    }
    if (lineParts[0] == 'addx') {
      xRegList.add(xReg);
      xRegList.add(xReg);
      xReg += int.parse(lineParts[1]);
    }
  }
  int sumOfSignalStrength = 0;
  for (var clockIdx = 20; clockIdx < xRegList.length; clockIdx += 40) {
    final signalStrength = clockIdx * xRegList[clockIdx];
    sumOfSignalStrength += signalStrength;
  }
  return sumOfSignalStrength;
}

void doPart2(List<String> lines) {
  int xReg = 1;
  int pos = 0;

  String lineToPrint = '';
  for (final line in lines) {
    final lineParts = line.split(' ');
    if (lineParts[0] == 'noop') {
      lineToPrint += getPixel(pos, xReg);
      pos = (pos + 1) % 40;
      lineToPrint = printCheck(pos, lineToPrint);
    }
    if (lineParts[0] == 'addx') {
      lineToPrint += getPixel(pos, xReg);
      pos = (pos + 1) % 40;
      lineToPrint = printCheck(pos, lineToPrint);
      lineToPrint += getPixel(pos, xReg);
      pos = (pos + 1) % 40;
      lineToPrint = printCheck(pos, lineToPrint);
      xReg += int.parse(lineParts[1]);
    }
  }
}

String printCheck(int pos, String lineToPrint) {
  if (pos == 0) {
    print(lineToPrint);
    lineToPrint = '';
  }
  return lineToPrint;
}

String getPixel(int pos, int xReg) {
  return isSpritepixel(pos, xReg) ? '#' : ' ';
}

bool isSpritepixel(int pos, int xReg) {
  return (pos >= xReg - 1 && pos < xReg + 2);
}
