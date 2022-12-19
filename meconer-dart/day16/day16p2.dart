import 'dart:math';

import '../util/util.dart';

//const String inputFile = 'day16/example.txt';
const String inputFile = 'day16/input.txt';

Future<void> main(List<String> args) async {
  var inputLines = await readInput(inputFile);
  print('Part 2:');
  print(calcResult(inputLines));

  inputLines = await readInput(inputFile);
}

const int totalTime = 26;

int calcResult(List<String> inputLines) {
  ValveSystem valveSystem = ValveSystem.fromInputLines(inputLines);
  valveSystem.calculateDistances();
  valveSystem.removeIrrelevantNodes();

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
    Valve startValve = findValveWithName('AA')!;
    int bestResult = 0;
    int pathCount = 0;
    final myRemainingValves = Set<Valve>.from(valvesWithFlow);
    for (final myNextValve in valvesWithFlow) {
      print('MyNextValve : ${myNextValve.name}');
      myRemainingValves.remove(myNextValve);
      String myPath = myNextValve.name;
      for (Valve elephantsNextValve in myRemainingValves) {
        final remainingValves = Set<Valve>.from(valvesWithFlow);
        remainingValves.remove(myNextValve);
        remainingValves.remove(elephantsNextValve);
        print('Elephants next valve : ${elephantsNextValve.name}');
        String elephantsPath = elephantsNextValve.name;
        pathCount++;
        int myTime = 1 + startValve.distanceTo[myNextValve.name]!;
        int myResultForThisValve = myNextValve.flowRate * (totalTime - myTime);
        myPath = '$myPath - $myTime';

        int elephantsTime = 1 + startValve.distanceTo[elephantsNextValve.name]!;
        int elephantsResultForThisValve =
            elephantsNextValve.flowRate * (totalTime - elephantsTime);
        elephantsPath = '$elephantsPath - $elephantsTime';

        int resultOfPath = calcBestPathValue(myNextValve, elephantsNextValve,
            remainingValves, myTime, elephantsTime, myPath, elephantsPath);

        int result =
            resultOfPath + myResultForThisValve + elephantsResultForThisValve;
        print('$pathCount : $result');
        bestResult = max(result, bestResult);
        print('Best so far : $bestResult');
      }
    }
    return bestResult;
  }

  int calcBestPathValue(
      Valve myStartValve,
      Valve elephantsStartValve,
      Set<Valve> valvesToCheck,
      int myElapsedTime,
      int elephantsElapsedTime,
      String myPath,
      String elephantsPath) {
    if (valvesToCheck.isEmpty) {
      return 0;
    }
    if (myElapsedTime > totalTime && elephantsElapsedTime > totalTime) {
      return 0;
    }
    int bestResult = 0;
    if (myElapsedTime >= totalTime) {
      // Only elephant has time left. Check best of that
      Set<Valve> elephValvesToCheck = Set<Valve>.from(valvesToCheck);
      while (elephValvesToCheck.isNotEmpty) {
        final elephantsNextValve = elephValvesToCheck.first;
        elephValvesToCheck.remove(elephantsNextValve);
        final remainingValves = Set<Valve>.from(valvesToCheck);
        remainingValves.remove(elephantsNextValve);

        int elephantsTime =
            elephantsStartValve.distanceTo[elephantsNextValve.name]!;
        String nextElephantsPath =
            elephantsPath + ' => ${elephantsNextValve.name} - $elephantsTime';
        elephantsTime += 1 + elephantsElapsedTime;

        if (elephantsTime < totalTime) {
          int resultOfPath = calcBestPathValue(
              myStartValve,
              elephantsNextValve,
              remainingValves,
              myElapsedTime,
              elephantsTime,
              myPath,
              nextElephantsPath);
          int result = resultOfPath +
              elephantsNextValve.flowRate * (totalTime - elephantsTime);
          bestResult = max(bestResult, result);
        }
      }
    } else if (elephantsElapsedTime >= totalTime) {
      // Only I have time left.
      Set<Valve> myValvesToCheck = Set<Valve>.from(valvesToCheck);
      while (myValvesToCheck.isNotEmpty) {
        final myNextValve = myValvesToCheck.first;
        myValvesToCheck.remove(myNextValve);

        final remainingValves = Set<Valve>.from(valvesToCheck);
        remainingValves.remove(myNextValve);

        int myTime = myStartValve.distanceTo[myNextValve.name]!;
        String nextMyPath = myPath + ' => ${myNextValve.name} - $myTime';
        myTime += 1 + myElapsedTime;

        if (myTime < totalTime) {
          int resultOfPath = calcBestPathValue(
              myNextValve,
              elephantsStartValve,
              remainingValves,
              myTime,
              elephantsElapsedTime,
              nextMyPath,
              elephantsPath);
          int result =
              resultOfPath + myNextValve.flowRate * (totalTime - myTime);
          bestResult = max(bestResult, result);
        }
      }
    } else {
      if (valvesToCheck.length == 1) {
        return tryMeAndElephantToLastValve(myStartValve, elephantsStartValve,
            valvesToCheck.first, myElapsedTime, elephantsElapsedTime);
      }
      for (final myNextValve in valvesToCheck) {
        Set<Valve> remainingValves = Set<Valve>.from(valvesToCheck);
        remainingValves.remove(myNextValve);

        int myTime = myStartValve.distanceTo[myNextValve.name]!;
        String nextMyPath = myPath + ' => ${myNextValve.name} - $myTime';
        myTime += 1 + myElapsedTime;

        for (final elephantsNextValve in remainingValves) {
          Set<Valve> elephantsRemainingValves = Set.from(remainingValves);
          elephantsRemainingValves.remove(elephantsNextValve);

          int elephantsTime =
              elephantsStartValve.distanceTo[elephantsNextValve.name]!;
          String nextElephantsPath =
              elephantsPath + ' => ${elephantsNextValve.name} - $elephantsTime';
          elephantsTime += 1 + elephantsElapsedTime;

          int resultOfPath = calcBestPathValue(
              myNextValve,
              elephantsNextValve,
              elephantsRemainingValves,
              myTime,
              elephantsTime,
              nextMyPath,
              nextElephantsPath);
          int result = resultOfPath;
          if (myTime < totalTime) {
            result += myNextValve.flowRate * (totalTime - myTime);
          }
          if (elephantsTime < totalTime) {
            result += elephantsNextValve.flowRate * (totalTime - elephantsTime);
          }
          bestResult = max(result, bestResult);
        }
      }
    }
    return bestResult;
  }

  Valve getUnvisitedWithLowestDist(Set<Valve> unVisitedNodes) {
    List<Valve> list = unVisitedNodes.toList();
    list.sort((a, b) => a.dijkstraDist.compareTo(b.dijkstraDist));
    return list.first;
  }

  int tryMeAndElephantToLastValve(Valve myStartValve, Valve elephantsStartValve,
      Valve lastValve, int myElapsedTime, int elephantsElapsedTime) {
    int bestResult = 0;
    // Me first
    int timeToValve = myStartValve.distanceTo[lastValve.name]!;
    timeToValve++; // For the time to turn the valve on
    if (myElapsedTime + timeToValve < totalTime) {
      bestResult =
          lastValve.flowRate * (totalTime - myElapsedTime - timeToValve);
    }
    // Try elephant
    timeToValve = elephantsStartValve.distanceTo[lastValve.name]!;
    timeToValve++; // For the time to turn the valve on
    if (elephantsElapsedTime + timeToValve < totalTime) {
      bestResult = max(
          bestResult,
          lastValve.flowRate *
              (totalTime - elephantsElapsedTime - timeToValve));
    }
    return bestResult;
  }

  int getMaxResultFromRemainingValves(
      Set<Valve> remainingValves, int remainingTime) {
    List<Valve> list = remainingValves.toList();
    list.sort((a, b) => b.flowRate.compareTo(a.flowRate));
    int bestValue = 0;
    for (int i = 0; i < list.length; i++) {
      bestValue += (remainingTime - i) * list[i].flowRate;
    }
    return bestValue;
  }

  void calculateDistances() {
    for (final firstValve in valveList) {
      for (final secondValve in valveList) {
        if (firstValve != secondValve) {
          int distance = findShortestPathToValve(firstValve, secondValve);

          firstValve.distanceTo[secondValve.name] = distance;
        }
      }
    }
  }

  void removeIrrelevantNodes() {
    // Remove nodes
    List<Valve> newList = [];
    for (Valve valve in valveList) {
      if (valve.name == 'AA' || valve.flowRate > 0) {
        newList.add(valve);
      }
    }

    // Remove the neighbours that was deleted
    for (Valve valve in newList) {
      List<String> newNeighbourList = [];
      for (String neighbourName in valve.neighbours) {
        for (final valveToCheck in newList) {
          if (valveToCheck.name == neighbourName) {
            newNeighbourList.add(neighbourName);
          }
        }
      }
      valve.neighbours = newNeighbourList;
    }

    // Remove unnecessary distance entries
    for (Valve valve in newList) {
      Map<String, int> newDistTo = {};
      for (final key in valve.distanceTo.keys) {
        for (final valveToCheck in newList) {
          if (valveToCheck.name == key) {
            newDistTo[key] = valve.distanceTo[key]!;
            break;
          }
        }
      }
      valve.distanceTo = newDistTo;
    }
    valveList = newList;
  }
}

class Valve {
  String name;
  List<String> neighbours = [];
  int flowRate;
  int dijkstraDist = veryLargeNumber;

  Map<String, int> distanceTo = {};

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
