import '../util/util.dart';

//const String inputFile = 'day20/example.txt';
const String inputFile = 'day20/input.txt';

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

  origNumbers = [];
  for (int i = 0; i < inputLines.length; i++) {
    final inputLine = inputLines[i];
    origNumbers.add(Number(i, int.parse(inputLine)));
  }

  print('Part 2:');
  int resultP2 = calcResultP2(origNumbers);
  print(resultP2);
}

class Number {
  int pos;
  int number;
  Number(this.pos, this.number);
}

int calcResultP1(List<Number> numbers) {
  int listLength = numbers.length;
  printNumbers(numbers);
  for (int idxToMove = 0; idxToMove < numbers.length; idxToMove++) {
    int posToMove = numbers[idxToMove].pos;
    int numberToMove = numbers[idxToMove].number;
    if (numberToMove == 0) continue;

    int newPosition = numberToMove + posToMove;
    newPosition = newPosition % (listLength - 1);

    for (final number in numbers) {
      if (number.pos > posToMove) number.pos--;
    }
    numbers[idxToMove].pos = newPosition;

    for (int i = 0; i < listLength; i++) {
      if (i != idxToMove) {
        if (numbers[i].pos >= newPosition) numbers[i].pos++;
      }
    }
    printNumbers(numbers);
  }

  numbers.sort((a, b) => a.pos.compareTo(b.pos));
  int posOfZero = 0;
  for (int i = 0; i < numbers.length; i++) {
    if (numbers[i].number == 0) posOfZero = i;
  }
  int number1 = numbers[(1000 + posOfZero) % listLength].number;
  int number2 = numbers[(2000 + posOfZero) % listLength].number;
  int number3 = numbers[(3000 + posOfZero) % listLength].number;
  return number1 + number2 + number3;
}

int calcResultP2(List<Number> numbers) {
  int decryptionKey = 811589153;
  for (var number in numbers) {
    number.number *= decryptionKey;
  }
  int listLength = numbers.length;

  printNumbers(numbers);

  for (var n = 0; n < 10; n++) {
    for (int idxToMove = 0; idxToMove < numbers.length; idxToMove++) {
      int posToMove = numbers[idxToMove].pos;
      int numberToMove = numbers[idxToMove].number;
      if (numberToMove == 0) continue;

      int newPosition = numberToMove + posToMove;
      newPosition = newPosition % (listLength - 1);

      for (final number in numbers) {
        if (number.pos > posToMove) number.pos--;
      }
      numbers[idxToMove].pos = newPosition;

      for (int i = 0; i < listLength; i++) {
        if (i != idxToMove) {
          if (numbers[i].pos >= newPosition) numbers[i].pos++;
        }
      }
    }
    printNumbers(numbers);
  }

  numbers.sort((a, b) => a.pos.compareTo(b.pos));
  int posOfZero = 0;
  for (int i = 0; i < numbers.length; i++) {
    if (numbers[i].number == 0) posOfZero = i;
  }
  int number1 = numbers[(1000 + posOfZero) % listLength].number;
  int number2 = numbers[(2000 + posOfZero) % listLength].number;
  int number3 = numbers[(3000 + posOfZero) % listLength].number;
  return number1 + number2 + number3;
}

void printNumbers(List<Number> numbers) {
  return;
  List<Number> printList = List.from(numbers);
  printList.sort((a, b) => a.pos.compareTo(b.pos));
  String line = '';
  for (final number in printList) {
    line += '${number.number}, ';
  }
  print(line);
}

int oldCalcResultP1(List<Number> origNumbers) {
  List<int> newNumbers = [];
  for (final number in origNumbers) {
    newNumbers.add(number.number);
  }
  int listLength = origNumbers.length;
  for (int idxToMove = 0; idxToMove < origNumbers.length; idxToMove++) {
    int posToMove = origNumbers[idxToMove].pos;
    int numberToMove = origNumbers[idxToMove].number;
    if (numberToMove == 0) continue;

    int newPosition = numberToMove + posToMove;

    if (newPosition <= 0) newPosition--;
    if (newPosition >= listLength) newPosition++;

    if (numberToMove > listLength) newPosition--;
    if (numberToMove < -listLength) newPosition++;

    while (newPosition <= 0) {
      newPosition += listLength;
    }
    while (newPosition >= listLength) {
      newPosition -= listLength;
    }

    final listBeforeNumber = newNumbers.sublist(0, posToMove);
    final listAfterNumber = newNumbers.sublist(posToMove + 1);

    for (final number in origNumbers) {
      if (number.pos > posToMove) number.pos--;
    }

    if (newPosition < listBeforeNumber.length) {
      listBeforeNumber.insert(newPosition, numberToMove);
    } else {
      listAfterNumber.insert(
          newPosition - listBeforeNumber.length, numberToMove);
    }

    for (final number in origNumbers) {
      if (number.pos >= newPosition) number.pos++;
    }
    origNumbers[idxToMove].pos = newPosition;

    newNumbers = listBeforeNumber + listAfterNumber;
  }
  int posOfZero = 0;
  for (int i = 0; i < newNumbers.length; i++) {
    if (newNumbers[i] == 0) posOfZero = i;
  }
  int number1 = newNumbers[(1000 + posOfZero) % listLength];
  int number2 = newNumbers[(2000 + posOfZero) % listLength];
  int number3 = newNumbers[(3000 + posOfZero) % listLength];
  return number1 + number2 + number3;
}
