# spotify_rabbit_hole
Choose an artist. Takes i songs from j related artists. Repeat k times. Update your queue or plot the resulting graph

### Usage:
```
positional arguments:
  artist                Input the name of the desired artist

optional arguments:
  -h, --help              Show this help message and exit                                    
  -t TOTAL, --total       Total related artists                   (default = 5)                    
  -r RELATED, --related   Number of related artists per artist    (default = 2)                  
  -s SONGS, --songs       Number of songs per artist              (default = 1)              
  -p PLOT, --plot         Plot graph of related artists           (default = False)                    
```

#### Example:
```
$python rabbit_hole.py Alt-J
```
```
Artists:
alt-J, Grouplove, Beirut, Bleachers, Hippo Campus, Fleet Foxes
----------------------------------------
Grouplove:
        -Bleachers, Hippo Campus
alt-J:
        -Grouplove, Beirut
Beirut:
        -Fleet Foxes
----------------------------------------
Total Songs: 5
Add songs to queue? Y/N?
```

#### Graph example:
> Searched for: Led Zeppelin

![GitHub Logo](/led_zeppelin_30_test.png)
