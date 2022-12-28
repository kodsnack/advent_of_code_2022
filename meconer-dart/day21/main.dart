import '../util/util.dart';

//const String inputFile = 'day21/example.txt';
const String inputFile = 'day21/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);

  print('Part 1:');
  num resultP1 = calcResultP1(inputLines);
  print(resultP1);

  print('Part 2:');
  int resultP2 = calcResultP2(inputLines);
  print(resultP2);
}

class Monkey {
  String name;
  num yelledNumber = 0;
  bool hasYelled = false;
  Operation? operation;

  Monkey(this.name);

  factory Monkey.fromInputLine(String inputLine) {
    String name = inputLine.split(':')[0];
    Monkey monkey = Monkey(name);
    String opOrNumber = inputLine.split(':')[1].trim();
    final opNumberParts = opOrNumber.split(' ');
    if (opNumberParts.length == 1) {
      monkey.yelledNumber = int.parse(opNumberParts[0].trim());
      monkey.hasYelled = true;
    } else {
      monkey.operation =
          Operation(opNumberParts[0], opNumberParts[1], opNumberParts[2]);
    }
    return monkey;
  }
}

class Operation {
  String monkey1;
  String monkey2;
  String operator;

  Operation(this.monkey1, this.operator, this.monkey2);

  num doOperation(num val1, num val2) {
    switch (operator) {
      case '+':
        return val1 + val2;
      case '*':
        return val1 * val2;
      case '-':
        return val1 - val2;
      case '/':
        return val1 / val2;
      case '=':
        return val1.compareTo(val2);
      default:
        return 0;
    }
  }
}

num calcResultP1(List<String> inputLines) {
  Map<String, Monkey> monkeys = Map();

  for (var inputLine in inputLines) {
    Monkey monkey = Monkey.fromInputLine(inputLine);
    monkeys[monkey.name] = monkey;
  }

  while (!monkeys['root']!.hasYelled) {
    for (Monkey monkey in monkeys.values) {
      if (!monkey.hasYelled) {
        // Must be an operation

        if (monkeys[monkey.operation!.monkey1]!.hasYelled &&
            monkeys[monkey.operation!.monkey2]!.hasYelled) {
          num val1 = monkeys[monkey.operation!.monkey1]!.yelledNumber;
          num val2 = monkeys[monkey.operation!.monkey2]!.yelledNumber;
          num val = monkey.operation!.doOperation(val1, val2);
          monkey.yelledNumber = val;
          monkey.hasYelled = true;
        }
      }
    }
  }

  return monkeys['root']!.yelledNumber;
}

// På uppgiftens input så är vänstra värdet en linjär funktion av inputvärdet
// Högra värdet är konstant 52282191702834.0
/*
leftVal = f(input) = k*x + C
Två av testade värden ger
f(0) = 107992431124288.5 => C = 107992431124288.5

f(100000001) = 107990626679826.0 => k = -18.044444444555555 ungefär.
 
Vi vill att f(input) = 52282191702834.0

k * input + C = 52282191702834.0
dvs input = (52282191702834.0 - C) / k

vilket blir ungefär 3087390115701.9897

Vi börjar med testinput på 3087390115700 och räknar uppåt

Hittat resultatet på 3087390115721! 

*/
int calcResultP2(List<String> inputLines) {
  Map<String, Monkey> monkeys = Map();

  for (var inputLine in inputLines) {
    Monkey monkey = Monkey.fromInputLine(inputLine);
    if (monkey.name == 'root') {
      monkey.operation!.operator = '=';
    }
    monkeys[monkey.name] = monkey;
  }

  bool ready = false;
  int testValue = 3087390115700;
  while (!ready) {
    // Reset all monkeys
    for (Monkey monkey in monkeys.values) {
      if (monkey.operation != null) monkey.hasYelled = false;
    }

    monkeys['humn']!.yelledNumber = testValue;

    while (!monkeys['root']!.hasYelled) {
      for (Monkey monkey in monkeys.values) {
        if (!monkey.hasYelled) {
          // Must be an operation

          if (monkeys[monkey.operation!.monkey1]!.hasYelled &&
              monkeys[monkey.operation!.monkey2]!.hasYelled) {
            num val1 = monkeys[monkey.operation!.monkey1]!.yelledNumber;
            num val2 = monkeys[monkey.operation!.monkey2]!.yelledNumber;
            num val = monkey.operation!.doOperation(val1, val2);
            monkey.yelledNumber = val;
            monkey.hasYelled = true;
          }
        }
      }
    }

    ready = monkeys['root']!.yelledNumber == 0;
    final monkeyLeft = monkeys[monkeys['root']!.operation!.monkey1];
    num leftVal = monkeyLeft!.yelledNumber;
    final monkeyRight = monkeys[monkeys['root']!.operation!.monkey2];
    num rightVal = monkeyRight!.yelledNumber;

    print(
        '$testValue : ${monkeyLeft.name}->$leftVal == ${monkeyRight.name}->$rightVal');
//    print('$testValue, $leftVal, $rightVal');
    if (!ready) {
      testValue++;
    } else {
      print('Found');
    }
    //ready = true;
  }

  return testValue;
}
