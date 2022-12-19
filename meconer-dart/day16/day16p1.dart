import 'dart:math';

import '../util/util.dart';

//const String inputFile = 'day16/example.txt';
const String inputFile = 'day16/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);
  print('Part 1:');
  print(calcResult(inputLines));
}

const int totalTime = 30;

int calcResult(List<String> inputLines) {
  ValveSystem valveSystem = ValveSystem.fromInputLines(inputLines);

  int result = valveSystem.findBestPath();
  return result;
}

class ValveSystem {
  List<Valve> valveList = [];

  ValveSystem();

  factory ValveSystem.fromInputLines(List<String> inputLines) {
    ValveSystem valveSystem = ValveSystem();
    for (final inputLine in inputLines) {
      Valve valve = Valve.fromInputLine(inputLine);
      valveSystem.valveList.add(valve);
    }

    return valveSystem;
  }

  int findShortestPathToValve(Valve startValve, Valve target) {
    // Dijkstra setup
    Set<Valve> unVisitedNodes = {};
    Set<Valve> visitedNodes = {};
    Set<Valve> allNodes = {};
    for (final valve in valveList) {
      allNodes.add(valve);
      if (valve == startValve) {
        valve.dijkstraDist = 0;
        visitedNodes.add(valve);
      } else {
        unVisitedNodes.add(valve);
        valve.dijkstraDist = veryLargeNumber;
      }
    }

    Valve currValve = startValve;
    while (true) {
      if (currValve == target) {
        return currValve.dijkstraDist;
      }
      for (final nextValveName in currValve.neighbours) {
        Valve nextValve = findValveWithName(nextValveName)!;
        if (currValve.dijkstraDist + 1 < nextValve.dijkstraDist) {
          nextValve.dijkstraDist = currValve.dijkstraDist + 1;
        }
      }
      visitedNodes.add(currValve);
      unVisitedNodes.remove(currValve);
      currValve = getUnvisitedWithLowestDist(unVisitedNodes);
    }
  }

  Set<Valve> findValvesWithFlow() {
    Set<Valve> valvesWithFlow = {};
    for (var valve in valveList) {
      if (valve.flowRate > 0) valvesWithFlow.add(valve);
    }
    return valvesWithFlow;
  }

  Valve? findValveWithName(String s) {
    for (var valve in valveList) {
      if (valve.name == s) {
        return valve;
      }
    }
    return null;
  }

  int findBestPath() {
    Set<Valve> valvesWithFlow = findValvesWithFlow();
    Valve currValve = findValveWithName('AA')!;
    int bestResult = 0;
    for (final nextValve in valvesWithFlow) {
      final remainingValves = Set<Valve>.from(valvesWithFlow);
      int time = 1 + findShortestPathToValve(currValve, nextValve);
      remainingValves.remove(nextValve);
      int resultOfPath = calcBestPathValue(nextValve, remainingValves, time);
      int result = resultOfPath + nextValve.flowRate * (totalTime - time);
      print(result);
      bestResult = max(result, bestResult);
    }
    return bestResult;
  }

  int calcBestPathValue(
      Valve startValve, Set<Valve> valvesToCheck, int elapsedTime) {
    if (valvesToCheck.isEmpty) {
      return 0;
    }
    if (elapsedTime > 30) {
      return 0;
    }
    int bestResult = 0;
    for (final nextValve in valvesToCheck) {
      final remainingValves = Set<Valve>.from(valvesToCheck);
      int time = findShortestPathToValve(startValve, nextValve);
      time += 1 + elapsedTime;
      remainingValves.remove(nextValve);
      int resultOfPath = calcBestPathValue(nextValve, remainingValves, time);
      int result = resultOfPath + nextValve.flowRate * (totalTime - time);
      bestResult = max(result, bestResult);
    }
    return bestResult;
  }

  Valve getUnvisitedWithLowestDist(Set<Valve> unVisitedNodes) {
    List<Valve> list = unVisitedNodes.toList();
    list.sort((a, b) => a.dijkstraDist.compareTo(b.dijkstraDist));
    return list.first;
  }
}

class Valve {
  String name;
  List<String> neighbours = [];
  int flowRate;
  int dijkstraDist = veryLargeNumber;

  Valve(this.name, this.flowRate);

  factory Valve.fromInputLine(String inputLine) {
    // Create the valve;
    String name = inputLine.split(' ')[1];
    int flowRate = int.parse(inputLine.split(';')[0].split('=')[1]);
    Valve valve = Valve(name, flowRate);

    // Create the list of paths to other valves
    final lineParts = inputLine.split(' ');
    while (!lineParts.last.contains('valve')) {
      String path = lineParts.removeLast();
      if (path.endsWith(',')) path = path.substring(0, path.length - 1);
      valve.neighbours.add(path);
    }
    return valve;
  }
}
