namespace adventofcode;

public class Utils 
{
    public static List<string> GetData(int day, string delimiter)
    {
        var fileData = System.IO.File.ReadAllText($"day{day}.txt");
        var data = fileData.Split(delimiter);

        return data.ToList();
    }
}