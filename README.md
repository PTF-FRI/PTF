# PTF
TODO: 04-07

Format ZZ-Ceti.txt file as a csv (comma separated value) file, so that multidownload.py will read it. (Use awk?)

Sort LikelyWD-Vizier file's stars by likeliness of them being a white dwarf (which is the 4th column). Then get rid of that    column to make the format acceptable to mulidownload.py. (Awk again?)

Combine all these files into one big one, and feed it to multidownload.py

After that, search through data that is created and delete all with an "nobs"/"ngoodobs" field that is lower (\<10? well have to talk about it). Might need to download an XML parser to do this. For sure this will be python code that does this.
