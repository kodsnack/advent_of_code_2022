import '../util/util.dart';

//const String inputFile = 'day25/example.txt';
const String inputFile = 'day25/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);

  print('Part 1:');
  String resultP1 = calcResultP1(inputLines);
  print(resultP1);
}

String calcResultP1(List<String> inputLines) {
  int sum = 0;
  for (var line in inputLines) {
    int number = intFromSnafu(line);
    print('$line => $number');
    sum += number;
  }
  return snafuFromInt(sum);
}

int intFromSnafu(String line) {
  int digitVal = 1;
  Map<String, int> snafuNumbers = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2};
  int number = 0;
  while (line.isNotEmpty) {
    String char = line.substring(line.length - 1);
    int snafuNumber = snafuNumbers[char]!;
    number += digitVal * snafuNumber;
    line = line.substring(0, line.length - 1);
    digitVal *= 5;
  }
  return number;
}

String snafuFromInt(int number) {
  String snafu = '';
  List<String> snafuDigits = ['=', '-', '0', '1', '2'];

  int digValue = 1;
  int maxVal = 2; // Max value with 1 digit
  int digits = 0;
  while (maxVal < number) {
    digits++;
    digValue *= 5;
    maxVal += 2 * digValue;
  }
  for (int digit = digits; digit >= 0; digit--) {
    int currNumber = number ~/ digValue;
    int rest = number - currNumber * digValue;
    if (rest.abs() > 2 * digValue / 5) currNumber = currNumber + rest.sign;
    int snafuIdx = currNumber + 2;
    snafu += snafuDigits[snafuIdx];
    number = number - currNumber * digValue;
    digValue ~/= 5;
  }
  return snafu;
}
