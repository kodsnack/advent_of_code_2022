import 'dart:io';

//const String inputFile = 'day2/example.txt';
const String inputFile = 'day2/input.txt';

Future<void> main(List<String> args) async {
  final lines = await readInput();
  print('Part 1:');
  print(calculateScorePart1(lines));
  print('\nPart 2:');
  print(calculateScorePart2(lines));
}

int calculateScorePart1(List<String> lines) {
  int totalScore = 0;
  for (final line in lines) {
    final moves = line.split(' ');
    final opponentMove = moves[0];
    final myMove = moves[1];
    int score = getScorePart1(opponentMove, myMove);
    totalScore += score;
  }
  return totalScore;
}

int calculateScorePart2(List<String> lines) {
  int totalScore = 0;
  for (final line in lines) {
    final moves = line.split(' ');
    final opponentMove = moves[0];
    final lossDrawWin = moves[1];
    int score = getScorePart2(opponentMove, lossDrawWin);
    totalScore += score;
  }
  return totalScore;
}

int getScorePart1(String opponentMove, String myMove) {
  // Calculate win points
  // 0 for loss, 3 for draw and 6 for win
  int winScore = 0;
  switch (opponentMove) {
    case 'A': // rock
      if (myMove == 'X') {
        // rock , rock => draw
        winScore = 3;
      } else if (myMove == 'Y') {
        // rock , paper => win
        winScore = 6;
      } else {
        // rock , scissor => loss
        winScore = 0;
      }
      break;

    case 'B': // paper
      if (myMove == 'X') {
        // paper , rock => loss
        winScore = 0;
      } else if (myMove == 'Y') {
        // paper , paper => draw
        winScore = 3;
      } else {
        // paper , scissor => win
        winScore = 6;
      }
      break;

    case 'C': // scissor
      if (myMove == 'X') {
        // scissor , rock => win
        winScore = 6;
      } else if (myMove == 'Y') {
        // scissor , paper => loss
        winScore = 0;
      } else {
        // scissor , scissor => draw
        winScore = 3;
      }
      break;
    default:
  }

  // And then points for my move
  int moveScore = 0;
  switch (myMove) {
    case 'X':
      moveScore = 1;
      break;
    case 'Y':
      moveScore = 2;
      break;
    case 'Z':
      moveScore = 3;
      break;
    default:
  }

  return winScore + moveScore;
}

int getScorePart2(String opponentMove, String lossDrawWin) {
  // Calculate win points
  // 0 for loss, 3 for draw and 6 for win
  int score = 0;
  switch (opponentMove) {
    case 'A': // rock
      if (lossDrawWin == 'X') {
        // rock , loss => scissor => 0 for loss and 3 for scissor
        score = 3;
      } else if (lossDrawWin == 'Y') {
        // rock , draw => rock => 3 for draw and 1 for rock
        score = 4;
      } else {
        // rock , win => paper => 6 for win and 2 for paper
        score = 8;
      }
      break;

    case 'B': // paper
      if (lossDrawWin == 'X') {
        // paper , loss => rock => 0 for loss and 1 for rock
        score = 1;
      } else if (lossDrawWin == 'Y') {
        // paper , draw => paper => 3 for draw and 2 for paper
        score = 5;
      } else {
        // paper , win => scissor => 6 for win and 3 for scissor
        score = 9;
      }
      break;

    case 'C': // scissor
      if (lossDrawWin == 'X') {
        // scissor , loss => paper => 0 for loss and 2for paper
        score = 2;
      } else if (lossDrawWin == 'Y') {
        // scissor , draw => scissor => 3 for draw and 3 for scissor
        score = 6;
      } else {
        // scissor , win => rock => 6 for win and 1 for rock
        score = 7;
      }
      break;
    default:
  }

  return score;
}

Future<List<String>> readInput() {
  final file = File(inputFile);
  return file.readAsLines();
}
