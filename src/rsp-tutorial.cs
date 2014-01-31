// Tutorial program for The Red Spider Project
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Threading;

public static class EnumerableExtensions
{
  public static IEnumerable<T> Slowly<T>(
    this IEnumerable<T> source,
    int minDelay,
    int maxDelay)
  {
    var random = new Random();
    foreach (var item in source)
    {
      Thread.Sleep(random.Next(minDelay, maxDelay));
      yield return item;
    }
  }

  public static IEnumerable<T> InjectEvery<T>(
    this IEnumerable<T> source,
    int frequency,
    T injection)
  {
    var lastSeen = 0;
    var step = 0;
    foreach (var item in source)
    {
      if (object.Equals(item, injection))
        lastSeen = step;

      if ((step - lastSeen) >= frequency)
      {
        lastSeen = step;
        yield return injection;
      }

      step += 1;

      yield return item;
    }
  }
}

public static class Tutorial
{
  static string IntroText =
    "Welcome to the Red Spider Project tutorial. " +
    "I will be your faithful guide through the " +
    "possibilities of the project. While in " +
    "rsshell you can call me at any time with the " +
    "following command:\n\n" +
    "\trsp-tutorial\n\n" +
    "I can even do some of the work for you and " +
    "point you to other sources for more help. " +
    "Let's get started!\n";

  static Dictionary<string, Action> InitialOptions =
    new Dictionary<string, Action>
    {
      { "Explore the installed software.", Explore },
      { "Learn about the RSP Community.", Learn },
      { "Contribute to the project.", Contribute },
      { "Quit.", Quit }
    };

  static void Explore()
  {
    Display("Let's go exploring!");
  }

  static void Learn()
  {
    Display("Let's learn about the RSP :)");
  }

  static void Contribute()
  {
    Display("I'll teach you how to contribute!");
    Prompt(new Dictionary<string, Action>
    {
      { "Help out with stuff other people are " +
        "currently working on.",
        HelpOut },
      { "Work on an idea of my own.", WorkOnMyOwn },
      { "Get inspired!", FreeIdeas },
      { "Improve the documentation.", Documentation },
      { "Go to the main menu.", MainMenu },
      { "Quit.", Quit }
    });
  }

  static void HelpOut()
  {
    // TODO
    Display("I'll show you how to help out!");
  }

  static void WorkOnMyOwn()
  {
    // TODO
    Display("I'll show you how to get started!");
  }

  static void FreeIdeas()
  {
    // TODO
    // Pull these in realtime please :)
    Display("Here's a list of free ideas!");
  }

  static void Documentation()
  {
    // TODO
    Display("Here's how to help with documentation.");
  }

  static void Quit()
  {
    Display("Bye now!");
  }

  static void MainMenu()
  {
    Prompt(InitialOptions);
  }

  static void Display(
    string text,
    bool newline = true)
  {
    foreach (var c in text
      .Slowly(20, 80)
      .InjectEvery(40, '\n'))
      Console.Write(c);

    if (newline) Console.Write('\n');
  }

  static void Prompt(
    Dictionary<string, Action> options)
  {
    var list = options
      .Select((pair, i) => new
      {
        Index = (i + 1).ToString(),
        Text = pair.Key,
        Action = pair.Value
      });

    Display("What would you like to do?\n");
    foreach (var option in list)
    {
      Display(string.Format(
        "{0}. {1}",
        option.Index,
        option.Text));
    }

    Display("\n\n> ", false);
    var response = Console.ReadLine().Trim();
    var chosen = list
      .FirstOrDefault(o => o.Index == response);

    if (chosen == null)
    {
      Display("Sorry, I didn't get that...");
      Prompt(options);
    }
    else
    {
      chosen.Action();
    }
  }

  static void Main()
  {
    Display(IntroText);

    MainMenu();
  }
}
