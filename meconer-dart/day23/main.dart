import '../util/util.dart';

const String inputFile = 'day23/example.txt';
//const String inputFile = 'day23/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);

  print('Part 1:');
  int resultP1 = calcResultP1(inputLines);
  print(resultP1);
}

int calcResultP1(List<String> inputLines) {
  return 0;
}
