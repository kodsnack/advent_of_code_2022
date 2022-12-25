import '../util/util.dart';

const String inputFile = 'day20/example.txt';
//const String inputFile = 'day20/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);

  List<Number> origNumbers = [];
  for (int i = 0; i < inputLines.length; i++) {
    final inputLine = inputLines[i];
    origNumbers.add(Number(i, int.parse(inputLine)));
  }

  print('Part 1:');
  int resultP1 = calcResultP1(origNumbers);
  print(resultP1);
}

class Number {
  int orderNo;
  int number;
  Number(this.orderNo, this.number);
}

int calcResultP1(List<Number> origNumbers) {
  for (int idxToMove = 0; idxToMove < origNumbers.length; idxToMove++) {}
  return 0;
}
