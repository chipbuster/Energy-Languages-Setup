Some of the directories in the Energy Languages repo are not ready to run as they
are. For example, in the README for CSharp, the authors imply that you
should run the following commands in every repository:

```
dotnet new console -o . -n tmp
dotnet restore
```

Well it turns out the first command won't run if you try it, and several languages
need setup like this. These scripts are to run that setup.
