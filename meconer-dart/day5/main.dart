import '../util/util.dart';

//const String inputFile = 'day5/example.txt';
const String inputFile = 'day5/input.txt';

Future<void> main(List<String> args) async {
  final lines = await readInput(inputFile);
  print('Part 1:');
  print(resultOfPart1(lines));
  print('Part 2:');
  print(resultOfPart2(lines));
}

String resultOfPart1(List<String> lines) {
  final stacks = getStacks(lines);
  final moves = getMoves(lines);
  doMoves(stacks, moves);
  String result = '';
  for (var stack in stacks) {
    result += stack.last;
  }
  return result;
}

String resultOfPart2(List<String> lines) {
  final stacks = getStacks(lines);
  final moves = getMoves(lines);
  doMovesPart2(stacks, moves);
  String result = '';
  for (var stack in stacks) {
    result += stack.last;
  }
  return result;
}

class Move {
  int noOfItemsToMove;
  int moveFrom;
  int moveTo;

  Move(this.noOfItemsToMove, this.moveFrom, this.moveTo);

  factory Move.fromMoveLine(String moveLine) {
    final lineParts = moveLine.trim().split(' ');
    return Move(int.parse(lineParts[1]), int.parse(lineParts[3]),
        int.parse(lineParts[5]));
  }

  void doMove(List<List<String>> stacks, String moveLine) {
    for (var moveNo = 0; moveNo < noOfItemsToMove; moveNo++) {
      final itemToMove = stacks[moveFrom - 1].removeLast();
      stacks[moveTo - 1].add(itemToMove);
    }
  }

  void doMovePart2(List<List<String>> stacks, String moveLine) {
    int end = stacks[moveFrom - 1].length;
    int start = end - noOfItemsToMove;
    List<String> itemsToMove = stacks[moveFrom - 1].sublist(start, end);
    stacks[moveFrom - 1].removeRange(start, end);
    stacks[moveTo - 1].addAll(itemsToMove);
  }
}

void doMoves(List<List<String>> stacks, List<String> moves) {
  for (final moveLine in moves) {
    final move = Move.fromMoveLine(moveLine);
    move.doMove(stacks, moveLine);
  }
}

void doMovesPart2(List<List<String>> stacks, List<String> moves) {
  for (final moveLine in moves) {
    final move = Move.fromMoveLine(moveLine);
    move.doMovePart2(stacks, moveLine);
  }
}

List<List<String>> getStacks(List<String> lines) {
  final stackListLineNo = findStackListLineNo(lines);
  int noOfStacks = findNoOfStacks(lines, stackListLineNo);
  List<List<String>> stacks = List.generate(noOfStacks, (_) => []);
  for (int lineNo = stackListLineNo - 1; lineNo >= 0; lineNo--) {
    for (var stackNo = 0; stackNo < noOfStacks; stackNo++) {
      int stackLetterPos = 1 + stackNo * 4;
      String stackLetterOrSpace = lines[lineNo][stackLetterPos];
      if (stackLetterOrSpace != ' ') {
        // Push letter on this stack
        stacks[stackNo].add(stackLetterOrSpace);
      }
    }
  }
  return stacks;
}

List<String> getMoves(List<String> lines) {
  int stackListLineNo = findStackListLineNo(lines);
  return lines.sublist(stackListLineNo + 2);
}

int findStackListLineNo(List<String> lines) {
  int moveStartLineNo = 0;
  for (int lineNo = 0; lineNo < lines.length; lineNo++) {
    if (lines[lineNo].trim().isEmpty) {
      // Stacklist line is the line above the first empty line
      moveStartLineNo = lineNo - 1;
      break;
    }
  }
  return moveStartLineNo;
}

int findNoOfStacks(List<String> lines, int stackListLineNo) {
  return int.parse(lines[stackListLineNo].trim().split(' ').last);
}
