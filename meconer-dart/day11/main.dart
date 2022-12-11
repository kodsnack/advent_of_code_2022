import '../util/util.dart';

//const String inputFile = 'day11/example.txt';
const String inputFile = 'day11/input.txt';

Future<void> main(List<String> args) async {
  var lines = await readInput(inputFile);
  print('Part 1:');
  print(calcResultPart1(lines));

  print('Part 2:');
  lines = await readInput(inputFile);
  print(calcResultPart2(lines));
}

int calcResultPart1(List<String> lines) {
  final monkeyList = buildMonkeyList(lines);
  for (int roundNo = 0; roundNo < 20; roundNo++) {
    doRound(monkeyList);
  }
  List<int> inspectionCounts = [];
  for (final monkey in monkeyList) {
    inspectionCounts.add(monkey.inspectionCount);
  }
  inspectionCounts.sort();
  inspectionCounts = inspectionCounts.reversed.toList();
  return inspectionCounts[0] * inspectionCounts[1];
}

int calcResultPart2(List<String> lines) {
  final monkeyList = buildMonkeyList(lines);
  final monkeyCommon = getMonkeyCommon(monkeyList);
  for (int roundNo = 0; roundNo < 10000; roundNo++) {
    doRoundPart2(monkeyList, monkeyCommon);
  }
  List<int> inspectionCounts = [];
  for (final monkey in monkeyList) {
    inspectionCounts.add(monkey.inspectionCount);
  }
  inspectionCounts.sort();
  inspectionCounts = inspectionCounts.reversed.toList();
  return inspectionCounts[0] * inspectionCounts[1];
}

int getMonkeyCommon(List<Monkey> monkeyList) {
  int common = 1;
  for (final monkey in monkeyList) {
    common = common * monkey.divisor;
  }
  return common;
}

void doRound(List<Monkey> monkeyList) {
  for (final monkey in monkeyList) {
    // Inspect items
    monkey.inspectItems(monkeyList);
  }
}

void doRoundPart2(List<Monkey> monkeyList, int monkeyCommon) {
  for (final monkey in monkeyList) {
    // Inspect items
    monkey.inspectItemsPart2(monkeyList, monkeyCommon);
  }
}

List<Monkey> buildMonkeyList(List<String> lines) {
  List<Monkey> monkeyList = [];
  while (lines.isNotEmpty) {
    lines.removeAt(0); // Skip monkey no

    // Starting items
    final itemStr = lines.first.split(':')[1].split(',');
    final items = itemStr.map((e) => int.parse(e)).toList();
    lines.removeAt(0);

    // Operation
    final operation = buildOperation(lines.first);
    lines.removeAt(0);

    // Divisor
    final divisor = int.parse(lines.first.split(' ').last);
    lines.removeAt(0);

    // Monkey to throw to if divisible by divisor
    final trueMonkey = int.parse(lines.first.split(' ').last);
    lines.removeAt(0);

    // Monkey to throw to if _NOT_ divisible by divisor
    final falseMonkey = int.parse(lines.first.split(' ').last);
    lines.removeAt(0);

    // Remove empty line if we are not on the last monkey
    if (lines.isNotEmpty) lines.removeAt(0);

    Monkey monkey = Monkey(items, operation, divisor, trueMonkey, falseMonkey);
    monkeyList.add(monkey);
  }
  return monkeyList;
}

int Function(int) buildOperation(String line) {
  final opStr = line.split(':')[1].split('=')[1];
  final opParts = opStr.trim().split(' ');
  if (opParts[0] != 'old') throw Exception('Left part should always be old');

  if (opParts[2] == 'old') {
    if (opParts[1] == '*') {
      return ((old) => old * old);
    } else {
      // We have only * and + operators
      return ((old) => old + old);
    }
  } else {
    if (opParts[1] == '*') {
      return ((old) => old * int.parse(opParts[2]));
    } else {
      // We have only * and + operators
      return ((old) => old + int.parse(opParts[2]));
    }
  }
}

class Monkey {
  List<int> startingItems;
  int Function(int) operation;
  int divisor;
  int monkeyToThrowToIfTrue;
  int monkeyToThrowToIfFalse;
  int inspectionCount = 0;

  Monkey(this.startingItems, this.operation, this.divisor,
      this.monkeyToThrowToIfTrue, this.monkeyToThrowToIfFalse);

  void inspectItems(List<Monkey> monkeyList) {
    for (int item in startingItems) {
      // Do operation
      item = operation(item);
      // Get bored
      item = item ~/ 3; // Integer division
      // Check if divisible with divisor
      if (item % divisor == 0) {
        // True! Is divisible
        monkeyList[monkeyToThrowToIfTrue].startingItems.add(item);
      } else {
        // False, not divisible
        monkeyList[monkeyToThrowToIfFalse].startingItems.add(item);
      }
      inspectionCount++;
    }
    startingItems = [];
  }

  void inspectItemsPart2(List<Monkey> monkeyList, int monkeyCommon) {
    for (int item in startingItems) {
      // Do operation
      item = operation(item);
      item = item % monkeyCommon;
      // Check if divisible with divisor
      if (item % divisor == 0) {
        // True! Is divisible
        monkeyList[monkeyToThrowToIfTrue].startingItems.add(item);
      } else {
        // False, not divisible
        monkeyList[monkeyToThrowToIfFalse].startingItems.add(item);
      }
      inspectionCount++;
    }
    startingItems = [];
  }
}
